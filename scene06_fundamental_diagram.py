from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 6 — THE FUNDAMENTAL DIAGRAM
#  Render: manim -pql scene06_fundamental_diagram.py Scene06_FundamentalDiagram
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene06_FundamentalDiagram(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT I · Scene 6 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE — CONNECT TO SCENE 5 AND EXPLAIN WHY THIS GRAPH MATTERS
        # ─────────────────────────────────────────────────────────────────────
        title = Text("The Fundamental Diagram", font_size=50, weight=BOLD, color=WHITE)
        sub   = Text("Traffic flux  f(ρ)  as a function of density",
                     font_size=26, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "In the previous scene, we combined the Greenshields velocity model "
            "with the traffic flow equation. "
            "The result was a new function that relates traffic flow "
            "directly to traffic density. "
            "But equations alone rarely reveal the full story. "
            "To truly understand how traffic behaves, "
            "we need to visualise this relationship. "
            "That visualisation is called the Fundamental Diagram. "
            "It is one of the most important graphs in traffic flow theory "
            "because it summarises how efficiently a road carries traffic "
            "under different conditions."
        ):
            self.play(Write(title),                 run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15), run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # AXES  (stay on screen through sections 2–6)
        # Normalised: x = ρ/ρ_j ∈ [0,1],  f_norm = 4x(1−x)
        # ─────────────────────────────────────────────────────────────────────
        ax = Axes(
            x_range=[0, 1.18, 0.5],
            y_range=[0, 1.18, 0.5],
            x_length=5.5,
            y_length=4.5,
            axis_config={
                "color":           GREY_B,
                "include_tip":     True,
                "tip_width":       0.18,
                "tip_height":      0.22,
                "include_numbers": False,
            },
        )
        ax.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.35)

        x_lbl = MathTex(r"\rho\;\text{(density)}", font_size=24
                        ).next_to(ax.x_axis.get_end(), RIGHT * 0.5)
        y_lbl = MathTex(r"f(\rho)\;\text{(flux)}", font_size=24
                        ).next_to(ax.y_axis.get_end(), UP * 0.6)

        rhoj_lbl = MathTex(r"\rho_j",   font_size=21, color="#aaaaaa"
                           ).next_to(ax.c2p(1.0, 0), DOWN * 0.9)
        rhoc_lbl = MathTex(r"\rho_c",   font_size=21, color=YELLOW
                           ).next_to(ax.c2p(0.5, 0), DOWN * 0.9)
        fmax_lbl = MathTex(r"f_{\max}", font_size=21, color=YELLOW
                           ).next_to(ax.c2p(0, 1.0), LEFT * 0.7)

        full_curve = ax.plot(lambda x: 4 * x * (1 - x), x_range=[0, 1.0],
                             color="#4a90e2", stroke_width=3)
        free_curve = ax.plot(lambda x: 4 * x * (1 - x), x_range=[0, 0.5],
                             color=GREEN, stroke_width=3)
        cong_curve = ax.plot(lambda x: 4 * x * (1 - x), x_range=[0.5, 1.0],
                             color=RED,   stroke_width=3)

        dot_origin = Dot(ax.c2p(0,   0),   color=WHITE,  radius=0.09)
        dot_peak   = Dot(ax.c2p(0.5, 1.0), color=YELLOW, radius=0.10)
        dot_end    = Dot(ax.c2p(1.0, 0),   color=WHITE,  radius=0.09)

        rho_v_dash = DashedLine(ax.c2p(0.5, 0),   ax.c2p(0.5, 1.0),
                                color=YELLOW, stroke_width=1.5, dash_length=0.15)
        f_h_dash   = DashedLine(ax.c2p(0,   1.0), ax.c2p(0.5, 1.0),
                                color=YELLOW, stroke_width=1.5, dash_length=0.15)

        plot_title = Text("Fundamental Diagram  (Greenshields)",
                          font_size=27, weight=BOLD, color=WHITE)
        plot_title.to_edge(UP).shift(DOWN * 0.52)

        # ─────────────────────────────────────────────────────────────────────
        # 2. PLOT THE PARABOLA — TEACH THE GRAPH, THEN EXPLAIN ENDPOINTS
        # ─────────────────────────────────────────────────────────────────────
        f_formula = MathTex(
            r"f(\rho)=v_f\,\rho\!\left(1-\tfrac{\rho}{\rho_j}\right)",
            font_size=26, color=YELLOW,
        )
        f_formula.move_to(RIGHT * 3.5 + UP * 2.1)

        # Block A: how to read the graph
        with self.voiceover(
            "Let us plot the traffic flow for every possible traffic density. "
            "Along the horizontal axis, we measure traffic density. "
            "Along the vertical axis, we measure traffic flow. "
            "As density changes from an empty road "
            "to a completely congested road, "
            "the graph traces out this smooth curve."
        ):
            self.play(FadeIn(plot_title),                run_time=rt(0.6))
            self.play(Create(ax), FadeIn(x_lbl, y_lbl),  run_time=rt(0.9))
            self.play(FadeIn(f_formula),                 run_time=rt(0.6))
            self.play(FadeIn(dot_origin, dot_end, rhoj_lbl), run_time=rt(0.5))
            self.play(Create(full_curve),                run_time=rt(1.3))

        self.wait(rt(0.4))

        # Block B: explain the endpoints slowly
        with self.voiceover(
            "Notice that the graph begins at zero. "
            "This makes perfect sense. "
            "If there are no vehicles on the road, "
            "then no vehicles can pass a given point. "
            "The traffic flow must therefore be zero. "
            "Now look at the opposite end. "
            "The road is completely full. "
            "Every available space is occupied. "
            "Although there are many vehicles, they cannot move. "
            "Since the velocity is zero, the traffic flow once again becomes zero. "
            "These two extreme situations are very different physically, "
            "yet they produce exactly the same traffic flow."
        ):
            self.play(Indicate(dot_origin, scale_factor=1.8, color=WHITE),
                      run_time=rt(0.8))
            self.wait(rt(0.5))
            self.play(Indicate(dot_end, scale_factor=1.8, color=WHITE),
                      run_time=rt(0.8))

        self.wait(rt(0.4))

        # ─────────────────────────────────────────────────────────────────────
        # 3. CRITICAL DENSITY — QUESTION → CALCULUS → PHYSICAL MEANING
        # ─────────────────────────────────────────────────────────────────────
        deriv_steps = VGroup(
            MathTex(
                r"\frac{df}{d\rho}"
                r"= v_f\!\left(1 - \frac{2\rho}{\rho_j}\right) = 0",
                font_size=24,
            ),
            MathTex(r"\Rightarrow\;\rho_c = \frac{\rho_j}{2}",
                    font_size=26, color=YELLOW),
            MathTex(r"\Rightarrow\;f_{\max} = \frac{v_f\,\rho_j}{4}",
                    font_size=26, color=YELLOW),
        ).arrange(DOWN, buff=0.40, aligned_edge=LEFT)
        deriv_steps.move_to(RIGHT * 3.5 + DOWN * 0.3)

        # Block A: the big question
        with self.voiceover(
            "If traffic flow is zero at both extremes, "
            "then somewhere between them, "
            "there must be a point where the road carries "
            "the largest possible number of vehicles. "
            "The question is: where is that point?"
        ):
            self.play(FadeOut(f_formula), run_time=rt(0.4))
            self.play(
                Create(rho_v_dash), Create(f_h_dash),
                FadeIn(dot_peak, rhoc_lbl, fmax_lbl),
                run_time=rt(0.9),
            )

        self.wait(rt(0.4))

        # Block B: calculus → ρc
        with self.voiceover(
            "To locate the highest point on the curve, "
            "we use a familiar idea from calculus. "
            "At a maximum, the slope of the curve must be zero. "
            "Therefore, we differentiate the traffic flow function "
            "with respect to density and set the derivative equal to zero. "
            "The result is the critical density — "
            "exactly half of the jam density."
        ):
            for step in deriv_steps:
                self.play(FadeIn(step, shift=LEFT * 0.2), run_time=rt(0.8))
                self.wait(rt(0.18))

        self.wait(rt(0.4))
        self.play(FadeOut(deriv_steps), run_time=rt(0.5))

        # Block C: physical meaning — this section was missing
        with self.voiceover(
            "Notice something remarkable. "
            "The road reaches its maximum performance "
            "before it becomes crowded. "
            "Waiting until the road is almost full is already too late. "
            "Maximum efficiency occurs somewhere in the middle — "
            "where there are enough vehicles to maintain a high flow, "
            "but still enough space for them to move freely."
        ):
            self.play(Indicate(dot_peak, scale_factor=2.0, color=YELLOW),
                      run_time=rt(0.9))
            self.wait(rt(1.5))

        # ─────────────────────────────────────────────────────────────────────
        # 4. WAVE SPEED — BUILD TOWARD c(ρ) = f'(ρ)
        # ─────────────────────────────────────────────────────────────────────
        wave_title = Text("The Slope = The Wave Speed",
                          font_size=26, weight=BOLD, color=WHITE)
        wave_title.move_to(RIGHT * 3.5 + UP * 2.05)

        wave_def = MathTex(
            r"c(\rho) = f'(\rho) = v_f\!\left(1 - \tfrac{2\rho}{\rho_j}\right)",
            font_size=21, color=YELLOW,
        )
        wave_def.next_to(wave_title, DOWN, buff=0.25)

        wave_rows = VGroup(
            VGroup(
                MathTex(r"\rho < \rho_c\!:", font_size=21, color=GREEN),
                MathTex(r"c > 0",            font_size=21, color=GREEN),
                Text("  waves travel forward", font_size=17, color="#cccccc"),
            ).arrange(RIGHT, buff=0.14),
            VGroup(
                MathTex(r"\rho = \rho_c\!:", font_size=21, color=YELLOW),
                MathTex(r"c = 0",            font_size=21, color=YELLOW),
                Text("  waves stationary",    font_size=17, color="#cccccc"),
            ).arrange(RIGHT, buff=0.14),
            VGroup(
                MathTex(r"\rho > \rho_c\!:", font_size=21, color=RED),
                MathTex(r"c < 0",            font_size=21, color=RED),
                Text("  waves travel BACKWARD", font_size=17, color=RED),
            ).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        wave_rows.next_to(wave_def, DOWN, buff=0.28)

        phantom_note = Text(
            "Cars move forward.   Information moves backward.",
            font_size=17, color="#ff8888", weight=BOLD,
        )
        phantom_note.next_to(wave_rows, DOWN, buff=0.24)

        # Block A: "more than a capacity chart" + disturbances
        with self.voiceover(
            "So far, we have treated this curve as a description of traffic flow. "
            "Surprisingly, it contains much more information than that. "
            "Remember the small disturbances we observed in traffic? "
            "A driver brakes. "
            "Another driver accelerates. "
            "Those disturbances travel through the traffic stream like waves."
        ):
            self.play(FadeIn(wave_title), run_time=rt(0.6))

        # Block B: wave speed formula — explain before giving it
        with self.voiceover(
            "The derivative of the traffic flow function "
            "tells us how quickly these disturbances move through traffic. "
            "This quantity is called the characteristic speed, "
            "or wave speed. "
            "Unlike vehicle speed, "
            "wave speed describes how changes in traffic "
            "propagate from one driver to another."
        ):
            self.play(Write(wave_def), run_time=rt(0.9))

        self.wait(rt(0.3))

        # Block C: free flow region — told as a story
        with self.voiceover(
            "On the left side of the graph, "
            "traffic density is relatively low. "
            "Vehicles move freely, "
            "and small disturbances travel in the same direction as the traffic. "
            "The wave speed is therefore positive."
        ):
            self.play(FadeIn(wave_rows[0], shift=RIGHT * 0.15), run_time=rt(0.6))

        self.wait(rt(0.25))

        # Block D: critical density
        with self.voiceover(
            "At the peak, "
            "the slope becomes zero. "
            "Disturbances no longer move forward or backward. "
            "They remain approximately stationary."
        ):
            self.play(FadeIn(wave_rows[1], shift=RIGHT * 0.15), run_time=rt(0.6))

        self.wait(rt(0.25))

        # Block E: congested region — the key insight
        with self.voiceover(
            "On the right side, "
            "the situation changes dramatically. "
            "Traffic has become heavily congested. "
            "The slope is now negative. "
            "This means disturbances travel backward, "
            "even though every vehicle continues moving forward."
        ):
            self.play(FadeIn(wave_rows[2], shift=RIGHT * 0.15), run_time=rt(0.6))

        self.wait(rt(0.4))

        # Block F: the beautiful sentence, then reconnect to Scene 1
        with self.voiceover(
            "Cars move forward. "
            "But information moves backward. "
            "This explains the mysterious traffic jam from Scene One. "
            "A driver brakes. "
            "The driver behind reacts. "
            "Then the next driver reacts. "
            "And the next. "
            "The disturbance travels backward through the traffic stream, "
            "even though every vehicle is moving forward. "
            "This is what we call a phantom traffic jam — "
            "and the entire explanation is contained within the sign "
            "of this derivative."
        ):
            self.play(FadeIn(phantom_note, shift=UP * 0.1), run_time=rt(0.6))
            self.wait(rt(2.5))

        self.wait(rt(0.4))
        self.play(
            FadeOut(VGroup(wave_title, wave_def, wave_rows, phantom_note)),
            run_time=rt(0.6),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. THREE TRAFFIC REGIMES — COLOUR-CODED VISUAL SUMMARY
        # ─────────────────────────────────────────────────────────────────────
        free_lbl = Text("Free Flow",  font_size=19, weight=BOLD, color=GREEN)
        crit_lbl = Text("Capacity",   font_size=17, weight=BOLD, color=YELLOW)
        cong_lbl = Text("Congested",  font_size=19, weight=BOLD, color=RED)
        free_lbl.move_to(ax.c2p(0.22, 0.60))
        cong_lbl.move_to(ax.c2p(0.78, 0.60))
        crit_lbl.next_to(dot_peak, UP, buff=0.13)

        regime_rows = VGroup(
            VGroup(Dot(radius=0.07, color=GREEN),
                   Text("  Free flow:   ρ < ρ_c  — fast, sparse, forward wave",
                        font_size=18, color="#cccccc")).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.07, color=YELLOW),
                   Text("  Capacity:    ρ = ρ_c  — peak throughput",
                        font_size=18, color="#cccccc")).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.07, color=RED),
                   Text("  Congested:  ρ > ρ_c  — slow, dense, backward wave",
                        font_size=18, color="#cccccc")).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        regime_rows.move_to(RIGHT * 3.5 + DOWN * 0.05)

        with self.voiceover(
            "We can now colour-code the fundamental diagram. "
            "The green region represents free flow — "
            "low density, high speed, forward-propagating waves. "
            "The red region represents congested traffic — "
            "high density, low speed, backward-propagating waves. "
            "The peak marks the critical density — "
            "the boundary between these two regimes, "
            "and the point of maximum road efficiency."
        ):
            self.play(
                FadeOut(full_curve),
                FadeIn(free_curve),
                FadeIn(cong_curve),
                run_time=rt(0.7),
            )
            self.play(
                FadeIn(free_lbl), FadeIn(crit_lbl), FadeIn(cong_lbl),
                run_time=rt(0.7),
            )
            self.play(
                LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in regime_rows],
                            lag_ratio=0.30),
                run_time=rt(1.0),
            )

        # ─────────────────────────────────────────────────────────────────────
        # 6. ROAD CAPACITY — WHY ENGINEERS AIM LEFT OF ρ_c
        # ─────────────────────────────────────────────────────────────────────
        with self.voiceover(
            "Engineers try to operate traffic to the left of the critical density. "
            "In this region, adding more vehicles still increases the traffic flow. "
            "But once the density exceeds the critical value, "
            "every additional vehicle actually reduces the road's efficiency. "
            "More traffic no longer means more flow. "
            "Instead, congestion begins to dominate. "
            "An incident, a merge, a sudden influx — "
            "anything that pushes density past the critical value "
            "tips the system onto the congested branch, "
            "and phantom jams begin to form."
        ):
            self.play(
                Indicate(dot_peak, scale_factor=2.2, color=YELLOW),
                Indicate(fmax_lbl, scale_factor=1.4, color=YELLOW),
                run_time=rt(1.0),
            )
            self.wait(rt(1.8))

        self.wait(rt(0.4))
        self.play(
            FadeOut(VGroup(
                plot_title, ax, x_lbl, y_lbl,
                free_curve, cong_curve,
                dot_origin, dot_peak, dot_end,
                rho_v_dash, f_h_dash,
                rhoj_lbl, rhoc_lbl, fmax_lbl,
                free_lbl, crit_lbl, cong_lbl,
                regime_rows,
            )),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 7. CLOSING — COMPLETE SUMMARY + CONSERVATION OF VEHICLES
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Conservation of Vehicles",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_eq    = MathTex(
            r"\frac{\partial \rho}{\partial t}"
            r"+ \frac{\partial f(\rho)}{\partial x} = 0",
            font_size=58, color=YELLOW,
        )
        prev_desc  = Text(
            "The LWR PDE — derived from first principles",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.6)
        prev_eq.next_to(prev_title, DOWN, buff=0.45)
        prev_desc.next_to(prev_eq,  DOWN, buff=0.38)

        with self.voiceover(
            "We have now completed the mathematical description of traffic flow. "
            "We understand density. "
            "We understand velocity. "
            "We understand traffic flow. "
            "We have chosen the Greenshields velocity model. "
            "And we have obtained the traffic flux function. "
            "The only remaining question is: "
            "how does traffic density change with time? "
            "To answer that, "
            "we must derive the governing equation of the LWR model "
            "using one of the most fundamental principles in physics: "
            "the conservation of vehicles."
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
        __file__, "Scene06_FundamentalDiagram",
    ])
