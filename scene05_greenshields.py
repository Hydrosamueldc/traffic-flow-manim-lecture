from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 5 — THE GREENSHIELDS MODEL
#  Render: manim -pql scene05_greenshields.py Scene05_Greenshields
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene05_Greenshields(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT I · Scene 5 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE — OPENING QUESTION
        # ─────────────────────────────────────────────────────────────────────
        title  = Text("The Greenshields Model", font_size=50, weight=BOLD, color=WHITE)
        sub    = Text("A mathematical model for traffic velocity",
                      font_size=26, color="#8899cc")
        byline = Text("Bruce D. Greenshields  ·  1935",
                      font_size=22, color="#ffaa44")
        sub.next_to(title, DOWN, buff=0.35)
        byline.next_to(sub,  DOWN, buff=0.22)

        with self.voiceover(
            "So far, we have developed an important relationship. "
            "Traffic flow depends on both density and velocity. "
            "We also discovered that velocity decreases as density increases. "
            "But we still have one important question. "
            "Exactly how does velocity decrease? "
            "Is the relationship linear? "
            "Is it curved? "
            "Or is it something completely different? "
            "To answer this, we need a mathematical model."
        ):
            self.play(Write(title),                    run_time=rt(1.4))
            self.play(FadeIn(sub,    shift=UP * 0.15), run_time=rt(0.7))
            self.play(FadeIn(byline, shift=UP * 0.10), run_time=rt(0.6))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub, byline)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. WHY GREENSHIELDS? — HISTORY THEN JUSTIFICATION
        # ─────────────────────────────────────────────────────────────────────
        need_title = Text("A Mathematical Model for  v(ρ)",
                          font_size=36, weight=BOLD, color=WHITE)
        need_title.to_edge(UP).shift(DOWN * 0.62)

        known  = MathTex(r"\text{Known: } q = \rho \cdot v(\rho)", font_size=30)
        needed = MathTex(r"\text{Need: an explicit formula for } v(\rho)",
                         font_size=28, color=YELLOW)
        known.center().shift(UP * 1.65)
        needed.next_to(known, DOWN, buff=0.28)

        models_lbl = Text("Candidate speed–density models:", font_size=20, color="#8899cc")
        models_lbl.next_to(needed, DOWN, buff=0.38)

        model_rows = VGroup(
            VGroup(
                Text("Greenshields (1935):", font_size=20, color=YELLOW, weight=BOLD),
                MathTex(r"v_f\!\left(1-\rho/\rho_j\right)", font_size=20, color=YELLOW),
                Text(" — linear", font_size=18, color="#aaaaaa"),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Text("Greenberg (1959):",          font_size=20, color="#777777"),
                MathTex(r"c_0\ln(\rho_j/\rho)",   font_size=20, color="#777777"),
                Text(" — logarithmic",             font_size=18, color="#666666"),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Text("del Castillo & Benitez (1995):", font_size=20, color="#777777"),
                MathTex(r"\text{exponential form}",   font_size=20, color="#777777"),
                Text(" — smooth near jam",            font_size=18, color="#666666"),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        model_rows.next_to(models_lbl, DOWN, buff=0.18)

        choice_lbl = Text(
            "This project uses Greenshields — simple enough to analyse,\n"
            "yet realistic enough to capture essential traffic behaviour.",
            font_size=19, color=GREEN, line_spacing=1.3,
        )
        choice_lbl.next_to(model_rows, DOWN, buff=0.28)

        # Block A: Greenshields' history — observations before equations
        with self.voiceover(
            "One of the earliest and most influential attempts "
            "was proposed by Bruce Greenshields in 1935. "
            "Rather than beginning with equations, "
            "Greenshields began with observations. "
            "He recorded real traffic at an intersection, "
            "measured vehicle speeds, "
            "estimated traffic density, "
            "and plotted one against the other. "
            "Surprisingly, the data suggested a simple pattern. "
            "As density increased, the average speed decreased almost linearly."
        ):
            self.play(FadeIn(need_title),                  run_time=rt(0.6))
            self.play(Write(known),                        run_time=rt(0.9))
            self.play(Write(needed),                       run_time=rt(0.8))
            self.play(FadeIn(models_lbl),                  run_time=rt(0.4))
            self.play(FadeIn(model_rows[0], shift=RIGHT * 0.15), run_time=rt(0.5))

        # Block B: other models and why this project uses Greenshields
        with self.voiceover(
            "Since Greenshields' work, "
            "many other speed-density models have been proposed. "
            "Some use logarithmic relationships. "
            "Others use exponential functions. "
            "Many produce more accurate results for specific traffic conditions. "
            "So why are we using Greenshields? "
            "The answer is simple. "
            "This project focuses on understanding the mathematical behaviour "
            "of the LWR model. "
            "Greenshields provides a relationship that is simple enough to analyse, "
            "yet realistic enough to capture the essential features of traffic flow. "
            "Its mathematical simplicity makes it an excellent choice "
            "for studying numerical methods "
            "such as the Upwind and Lax-Wendroff schemes."
        ):
            for row in model_rows[1:]:
                self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=rt(0.5))
            self.play(FadeIn(choice_lbl, shift=UP * 0.1),  run_time=rt(0.6))

        self.wait(rt(0.5))
        self.play(
            FadeOut(VGroup(need_title, known, needed, models_lbl,
                           model_rows, choice_lbl)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 3. THE LINEAR ASSUMPTION — ASSUMPTION → EQUATION → SYMBOLS → SENSE CHECK
        # ─────────────────────────────────────────────────────────────────────
        lin_title = Text("Greenshields' Linear Assumption",
                         font_size=34, weight=BOLD, color=WHITE)
        lin_title.to_edge(UP).shift(DOWN * 0.60)

        gs_eq = MathTex(
            r"v(\rho) = v_f\!\left(1 - \frac{\rho}{\rho_j}\right)",
            font_size=52, color=YELLOW,
        )
        gs_eq.center().shift(UP * 0.65)

        gs_note = MathTex(
            r"v_f = \text{free-flow speed,}\quad \rho_j = \text{jam density}",
            font_size=24, color="#8899cc",
        )
        gs_note.next_to(gs_eq, DOWN, buff=0.35)

        bc1 = MathTex(r"v(0)        = v_f(1 - 0) = v_f\;\checkmark",
                      font_size=26, color=GREEN)
        bc2 = MathTex(r"v(\rho_j)   = v_f(1 - 1) = 0\;\checkmark",
                      font_size=26, color=GREEN)
        bcs = VGroup(bc1, bc2).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        bcs.next_to(gs_note, DOWN, buff=0.38)

        # Block A: the assumption, then reveal the equation
        with self.voiceover(
            "What assumption did Greenshields make? "
            "He assumed that the decrease in speed "
            "is proportional to the increase in density. "
            "In other words, the relationship between velocity and density "
            "is a straight line. "
            "This gives us the Greenshields model."
        ):
            self.play(FadeIn(lin_title),               run_time=rt(0.6))
            self.play(Write(gs_eq),                    run_time=rt(1.2))

        self.wait(rt(0.3))

        # Block B: explain every symbol
        with self.voiceover(
            "This equation contains only two physical parameters. "
            "The first is the free-flow speed, denoted by v sub f. "
            "This is the speed vehicles can achieve when the road is completely empty. "
            "The second is the jam density, denoted by rho sub j. "
            "This represents the maximum number of vehicles "
            "that can physically occupy the road."
        ):
            self.play(FadeIn(gs_note, shift=UP * 0.1), run_time=rt(0.7))

        self.wait(rt(0.3))

        # Block C: common-sense test — boundary conditions told as a story
        with self.voiceover(
            "Let us see whether this equation agrees with common sense. "
            "If the road is empty, the density is zero. "
            "Substituting this into the equation gives the free-flow speed. "
            "Exactly what we expect. "
            "Now consider the opposite situation. "
            "The road has reached its maximum possible density. "
            "Every available space is occupied. "
            "Substituting the jam density into the equation gives zero velocity. "
            "Once again, the model agrees perfectly with physical intuition."
        ):
            self.play(FadeIn(bc1, shift=RIGHT * 0.2), run_time=rt(0.7))
            self.play(FadeIn(bc2, shift=RIGHT * 0.2), run_time=rt(0.7))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(lin_title, gs_eq, gs_note, bcs)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 4. v vs ρ PLOT — TEACH THE VIEWER HOW TO READ IT
        # ─────────────────────────────────────────────────────────────────────
        plot_title = Text("Greenshields  v – ρ  Diagram",
                          font_size=30, weight=BOLD, color=WHITE)
        plot_title.to_edge(UP).shift(DOWN * 0.52)

        ax = Axes(
            x_range=[0, 1.18, 0.5],
            y_range=[0, 1.18, 0.5],
            x_length=5.2,
            y_length=4.0,
            axis_config={
                "color": GREY_B,
                "include_tip": True,
                "tip_width": 0.18,
                "tip_height": 0.22,
                "include_numbers": False,
            },
        )
        ax.to_edge(LEFT).shift(RIGHT * 0.6 + DOWN * 0.35)

        x_lbl = MathTex(r"\rho", font_size=28).next_to(ax.x_axis.get_end(), RIGHT * 0.6)
        y_lbl = MathTex(r"v",    font_size=28).next_to(ax.y_axis.get_end(), UP    * 0.6)

        rhoj_lbl = MathTex(r"\rho_j", font_size=21, color=RED
                           ).next_to(ax.c2p(1, 0), DOWN * 0.8)
        vf_lbl   = MathTex(r"v_f",    font_size=21, color=GREEN
                           ).next_to(ax.c2p(0, 1), LEFT * 0.8)

        graph_line = ax.plot(lambda x: 1 - x, x_range=[0, 1.0],
                             color="#4a90e2", stroke_width=3)

        dot_top = Dot(ax.c2p(0, 1), color=GREEN, radius=0.09)
        dot_bot = Dot(ax.c2p(1, 0), color=RED,   radius=0.09)

        panel = VGroup(
            MathTex(r"v(\rho) = v_f\!\left(1 - \tfrac{\rho}{\rho_j}\right)",
                    font_size=27, color=YELLOW),
            Text("Linear — speed decreases in direct\n"
                 "proportion to density increase.",
                 font_size=18, color="#aaaaaa", line_spacing=1.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        panel.move_to(RIGHT * 3.3 + DOWN * 0.4)

        with self.voiceover(
            "We can now visualise the entire relationship. "
            "Along the horizontal axis, we measure traffic density. "
            "Along the vertical axis, we measure traffic velocity. "
            "Every point on this line represents a possible traffic condition. "
            "Here, the road is empty, "
            "so vehicles travel at the free-flow speed. "
            "As density increases, average speed decreases steadily. "
            "Eventually, when the density reaches the jam density, "
            "traffic comes to a complete stop. "
            "The straight line reflects Greenshields' assumption "
            "that the relationship is linear — "
            "a direct proportional decrease in speed "
            "for every additional vehicle on the road."
        ):
            self.play(FadeIn(plot_title),                      run_time=rt(0.6))
            self.play(Create(ax), FadeIn(x_lbl, y_lbl),        run_time=rt(0.9))
            self.play(FadeIn(rhoj_lbl), FadeIn(vf_lbl),        run_time=rt(0.5))
            self.play(FadeIn(dot_top), FadeIn(dot_bot),         run_time=rt(0.4))
            self.play(Create(graph_line),                       run_time=rt(1.1))
            self.play(
                LaggedStart(*[FadeIn(p, shift=LEFT * 0.15) for p in panel],
                            lag_ratio=0.4),
                run_time=rt(0.9),
            )

        self.wait(rt(0.7))
        self.play(
            FadeOut(VGroup(plot_title, ax, x_lbl, y_lbl,
                           rhoj_lbl, vf_lbl, graph_line,
                           dot_top, dot_bot, panel)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. DERIVE THE TRAFFIC FLUX f(ρ) — ANTICIPATION THEN ALGEBRA
        # ─────────────────────────────────────────────────────────────────────
        deriv_title = Text("Combining the Two Results",
                           font_size=30, weight=BOLD, color=WHITE)
        deriv_title.to_edge(UP).shift(DOWN * 0.58)

        steps = VGroup(
            MathTex(r"q \;=\; \rho \cdot v(\rho)",
                    font_size=36),
            MathTex(r"=\; \rho \cdot v_f\!\left(1 - \frac{\rho}{\rho_j}\right)",
                    font_size=36),
            MathTex(r"f(\rho) \;=\; v_f\,\rho\!\left(1 - \frac{\rho}{\rho_j}\right)",
                    font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        steps.center().shift(UP * 0.25)

        para_note = MathTex(
            r"f(\rho)\;\text{is the }\textit{flux function}"
            r"\;\text{— quadratic in }\rho\text{, a downward parabola}",
            font_size=23, color="#8899cc",
        )
        para_note.next_to(steps, DOWN, buff=0.42)

        # Block A: anticipation before the algebra
        with self.voiceover(
            "We now have everything we need. "
            "Earlier, we derived the fundamental equation "
            "q equals rho times v. "
            "We have also obtained an explicit expression for velocity. "
            "So what happens if we combine the two?"
        ):
            self.play(FadeIn(deriv_title), run_time=rt(0.6))
            self.play(Write(steps[0]),     run_time=rt(0.9))

        self.wait(rt(0.3))

        # Block B: step-by-step substitution, pause after each step
        with self.voiceover(
            "We substitute the Greenshields expression for velocity "
            "directly into the flow equation. "
            "Expanding the product gives us a quadratic expression in density. "
            "This result is called the traffic flux function, "
            "written as f of rho."
        ):
            self.play(Write(steps[1]), run_time=rt(0.9))
            self.wait(rt(0.4))
            self.play(Write(steps[2]), run_time=rt(0.9))

        self.wait(rt(0.3))

        # Block C: explain what the flux function means
        with self.voiceover(
            "This function tells us how the traffic flow changes "
            "as the density changes. "
            "Unlike the velocity relationship, which is linear, "
            "the flux function is quadratic — a downward parabola. "
            "It equals zero when the road is empty "
            "and zero again when the road is at jam density. "
            "As we will soon see, "
            "this parabolic shape explains some of the most interesting "
            "behaviours observed in real traffic."
        ):
            self.play(FadeIn(para_note, shift=UP * 0.1), run_time=rt(0.7))

        self.wait(rt(0.7))
        self.play(FadeOut(VGroup(deriv_title, steps, para_note)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 6. TRANSITION — BUILD ANTICIPATION FOR THE FUNDAMENTAL DIAGRAM
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: The Fundamental Diagram",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_eq    = MathTex(
            r"f(\rho) = v_f\,\rho\!\left(1 - \dfrac{\rho}{\rho_j}\right)",
            font_size=44, color=YELLOW,
        )
        prev_desc  = Text(
            "Where is the maximum flow achieved?  At what density?",
            font_size=23, color="#8899cc",
        )

        prev_title.center().shift(UP * 1.6)
        prev_eq.next_to(prev_title, DOWN, buff=0.45)
        prev_desc.next_to(prev_eq,  DOWN, buff=0.38)

        with self.voiceover(
            "We now know how traffic flow depends on density. "
            "But what does this function actually look like? "
            "Where is the maximum traffic flow achieved? "
            "At what density does the road operate most efficiently? "
            "These questions are answered by one of the most important graphs "
            "in traffic flow theory: "
            "the Fundamental Diagram."
        ):
            self.play(Write(prev_title),                   run_time=rt(0.9))
            self.play(Write(prev_eq),                      run_time=rt(1.1))
            self.play(FadeIn(prev_desc, shift=UP * 0.1),   run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(prev_title, prev_eq, prev_desc)), run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene05_Greenshields",
    ])
