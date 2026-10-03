from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 13 — THE UPWIND FINITE DIFFERENCE SCHEME
#  Render: manim -pql scene13_upwind_scheme.py Scene13_UpwindScheme
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene13_UpwindScheme(VoiceoverScene):

    BG_COLOR = "#0d1117"

    # ── grid geometry ─────────────────────────────────────────────────────────
    N_J  = 6      # columns  j = 0 … 5
    N_N  = 4      # rows     n = 0 … 3
    DX   = 0.82   # horizontal cell size (Manim units)
    DT   = 0.95   # vertical   cell size
    GX0  = -5.60  # x-coord of j = 0
    GY0  = -2.00  # y-coord of n = 0

    def gp(self, j, n):
        return np.array([self.GX0 + j * self.DX, self.GY0 + n * self.DT, 0])

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT IV · Scene 13 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("The Upwind Finite Difference Scheme",
                     font_size=44, weight=BOLD, color=WHITE)
        sub   = Text("Discretising the LWR equation in space and time",
                     font_size=26, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "We now have everything a computer needs. "
            "We have divided the road into grid points. "
            "We have divided time into discrete time levels. "
            "We know the traffic density at the initial time. "
            "The only remaining question is: "
            "how do we compute the traffic density "
            "one time step later? "
            "The first numerical method we will study "
            "is called the Upwind scheme. "
            "Although the final formula looks simple, "
            "it is not chosen at random. "
            "It comes directly from one of the most important ideas "
            "we've already learned: "
            "the method of characteristics."
        ):
            self.play(Write(title),                     run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. RECALL THE GRID
        # ─────────────────────────────────────────────────────────────────────
        grid_title = Text("Recall: The Finite Difference Grid",
                          font_size=26, weight=BOLD, color=WHITE)
        grid_title.to_edge(UP).shift(DOWN * 0.52)

        # Horizontal grid lines (constant n)
        h_lines = VGroup(*[
            Line(self.gp(0, n), self.gp(self.N_J - 1, n),
                 color=GREY_B, stroke_width=0.8, stroke_opacity=0.30)
            for n in range(self.N_N)
        ])
        # Vertical grid lines (constant j)
        v_lines = VGroup(*[
            Line(self.gp(j, 0), self.gp(j, self.N_N - 1),
                 color=GREY_B, stroke_width=0.8, stroke_opacity=0.30)
            for j in range(self.N_J)
        ])
        # Grid dots
        grid_dots = VGroup(*[
            Dot(self.gp(j, n), radius=0.07, color=GREY_B, fill_opacity=0.55)
            for j in range(self.N_J)
            for n in range(self.N_N)
        ])

        # Axis arrows
        x_arrow = Arrow(
            self.gp(-0.3, -0.25), self.gp(self.N_J - 0.4, -0.25),
            color=GREY_B, stroke_width=1.8, buff=0,
            max_tip_length_to_length_ratio=0.06,
        )
        t_arrow = Arrow(
            self.gp(-0.45, -0.3), self.gp(-0.45, self.N_N - 0.4),
            color=GREY_B, stroke_width=1.8, buff=0,
            max_tip_length_to_length_ratio=0.06,
        )
        x_arrow_lbl = MathTex(r"j", font_size=22, color=GREY_B
                              ).next_to(x_arrow.get_end(), RIGHT * 0.4)
        t_arrow_lbl = MathTex(r"n", font_size=22, color=GREY_B
                              ).next_to(t_arrow.get_end(), UP * 0.4)

        # j and n index labels
        j_lbls = VGroup(*[
            MathTex(str(j), font_size=16, color="#777777"
                    ).next_to(self.gp(j, 0), DOWN * 0.75)
            for j in range(self.N_J)
        ])
        n_lbls = VGroup(*[
            MathTex(str(n), font_size=16, color="#777777"
                    ).next_to(self.gp(0, n), LEFT * 0.70)
            for n in range(self.N_N)
        ])

        recall_note = VGroup(
            MathTex(r"\rho_j^n \approx \rho(x_j,\,t^n)", font_size=24, color=YELLOW),
            Text("known bottom row  →  march forward, one row at a time",
                 font_size=18, color="#8899cc"),
        ).arrange(DOWN, buff=0.20)
        recall_note.move_to(RIGHT * 3.3 + UP * 1.0)

        # Rebuild the grid quickly — full teaching already happened in Scene 12
        with self.voiceover(
            "Before deriving the scheme, "
            "let's briefly recall the finite difference grid. "
            "Every point stores one numerical approximation, "
            "rho sub j superscript n. "
            "The bottom row comes from the initial condition. "
            "Our task is to compute every row above it, "
            "one time step at a time."
        ):
            self.play(FadeIn(grid_title),                              run_time=rt(0.4))
            self.play(Create(h_lines), Create(v_lines),                run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.7) for d in grid_dots], lag_ratio=0.02),
                run_time=rt(0.6),
            )
            self.play(
                GrowArrow(x_arrow), GrowArrow(t_arrow),
                FadeIn(x_arrow_lbl), FadeIn(t_arrow_lbl),
                run_time=rt(0.5),
            )
            self.play(FadeIn(j_lbls), FadeIn(n_lbls), run_time=rt(0.4))
            self.play(FadeIn(recall_note, shift=LEFT * 0.1),          run_time=rt(0.6))

        self.wait(rt(0.4))
        self.play(FadeOut(recall_note), run_time=rt(0.4))

        # ─────────────────────────────────────────────────────────────────────
        # 3. WHY "UPWIND"? — MOTIVATION FROM CHARACTERISTICS
        # ─────────────────────────────────────────────────────────────────────
        why_title = Text("Which Neighbours Do We Use?",
                         font_size=23, weight=BOLD, color=WHITE)
        why_title.move_to(RIGHT * 3.3 + UP * 2.0)

        why_body = VGroup(
            Text("From Scene 11:", font_size=18, weight=BOLD, color="#aaaacc"),
            Text("information travels at wave speed  c(ρ) = f'(ρ).", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        why_free = VGroup(
            Text("c > 0  (free flow):", font_size=18, weight=BOLD, color=GREEN),
            Text("  information arrives from the LEFT.", font_size=18, color=GREEN),
            Text("  → use the point at  j − 1  (backward difference).", font_size=18, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        why_cong = VGroup(
            Text("c < 0  (congested):", font_size=18, weight=BOLD, color=RED),
            Text("  information arrives from the RIGHT.", font_size=18, color=RED),
            Text("  → use the point at  j + 1  (forward difference).", font_size=18, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        why_sum = VGroup(
            Text("The scheme always looks upstream —", font_size=18, color=YELLOW),
            Text("in the direction information is coming from.", font_size=18, color=YELLOW),
            Text("Hence: the Upwind scheme.", font_size=18, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        why_panel = VGroup(why_body, why_free, why_cong, why_sum
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        why_panel.next_to(why_title, DOWN, buff=0.28)

        # Flow-direction arrows drawn on the grid itself, next to the
        # reference point used later for the stencil (j=3, n=1).
        FJ, FN = 3, 1
        flow_pt = self.gp(FJ, FN)
        flow_left_arrow = Arrow(
            self.gp(FJ - 1, FN), flow_pt, color=GREEN, stroke_width=3.5,
            buff=0.16, max_tip_length_to_length_ratio=0.35,
        )
        flow_right_arrow = Arrow(
            self.gp(FJ + 1, FN), flow_pt, color=RED, stroke_width=3.5,
            buff=0.16, max_tip_length_to_length_ratio=0.35,
        )

        # Block A: the question
        with self.voiceover(
            "Imagine you're trying to predict "
            "the traffic density at this point. "
            "Which neighbouring value should influence your prediction? "
            "Should you look to the left? "
            "Or should you look to the right? "
            "Surprisingly, "
            "the LWR equation already tells us the answer."
        ):
            self.play(FadeIn(why_title), run_time=rt(0.5))
            self.play(FadeIn(why_body,  shift=RIGHT * 0.1), run_time=rt(0.5))

        self.wait(rt(0.5))

        # Block B: the answer, with the flow visualised on the grid
        with self.voiceover(
            "Remember the characteristic curves. "
            "They showed us the direction "
            "in which traffic information travels. "
            "If the wave speed is positive, "
            "information arrives from the left. "
            "Therefore, the left neighbour "
            "contains the information we need. "
            "If the wave speed is negative, "
            "information arrives from the right. "
            "Then the right neighbour becomes the correct choice."
        ):
            self.play(FadeIn(why_free,  shift=RIGHT * 0.1), run_time=rt(0.5))
            self.play(GrowArrow(flow_left_arrow),            run_time=rt(0.5))
            self.wait(rt(0.3))
            self.play(FadeOut(flow_left_arrow),               run_time=rt(0.3))
            self.play(FadeIn(why_cong,  shift=RIGHT * 0.1), run_time=rt(0.5))
            self.play(GrowArrow(flow_right_arrow),            run_time=rt(0.5))
            self.wait(rt(0.3))
            self.play(FadeOut(flow_right_arrow),              run_time=rt(0.3))

        self.wait(rt(0.3))

        # Block C: name the method
        with self.voiceover(
            "In other words, "
            "we always look upstream — "
            "toward the direction from which information is coming. "
            "That simple idea gives the method its name: "
            "the Upwind scheme."
        ):
            self.play(FadeIn(why_sum,   shift=RIGHT * 0.1), run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(why_title, why_panel)), run_time=rt(0.5))

        # ─────────────────────────────────────────────────────────────────────
        # 4. DERIVATION + STENCIL (stencil on grid, algebra on right)
        # ─────────────────────────────────────────────────────────────────────
        SJ, SN = 3, 1   # stencil reference point

        dot_prev = Dot(self.gp(SJ - 1, SN),   radius=0.14, color=GREEN)
        dot_curr = Dot(self.gp(SJ,     SN),   radius=0.14, color=BLUE_B)
        dot_next = Dot(self.gp(SJ,     SN+1), radius=0.16, color=YELLOW)

        st_line1 = Line(self.gp(SJ-1, SN), self.gp(SJ, SN+1),
                        color=GREEN, stroke_width=2.2)
        st_line2 = Line(self.gp(SJ,   SN), self.gp(SJ, SN+1),
                        color=BLUE_B, stroke_width=2.2)

        lbl_prev = MathTex(r"\rho_{j-1}^n", font_size=16, color=GREEN
                           ).next_to(dot_prev, DOWN * 0.85)
        lbl_curr = MathTex(r"\rho_j^n",     font_size=16, color=BLUE_B
                           ).next_to(dot_curr, RIGHT * 0.75)
        lbl_next = MathTex(r"\rho_j^{n+1}", font_size=16, color=YELLOW
                           ).next_to(dot_next, UP * 0.85)

        stencil_grp = VGroup(dot_prev, dot_curr, dot_next,
                             st_line1, st_line2,
                             lbl_prev, lbl_curr, lbl_next)

        # Right panel: derivation steps
        deriv_title = Text("Derivation", font_size=23, weight=BOLD, color=WHITE)
        deriv_title.move_to(RIGHT * 3.3 + UP * 2.0)

        step_a = MathTex(
            r"\frac{\rho_j^{n+1}-\rho_j^n}{\Delta t}"
            r"+\frac{f_j^n - f_{j-1}^n}{\Delta x}=0",
            font_size=21,
        )
        step_a.next_to(deriv_title, DOWN, buff=0.38)

        step_a_note = Text("substitute forward-time, backward-space differences",
                           font_size=15, color="#888888")
        step_a_note.next_to(step_a, DOWN, buff=0.12)

        step_b = MathTex(
            r"\rho_j^{n+1} = \rho_j^n"
            r"- \frac{\Delta t}{\Delta x}\bigl(f_j^n - f_{j-1}^n\bigr)",
            font_size=21,
        )
        step_b.next_to(step_a_note, DOWN, buff=0.28)

        lam_def = MathTex(r"\lambda \;=\; \frac{\Delta t}{\Delta x}",
                          font_size=20, color="#8899cc")
        lam_def.next_to(step_b, DOWN, buff=0.22)

        final_eq = MathTex(
            r"\rho_j^{n+1} = \rho_j^n - \lambda\bigl(f_j^n - f_{j-1}^n\bigr)",
            font_size=24, color=YELLOW,
        )
        final_eq.next_to(lam_def, DOWN, buff=0.28)
        final_box = SurroundingRectangle(final_eq, color="#334466", buff=0.24)
        final_grp = VGroup(final_box, final_eq)

        # Block A: show stencil
        with self.voiceover(
            "To compute one new value, "
            "the Upwind scheme does not use the entire grid. "
            "It needs only three points: "
            "the current grid point, "
            "rho sub j superscript n; "
            "the upstream neighbour, "
            "rho sub j minus one superscript n; "
            "and the unknown point at the next time level, "
            "rho sub j superscript n plus one. "
            "This small collection of points "
            "is called the computational stencil."
        ):
            self.play(FadeIn(deriv_title), run_time=rt(0.5))
            self.play(
                FadeIn(dot_prev), FadeIn(dot_curr), FadeIn(dot_next),
                run_time=rt(0.6),
            )
            self.play(Create(st_line1), Create(st_line2), run_time=rt(0.5))
            self.play(FadeIn(lbl_prev), FadeIn(lbl_curr), FadeIn(lbl_next),
                      run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: substitute into LWR
        with self.voiceover(
            "We begin with the LWR equation. "
            "Since the computer cannot calculate derivatives directly, "
            "we replace each derivative "
            "with a finite difference approximation — "
            "a forward difference in time, "
            "and a backward difference in space. "
            "Substituting these approximations into the LWR equation "
            "produces a discrete equation "
            "relating the three stencil points."
        ):
            self.play(Write(step_a), run_time=rt(1.0))
            self.play(FadeIn(step_a_note, shift=UP * 0.1), run_time=rt(0.4))

        self.wait(rt(0.3))

        # Block C: rearrange for the unknown
        with self.voiceover(
            "Finally, we rearrange the equation "
            "so that the unknown value, "
            "rho sub j superscript n plus one, "
            "appears by itself. "
            "Writing lambda for the ratio of the time step to the spatial step, "
            "this gives us the numerical rule "
            "that the computer will apply repeatedly "
            "throughout the simulation."
        ):
            self.play(Write(step_b), run_time=rt(0.9))
            self.play(FadeIn(lam_def, shift=UP * 0.1), run_time=rt(0.5))
            self.wait(rt(0.3))
            self.play(Write(final_eq), Create(final_box), run_time=rt(0.9))

        self.wait(rt(0.4))

        # Block D: explain what the formula actually says
        with self.voiceover(
            "This formula tells a simple story. "
            "Start with the current traffic density. "
            "Then correct it "
            "according to the difference in traffic flow "
            "between the current point and its upstream neighbour. "
            "Repeating this calculation across every grid point, "
            "and at every time step, "
            "gradually builds the entire numerical solution."
        ):
            self.wait(rt(0.3))

        self.wait(rt(0.3))
        # Compact: keep stencil + boxed formula, remove intermediate steps
        self.play(
            FadeOut(VGroup(deriv_title, step_a, step_a_note, step_b, lam_def)),
            final_grp.animate.move_to(RIGHT * 3.3 + UP * 1.15),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. CFL STABILITY CONDITION
        # ─────────────────────────────────────────────────────────────────────
        cfl_title = Text("CFL Stability Condition",
                         font_size=23, weight=BOLD, color=WHITE)
        cfl_title.move_to(RIGHT * 3.3 + UP * 0.10)

        cfl_ineq = MathTex(
            r"\nu \;=\; \bigl|c(\rho)\bigr|\,\frac{\Delta t}{\Delta x} \;\leq\; 1",
            font_size=26, color=YELLOW,
        )
        cfl_ineq.next_to(cfl_title, DOWN, buff=0.28)

        cfl_rows = VGroup(
            Text("ν  is the CFL number  (Courant–Friedrichs–Lewy).", font_size=17, color="#cccccc"),
            Text("ν > 1 :  wave crosses more than one cell per step", font_size=17, color=RED),
            Text("         → information skipped → instability.", font_size=17, color=RED),
            Text("ν ≤ 1 :  the upwind scheme is stable.", font_size=17, color=GREEN),
            Text("For Greenshields:  max|c| = v_f  →  Δt ≤ Δx / v_f.", font_size=17, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        cfl_rows.next_to(cfl_ineq, DOWN, buff=0.26)

        # Block A: the question
        with self.voiceover(
            "Can we choose the time step to be as large as we like?"
        ):
            self.play(FadeIn(cfl_title), run_time=rt(0.5))

        self.wait(rt(0.4))

        # Block B: no — and why
        with self.voiceover(
            "Unfortunately, no. "
            "Remember that traffic information "
            "moves with the characteristic speed. "
            "During one time step, "
            "the disturbance should not travel "
            "farther than one grid cell. "
            "Otherwise, the numerical method "
            "will miss the information it is supposed to follow."
        ):
            self.play(Write(cfl_ineq),   run_time=rt(0.8))

        self.wait(rt(0.3))

        # Block C: name the condition
        with self.voiceover(
            "This requirement is known as the "
            "Courant-Friedrichs-Lewy, or CFL, condition. "
            "It is one of the most important stability conditions "
            "in numerical analysis. "
            "For the Greenshields model, "
            "the maximum wave speed equals v sub f. "
            "So we must choose a time step satisfying "
            "delta t at most delta x divided by v sub f."
        ):
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in cfl_rows],
                            lag_ratio=0.22),
                run_time=rt(0.9),
            )

        self.wait(rt(0.5))

        # Fade out everything — grid + all right-panel content
        self.play(
            FadeOut(VGroup(
                grid_title,
                h_lines, v_lines, grid_dots,
                x_arrow, t_arrow, x_arrow_lbl, t_arrow_lbl,
                j_lbls, n_lbls,
                stencil_grp,
                final_grp,
                cfl_title, cfl_ineq, cfl_rows,
            )),
            run_time=rt(0.9),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 6. PROPERTIES OF THE UPWIND SCHEME
        # ─────────────────────────────────────────────────────────────────────
        props_title = Text("Properties of the Upwind Scheme",
                           font_size=34, weight=BOLD, color=WHITE)
        props_title.to_edge(UP).shift(DOWN * 0.62)

        formula_ref = MathTex(
            r"\rho_j^{n+1} = \rho_j^n - \lambda\bigl(f_j^n - f_{j-1}^n\bigr)",
            font_size=28, color=YELLOW,
        )
        formula_ref.next_to(props_title, DOWN, buff=0.38)

        def prop_row(label, body, lbl_color=WHITE):
            return VGroup(
                Text(label + ":", font_size=20, weight=BOLD, color=lbl_color),
                Text("  " + body, font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.10)

        prop_rows = VGroup(
            prop_row("Accuracy",   "first-order in space and time  [ O(Δx) + O(Δt) ]",
                     lbl_color="#aaaacc"),
            prop_row("Stability",  "guaranteed when the CFL number  ν ≤ 1",
                     lbl_color="#aaaacc"),
            prop_row("Diffusion",  "numerical diffusion smears sharp shocks over several cells",
                     lbl_color="#aaaacc"),
            prop_row("Simplicity", "three-point stencil, easy to implement",
                     lbl_color="#aaaacc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        prop_rows.next_to(formula_ref, DOWN, buff=0.42)

        connect_note = VGroup(
            Text("This limitation matters for our project:", font_size=19, color="#cccccc"),
            Text("comparing how well each scheme captures", font_size=19, color="#cccccc"),
            Text("shock waves and rarefaction waves will be", font_size=19, color="#cccccc"),
            Text("a key point of comparison in the next scene.", font_size=19, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        connect_note.next_to(prop_rows, DOWN, buff=0.34)

        # Block A: properties, told as a story
        with self.voiceover(
            "The Upwind scheme has several important strengths. "
            "It is easy to implement. "
            "It is computationally efficient. "
            "And when the CFL condition is satisfied, "
            "it is stable. "
            "However, this simplicity comes at a price. "
            "Because the method is only first-order accurate, "
            "it introduces numerical diffusion. "
            "Instead of preserving sharp shock waves, "
            "it gradually smooths them out, "
            "making the transition between traffic states "
            "appear more gradual than it really is."
        ):
            self.play(FadeIn(props_title), run_time=rt(0.5))
            self.play(Write(formula_ref),  run_time=rt(0.9))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in prop_rows],
                            lag_ratio=0.28),
                run_time=rt(1.0),
            )

        self.wait(rt(0.3))

        # Block B: connect the limitation to this project's objective
        with self.voiceover(
            "This limitation is particularly important for our project. "
            "One of our objectives is to compare "
            "how different numerical methods "
            "capture shock waves and rarefaction waves. "
            "The numerical diffusion introduced by the Upwind scheme "
            "will become one of the key points of comparison "
            "in the next scene."
        ):
            self.play(FadeIn(connect_note, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(props_title, formula_ref, prop_rows, connect_note)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 7. PREVIEW — LAX-WENDROFF
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: The Lax-Wendroff Scheme",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_eq    = MathTex(
            r"\rho_j^{n+1} = \rho_j^n"
            r"- \frac{\lambda}{2}\bigl(f_{j+1}^n - f_{j-1}^n\bigr)"
            r"+ \frac{\lambda^2 c_j^n}{2}"
            r"\bigl(f_{j+1}^n - 2f_j^n + f_{j-1}^n\bigr)",
            font_size=24, color=YELLOW,
        )
        prev_desc  = Text(
            "Second-order accurate — but introduces numerical dispersion near shocks",
            font_size=22, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.8)
        prev_eq.next_to(prev_title, DOWN, buff=0.45)
        prev_desc.next_to(prev_eq,  DOWN, buff=0.40)

        with self.voiceover(
            "The Upwind scheme gives us "
            "a stable and reliable numerical solution. "
            "But it sacrifices accuracy near sharp traffic features. "
            "Naturally, we ask: "
            "can we build a method "
            "that preserves sharp shocks more accurately? "
            "The answer is yes. "
            "The next method, called the Lax-Wendroff scheme, "
            "achieves second-order accuracy "
            "by using additional mathematical information. "
            "But, as we'll discover, "
            "greater accuracy also introduces a new challenge: "
            "instead of numerical diffusion, "
            "Lax-Wendroff introduces numerical dispersion — "
            "spurious oscillations that appear near sharp features."
        ):
            self.play(Write(prev_title),                        run_time=rt(0.9))
            self.play(Write(prev_eq),                           run_time=rt(1.3))
            self.play(FadeIn(prev_desc, shift=UP * 0.1),        run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(
            FadeOut(VGroup(prev_title, prev_eq, prev_desc)),
            run_time=rt(0.8),
        )
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene13_UpwindScheme",
    ])
