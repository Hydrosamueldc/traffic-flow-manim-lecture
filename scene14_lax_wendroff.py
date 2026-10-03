from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 14 — THE LAX-WENDROFF SCHEME
#  Render: manim -pql scene14_lax_wendroff.py Scene14_LaxWendroff
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene14_LaxWendroff(VoiceoverScene):

    BG_COLOR = "#0d1117"

    # ── grid geometry (shared visual language with Scene 13) ──────────────────
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

        progress_lbl = Text("ACT IV · Scene 14 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("The Lax-Wendroff Scheme",
                     font_size=46, weight=BOLD, color=WHITE)
        sub   = Text("Trading simplicity for second-order accuracy",
                     font_size=26, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "In the previous scene, "
            "we developed the Upwind scheme. "
            "It was simple. "
            "Stable. "
            "Easy to implement. "
            "But it had one important weakness. "
            "Whenever a sharp shock wave appeared, "
            "the solution became increasingly blurred. "
            "This effect, known as numerical diffusion, "
            "reduced the accuracy of the simulation. "
            "Naturally, we ask: "
            "can we improve the accuracy "
            "without abandoning the finite difference approach? "
            "The answer is yes. "
            "The method we study in this scene "
            "is called the Lax-Wendroff scheme."
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

        h_lines = VGroup(*[
            Line(self.gp(0, n), self.gp(self.N_J - 1, n),
                 color=GREY_B, stroke_width=0.8, stroke_opacity=0.30)
            for n in range(self.N_N)
        ])
        v_lines = VGroup(*[
            Line(self.gp(j, 0), self.gp(j, self.N_N - 1),
                 color=GREY_B, stroke_width=0.8, stroke_opacity=0.30)
            for j in range(self.N_J)
        ])
        grid_dots = VGroup(*[
            Dot(self.gp(j, n), radius=0.07, color=GREY_B, fill_opacity=0.55)
            for j in range(self.N_J)
            for n in range(self.N_N)
        ])

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
            Text("The Upwind scheme:", font_size=19, color="#aaaacc"),
            MathTex(r"\rho_j^{n+1} = \rho_j^n - \lambda\bigl(f_j^n - f_{j-1}^n\bigr)",
                    font_size=22, color="#8899cc"),
            Text("stable, but smears sharp shocks.", font_size=19, color="#aaaacc"),
        ).arrange(DOWN, buff=0.20)
        recall_note.move_to(RIGHT * 3.3 + UP * 1.0)

        with self.voiceover(
            "The computational grid remains exactly the same. "
            "Every grid point stores "
            "one approximation of the traffic density. "
            "The difference lies not in the grid, "
            "but in how we update those values."
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
        # 3. THE BIG IDEA — KEEP MORE OF THE TAYLOR SERIES
        # ─────────────────────────────────────────────────────────────────────
        idea_title = Text("The Big Idea",
                          font_size=25, weight=BOLD, color=WHITE)
        idea_title.move_to(RIGHT * 3.3 + UP * 2.0)

        taylor_full = MathTex(
            r"\rho(x,t+\Delta t) = \rho + \Delta t\,\rho_t"
            r"+ \frac{\Delta t^2}{2}\rho_{tt} + \cdots",
            font_size=22, color=WHITE,
        )
        taylor_full.next_to(idea_title, DOWN, buff=0.30)

        # A small "staircase" visual: each rung is one more Taylor term,
        # with Upwind stopping early and Lax-Wendroff climbing one step higher.
        stair = VGroup(
            Text("●  current value  ρ", font_size=17, color="#cccccc"),
            Text("↑   + Δt·ρₜ   (first-order)", font_size=17, color="#4a90e2"),
            Text("●   ← Upwind stops here", font_size=16, weight=BOLD, color="#4a90e2"),
            Text("↑   + (Δt²/2)·ρₜₜ   (second-order)", font_size=17, color=YELLOW),
            Text("●   ← Lax-Wendroff continues", font_size=16, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        stair.next_to(taylor_full, DOWN, buff=0.40)

        # Block A: the question, framed as prediction
        with self.voiceover(
            "Why was the Upwind scheme only first-order accurate? "
            "The answer comes from a familiar mathematical tool: "
            "the Taylor series. "
            "Think of the Taylor series "
            "as a way of predicting the future "
            "using information available at the present. "
            "Every additional term we keep "
            "improves that prediction."
        ):
            self.play(FadeIn(idea_title), run_time=rt(0.5))
            self.play(Write(taylor_full), run_time=rt(1.1))
            self.play(FadeIn(stair[0], shift=UP * 0.1), run_time=rt(0.4))

        self.wait(rt(0.3))

        # Block B: Upwind stops at the first rung
        with self.voiceover(
            "The Upwind scheme keeps only the first-order information. "
            "Everything else is discarded. "
            "That simplification makes the method stable, "
            "but it also limits its accuracy."
        ):
            self.play(FadeIn(stair[1], shift=UP * 0.1), run_time=rt(0.5))
            self.play(FadeIn(stair[2], shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.4))

        # Block C: Lax-Wendroff climbs one step higher
        with self.voiceover(
            "The Lax-Wendroff scheme keeps one additional term. "
            "Surprisingly, "
            "this single decision changes the behaviour "
            "of the entire numerical method."
        ):
            self.play(FadeIn(stair[3], shift=UP * 0.1), run_time=rt(0.5))
            self.play(FadeIn(stair[4], shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(idea_title, taylor_full, stair)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 4. THE SECOND TIME DERIVATIVE — USING THE PDE TWICE
        # ─────────────────────────────────────────────────────────────────────
        pde_title = Text("Using the PDE Twice",
                         font_size=25, weight=BOLD, color=WHITE)
        pde_title.move_to(RIGHT * 3.3 + UP * 2.0)

        pde_step1 = MathTex(
            r"\text{LWR: }\quad \rho_t = -f_x",
            font_size=22,
        )
        pde_step2 = MathTex(
            r"\rho_{tt} = -(f_t)_x = -(c\,\rho_t)_x = (c\,f_x)_x",
            font_size=21,
        )
        pde_step3 = MathTex(
            r"\approx\; c\,f_{xx}",
            font_size=22, color="#8899cc",
        )
        pde_note = Text(
            "treating c as locally constant near this grid point",
            font_size=15, color="#888888",
        )

        pde_panel = VGroup(pde_step1, pde_step2, pde_step3, pde_note
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        pde_panel.next_to(pde_title, DOWN, buff=0.30)

        # Block A: the extra term contains an unknown quantity
        with self.voiceover(
            "The extra Taylor term "
            "contains a quantity we don't yet know: "
            "the second derivative with respect to time. "
            "At first, this seems like a problem. "
            "But remember — "
            "the LWR equation already tells us "
            "how the traffic density changes with time."
        ):
            self.play(FadeIn(pde_title), run_time=rt(0.5))
            self.play(Write(pde_step1),  run_time=rt(0.8))

        self.wait(rt(0.3))

        # Block B: reuse the governing equation instead of guessing
        with self.voiceover(
            "So instead of introducing a new unknown, "
            "we simply use the governing equation again. "
            "By differentiating the LWR equation "
            "one more time, "
            "we convert the unknown time derivative "
            "into spatial derivatives — "
            "quantities we already know how to approximate "
            "on the computational grid."
        ):
            self.play(Write(pde_step2), run_time=rt(1.0))

        self.wait(rt(0.3))

        # Block C: the frozen-coefficient simplification
        with self.voiceover(
            "Treating the wave speed c "
            "as locally constant near this grid point — "
            "a reasonable approximation over one small time step — "
            "this simplifies to c times the second spatial derivative of the flux. "
            "We now have everything we need "
            "to write down the full update rule."
        ):
            self.play(Write(pde_step3), run_time=rt(0.7))
            self.play(FadeIn(pde_note, shift=UP * 0.1), run_time=rt(0.4))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(pde_title, pde_panel)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 5. THE STENCIL — FOUR POINTS INSTEAD OF THREE
        # ─────────────────────────────────────────────────────────────────────
        SJ, SN = 3, 1

        dot_left  = Dot(self.gp(SJ - 1, SN),   radius=0.14, color=GREEN)
        dot_curr  = Dot(self.gp(SJ,     SN),   radius=0.14, color=BLUE_B)
        dot_right = Dot(self.gp(SJ + 1, SN),   radius=0.14, color="#cc66ff")
        dot_next  = Dot(self.gp(SJ,     SN+1), radius=0.16, color=YELLOW)

        st_line1 = Line(self.gp(SJ-1, SN), self.gp(SJ, SN+1), color=GREEN,     stroke_width=2.0)
        st_line2 = Line(self.gp(SJ,   SN), self.gp(SJ, SN+1), color=BLUE_B,    stroke_width=2.0)
        st_line3 = Line(self.gp(SJ+1, SN), self.gp(SJ, SN+1), color="#cc66ff", stroke_width=2.0)

        lbl_left  = MathTex(r"\rho_{j-1}^n", font_size=16, color=GREEN
                            ).next_to(dot_left, DOWN * 0.85)
        lbl_curr  = MathTex(r"\rho_j^n",     font_size=16, color=BLUE_B
                            ).next_to(dot_curr, DOWN * 0.85)
        lbl_right = MathTex(r"\rho_{j+1}^n", font_size=16, color="#cc66ff"
                            ).next_to(dot_right, DOWN * 0.85)
        lbl_next  = MathTex(r"\rho_j^{n+1}", font_size=16, color=YELLOW
                            ).next_to(dot_next, UP * 0.85)

        stencil_grp = VGroup(dot_left, dot_curr, dot_right, dot_next,
                             st_line1, st_line2, st_line3,
                             lbl_left, lbl_curr, lbl_right, lbl_next)

        stencil_note = VGroup(
            Text("Upwind used two points at time n.", font_size=19, color="#aaaacc"),
            Text("Lax-Wendroff uses three —", font_size=19, weight=BOLD, color=YELLOW),
            Text("one on each side of the current point.", font_size=19, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        stencil_note.move_to(RIGHT * 3.3 + UP * 1.4)

        with self.voiceover(
            "Notice how the stencil has changed. "
            "The Upwind scheme looked primarily in one direction, "
            "following the flow of information. "
            "The Lax-Wendroff scheme "
            "takes a more balanced view. "
            "It gathers information "
            "from both neighbouring points simultaneously — "
            "the point to the left, "
            "and the point to the right. "
            "This wider stencil captures more "
            "of the local behaviour of the solution, "
            "leading to higher accuracy."
        ):
            self.play(
                FadeIn(dot_left), FadeIn(dot_curr), FadeIn(dot_right), FadeIn(dot_next),
                run_time=rt(0.7),
            )
            self.play(Create(st_line1), Create(st_line2), Create(st_line3), run_time=rt(0.5))
            self.play(
                FadeIn(lbl_left), FadeIn(lbl_curr), FadeIn(lbl_right), FadeIn(lbl_next),
                run_time=rt(0.5),
            )
            self.play(FadeIn(stencil_note, shift=LEFT * 0.1), run_time=rt(0.6))

        self.wait(rt(0.5))
        self.play(FadeOut(stencil_note), run_time=rt(0.4))

        # ─────────────────────────────────────────────────────────────────────
        # 6. THE FINAL FORMULA
        # ─────────────────────────────────────────────────────────────────────
        formula_title = Text("The Lax-Wendroff Update Rule",
                             font_size=23, weight=BOLD, color=WHITE)
        formula_title.move_to(RIGHT * 3.3 + UP * 2.0)

        sub_step = MathTex(
            r"\rho_j^{n+1} = \rho_j^n - \Delta t\,f_x + \frac{\Delta t^2}{2}\,c\,f_{xx}",
            font_size=20,
        )
        sub_note = Text(
            "central differences:  f_x ≈ (f_{j+1}-f_{j-1})/2Δx,  f_xx ≈ (f_{j+1}-2f_j+f_{j-1})/Δx²",
            font_size=13, color="#888888",
        )

        final_eq = MathTex(
            r"\rho_j^{n+1} = \rho_j^n"
            r"- \frac{\lambda}{2}\bigl(f_{j+1}^n - f_{j-1}^n\bigr)"
            r"+ \frac{\lambda^2 c_j^n}{2}"
            r"\bigl(f_{j+1}^n - 2f_j^n + f_{j-1}^n\bigr)",
            font_size=22, color=YELLOW,
        )

        formula_panel = VGroup(sub_step, sub_note).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        formula_panel.next_to(formula_title, DOWN, buff=0.30)
        final_eq.next_to(formula_panel, DOWN, buff=0.40)
        final_box = SurroundingRectangle(final_eq, color="#334466", buff=0.22)
        final_grp = VGroup(final_box, final_eq)

        # Block A: substitute central differences
        with self.voiceover(
            "We substitute central differences "
            "for the spatial derivative of the flux "
            "and its second derivative — "
            "one using the left and right neighbours, "
            "the other using all three stencil points."
        ):
            self.play(FadeIn(formula_title), run_time=rt(0.5))
            self.play(Write(sub_step),       run_time=rt(1.0))
            self.play(FadeIn(sub_note, shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.4))

        # Block B: reveal the boxed formula — explain meaning, not algebra
        with self.voiceover(
            "This gives us the complete Lax-Wendroff update rule. "
            "Although this equation looks more complicated, "
            "its structure is surprisingly logical. "
            "The first correction term "
            "estimates how traffic flow changes "
            "across neighbouring grid points. "
            "The second correction term "
            "compensates for the leading truncation error "
            "of that first approximation, "
            "allowing the scheme "
            "to achieve second-order accuracy. "
            "Together, they produce a much more accurate prediction "
            "of the future traffic density."
        ):
            self.play(Write(final_eq), run_time=rt(1.4))
            self.play(Create(final_box), run_time=rt(0.5))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(formula_title, sub_step, sub_note)),
            final_grp.animate.move_to(RIGHT * 3.3 + UP * 1.2),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 7. CFL CONDITION — THE SAME REQUIREMENT
        # ─────────────────────────────────────────────────────────────────────
        cfl_title = Text("The CFL Condition — Still Required",
                         font_size=22, weight=BOLD, color=WHITE)
        cfl_title.move_to(RIGHT * 3.3 + UP * 0.15)

        cfl_ineq = MathTex(
            r"\nu \;=\; \bigl|c(\rho)\bigr|\,\frac{\Delta t}{\Delta x} \;\leq\; 1",
            font_size=25, color=YELLOW,
        )
        cfl_ineq.next_to(cfl_title, DOWN, buff=0.28)

        cfl_note = VGroup(
            Text("A wider stencil doesn't relax this rule —", font_size=17, color="#cccccc"),
            Text("information still can't outrun the grid.", font_size=17, color="#cccccc"),
            Text("The same CFL limit governs both schemes.", font_size=17, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cfl_note.next_to(cfl_ineq, DOWN, buff=0.28)

        with self.voiceover(
            "Even though the Lax-Wendroff scheme "
            "is more sophisticated, "
            "it cannot violate "
            "the laws of information propagation. "
            "A traffic disturbance still cannot travel "
            "farther than one computational cell "
            "during a single time step. "
            "Therefore, the same CFL condition "
            "remains essential for stability."
        ):
            self.play(FadeIn(cfl_title), run_time=rt(0.5))
            self.play(Write(cfl_ineq),   run_time=rt(0.8))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in cfl_note],
                            lag_ratio=0.25),
                run_time=rt(0.8),
            )

        self.wait(rt(0.5))

        self.play(
            FadeOut(VGroup(
                grid_title, h_lines, v_lines, grid_dots,
                x_arrow, t_arrow, x_arrow_lbl, t_arrow_lbl,
                j_lbls, n_lbls, stencil_grp, final_grp,
                cfl_title, cfl_ineq, cfl_note,
            )),
            run_time=rt(0.9),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 8. THE COST — NUMERICAL DISPERSION
        # ─────────────────────────────────────────────────────────────────────
        cost_title = Text("The Cost of Extra Accuracy",
                          font_size=32, weight=BOLD, color=WHITE)
        cost_title.to_edge(UP).shift(DOWN * 0.60)

        cmp_ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.2, 1.3, 1],
            x_length=5.4,
            y_length=3.6,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.16, "tip_height": 0.20, "include_numbers": False,
            },
        )
        cmp_ax.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.55)

        def exact_shape(x):
            return 1.0 if x < 0 else 0.0

        def diffused_shape(x):
            return 0.5 * (1 - np.tanh(1.4 * x))

        def dispersive_shape(x):
            base = 0.5 * (1 - np.tanh(3.2 * x))
            ripple = 0.11 * np.exp(-1.1 * x**2) * np.sin(4.5 * x) if x > -1.4 else 0.0
            return base + ripple

        exact_curve = cmp_ax.plot(exact_shape, x_range=[-3, -0.02], color=GREY_B, stroke_width=2.5)
        exact_curve2 = cmp_ax.plot(exact_shape, x_range=[0.02, 3], color=GREY_B, stroke_width=2.5)
        upwind_curve = cmp_ax.plot(diffused_shape,   x_range=[-3, 3], color="#4a90e2", stroke_width=3)
        lw_curve      = cmp_ax.plot(dispersive_shape, x_range=[-3, 3], color="#ff8844", stroke_width=3)

        legend = VGroup(
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=GREY_B, stroke_width=2.5),
                   Text("exact shock", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color="#4a90e2", stroke_width=3),
                   Text("Upwind — smeared", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color="#ff8844", stroke_width=3),
                   Text("Lax-Wendroff — oscillates", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        legend.next_to(cmp_ax, DOWN, buff=0.25)

        cost_note = VGroup(
            Text("Near a sharp shock, the solution", font_size=20, color="#cccccc"),
            Text("overshoots, then undershoots,", font_size=20, color="#cccccc"),
            Text("before settling down —", font_size=20, color="#cccccc"),
            Text("numerical dispersion.", font_size=20, weight=BOLD, color="#ff8844"),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("These oscillations are not real traffic", font_size=18, color="#888888"),
            Text("behaviour — the numerical method creates them.", font_size=18, color="#888888"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        cost_note.move_to(RIGHT * 3.3 + UP * 0.35)

        # Block A: pose the trade-off
        with self.voiceover(
            "So the Lax-Wendroff scheme is more accurate. "
            "Does that mean it is simply better? "
            "Not quite. "
            "Every improvement in numerical methods "
            "tends to come with a trade-off, "
            "and this one is no exception."
        ):
            self.play(FadeIn(cost_title), run_time=rt(0.5))
            self.play(Create(cmp_ax),     run_time=rt(0.6))
            self.play(Create(exact_curve), Create(exact_curve2), run_time=rt(0.6))

        self.wait(rt(0.3))

        # Block B: the Upwind result — smeared
        with self.voiceover(
            "Consider how each scheme handles a sharp shock. "
            "The Upwind scheme smears the shock "
            "across several grid cells — "
            "the profile stays smooth, "
            "but the sharp edge is lost."
        ):
            self.play(Create(upwind_curve), run_time=rt(1.0))

        self.wait(rt(0.3))

        # Block C: the Lax-Wendroff result — slow down on the dispersion
        with self.voiceover(
            "Higher accuracy does not come for free. "
            "By reducing numerical diffusion, "
            "the Lax-Wendroff scheme "
            "introduces a different type of numerical error. "
            "Near sharp discontinuities, "
            "the solution begins to oscillate. "
            "Instead of smoothly approaching the exact shock, "
            "it overshoots... "
            "then undershoots... "
            "before settling back. "
            "These artificial oscillations "
            "are called numerical dispersion. "
            "They are not real traffic behaviour — "
            "they are created entirely "
            "by the numerical method itself."
        ):
            self.play(Create(lw_curve),     run_time=rt(1.0))
            self.play(FadeIn(legend, shift=UP * 0.1), run_time=rt(0.5))
            self.play(FadeIn(cost_note, shift=LEFT * 0.1), run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(cost_title, cmp_ax, exact_curve, exact_curve2,
                           upwind_curve, lw_curve, legend, cost_note)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 9. PROPERTIES OF THE LAX-WENDROFF SCHEME
        # ─────────────────────────────────────────────────────────────────────
        props_title = Text("Properties of the Lax-Wendroff Scheme",
                           font_size=32, weight=BOLD, color=WHITE)
        props_title.to_edge(UP).shift(DOWN * 0.62)

        formula_ref = MathTex(
            r"\rho_j^{n+1} = \rho_j^n"
            r"- \frac{\lambda}{2}\bigl(f_{j+1}^n - f_{j-1}^n\bigr)"
            r"+ \frac{\lambda^2 c_j^n}{2}"
            r"\bigl(f_{j+1}^n - 2f_j^n + f_{j-1}^n\bigr)",
            font_size=24, color=YELLOW,
        )
        formula_ref.next_to(props_title, DOWN, buff=0.38)

        def prop_row(label, body, lbl_color=WHITE):
            return VGroup(
                Text(label + ":", font_size=20, weight=BOLD, color=lbl_color),
                Text("  " + body, font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.10)

        prop_rows = VGroup(
            prop_row("Accuracy",    "second-order in space and time  [ O(Δx²) + O(Δt²) ]",
                     lbl_color="#aaaacc"),
            prop_row("Stability",   "guaranteed when the CFL number  ν ≤ 1",
                     lbl_color="#aaaacc"),
            prop_row("Dispersion",  "spurious oscillations near sharp gradients",
                     lbl_color="#aaaacc"),
            prop_row("Cost",        "five-point stencil, slightly more computation per step",
                     lbl_color="#aaaacc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        prop_rows.next_to(formula_ref, DOWN, buff=0.42)

        connect_note = VGroup(
            Text("This is the trade-off at the heart of this project:", font_size=19, color="#cccccc"),
            Text("Upwind smears shocks but stays well-behaved;", font_size=19, color="#cccccc"),
            Text("Lax-Wendroff sharpens them, at the cost of ringing.", font_size=19, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        connect_note.next_to(prop_rows, DOWN, buff=0.34)

        # Block A: properties, as a story
        with self.voiceover(
            "Let us summarise the Lax-Wendroff scheme. "
            "Because it retains one more term "
            "of the Taylor expansion, "
            "it is second-order accurate "
            "in both space and time. "
            "Halving the grid spacing "
            "now quarters the error, "
            "instead of merely halving it. "
            "It remains stable "
            "under the same CFL condition. "
            "But because it uses a symmetric, "
            "centred approximation, "
            "it introduces numerical dispersion — "
            "the oscillations we just observed near sharp fronts. "
            "And its five-point stencil "
            "requires slightly more computation "
            "at every step."
        ):
            self.play(FadeIn(props_title), run_time=rt(0.5))
            self.play(Write(formula_ref),  run_time=rt(0.9))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in prop_rows],
                            lag_ratio=0.28),
                run_time=rt(1.0),
            )

        self.wait(rt(0.3))

        # Block B: the central trade-off, stated plainly
        with self.voiceover(
            "We can now see that neither numerical method is perfect. "
            "The Upwind scheme sacrifices sharpness "
            "in exchange for stability. "
            "The Lax-Wendroff scheme "
            "preserves sharp features much better, "
            "but may introduce oscillations near discontinuities. "
            "Neither approach is universally superior. "
            "Each makes a different compromise "
            "between stability and accuracy. "
            "In the next scene, "
            "we place both schemes side by side "
            "on identical test problems, "
            "and see exactly how this trade-off plays out."
        ):
            self.play(FadeIn(connect_note, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(props_title, formula_ref, prop_rows, connect_note)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 10. PREVIEW — SCENE 15: COMPARISON
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Upwind vs Lax-Wendroff",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_desc  = Text(
            "Same test problems. Same grid. Two very different answers.",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.3)
        prev_desc.next_to(prev_title, DOWN, buff=0.40)

        with self.voiceover(
            "Up to this point, "
            "we have studied both numerical methods independently. "
            "We understand how each one is derived. "
            "We understand their strengths. "
            "We understand their weaknesses. "
            "But theory alone is not enough. "
            "The real question is: "
            "how do they perform on the same traffic problem? "
            "In the next scene, "
            "we will simulate identical traffic scenarios "
            "using both methods, "
            "compare their solutions "
            "with the exact analytical results, "
            "and discover which method performs better "
            "under different traffic conditions."
        ):
            self.play(Write(prev_title),                     run_time=rt(0.9))
            self.play(FadeIn(prev_desc, shift=UP * 0.1),     run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(prev_title, prev_desc)),   run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene14_LaxWendroff",
    ])
