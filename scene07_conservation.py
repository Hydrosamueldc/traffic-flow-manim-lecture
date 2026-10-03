from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 7 — CONSERVATION OF VEHICLES
#  Render: manim -pql scene07_conservation.py Scene07_Conservation
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene07_Conservation(VoiceoverScene):

    BG_COLOR  = "#0d1117"
    ASPHALT   = "#252525"
    SEG_COLOR = "#1a4a00"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT II · Scene 7 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE — SUMMARISE THE JOURNEY BEFORE INTRODUCING THE PDE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Conservation of Vehicles", font_size=50, weight=BOLD, color=WHITE)
        sub   = Text("Deriving the LWR partial differential equation",
                     font_size=26, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "Throughout this project, "
            "we have introduced the fundamental quantities needed to describe traffic. "
            "We learned how to measure traffic density. "
            "We introduced traffic velocity. "
            "We combined them to obtain the traffic flow. "
            "We selected the Greenshields velocity model. "
            "And we constructed the fundamental diagram. "
            "But despite everything we have learned, "
            "one important question remains unanswered. "
            "How does traffic density actually change over time? "
            "To answer that question, we need a governing equation."
        ):
            self.play(Write(title),                     run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. THE CONSERVATION PRINCIPLE — ASK FIRST, THEN STATE
        # ─────────────────────────────────────────────────────────────────────
        princ_title = Text("The Conservation Principle",
                           font_size=36, weight=BOLD, color=WHITE)
        princ_title.to_edge(UP).shift(DOWN * 0.62)

        law_txt = Text(
            "Vehicles are neither created nor destroyed on the road.",
            font_size=26, color=WHITE,
        )
        law_box = SurroundingRectangle(law_txt, color="#334455", buff=0.30)
        law_grp = VGroup(law_box, law_txt)
        law_grp.center().shift(UP * 0.9)

        balance = MathTex(
            r"\frac{d}{dt}\bigl(\text{vehicles in segment}\bigr)"
            r"\;=\; f_{\text{in}} - f_{\text{out}}",
            font_size=30,
        )
        balance.next_to(law_grp, DOWN, buff=0.50)

        balance_note = MathTex(
            r"f_{\text{in}} = f\!\bigl(\rho(x,t)\bigr),\qquad "
            r"f_{\text{out}} = f\!\bigl(\rho(x+\Delta x,\,t)\bigr)",
            font_size=25, color="#8899cc",
        )
        balance_note.next_to(balance, DOWN, buff=0.30)

        # Block A: pose the question before stating the principle
        with self.voiceover(
            "Imagine watching a short section of highway from above. "
            "Suppose that, after one minute, "
            "you notice there are more vehicles inside that section than before. "
            "How could that happen? "
            "There are really only two possibilities. "
            "Either more vehicles entered the section from one end, "
            "or fewer vehicles left through the other. "
            "There is no other possibility. "
            "Vehicles cannot suddenly appear out of nowhere. "
            "They cannot simply vanish. "
            "They can only move from one location to another. "
            "This simple observation is known as "
            "the principle of conservation of vehicles."
        ):
            self.play(FadeIn(princ_title),               run_time=rt(0.6))
            self.wait(rt(3.0))
            self.play(Create(law_box), Write(law_txt),   run_time=rt(1.0))

        self.wait(rt(0.4))

        # Block B: state the balance equation
        with self.voiceover(
            "The principle gives us an equation immediately. "
            "The number of vehicles inside a road segment "
            "changes only because of the difference "
            "between what flows in and what flows out. "
            "If more vehicles enter than leave, the count increases. "
            "If more vehicles leave than enter, the count decreases."
        ):
            self.play(Write(balance), run_time=rt(0.9))

        self.wait(rt(0.3))

        # Block C: identify the two flux terms
        with self.voiceover(
            "The inflow at the left boundary is determined by the traffic flow function "
            "evaluated at position x. "
            "The outflow at the right boundary is determined by the same function "
            "evaluated at position x plus delta x. "
            "Both are evaluated at the current time t."
        ):
            self.play(FadeIn(balance_note, shift=UP * 0.1), run_time=rt(0.7))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(princ_title, law_grp, balance, balance_note)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 3. ROAD SEGMENT DIAGRAM — SLOWED INTO THREE BLOCKS
        # ─────────────────────────────────────────────────────────────────────
        RY, RH = -1.9, 0.9

        road     = Rectangle(width=14.0, height=RH,
                             fill_color=self.ASPHALT, fill_opacity=1,
                             stroke_width=0).move_to([0, RY, 0])
        road_top = Line(LEFT * 7, RIGHT * 7, color=WHITE, stroke_width=1.5
                        ).move_to([0, RY + RH / 2, 0])
        road_bot = Line(LEFT * 7, RIGHT * 7, color=WHITE, stroke_width=1.5
                        ).move_to([0, RY - RH / 2, 0])

        SEG_X0, SEG_X1 = -2.5, 2.5
        seg = Rectangle(
            width=SEG_X1 - SEG_X0, height=RH,
            fill_color=self.SEG_COLOR, fill_opacity=0.55,
            stroke_color="#55cc44", stroke_width=1.8,
        ).move_to([(SEG_X0 + SEG_X1) / 2, RY, 0])

        bd_left  = DashedLine(
            [SEG_X0, RY - RH / 2 - 0.05, 0], [SEG_X0, RY + RH / 2 + 0.50, 0],
            color="#55cc44", stroke_width=1.8, dash_length=0.15,
        )
        bd_right = DashedLine(
            [SEG_X1, RY - RH / 2 - 0.05, 0], [SEG_X1, RY + RH / 2 + 0.50, 0],
            color="#55cc44", stroke_width=1.8, dash_length=0.15,
        )

        x_lbl   = MathTex(r"x",            font_size=24, color="#55cc44"
                          ).next_to([SEG_X0, RY - RH / 2, 0], DOWN * 0.85)
        xdx_lbl = MathTex(r"x + \Delta x", font_size=24, color="#55cc44"
                          ).next_to([SEG_X1, RY - RH / 2, 0], DOWN * 0.85)

        dx_arr = DoubleArrow(
            start=[SEG_X0, RY - RH / 2 - 0.65, 0],
            end=[SEG_X1,   RY - RH / 2 - 0.65, 0],
            color="#55cc44", stroke_width=1.8, buff=0,
            max_tip_length_to_length_ratio=0.05,
        )
        dx_lbl = MathTex(r"\Delta x", font_size=22, color="#55cc44"
                         ).next_to(dx_arr, DOWN, buff=0.1)

        veh_dots = VGroup(*[
            Dot([SEG_X0 + 0.75 + i * 1.1, RY, 0], radius=0.13,
                color=["#4a90e2", "#e74c3c", "#2ecc71", "#f39c12"][i])
            for i in range(4)
        ])
        N_lbl = MathTex(r"N(t) = \rho\,\Delta x", font_size=22, color="#aaaaaa")
        N_lbl.move_to([0, RY + RH / 2 + 0.30, 0])

        flux_in_arr  = Arrow([-5.5, RY, 0], [SEG_X0 - 0.05, RY, 0],
                             color=GREEN, stroke_width=3, buff=0,
                             max_tip_length_to_length_ratio=0.11)
        flux_out_arr = Arrow([SEG_X1 + 0.05, RY, 0], [5.5, RY, 0],
                             color=RED,   stroke_width=3, buff=0,
                             max_tip_length_to_length_ratio=0.11)

        fin_lbl  = MathTex(r"f(\rho(x,t))",          font_size=20, color=GREEN)
        fout_lbl = MathTex(r"f(\rho(x+\Delta x,t))", font_size=20, color=RED)
        fin_lbl.next_to(flux_in_arr,  UP, buff=0.14)
        fout_lbl.next_to(flux_out_arr, UP, buff=0.14)

        diag_title = Text("Road Segment  [x,  x + Δx]",
                          font_size=28, weight=BOLD, color=WHITE)
        diag_title.to_edge(UP).shift(DOWN * 0.52)

        # Block A: introduce the control volume
        with self.voiceover(
            "Consider a small section of road "
            "extending from position x to position x plus delta x. "
            "We call this our control volume — "
            "a fixed region of the road that we observe over time. "
            "Rather than studying the entire highway at once, "
            "we focus our attention on this small region."
        ):
            self.play(
                FadeIn(diag_title), FadeIn(road), FadeIn(road_top), FadeIn(road_bot),
                run_time=rt(0.8),
            )
            self.play(FadeIn(seg),                                  run_time=rt(0.5))
            self.play(
                Create(bd_left), Create(bd_right),
                FadeIn(x_lbl), FadeIn(xdx_lbl),
                run_time=rt(0.6),
            )
            self.play(Create(dx_arr), FadeIn(dx_lbl),               run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: count vehicles inside the segment
        with self.voiceover(
            "If the traffic density inside the segment is rho, "
            "and the segment has length delta x, "
            "then the total number of vehicles inside the segment "
            "is simply density multiplied by length. "
            "Notice that the road itself has not changed — "
            "the length remains the same. "
            "Only the number of vehicles occupying that space is being counted."
        ):
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.7) for d in veh_dots], lag_ratio=0.12),
                FadeIn(N_lbl),
                run_time=rt(0.9),
            )

        self.wait(rt(0.3))

        # Block C: flux in and out
        with self.voiceover(
            "Vehicles continuously enter the segment from the left. "
            "At the same time, vehicles leave through the right boundary. "
            "If more vehicles enter than leave, "
            "the density inside increases. "
            "If more vehicles leave than enter, "
            "the density inside decreases. "
            "The rate of change inside is exactly "
            "the difference between those two fluxes."
        ):
            self.play(GrowArrow(flux_in_arr),  FadeIn(fin_lbl),  run_time=rt(0.7))
            self.play(GrowArrow(flux_out_arr), FadeIn(fout_lbl), run_time=rt(0.7))

        self.wait(rt(0.5))

        diag_group = VGroup(
            diag_title, road, road_top, road_bot, seg,
            bd_left, bd_right, x_lbl, xdx_lbl, dx_arr, dx_lbl,
            veh_dots, N_lbl, flux_in_arr, flux_out_arr, fin_lbl, fout_lbl,
        )
        self.play(FadeOut(diag_group), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 4. ALGEBRAIC DERIVATION — ONE VOICEOVER BLOCK PER STEP
        # ─────────────────────────────────────────────────────────────────────
        deriv_title = Text("From Conservation to PDE",
                           font_size=34, weight=BOLD, color=WHITE)
        deriv_title.to_edge(UP).shift(DOWN * 0.62)

        s1 = MathTex(
            r"\bigl[\rho(x,t+\Delta t)-\rho(x,t)\bigr]\Delta x"
            r"\;=\;\bigl[f(\rho(x,t))-f(\rho(x+\Delta x,t))\bigr]\Delta t",
            font_size=23,
        )
        s2 = MathTex(
            r"\frac{\rho(x,t+\Delta t)-\rho(x,t)}{\Delta t}"
            r"\;=\;-\frac{f(\rho(x+\Delta x,t))-f(\rho(x,t))}{\Delta x}",
            font_size=23,
        )
        s3 = MathTex(
            r"\xrightarrow{\;\Delta t,\,\Delta x\;\to\;0\;}",
            font_size=26, color="#aaaaaa",
        )
        s4 = MathTex(
            r"\frac{\partial \rho}{\partial t}"
            r"+ \frac{\partial f(\rho)}{\partial x} = 0",
            font_size=44, color=YELLOW,
        )

        deriv_steps = VGroup(s1, s2, s3).arrange(DOWN, buff=0.44, aligned_edge=LEFT)
        deriv_steps.center().shift(UP * 0.85)
        s4.next_to(deriv_steps, DOWN, buff=0.40)
        s4_box = SurroundingRectangle(s4, color="#334466", buff=0.28)

        self.play(FadeIn(deriv_title), run_time=rt(0.6))

        # Step 1: balance equation
        with self.voiceover(
            "We begin by expressing the change in the number of vehicles "
            "over a short time interval delta t. "
            "The left side represents the change in the number of vehicles "
            "inside the segment — "
            "the density after the interval minus the density before it, "
            "multiplied by the length delta x. "
            "The right side represents the net flow — "
            "what enters from the left minus what leaves through the right, "
            "multiplied by the time interval delta t."
        ):
            self.play(Write(s1), run_time=rt(1.3))

        self.wait(rt(0.4))

        # Step 2: divide by Δx and Δt
        with self.voiceover(
            "Next, we divide both sides by the length of the segment "
            "and by the time interval. "
            "On the left side, this gives us the rate of change of density. "
            "On the right side, it gives us the spatial difference in flow, "
            "also expressed as a rate."
        ):
            self.play(Write(s2), run_time=rt(1.2))

        self.wait(rt(0.4))

        # Step 3: take the limit
        with self.voiceover(
            "Finally, we imagine making both the length of the segment "
            "and the time interval smaller and smaller — "
            "shrinking them toward zero. "
            "In this limit, "
            "the finite differences on both sides "
            "become partial derivatives. "
            "The left side becomes the partial derivative of density with respect to time. "
            "The right side becomes the partial derivative of flow with respect to position. "
            "And the result is a partial differential equation."
        ):
            self.play(FadeIn(s3, shift=DOWN * 0.1), run_time=rt(0.5))
            self.play(Write(s4), Create(s4_box),    run_time=rt(1.0))

        self.wait(rt(0.8))
        self.play(
            FadeOut(VGroup(deriv_title, deriv_steps, s4_box)),
            s4.animate.move_to(ORIGIN),
            run_time=rt(1.0),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. THE LWR MODEL — REVEAL, EXPLAIN TERMS, DIFFICULTY, PROJECT
        # ─────────────────────────────────────────────────────────────────────
        lwr_title = Text("The LWR Traffic Flow Model",
                         font_size=36, weight=BOLD, color=WHITE)
        lwr_title.to_edge(UP).shift(DOWN * 0.62)

        lwr_eq = s4   # already at ORIGIN

        # Term-by-term annotations (shown then faded before gs_sub appears)
        term1_row = VGroup(
            MathTex(r"\frac{\partial\rho}{\partial t}", font_size=28, color=YELLOW),
            Text("—  rate of change of density with time",
                 font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.28)

        term2_row = VGroup(
            MathTex(r"\frac{\partial f(\rho)}{\partial x}", font_size=28, color=YELLOW),
            Text("—  rate of change of flow with position",
                 font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.28)

        terms_grp = VGroup(term1_row, term2_row).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        terms_grp.next_to(lwr_eq, DOWN, buff=0.55)

        gs_sub = MathTex(
            r"f(\rho) = v_f\,\rho\!\left(1 - \frac{\rho}{\rho_j}\right)"
            r"\quad\text{(Greenshields flux)}",
            font_size=27, color="#8899cc",
        )
        gs_sub.next_to(lwr_eq, DOWN, buff=0.50)

        props = VGroup(
            Text("The equation is nonlinear — smooth solutions can break down",
                 font_size=21, color="#cccccc"),
            Text("Shock waves can form and propagate under realistic conditions",
                 font_size=21, color="#cccccc"),
            Text("Exact solutions are often impossible — numerical methods are essential",
                 font_size=21, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        props.next_to(gs_sub, DOWN, buff=0.36)

        # Block A: the major reveal — let it breathe
        with self.voiceover(
            "This is the Lighthill-Whitham-Richards equation, "
            "commonly known as the LWR model. "
            "It is the mathematical law that governs "
            "how traffic density evolves over both space and time. "
            "Every scene in this project has been leading to this moment. "
            "Take a moment to appreciate what this equation represents."
        ):
            self.play(FadeIn(lwr_title), run_time=rt(0.6))
            self.wait(rt(2.5))

        self.wait(rt(0.4))

        # Block B: explain every term
        with self.voiceover(
            "Let us read the equation carefully, term by term. "
            "The first term, partial rho over partial t, "
            "describes how traffic density changes with time "
            "at a fixed position on the road. "
            "The second term, partial f of rho over partial x, "
            "describes how the traffic flow changes "
            "from one location to the next. "
            "Together, these two terms enforce the conservation of vehicles. "
            "If the flow is decreasing along the road, "
            "more vehicles are accumulating — density increases. "
            "If the flow is increasing, vehicles are spreading out — density decreases. "
            "The equation says: those two effects must always balance."
        ):
            self.play(
                LaggedStart(
                    FadeIn(term1_row, shift=RIGHT * 0.15),
                    FadeIn(term2_row, shift=RIGHT * 0.15),
                    lag_ratio=0.45,
                ),
                run_time=rt(0.9),
            )
            self.wait(rt(2.2))

        self.wait(rt(0.4))
        self.play(FadeOut(terms_grp), run_time=rt(0.5))

        # Block C: substitute Greenshields
        with self.voiceover(
            "Substituting the Greenshields flux function "
            "that we derived in Scene Five "
            "gives us a fully specified model. "
            "We now have a single equation with a single unknown: "
            "the density field rho of x and t."
        ):
            self.play(FadeIn(gs_sub, shift=UP * 0.1), run_time=rt(0.8))

        self.wait(rt(0.4))

        # Block D: why it is difficult to solve
        with self.voiceover(
            "Although the equation looks compact, "
            "solving it is not always straightforward. "
            "The traffic flow function is nonlinear, "
            "which means the equation itself is nonlinear. "
            "Under realistic traffic conditions, "
            "smooth solutions can break down. "
            "Abrupt changes in density — known as shock waves — "
            "can form and propagate through the traffic stream. "
            "These are mathematically sharp discontinuities "
            "that cannot be captured by simple algebraic formulas."
        ):
            self.play(
                LaggedStart(
                    FadeIn(props[0], shift=RIGHT * 0.2),
                    FadeIn(props[1], shift=RIGHT * 0.2),
                    lag_ratio=0.40,
                ),
                run_time=rt(0.9),
            )

        self.wait(rt(0.4))

        # Block E: connect to the project
        with self.voiceover(
            "This brings us to the central objective of this project. "
            "Rather than searching for exact analytical solutions, "
            "we will approximate the solution of the LWR equation "
            "using finite difference numerical methods. "
            "Specifically, we will implement and compare "
            "two numerical schemes: "
            "the Upwind scheme and the Lax-Wendroff scheme. "
            "We will evaluate their accuracy, their stability, "
            "and their ability to capture important traffic phenomena "
            "such as the formation and propagation of shock waves."
        ):
            self.play(FadeIn(props[2], shift=RIGHT * 0.2), run_time=rt(0.7))
            self.wait(rt(1.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(lwr_title, lwr_eq, gs_sub, props)), run_time=rt(0.8))

        # ─────────────────────────────────────────────────────────────────────
        # 5b. KEY TAKEAWAYS
        # ─────────────────────────────────────────────────────────────────────
        kt_title = Text("Key Takeaways", font_size=34, weight=BOLD, color="#e8b84b")
        kt_title.to_edge(UP).shift(DOWN * 0.62)

        kt_bullets = VGroup(
            Text("• Vehicles are conserved — never created or destroyed on the road.",
                 font_size=23, color=WHITE),
            Text("• Balancing inflow and outflow across a small segment gives a PDE.",
                 font_size=23, color=WHITE),
            Text("• The result is the LWR equation:  ∂ρ/∂t + ∂f(ρ)/∂x = 0.",
                 font_size=23, color=YELLOW),
            Text("• Because f(ρ) is nonlinear, this equation can form shock waves.",
                 font_size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        kt_bullets.next_to(kt_title, DOWN, buff=0.55)

        with self.voiceover(
            "Before moving on, let's recap. "
            "Vehicles are conserved — never created or destroyed on the road. "
            "Balancing inflow and outflow across a small segment gives us a PDE. "
            "The result is the LWR equation, "
            "relating the density and flow of traffic. "
            "And because the flow function is nonlinear, "
            "this equation can form shock waves."
        ):
            self.play(FadeIn(kt_title), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in kt_bullets],
                            lag_ratio=0.35),
                run_time=rt(1.6),
            )
            self.wait(rt(1.5))

        self.wait(rt(0.4))
        self.play(FadeOut(VGroup(kt_title, kt_bullets)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 6. PREVIEW — METHOD OF CHARACTERISTICS
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Method of Characteristics",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_eq    = MathTex(
            r"\frac{dx}{dt} = f'(\rho) = c(\rho)",
            font_size=52, color=YELLOW,
        )
        prev_desc  = Text(
            "Characteristic curves — lines of constant density in (x, t) space",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.6)
        prev_eq.next_to(prev_title, DOWN, buff=0.45)
        prev_desc.next_to(prev_eq,  DOWN, buff=0.38)

        with self.voiceover(
            "Before we can approximate the solution numerically, "
            "we first need to understand "
            "how information travels through the LWR equation itself. "
            "This naturally leads us to one of the most powerful analytical tools "
            "for first-order hyperbolic equations: "
            "the method of characteristics. "
            "Understanding the characteristic structure of the equation "
            "is what makes the design of numerical schemes non-trivial — "
            "and it will explain why the two schemes we study "
            "behave so differently from each other."
        ):
            self.play(Write(prev_title),                         run_time=rt(0.9))
            self.play(Write(prev_eq),                            run_time=rt(1.1))
            self.play(FadeIn(prev_desc, shift=UP * 0.1),         run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(prev_title, prev_eq, prev_desc)), run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene07_Conservation",
    ])
