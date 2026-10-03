from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 12 — THE FINITE DIFFERENCE GRID
#  Render: manim -pql scene12_grid_discretization.py Scene12_GridDiscretization
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene12_GridDiscretization(VoiceoverScene):

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

        progress_lbl = Text("ACT IV · Scene 12 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("The Finite Difference Grid",
                     font_size=46, weight=BOLD, color=WHITE)
        sub   = Text("Turning a continuous equation into something a computer can solve",
                     font_size=24, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "Throughout this project, "
            "we have treated traffic density "
            "as a continuous mathematical function. "
            "In theory, "
            "we can evaluate that function at any position, "
            "and at any instant in time. "
            "But computers don't work that way. "
            "A computer cannot store infinitely many numbers. "
            "It cannot evaluate a function at every possible location. "
            "So before we can solve the LWR equation numerically, "
            "we must answer one practical question: "
            "how can a computer represent a continuous traffic density "
            "using only a finite amount of information?"
        ):
            self.play(Write(title),                     run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. THE PROBLEM — A CONTINUOUS FUNCTION HAS INFINITELY MANY POINTS
        # ─────────────────────────────────────────────────────────────────────
        prob_title = Text("Too Much Information",
                          font_size=32, weight=BOLD, color=WHITE)
        prob_title.to_edge(UP).shift(DOWN * 0.62)

        curve_ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.2, 1],
            x_length=5.2,
            y_length=3.2,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.16, "tip_height": 0.20, "include_numbers": False,
            },
        )
        curve_ax.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.55)
        x_lbl = MathTex(r"x", font_size=22, color=GREY_B
                        ).next_to(curve_ax.x_axis.get_end(), RIGHT * 0.4)
        rho_lbl = MathTex(r"\rho", font_size=22, color=GREY_B
                          ).next_to(curve_ax.y_axis.get_end(), UP * 0.4)

        smooth_curve = curve_ax.plot(
            lambda x: 0.55 + 0.35 * np.sin(0.9 * x) - 0.05 * x,
            x_range=[0, 6], color="#4a90e2", stroke_width=3,
        )

        pde_note = VGroup(
            Text("The LWR equation is defined for", font_size=20, color="#cccccc"),
            Text("every real value of x and t.", font_size=20, color="#cccccc"),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("That is infinitely many points —", font_size=20, color=YELLOW),
            Text("far too many for any computer to store.", font_size=20, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        pde_note.move_to(RIGHT * 3.3 + UP * 0.35)

        with self.voiceover(
            "Consider this traffic density profile. "
            "Mathematically, "
            "the curve exists at every single point along the road. "
            "Between any two points, "
            "there are infinitely many more. "
            "That means the LWR equation is defined "
            "using infinitely many values of traffic density. "
            "While mathematics has no difficulty working with infinity, "
            "computers do. "
            "Every value stored in memory occupies space. "
            "Since a computer has only finite memory, "
            "it cannot store an infinite number of values."
        ):
            self.play(FadeIn(prob_title),                       run_time=rt(0.5))
            self.play(Create(curve_ax), FadeIn(x_lbl, rho_lbl), run_time=rt(0.7))
            self.play(Create(smooth_curve),                     run_time=rt(1.0))
            self.play(FadeIn(pde_note, shift=LEFT * 0.1),       run_time=rt(0.6))

        self.wait(rt(0.5))

        # ─────────────────────────────────────────────────────────────────────
        # 3. THE IDEA — SAMPLE AT FINITELY MANY POINTS
        # ─────────────────────────────────────────────────────────────────────
        # A dense swarm hints at the "infinitely many points" before collapsing
        # down to a handful of representative samples.
        swarm_xs = np.linspace(0.1, 5.9, 36)
        swarm_dots = VGroup(*[
            Dot(curve_ax.c2p(x, 0.55 + 0.35 * np.sin(0.9 * x) - 0.05 * x),
                radius=0.035, color=GREY_B, fill_opacity=0.7)
            for x in swarm_xs
        ])

        sample_xs = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        sample_dots = VGroup(*[
            Dot(curve_ax.c2p(x, 0.55 + 0.35 * np.sin(0.9 * x) - 0.05 * x),
                radius=0.08, color=YELLOW)
            for x in sample_xs
        ])

        idea_note = VGroup(
            Text("Equally spaced points,", font_size=20, color="#cccccc"),
            Text("separated by a fixed distance  Δx.", font_size=20, color=YELLOW),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("This process is called discretisation.", font_size=20, weight=BOLD, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        idea_note.move_to(RIGHT * 3.3 + UP * 0.35)

        with self.voiceover(
            "So what should we do? "
            "The solution is surprisingly simple. "
            "Instead of trying to remember every point on the curve, "
            "we keep only a carefully chosen collection of points. "
            "These points are equally spaced along the road, "
            "separated by a fixed distance, which we call delta x. "
            "At each of these locations, "
            "we store only one value: the traffic density. "
            "This process is called discretisation."
        ):
            self.play(FadeOut(pde_note),                        run_time=rt(0.3))
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.6) for d in swarm_dots], lag_ratio=0.015),
                run_time=rt(0.5),
            )
            self.play(
                FadeOut(swarm_dots),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in sample_dots], lag_ratio=0.15),
                run_time=rt(0.8),
            )
            self.play(FadeIn(idea_note, shift=LEFT * 0.1),      run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(prob_title, curve_ax, x_lbl, rho_lbl,
                           smooth_curve, sample_dots, idea_note)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4. BUILDING THE SPACE-TIME GRID
        # ─────────────────────────────────────────────────────────────────────
        grid_title = Text("The Space-Time Grid",
                          font_size=30, weight=BOLD, color=WHITE)
        grid_title.to_edge(UP).shift(DOWN * 0.55)

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

        space_note = VGroup(
            MathTex(r"x_j = j\,\Delta x", font_size=24, color=YELLOW),
            Text("  the  j-th  spatial grid point", font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.16)
        space_note.move_to(RIGHT * 3.3 + UP * 1.5)

        with self.voiceover(
            "Once we choose the spacing delta x, "
            "every location on the road receives an index. "
            "Rather than saying "
            "\"the point two hundred and thirty-seven metres from the start,\" "
            "we simply call it grid point j. "
            "The physical position is therefore written as "
            "x sub j equals j times delta x."
        ):
            self.play(FadeIn(grid_title),                       run_time=rt(0.5))
            self.play(Create(v_lines),                          run_time=rt(0.5))
            self.play(
                GrowArrow(x_arrow), FadeIn(x_arrow_lbl),
                run_time=rt(0.5),
            )
            self.play(FadeIn(j_lbls),                            run_time=rt(0.4))
            self.play(FadeIn(space_note, shift=LEFT * 0.1),      run_time=rt(0.6))

        self.wait(rt(0.4))

        time_note = VGroup(
            MathTex(r"t^n = n\,\Delta t", font_size=24, color=YELLOW),
            Text("  the  n-th  time level", font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.16)
        time_note.next_to(space_note, DOWN, buff=0.35)

        with self.voiceover(
            "We apply exactly the same idea to time. "
            "Instead of observing traffic continuously, "
            "we observe it only at specific instants, "
            "separated by a fixed time interval, delta t. "
            "Each observation receives its own index, n. "
            "The corresponding time is written as "
            "t superscript n equals n times delta t. "
            "Together, the spatial grid and the time grid "
            "form the finite difference grid."
        ):
            self.play(Create(h_lines),                           run_time=rt(0.5))
            self.play(
                GrowArrow(t_arrow), FadeIn(t_arrow_lbl),
                run_time=rt(0.5),
            )
            self.play(FadeIn(n_lbls),                            run_time=rt(0.4))
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.7) for d in grid_dots], lag_ratio=0.02),
                run_time=rt(0.7),
            )
            self.play(FadeIn(time_note, shift=LEFT * 0.1),       run_time=rt(0.6))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(space_note, time_note)), run_time=rt(0.5))

        # ─────────────────────────────────────────────────────────────────────
        # 5. THE GRID VALUE — WHAT WE ARE ACTUALLY COMPUTING
        # ─────────────────────────────────────────────────────────────────────
        value_note = VGroup(
            MathTex(r"\rho_j^n \;\approx\; \rho(x_j,\,t^n)",
                    font_size=28, color=YELLOW),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("our stored approximation to the true density,", font_size=20, color="#cccccc"),
            Text("at grid point  j,  at time level  n.", font_size=20, color="#cccccc"),
        ).arrange(DOWN, buff=0.18)
        value_note.move_to(RIGHT * 3.3 + UP * 0.5)

        highlight_pt = Dot(self.gp(3, 2), radius=0.15, color=YELLOW)
        highlight_ring = Circle(radius=0.22, color=YELLOW, stroke_width=2.5
                                ).move_to(self.gp(3, 2))

        with self.voiceover(
            "Every intersection of this grid "
            "contains exactly one number. "
            "That number is written as rho sub j superscript n. "
            "But what does this notation really mean? "
            "The subscript, j, "
            "tells us where we are on the road. "
            "The superscript, n, "
            "tells us when we are observing the traffic. "
            "Together, rho sub j superscript n "
            "represents our numerical approximation "
            "to the traffic density "
            "at position x sub j and time t superscript n. "
            "The entire numerical method boils down to one task: "
            "computing every one of these grid values."
        ):
            self.play(FadeIn(highlight_pt), Create(highlight_ring), run_time=rt(0.5))
            self.play(FadeIn(value_note, shift=LEFT * 0.1),         run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(value_note, highlight_pt, highlight_ring)), run_time=rt(0.5))

        # ─────────────────────────────────────────────────────────────────────
        # 6. THE INITIAL CONDITION — THE ONE ROW WE ALREADY KNOW
        # ─────────────────────────────────────────────────────────────────────
        bottom_row = VGroup(*[Dot(self.gp(j, 0), radius=0.10, color=GREEN)
                              for j in range(self.N_J)])
        bottom_lbl = MathTex(r"\rho_j^0 = \rho(x_j,\,0)", font_size=24, color=GREEN)
        bottom_lbl.move_to(RIGHT * 3.3 + UP * 1.4)

        ic_note = VGroup(
            Text("The bottom row  (n = 0)  is not computed —", font_size=19, color="#cccccc"),
            Text("it comes directly from the initial density.", font_size=19, color="#cccccc"),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Think of it as the starting photograph", font_size=19, weight=BOLD, color=YELLOW),
            Text("of the traffic.", font_size=19, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ic_note.next_to(bottom_lbl, DOWN, buff=0.32)

        with self.voiceover(
            "Notice that one row of the grid is already known. "
            "The bottom row, corresponding to time zero, "
            "comes directly from the initial traffic density. "
            "You can think of this row "
            "as the starting photograph of the traffic. "
            "Everything that happens afterwards "
            "must be computed from this initial snapshot."
        ):
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.6) for d in bottom_row], lag_ratio=0.10),
                run_time=rt(0.7),
            )
            self.play(FadeIn(bottom_lbl, shift=LEFT * 0.1),     run_time=rt(0.6))
            self.play(FadeIn(ic_note, shift=UP * 0.1),          run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(bottom_lbl, ic_note)), run_time=rt(0.5))

        # ─────────────────────────────────────────────────────────────────────
        # 7. MARCHING FORWARD IN TIME
        # ─────────────────────────────────────────────────────────────────────
        row1 = VGroup(*[Dot(self.gp(j, 1), radius=0.10, color=BLUE_B) for j in range(self.N_J)])
        row2 = VGroup(*[Dot(self.gp(j, 2), radius=0.10, color=BLUE_B) for j in range(self.N_J)])
        row3 = VGroup(*[Dot(self.gp(j, 3), radius=0.10, color=BLUE_B) for j in range(self.N_J)])

        march_arrow = Arrow(
            self.gp(self.N_J - 0.6, 0), self.gp(self.N_J - 0.6, self.N_N - 1),
            color=YELLOW, stroke_width=3, buff=0,
            max_tip_length_to_length_ratio=0.08,
        )

        march_note1 = VGroup(
            Text("A numerical scheme is a rule:", font_size=21, color="#cccccc"),
            MathTex(r"\{\rho_j^n\} \;\longrightarrow\; \{\rho_j^{n+1}\}", font_size=26, color=YELLOW),
        ).arrange(DOWN, buff=0.20)
        march_note1.move_to(RIGHT * 3.3 + UP * 0.95)

        march_note2 = VGroup(
            Text("Apply the rule once per row.", font_size=21, color="#cccccc"),
            Text("Marching forward, row by row,", font_size=21, color="#cccccc"),
            Text("fills in the entire grid.", font_size=21, weight=BOLD, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        march_note2.next_to(march_note1, DOWN, buff=0.32)

        part8_note = VGroup(
            Text("Although every method follows this", font_size=19, color="#cccccc"),
            Text("same strategy, each uses a different rule", font_size=19, color="#cccccc"),
            Text("for the next row — determining its", font_size=19, color="#cccccc"),
            Text("accuracy, stability, and efficiency.", font_size=19, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        part8_note.next_to(march_note2, DOWN, buff=0.34)

        # Block A: marching forward, told as a story
        with self.voiceover(
            "Imagine that we already know "
            "the traffic density at time level zero. "
            "The question is: "
            "how do we predict the traffic one instant later? "
            "A numerical method answers exactly that question. "
            "It takes one complete row of known values, "
            "and uses them to compute the next row. "
            "Once the new row has been calculated, "
            "the process repeats. "
            "Row after row, time step after time step, "
            "the solution gradually fills the entire grid."
        ):
            self.play(GrowArrow(march_arrow),                          run_time=rt(0.6))
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.6) for d in row1], lag_ratio=0.08),
                run_time=rt(0.5),
            )
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.6) for d in row2], lag_ratio=0.08),
                run_time=rt(0.5),
            )
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.6) for d in row3], lag_ratio=0.08),
                run_time=rt(0.5),
            )
            self.play(FadeIn(march_note1, shift=LEFT * 0.1),          run_time=rt(0.5))
            self.play(FadeIn(march_note2, shift=LEFT * 0.1),          run_time=rt(0.5))

        self.wait(rt(0.4))

        # Block B: important observation — different rules, different schemes
        with self.voiceover(
            "Although every numerical method "
            "follows this same overall strategy, "
            "they differ in one crucial detail. "
            "They use different rules to compute the next row. "
            "Choosing that update rule "
            "determines the accuracy, stability, "
            "and efficiency of the method."
        ):
            self.play(FadeIn(part8_note, shift=LEFT * 0.1),           run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(
                grid_title, h_lines, v_lines, grid_dots,
                x_arrow, t_arrow, x_arrow_lbl, t_arrow_lbl,
                j_lbls, n_lbls, bottom_row, row1, row2, row3,
                march_arrow, march_note1, march_note2, part8_note,
            )),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 8. PREVIEW — SCENE 13: THE UPWIND SCHEME
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: The Upwind Scheme",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_desc  = Text(
            "What is the actual rule that computes each new row?",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.3)
        prev_desc.next_to(prev_title, DOWN, buff=0.40)

        with self.voiceover(
            "We now have everything a computer needs. "
            "A finite grid. "
            "A known starting condition. "
            "And a framework for advancing through time. "
            "But one essential ingredient is still missing. "
            "How exactly do we calculate the next row? "
            "In the next scene, we'll derive our first numerical method, "
            "one that is guided directly "
            "by the direction in which information travels "
            "through the LWR equation. "
            "This method is known as the Upwind scheme."
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
        __file__, "Scene12_GridDiscretization",
    ])
