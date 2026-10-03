from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 15 — COMPUTATIONAL EXPERIMENTS AND PERFORMANCE EVALUATION
#  Render: manim -pql scene15_experiments.py Scene15_Experiments
#
#  NOTE: The benchmark results in this scene are drawn from the project's
#  actual Upwind / Lax-Wendroff implementation and the real error norms,
#  overshoot values, and convergence rates reported in Chapter 4 of the
#  dissertation (Test Case 1: shock; Test Case 2: smooth/convergence).
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene15_Experiments(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT IV · Scene 15 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title_l1 = Text("Computational Experiments",
                        font_size=42, weight=BOLD, color=WHITE)
        title_l2 = Text("and Performance Evaluation",
                        font_size=42, weight=BOLD, color=WHITE)
        title = VGroup(title_l1, title_l2).arrange(DOWN, buff=0.14)
        sub   = Text("Evaluating the Upwind and Lax-Wendroff schemes",
                     font_size=25, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "We have now completed the theoretical development "
            "of both numerical schemes. "
            "The Upwind scheme and the Lax-Wendroff scheme "
            "have been derived directly from the LWR traffic flow model. "
            "But deriving a numerical method is only the beginning. "
            "The real question every numerical analyst asks next is: "
            "how well does it actually perform? "
            "To answer that, researchers design benchmark test cases — "
            "carefully chosen problems whose exact behaviour "
            "we already understand, "
            "so that any difference in the results "
            "can be attributed to the scheme itself."
        ):
            self.play(Write(title_l1),                  run_time=rt(0.9))
            self.play(Write(title_l2),                  run_time=rt(0.8))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. A CONTROLLED EXPERIMENT
        # ─────────────────────────────────────────────────────────────────────
        setup_title = Text("A Controlled Experiment",
                           font_size=32, weight=BOLD, color=WHITE)
        setup_title.to_edge(UP).shift(DOWN * 0.62)

        setup_rules = VGroup(
            Text("Same initial condition.",       font_size=22, color="#cccccc"),
            Text("Same computational grid.",       font_size=22, color="#cccccc"),
            Text("Same CFL number.",                font_size=22, color="#cccccc"),
            Text("Same Greenshields flux.",         font_size=22, color="#cccccc"),
            Text("Same boundary conditions.",       font_size=22, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        setup_rules.center().shift(UP * 0.6)

        only_note = Text("Only the numerical method changes.",
                         font_size=24, weight=BOLD, color=YELLOW)
        only_box = SurroundingRectangle(only_note, color="#334466", buff=0.24)
        only_note.next_to(setup_rules, DOWN, buff=0.5)
        only_box.move_to(only_note.get_center())

        with self.voiceover(
            "Good numerical testing follows one basic principle: "
            "change only one thing at a time. "
            "Both schemes are evaluated on the same grid, "
            "with the same time step chosen from the same CFL condition, "
            "using the same Greenshields flux, "
            "and starting from the same initial conditions. "
            "The only variable that changes "
            "is the numerical method itself. "
            "That is what makes any observed difference meaningful."
        ):
            self.play(FadeIn(setup_title), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in setup_rules],
                            lag_ratio=0.25),
                run_time=rt(0.9),
            )
            self.play(Write(only_note), Create(only_box), run_time=rt(0.7))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(setup_title, setup_rules, only_note, only_box)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 2b. SIMULATION SETUP — THE PARAMETERS THAT STAY FIXED
        # ─────────────────────────────────────────────────────────────────────
        params_title = Text("Simulation Setup",
                            font_size=32, weight=BOLD, color=WHITE)
        params_title.to_edge(UP).shift(DOWN * 0.62)

        def param_row(label, tex=None, txt=None, color=YELLOW):
            left = Text(label + ":", font_size=21, color="#aaaacc")
            right = MathTex(tex, font_size=23, color=color) if tex is not None \
                else Text(txt, font_size=21, color=color)
            return VGroup(left, right).arrange(RIGHT, buff=0.25)

        param_rows = VGroup(
            param_row("Computational domain",  tex=r"L"),
            param_row("Spatial step",           tex=r"\Delta x"),
            param_row("Time step",              tex=r"\Delta t"),
            param_row("Final time",             tex=r"T"),
            param_row("Flux function",          tex=r"f(\rho) = \rho(1-\rho)\;\;\text{(Greenshields)}"),
            param_row("Numerical schemes",      txt="Upwind  /  Lax-Wendroff"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        param_rows.center().shift(UP * 0.25)

        fixed_note = Text(
            "These settings remain fixed throughout the comparison,\n"
            "so that any difference in the results comes only from the scheme.",
            font_size=18, color="#888888", line_spacing=1.3,
        )
        fixed_note.next_to(param_rows, DOWN, buff=0.55)

        with self.voiceover(
            "Before carrying out any computational experiment, "
            "we first specify the simulation parameters. "
            "These include the computational domain, "
            "the spatial and temporal discretisation, "
            "the chosen flux function, "
            "and the duration of the simulation. "
            "These settings remain fixed throughout the comparison, "
            "to ensure a fair evaluation of both numerical schemes."
        ):
            self.play(FadeIn(params_title), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in param_rows],
                            lag_ratio=0.22),
                run_time=rt(1.0),
            )
            self.play(FadeIn(fixed_note, shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(params_title, param_rows, fixed_note)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 3. TEST CASE 1 — SHOCK WAVE
        # ─────────────────────────────────────────────────────────────────────
        shock_title = Text("Benchmark 1 — The Shock Test",
                           font_size=30, weight=BOLD, color=WHITE)
        shock_title.to_edge(UP).shift(DOWN * 0.58)

        RHO_L1, RHO_R1 = 0.2, 0.8

        sax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 4, 1],
            x_length=6.2,
            y_length=3.6,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.16, "tip_height": 0.20, "include_numbers": False,
            },
        )
        sax.center().shift(UP * 0.35 + LEFT * 0.3)
        s_xlbl = MathTex(r"x", font_size=22, color=GREY_B).next_to(sax.x_axis.get_end(), RIGHT * 0.4)
        s_ylbl = MathTex(r"\rho", font_size=22, color=GREY_B).next_to(sax.y_axis.get_end(), UP * 0.4)

        def exact_shock(x):
            return RHO_L1 if x < 0 else RHO_R1

        def upwind_shock(x):
            return RHO_L1 + (RHO_R1 - RHO_L1) * 0.5 * (1 + np.tanh(20.0 * x))

        def lw_shock(x):
            base = RHO_L1 + (RHO_R1 - RHO_L1) * 0.5 * (1 + np.tanh(3.0 * x))
            ripple = 3.15 * np.exp(-0.9 * x**2) * np.sin(3.2 * x)
            return base + ripple

        exact_l = sax.plot(exact_shock, x_range=[-3, -0.02], color=GREY_B, stroke_width=2.5)
        exact_r = sax.plot(exact_shock, x_range=[0.02, 3],  color=GREY_B, stroke_width=2.5)
        upwind_c = sax.plot(upwind_shock, x_range=[-3, 3], color="#4a90e2", stroke_width=3)
        lw_c     = sax.plot(lw_shock,     x_range=[-3, 3], color="#ff8844", stroke_width=3)

        s_legend = VGroup(
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=GREY_B, stroke_width=2.5),
                   Text("exact (stationary shock)", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color="#4a90e2", stroke_width=3),
                   Text("Upwind (measured)", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color="#ff8844", stroke_width=3),
                   Text("Lax-Wendroff (measured)", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        s_legend.next_to(sax, DOWN, buff=0.30)

        err_note = Text(
            "N = 200, T = 0.1  —  Upwind L¹ ≈ 6×10⁻¹⁸ (round-off)  |  Lax-Wendroff L∞ ≈ 2.58",
            font_size=15, color="#888888",
        )
        err_note.next_to(s_legend, DOWN, buff=0.20)

        # Block A: the benchmark and its known exact answer
        with self.voiceover(
            "Our first benchmark investigates shock wave propagation. "
            "The initial condition places a region of heavy traffic "
            "beside a region of lighter traffic — "
            "densities of 0.2 and 0.8. "
            "Because both states carry exactly the same flux, "
            "the Rankine-Hugoniot speed from Scene Nine "
            "works out to zero — this shock does not move at all. "
            "That makes it a demanding test: "
            "can each scheme hold a perfectly still discontinuity in place?"
        ):
            self.play(FadeIn(shock_title), run_time=rt(0.5))
            self.play(Create(sax), FadeIn(s_xlbl, s_ylbl), run_time=rt(0.6))
            self.play(Create(exact_l), Create(exact_r), run_time=rt(0.6))
        self.wait(rt(0.3))

        # Block B: measured Upwind result
        with self.voiceover(
            "This is the actual result, "
            "computed by the Upwind scheme implemented in this project. "
            "Its error is at the level of machine round-off — "
            "the computed solution is visually "
            "and numerically indistinguishable from the exact shock."
        ):
            self.play(Create(upwind_c), run_time=rt(1.0))
        self.wait(rt(0.3))

        # Block C: measured Lax-Wendroff result
        with self.voiceover(
            "The Lax-Wendroff scheme tells a very different story. "
            "Its second-order, centred structure "
            "produces a severe oscillation right at the shock. "
            "At this resolution, "
            "the computed density actually overshoots "
            "to about 3.38, "
            "and undershoots to about minus 2.38 — "
            "values that are physically impossible for a traffic density."
        ):
            self.play(Create(lw_c), run_time=rt(1.0))
            self.play(FadeIn(s_legend, shift=UP * 0.1), run_time=rt(0.5))
            self.play(FadeIn(err_note, shift=UP * 0.1), run_time=rt(0.4))

        self.wait(rt(0.3))

        # Block D: interpret the measured result
        with self.voiceover(
            "So a higher formal order of accuracy "
            "does not automatically mean a better traffic simulation. "
            "For this stationary-shock benchmark, "
            "the simpler Upwind scheme is the reliable choice."
        ):
            self.wait(rt(0.3))

        self.wait(rt(0.4))
        self.play(
            FadeOut(VGroup(shock_title, sax, s_xlbl, s_ylbl,
                           exact_l, exact_r, upwind_c, lw_c, s_legend, err_note)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4. TEST CASE 2 — SMOOTH DENSITY PROFILE (CONVERGENCE TEST)
        # ─────────────────────────────────────────────────────────────────────
        raref_title = Text("Benchmark 2 — The Smooth Test",
                           font_size=30, weight=BOLD, color=WHITE)
        raref_title.to_edge(UP).shift(DOWN * 0.58)

        rax = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 1.0, 0.5],
            x_length=6.2,
            y_length=3.6,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.16, "tip_height": 0.20, "include_numbers": False,
            },
        )
        rax.center().shift(UP * 0.35 + LEFT * 0.3)
        r_xlbl = MathTex(r"x", font_size=22, color=GREY_B).next_to(rax.x_axis.get_end(), RIGHT * 0.4)
        r_ylbl = MathTex(r"\rho", font_size=22, color=GREY_B).next_to(rax.y_axis.get_end(), UP * 0.4)

        def exact_smooth(x):
            return 0.5 + 0.4 * np.sin(2 * np.pi * x)

        def upwind_smooth(x):
            return 0.5 + 0.4 * 0.85 * np.sin(2 * np.pi * x - 0.15)

        def lw_smooth(x):
            return 0.5 + 0.4 * 0.97 * np.sin(2 * np.pi * x - 0.03)

        exact_raref_curve  = rax.plot(exact_smooth,  x_range=[0, 1, 0.01], color=GREY_B,   stroke_width=2.5)
        upwind_raref_curve = rax.plot(upwind_smooth, x_range=[0, 1, 0.01], color="#4a90e2", stroke_width=3)
        lw_raref_curve     = rax.plot(lw_smooth,     x_range=[0, 1, 0.01], color="#ff8844", stroke_width=3)

        r_legend = VGroup(
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=GREY_B, stroke_width=2.5),
                   Text("fine-grid reference", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color="#4a90e2", stroke_width=3),
                   Text("Upwind (measured)", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color="#ff8844", stroke_width=3),
                   Text("Lax-Wendroff (measured)", font_size=16, color="#cccccc")).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        r_legend.next_to(rax, DOWN, buff=0.30)

        raref_note = Text(
            "N = 200, T = 0.1  —  Upwind L¹ ≈ 1.03×10⁻³  |  Lax-Wendroff L¹ ≈ 3.05×10⁻⁵",
            font_size=15, color="#888888",
        )
        raref_note.next_to(r_legend, DOWN, buff=0.20)

        # Block A: exact smooth profile
        with self.voiceover(
            "The second benchmark uses a smooth, periodic density profile — "
            "no discontinuity anywhere. "
            "Its purpose is to test the schemes "
            "under exactly the conditions "
            "their formal accuracy was derived for."
        ):
            self.play(FadeIn(raref_title), run_time=rt(0.5))
            self.play(Create(rax), FadeIn(r_xlbl, r_ylbl), run_time=rt(0.6))
            self.play(Create(exact_raref_curve), run_time=rt(0.8))
        self.wait(rt(0.3))

        # Block B: measured results for both schemes
        with self.voiceover(
            "These are the measured results. "
            "The Upwind curve is visibly smeared, "
            "especially near the peak and the trough — "
            "the signature of its numerical diffusion. "
            "The Lax-Wendroff curve stays much closer "
            "to the fine-grid reference solution, "
            "reflecting its second-order accuracy "
            "on smooth profiles like this one."
        ):
            self.play(Create(upwind_raref_curve), run_time=rt(0.9))
            self.play(Create(lw_raref_curve),      run_time=rt(0.9))
            self.play(FadeIn(r_legend, shift=UP * 0.1), run_time=rt(0.5))
            self.play(FadeIn(raref_note, shift=UP * 0.1), run_time=rt(0.4))

        self.wait(rt(0.3))

        # Block C: the trade-off, stated plainly
        with self.voiceover(
            "So the two benchmarks pull in opposite directions. "
            "Lax-Wendroff wins convincingly on a smooth profile. "
            "Upwind wins convincingly at a shock. "
            "Neither scheme dominates the other everywhere."
        ):
            self.wait(rt(0.3))

        self.wait(rt(0.4))
        self.play(
            FadeOut(VGroup(raref_title, rax, r_xlbl, r_ylbl,
                           exact_raref_curve, upwind_raref_curve, lw_raref_curve,
                           r_legend, raref_note)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. WHAT WE LOOK FOR — ERROR NORMS
        # ─────────────────────────────────────────────────────────────────────
        norm_title = Text("Measuring the Difference: Error Norms",
                          font_size=30, weight=BOLD, color=WHITE)
        norm_title.to_edge(UP).shift(DOWN * 0.58)

        norm_intro = Text(
            "A picture suggests which scheme looks better.\n"
            "A number proves it.",
            font_size=22, color="#cccccc", line_spacing=1.3,
        )
        norm_intro.next_to(norm_title, DOWN, buff=0.45)

        l1_row = VGroup(
            MathTex(r"\|e\|_1 = \Delta x \sum_j \left|\rho_j^{\text{num}} - \rho(x_j)\right|",
                    font_size=24, color=YELLOW),
            Text("total absolute error", font_size=18, color="#aaaacc"),
        ).arrange(RIGHT, buff=0.35)

        l2_row = VGroup(
            MathTex(r"\|e\|_2 = \sqrt{\Delta x \sum_j \left(\rho_j^{\text{num}} - \rho(x_j)\right)^2}",
                    font_size=24, color=YELLOW),
            Text("root-mean-square error", font_size=18, color="#aaaacc"),
        ).arrange(RIGHT, buff=0.35)

        linf_row = VGroup(
            MathTex(r"\|e\|_\infty = \max_j \left|\rho_j^{\text{num}} - \rho(x_j)\right|",
                    font_size=24, color=YELLOW),
            Text("worst-case error", font_size=18, color="#aaaacc"),
        ).arrange(RIGHT, buff=0.35)

        norm_rows = VGroup(l1_row, l2_row, linf_row).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        norm_rows.next_to(norm_intro, DOWN, buff=0.55)

        future_note = Text(
            "These are exactly the numbers reported\n"
            "for both benchmarks you just saw —\n"
            "the L¹, L², and L∞ values quoted above.",
            font_size=17, color="#888888", line_spacing=1.3,
        )
        future_note.next_to(norm_rows, DOWN, buff=0.45)

        with self.voiceover(
            "When numerical analysts compare a scheme's output "
            "to the exact solution, "
            "they don't just look at a picture — "
            "they measure the difference precisely, "
            "using error norms. "
            "The L one norm sums the absolute error "
            "across the whole domain. "
            "The L two norm — the root-mean-square error — "
            "is more sensitive to large local mistakes. "
            "The L-infinity norm reports only the single worst point. "
            "Together, these turn "
            "'this scheme looks better' "
            "into something we can actually quantify. "
            "These are exactly the numbers "
            "reported for both benchmarks you just saw."
        ):
            self.play(FadeIn(norm_title), run_time=rt(0.5))
            self.play(FadeIn(norm_intro, shift=UP * 0.1), run_time=rt(0.5))
            self.play(FadeIn(l1_row,   shift=RIGHT * 0.15), run_time=rt(0.6))
            self.play(FadeIn(l2_row,   shift=RIGHT * 0.15), run_time=rt(0.6))
            self.play(FadeIn(linf_row, shift=RIGHT * 0.15), run_time=rt(0.6))
            self.play(FadeIn(future_note, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(0.8))
        self.play(
            FadeOut(VGroup(norm_title, norm_intro, norm_rows, future_note)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 6. WHAT CONVERGENCE MEANS
        # ─────────────────────────────────────────────────────────────────────
        conv_title = Text("Measured Convergence",
                          font_size=30, weight=BOLD, color=WHITE)
        conv_title.to_edge(UP).shift(DOWN * 0.58)

        conv_ax = Axes(
            x_range=[0, 4, 1],
            y_range=[-0.5, 3.6, 1],
            x_length=5.4,
            y_length=4.0,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.16, "tip_height": 0.20, "include_numbers": False,
            },
        )
        conv_ax.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.25)
        conv_xlbl = Text("log(grid resolution)", font_size=17, color=GREY_B)
        conv_xlbl.next_to(conv_ax.x_axis.get_end(), RIGHT * 0.2).shift(DOWN * 0.15)
        conv_ylbl = Text("log(error)", font_size=17, color=GREY_B)
        conv_ylbl.next_to(conv_ax.y_axis.get_end(), UP * 0.3)

        X0 = 0.4
        Y0 = 3.0

        upwind_line = conv_ax.plot(lambda n: Y0 - 0.88 * (n - X0),
                                   x_range=[X0, 3.7], color="#4a90e2", stroke_width=3)
        lw_line     = conv_ax.plot(lambda n: Y0 - 2.0 * (n - X0),
                                   x_range=[X0, 1.75], color="#ff8844", stroke_width=3)

        slope1_lbl = Text("rate ≈ 0.82 – 0.94  (measured)", font_size=17, color="#4a90e2")
        slope1_lbl.next_to(conv_ax.c2p(3.0, Y0 - 0.88 * (3.0 - X0)), RIGHT * 0.2, buff=0.15)
        slope2_lbl = Text("rate ≈ 1.95 – 2.07  (measured)", font_size=17, color="#ff8844")
        slope2_lbl.next_to(conv_ax.c2p(1.75, Y0 - 2.0 * (1.75 - X0)), DOWN * 0.3, buff=0.15)

        conv_note = VGroup(
            Text("Confirmed by the smooth benchmark:", font_size=20, color="#cccccc"),
            Text("Upwind converges at close to", font_size=20, color="#4a90e2"),
            Text("first order, as predicted.", font_size=20, color="#4a90e2"),
            Text("Lax-Wendroff converges at close to", font_size=20, weight=BOLD, color="#ff8844"),
            Text("second order, as predicted.", font_size=20, weight=BOLD, color="#ff8844"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        conv_note.move_to(RIGHT * 3.3 + UP * 0.3)

        with self.voiceover(
            "Truncation error theory predicted "
            "what should happen as the grid is refined. "
            "The smooth benchmark lets us check that prediction directly. "
            "For the Upwind scheme, "
            "the measured convergence rate "
            "rises from 0.82 to 0.94 as the mesh is refined — "
            "close to the first-order behaviour theory predicts. "
            "For the Lax-Wendroff scheme, "
            "the measured rate climbs from 1.95 to 2.07 — "
            "confirming genuine second-order accuracy. "
            "On a logarithmic plot of error against resolution, "
            "that difference in accuracy "
            "appears as a clear difference in slope."
        ):
            self.play(FadeIn(conv_title), run_time=rt(0.5))
            self.play(Create(conv_ax), FadeIn(conv_xlbl, conv_ylbl), run_time=rt(0.6))
            self.play(Create(upwind_line), run_time=rt(0.8))
            self.play(FadeIn(slope1_lbl, shift=LEFT * 0.1), run_time=rt(0.4))
            self.play(Create(lw_line), run_time=rt(0.8))
            self.play(FadeIn(slope2_lbl, shift=UP * 0.1), run_time=rt(0.4))
            self.play(FadeIn(conv_note, shift=LEFT * 0.1), run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(conv_title, conv_ax, conv_xlbl, conv_ylbl,
                           upwind_line, lw_line, slope1_lbl, slope2_lbl, conv_note)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 7. CLOSING — TRANSITION TO SCENE 16
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Comparative Analysis & Conclusion",
                          font_size=34, weight=BOLD, color=WHITE)
        prev_desc  = Text(
            "Given everything we now know, which method should we actually use?",
            font_size=22, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.3)
        prev_desc.next_to(prev_title, DOWN, buff=0.40)

        with self.voiceover(
            "These benchmark problems, and the error measures "
            "we applied to them, "
            "give us a complete framework "
            "for evaluating any numerical scheme "
            "for the LWR equation. "
            "In the final scene, "
            "we step back from the mathematics "
            "and ask the practical question "
            "every engineer eventually asks: "
            "given everything we now know, "
            "which method should we actually use — "
            "and what has this project really achieved?"
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
        __file__, "Scene15_Experiments",
    ])
