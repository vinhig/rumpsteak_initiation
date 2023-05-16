use futures::{
    channel::mpsc::{UnboundedReceiver, UnboundedSender},
    executor, try_join,
};
use rumpsteak::{
    channel::{Bidirectional, Nil}, session, try_session, End, Message, Receive, Role, Roles, Send, Select, Branch,
};
use std::{error::Error, result};

use rand::prelude::*;

type Result<T> = result::Result<T, Box<dyn Error>>;

type Channel = Bidirectional<UnboundedSender<Label>, UnboundedReceiver<Label>>;

#[derive(Roles)]
struct Roles(Client, Waiter, Barman);

#[derive(Role)]
#[message(Label)]
struct Client(#[route(Waiter)] Channel, #[route(Barman)] Nil);

#[derive(Role)]
#[message(Label)]
struct Waiter(#[route(Client)] Channel, #[route(Barman)] Channel);

#[derive(Role)]
#[message(Label)]
struct Barman(#[route(Client)] Nil, #[route(Waiter)] Channel);

#[derive(Message)]
enum Label {
    Ask(Ask),
    Prepare(Prepare),
    Serve(Serve),
    Bring(Bring),
    Reject(Reject),
    Excuse(Excuse),
}

struct Ask(String);
struct Prepare(String);
struct Serve(String);
struct Bring(String);
struct Reject(bool);
struct Excuse(bool);

#[session]
enum IsItInStock {
    Serve(Serve, End),
    Reject(Reject, End),
}

#[session]
enum ShouldIExcuse {
    Serve(Serve, Send<Client, Bring, End>),
    Reject(Reject, Send<Client, Excuse, End>),
}

#[session]
enum ShouldIPut1Star {
    Bring(Bring, End),
    Excuse(Excuse, End),
}

#[session]
type ProcessClient = Send<Waiter, Ask, Branch<Waiter, ShouldIPut1Star>>;

#[session]
type ProcessWaiter = Receive<Client, Ask, Send<Barman, Prepare, Branch<Barman, ShouldIExcuse>>>;

#[session]
type ProcessBarman = Receive<Waiter, Prepare, Select<Waiter, IsItInStock>>;

async fn client(role: &mut Client) -> Result<()> {
    try_session(role, |s: ProcessClient<'_, _>| async {
        let s = s.send(Ask(String::from("Martini"))).await?;

        println!("CLIENT: Asking for a Martini");
        let s = match s.branch().await? {
            ShouldIPut1Star::Excuse(Excuse(x), s) => {
                println!("CLIENT: wtf is that bar??");
                s
            }
            ShouldIPut1Star::Bring(Bring(x), s) => {
                println!("CLIENT: `{}` is ready!", &x);
                s
            }
        };
        
        Ok(((), s))
    })
    .await
}

async fn waiter(role: &mut Waiter) -> Result<()> {
    try_session(role, |s: ProcessWaiter<'_, _>| async {
        let (Ask(x), s) = s.receive().await?;
        println!("WAITER: Client asked for a `{}`", &x);
        
        let s = s.send(Prepare(x)).await?;

        let s = match s.branch().await? {
            ShouldIExcuse::Serve(Serve(x), s) => {
                println!("WAITER: Serving `{}` to client.", &x);
                s.send(Bring(x)).await?
            }
            ShouldIExcuse::Reject(Reject(x), s) => {
                println!("WAITER: Serving EXCUSES to client...");
                s.send(Excuse(x)).await?
            }
        };
        Ok(((), s))
    })
    .await
}

async fn barman(role: &mut Barman) -> Result<()> {
    try_session(role, |s: ProcessBarman<'_, _>| async {
        let (Prepare(x), s) = s.receive().await?;
        
        if rand::random() {
            println!("BARMAN: yes, we do have `{}` in stock.", &x);
            let s = s.select(Serve(x)).await?;
            return Ok(((), s));
        } else {
            println!("BARMAN: oops, time to buy some...");
            let s = s.select(Reject(true)).await?;
            return Ok(((), s));
        }
    })
    .await
}

fn main() {
    let Roles(mut a, mut b, mut c) = Roles::default();
    executor::block_on(async {
        try_join!(client(&mut a), waiter(&mut b), barman(&mut c)).unwrap();
    });
}
