from manim import *

class MultipartySessionType(Scene):
    def construct(self):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{amsmath}")
        tex_template.add_to_preamble(r"\usepackage{amssymb}")
        tex_template.add_to_preamble(r"\usepackage{ragged2e}")
        tex_template.add_to_preamble(r"\usepackage{tabto}")
        tex_template.add_to_preamble(r"\usepackage{tikz}")
        tex_template.add_to_preamble(r"\usepackage[utf8]{inputenc}")
        tex_template.add_to_preamble(r"""
\newcommand{\greencheck}{}%
\DeclareRobustCommand{\greencheck}{%
  \tikz\fill[scale=0.4, color=green]
  (0,.35) -- (.25,0) -- (1,.7) -- (.25,.15) -- cycle;%
}
""")
        intro = True
        message_passing = True
        intuition = True
        first_example = True
        syntax = True
        reduction = True
        what_the_paper_brought = True
        code_example = True

        if intro:
            title = Tex(
                r"\centering{Deadlock-free Asynchronous Message Reordering In Rust With Multiparty Session Types}",
                tex_template=tex_template,
                font_size=64,
            )
            title.scale(0.6)
            author = Tex(
                r"Vincent Higginson",
                tex_template=tex_template,
                font_size=18,
            )
            author.next_to(title, DOWN, buff=0.5)
            self.add_sound("~/Music/Multicore/message-passing-manim-sucks.mp3")
            self.play(FadeIn(title), FadeIn(author))
            self.wait(16)
            self.play(FadeOut(author))
            self.play(FadeOut(title))

        part1 = Tex(
            r"$\mathcal{A}.$ What is Multiparty Session Types?",
            tex_template=tex_template,
            font_size=32,
        )
        rect = SurroundingRectangle(part1)
        group = VGroup(rect, part1)
        self.play(FadeIn(group))
        self.play(group.animate.shift((DOWN*1.1+LEFT*1.3)*3))

        if message_passing:
            process1 = Circle(color=PINK, fill_opacity=0.7)
            process1.shift((UP+LEFT)*2.0)
            process1.scale(0.8)
            process2 = Circle(color=BLUE, fill_opacity=0.7)
            process2.scale(0.8)
            process2.shift((DOWN+LEFT)*2.0)
            process3 = Circle(color=GREEN, fill_opacity=0.7)
            process3.scale(0.8)
            process3.shift((DOWN+RIGHT)*2.0)
            process4 = Circle(color=RED, fill_opacity=0.7)
            process4.scale(0.8)
            process4.shift((UP+RIGHT)*2.0)

            self.play(Create(process4))
            self.play(Create(process3))
            self.play(Create(process2))
            self.play(Create(process1))

            arrow1 = Arrow(process1, process2)
            msg1 = Tex("Can I have a drink?", font_size=19)
            msg1.next_to(arrow1, LEFT)
            arrow2 = Arrow(process2, process3)
            msg2 = Tex("He wants a drink!", font_size=19)
            msg2.next_to(arrow2, DOWN)
            arrow3 = Arrow(process3, process4)
            msg3 = Tex("Prepare a drink...", font_size=19)
            msg3.next_to(arrow3)
            arrow4 = Arrow(process4, process1)
            msg4 = Tex("Oh what drink do you want?", font_size=19)
            msg4.next_to(arrow4, UP)

            self.wait(12.0)
            self.play(FadeIn(arrow1), FadeIn(msg1))
            self.play(FadeIn(arrow2), FadeIn(msg2))
            self.play(FadeIn(arrow3), FadeIn(msg3))
            self.play(FadeIn(arrow4), FadeIn(msg4))

            master = Square(color=WHITE, fill_opacity=0.7)
            master.scale(0.6)
            # master.shift(RIGHT*4.0)

            master_arrow1 = DoubleArrow(process1, master)
            master_arrow2 = DoubleArrow(process2, master)
            master_arrow3 = DoubleArrow(process3, master)
            master_arrow4 = DoubleArrow(process4, master)

            self.wait(4.0)

            self.play(FadeIn(master), FadeIn(master_arrow1), FadeIn(master_arrow2), FadeIn(master_arrow3), FadeIn(master_arrow4))

            master_cross = Cross(stroke_width=20)
            master_cross.scale(0.75)

            self.play(FadeIn(master_cross))
            self.wait(5.0)
            self.play(FadeOut(master), FadeOut(master_arrow1), FadeOut(master_arrow2), FadeOut(master_arrow3), FadeOut(master_arrow4) )
            self.play(FadeOut(master_cross))

            self.play(FadeOut(process1), FadeOut(process2), FadeOut(process3), FadeOut(process4), FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(arrow4), FadeOut(msg1), FadeOut(msg2), FadeOut(msg3), FadeOut(msg4))

        if intuition:
            label_global = Tex("Global", tex_template=tex_template, font_size=32)
            global_rule = VGroup(label_global, SurroundingRectangle(label_global, color=RED, fill_opacity=0.0))
            global_rule.shift(UP*2.0)

            label1 = Tex(r"Local$_1$", tex_template=tex_template, font_size=32)
            local_rule1 = VGroup(label1, SurroundingRectangle(label1, color=BLUE, fill_opacity=0.0))
            label2 = Tex(r"Local$_2$", tex_template=tex_template, font_size=32)
            local_rule2 = VGroup(label2, SurroundingRectangle(label2, color=BLUE, fill_opacity=0.0))
            label3 = Tex(r"Local$_3$", tex_template=tex_template, font_size=32)
            local_rule3 = VGroup(label3, SurroundingRectangle(label3, color=BLUE, fill_opacity=0.0))
            local_rule1.next_to(local_rule2, LEFT, buff=1.0)
            local_rule3.next_to(local_rule2, RIGHT, buff=1.0)

            arrow1 = Arrow(start=UP*0.8, end=DOWN*0.8)
            arrow1.shift(UP)

            self.play(FadeIn(global_rule))
            self.wait(8.0)
            self.play(FadeIn(arrow1))
            self.play(FadeIn(local_rule1), FadeIn(local_rule2), FadeIn(local_rule3))

            equality = Tex(r"\textit{All local rules are respected $\implies$ Global rules are respected.}", font_size=28)
            equality.shift(DOWN*1.7)
            hello = Tex(r"\textit{Multiparty Session Types provides the syntax, and verification tools to construct these sets.}", font_size=28)
            hello.next_to(equality, DOWN)

            self.wait(8.0)
            self.play(FadeIn(equality), FadeIn(hello))

            self.wait(18.0)

            self.play(FadeOut(global_rule), FadeOut(equality), FadeOut(hello), FadeOut(local_rule1), FadeOut(local_rule2), FadeOut(local_rule3), FadeOut(arrow1))

        self.play(FadeOut(group))

        part2 = Tex(
            r"$\mathcal{B}.$ Syntax Example?",
            tex_template=tex_template,
            font_size=32,
        )

        rect2 = SurroundingRectangle(part2)
        group2 = VGroup(rect2, part2)
        self.play(FadeIn(group2))
        self.play(group2.animate.shift((DOWN*1.1+LEFT*1.3)*3))

        if first_example:
            client_label = Tex(r"Client")
            client_label.shift(UP)
            client = VGroup(client_label, Square(color=YELLOW, side_length=0.8, fill_opacity=0.7))
            
            waiter_label = Tex(r"Waiter")
            waiter_label.shift(UP)
            waiter = VGroup(waiter_label, Square(color=RED, side_length=0.8, fill_opacity=0.7))
            
            barman_label = Tex(r"Barman")
            barman_label.shift(UP)
            barman = VGroup(barman_label, Square(color=BLUE, side_length=0.8, fill_opacity=0.7))

            client.shift(DOWN)
            waiter.shift(DOWN)
            barman.shift(DOWN)

            self.play(FadeIn(client))
            self.play(client.animate.shift(LEFT*3.0+UP*2.0))
            self.play(FadeIn(waiter))
            self.play(waiter.animate.shift(UP*2.0))
            self.play(FadeIn(barman))
            self.play(barman.animate.shift(RIGHT*3.0+UP*2.0))

            step1 = Arrow(start=LEFT*3.0+UP*1.2, end=UP*1.2, buff=1)
            step1_label = Tex(r"ask('Martini')", font_size=18)
            step1_label.next_to(step1, UP, buff=0.2)
            step2 = Arrow(start=UP*1.2, end=RIGHT*3.0+UP*1.2, buff=1)
            step2_label = Tex(r"prepare('Martini')", font_size=18)
            step2_label.next_to(step2, UP, buff=0.2)
            step3a = Arrow(start=RIGHT*3.0+UP*0.8, end=UP*0.8, buff=1)
            step3a_label = Tex(r"serve('Martini')", font_size=18)
            step3a_label.next_to(step3a, DOWN, buff=0.2)
            step4a = Arrow(start=UP*0.8, end=LEFT*3.0+UP*0.8, buff=1)
            step4a_label = Tex(r"bring('Martini')", font_size=18)
            step4a_label.next_to(step4a, DOWN, buff=0.2)

            step3b = Arrow(start=RIGHT*3.0+UP*0.8, end=UP*0.8, buff=1, color=YELLOW)
            step3b_label = Tex(r"reject(bool)", font_size=18)
            step3b_label.next_to(step3a, DOWN, buff=0.2)
            step4b = Arrow(start=UP*0.8, end=LEFT*3.0+UP*0.8, buff=1, color=YELLOW)
            step4b_label = Tex(r"excuse(bool)", font_size=18)
            step4b_label.next_to(step4a, DOWN, buff=0.2)

            self.play(FadeIn(step1), FadeIn(step1_label))
            self.wait(2)
            self.play(FadeIn(step2), FadeIn(step2_label))
            self.wait(3)
            self.play(FadeIn(step3a), FadeIn(step3a_label))
            self.wait(3)
            self.play(FadeIn(step4a), FadeIn(step4a_label))
            self.play(FadeOut(step3a), FadeOut(step3a_label), FadeOut(step4a), FadeOut(step4a_label))
            self.play(FadeIn(step3b), FadeIn(step3b_label), FadeIn(step4b), FadeIn(step4b_label))
            self.play(FadeOut(step3b), FadeOut(step3b_label), FadeOut(step4b), FadeOut(step4b_label))
            self.play(FadeIn(step3a), FadeIn(step3a_label), FadeIn(step4a), FadeIn(step4a_label))

            first_formula = r"""\begin{flushleft}
            Client $\longrightarrow$ Waiter:\textit{ask(Martini)}.Waiter $\longrightarrow$ Barman:\textit{prepare(Martini)}

            Barman $\longrightarrow$ Waiter: \{

            \quad \quad \textit{serve}(Martini).Waiter $\longrightarrow$ Client:\textit{bring}(Martini).end

            \quad \quad \textit{reject}(bool).Waiter $\longrightarrow$ Client:\textit{excuse}(bool).end

            \}\end{flushleft}
            """
            first_formula = Tex(first_formula, tex_template=tex_template, font_size=32)
            first_formula.shift(DOWN*1.2)

            self.play(Create(first_formula))

            self.wait(5.0)

            self.play(FadeOut(waiter), FadeOut(client), FadeOut(barman), FadeOut(step1), FadeOut(step1_label), FadeOut(step2), FadeOut(step2_label), FadeOut(step3a), FadeOut(step3a_label), FadeOut(step4a), FadeOut(step4a_label))

            self.play(first_formula.animate.shift(UP*3.4))

            local_formula1 = r"""\begin{flushleft}
            $P_{Client}$ = Waiter!ask(Martini)

            \quad .(Waiter?bring(Martini) + Waiter?reject(bool))

            \quad .end

            \end{flushleft}
            """
            local_formula1 = Tex(local_formula1, tex_template=tex_template, font_size=26)
            local_formula1.shift(DOWN*0.1 + LEFT*4.1)

            local_formula2 = r"""\begin{flushleft}
            $P_{Waiter}$ = Client?ask(Martini).Barman!prepare(Martini).
            
            \quad \quad ((Barman?serve(Martini).Client!bring(Martini))
            
            \quad \quad + (Barman?refuse(bool).Client!excuse(bool)))
            
            \quad.end
            \end{flushleft}
            """
            local_formula2 = Tex(local_formula2, tex_template=tex_template, font_size=26)
            local_formula2.shift(DOWN * 1.5)

            local_formula3 = r"""\begin{flushleft}
            $P_{Barman}$ = Waiter?prepare(Martini).

                \quad if (...) then

                    \quad \quad Waiter!serve(Martini).end

                \quad else

                    \quad \quad Waiter!refuse(bool).end

            \end{flushleft}
            """
            local_formula3 = Tex(local_formula3, tex_template=tex_template, font_size=26)
            local_formula3.shift(UP*0.3 + RIGHT*4.0)

            self.play(Create(local_formula1))
            self.wait(1.0)
            self.play(Create(local_formula2))
            self.wait(1.0)
            self.play(Create(local_formula3))

            self.wait(5)

            self.play(FadeOut(local_formula1), FadeOut(local_formula2), FadeOut(local_formula3), FadeOut(first_formula))

        if syntax:
            syntax1 = r"""\begin{flushleft}
            Receiving: From?msg(type)
            \end{flushleft}
            """
            syntax1 = Tex(syntax1, tex_template=tex_template, font_size=32)
            syntax1.shift(UP)

            syntax2 = r"""\begin{flushleft}
            Sending: To!msg(type)
            \end{flushleft}
            """
            syntax2 = Tex(syntax2, tex_template=tex_template, font_size=32)
            syntax2.next_to(syntax1, DOWN, buff=0.5)

            syntax3 = r"""\begin{flushleft}
            Logical Or: +
            \end{flushleft}
            """
            syntax3 = Tex(syntax3, tex_template=tex_template, font_size=32)
            syntax3.next_to(syntax2, DOWN, buff=0.5)

            syntax4 = r"""\begin{flushleft}
            End: end \textit{or} 0
            \end{flushleft}
            """
            syntax4 = Tex(syntax4, tex_template=tex_template, font_size=32)
            syntax4.next_to(syntax3, DOWN, buff=0.5)

            self.play(FadeIn(syntax1))
            self.play(FadeIn(syntax2))
            self.play(FadeIn(syntax3))
            self.play(FadeIn(syntax4))

            self.wait(8.0)

            self.play(FadeOut(syntax1))
            self.play(FadeOut(syntax2))
            self.play(FadeOut(syntax3))
            self.play(FadeOut(syntax4))

        if reduction:
            mps1 = r"""
            $\mathcal{M}=$
            """
            mps1 = Tex(mps1, tex_template=tex_template, font_size=32)
            mps1.shift(LEFT*3.45)

            mps2 = r"""
            client $\triangleleft$ $P_{Client}$
            """
            mps2 = Tex(mps2, tex_template=tex_template, font_size=32)
            mps2.next_to(mps1, RIGHT, buff=0.2)

            mps3 = r"""
            $\vert$ waiter $\triangleleft$ $P_{Waiter}$
            """
            mps3 = Tex(mps3, tex_template=tex_template, font_size=32)
            mps3.next_to(mps2, RIGHT, buff=0.2)

            mps4 = r"""
            $\vert$ barman $\triangleleft$ $P_{Barman}$
            """
            mps4 = Tex(mps4, tex_template=tex_template, font_size=32)
            mps4.next_to(mps3, RIGHT, buff=0.2)

            self.play(FadeIn(mps1))
            self.play(FadeIn(mps2))
            self.play(FadeIn(mps3))
            self.play(FadeIn(mps4))

            self.play(
                mps1.animate.shift(UP*1.4),
                mps2.animate.shift(UP*1.4),
                mps3.animate.shift(UP*1.4),
                mps4.animate.shift(UP*1.4),
            )

            arrow_reduction = Arrow(start=UP*0.7, end=DOWN*0.7)
            arrow_reduction.shift(UP*0.4)
            arrow_reduction_label = Tex(r"Reduction rules", tex_template=tex_template, font_size=24)
            arrow_reduction_label.next_to(arrow_reduction, LEFT)
            reduction_result = r"""
            $\mathcal{M}=$
            client $\triangleleft$ $0$
            $\vert$ waiter $\triangleleft$ $0$
            $\vert$ barman $\triangleleft$ $0$
            """
            reduction_result = Tex(reduction_result, tex_template=tex_template, font_size=32)
            reduction_result.next_to(arrow_reduction, DOWN)

            self.wait(2.0)

            self.play(FadeIn(arrow_reduction), FadeIn(arrow_reduction_label))
            self.play(FadeIn(reduction_result))

            doesnt_stuck = Tex(r"\greencheck", r"$\mathcal{M}$ won't get stuck!", tex_template=tex_template, font_size=28, color=GREEN)
            doesnt_stuck.shift(RIGHT*3.5+UP*0.3)
            doesnt_stuck.set_color_by_tex("greencheck", GREEN)

            self.wait(3.0)
            self.play(FadeIn(doesnt_stuck))

            self.wait(9.0)

            self.play(
                FadeOut(doesnt_stuck),
                FadeOut(arrow_reduction),
                FadeOut(arrow_reduction_label),
                FadeOut(reduction_result),
                FadeOut(mps1),
                FadeOut(mps2),
                FadeOut(mps3),
                FadeOut(mps4),
            )

        self.play(FadeOut(group2))

        if what_the_paper_brought:
            pass

        part4 = Tex(
            r"$\mathcal{D}.$ Rust Code Example?",
            tex_template=tex_template,
            font_size=32,
        )

        rect4 = SurroundingRectangle(part4)
        group4 = VGroup(rect4, part4)
        self.play(FadeIn(group4))
        self.wait(15.0)
        self.play(group4.animate.shift((DOWN*1.1+LEFT*1.3)*3))

        github = Tex(
            r"\verb|https://github.com/vinhig/rumpsteak_initiation|",
            tex_template=tex_template,
            font_size=18,
        )
        github.next_to(group4, RIGHT)
        self.play(FadeIn(github))

        if code_example:
            type_system_img = ImageMobject("~/Music/Multicore/type_system.png")
            type_system_img.scale(1.5)
            self.play(FadeIn(type_system_img))
            self.wait(2.0)
            self.play(FadeOut(type_system_img))

            actors_img = ImageMobject("~/Music/Multicore/actors.png")
            actors_channel_img = ImageMobject("~/Music/Multicore/actors_channel.png")
            labels_img = ImageMobject("~/Music/Multicore/labels.png")

            self.play(FadeIn(actors_img))
            self.wait(6.0)
            self.play(actors_img.animate.shift((DOWN*2.1+RIGHT*4.0)))

            self.play(FadeIn(actors_channel_img))
            self.wait(6.0)
            self.play(actors_channel_img.animate.shift((UP*1.35+LEFT*-2.7)))

            self.play(FadeIn(labels_img))
            self.wait(6.0)
            self.play(labels_img.animate.shift((LEFT*3.7)))

            self.wait(4.0)

            self.play(FadeOut(actors_img), FadeOut(actors_channel_img), FadeOut(labels_img))

            processes_img = ImageMobject("~/Music/Multicore/processes.png")
            select1_img = ImageMobject("~/Music/Multicore/is_it_in_stock.png")
            branch1_img = ImageMobject("~/Music/Multicore/should_i_put_1_star.png")
            branch2_img = ImageMobject("~/Music/Multicore/should_i_excuse.png")

            self.play(FadeIn(processes_img))
            self.wait(9.0)
            self.play(processes_img.animate.shift((UP*2.5)))

            self.play(FadeIn(select1_img))
            self.wait(1.5)
            self.play(select1_img.animate.shift((RIGHT*0.4+UP*-2.5)))

            self.play(FadeIn(branch1_img))
            self.wait(1.5)
            self.play(branch1_img.animate.shift((RIGHT*4.2+UP*-2.5)))

            self.play(FadeIn(branch2_img))
            self.wait(1.5)
            self.play(branch2_img.animate.shift((RIGHT*-3.4+UP*-0.7)))

            self.wait(1.5)

            self.play(FadeOut(processes_img), FadeOut(select1_img), FadeOut(branch1_img), FadeOut(branch2_img))

            client_img = ImageMobject("~/Music/Multicore/client_process.png")
            client_img.shift(UP*0.5)
            waiter_img = ImageMobject("~/Music/Multicore/waiter_process.png")
            waiter_img.shift(UP*0.5)
            barman_img = ImageMobject("~/Music/Multicore/barman_process.png")
            barman_img.shift(UP*0.5)

            self.play(FadeIn(client_img))
            self.wait(6.0)
            self.play(FadeOut(client_img))

            self.play(FadeIn(waiter_img))
            self.wait(6.0)
            self.play(FadeOut(waiter_img))

            self.play(FadeIn(barman_img))
            self.wait(6.0)
            self.play(FadeOut(barman_img))

        self.play(FadeOut(group4), FadeOut(github))

        the_end = Tex(
            r"The End!",
            tex_template=tex_template,
            font_size=64,
        )
        self.play(FadeIn(the_end))

        github = Tex(
            r"\verb|https://github.com/vinhig/rumpsteak_initiation|",
            tex_template=tex_template,
            font_size=32,
        )
        github.next_to(the_end, DOWN)
        self.play(FadeIn(github))

        self.wait()
