from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 11 — WHY NUMERICAL METHODS?
#  Render: manim -pql scene11_why_numerics.py Scene11_WhyNumerics
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene11_WhyNumerics(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT III · Scene 11 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Why Numerical Methods?",
                     font_size=50, weight=BOLD, color=WHITE)
        sub   = Text("From analysis to computation",
                     font_size=26, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "We have now completed the analytical journey "
            "of the LWR traffic flow model. "
            "We began by describing traffic using density, velocity, and flow. "
            "We developed the Greenshields velocity model "
            "and the fundamental diagram. "
            "We derived the LWR equation "
            "from the conservation of vehicles. "
            "We solved simple problems using the method of characteristics. "
            "We discovered how shock waves form "
            "when characteristics intersect. "
            "And we saw how rarefaction waves emerge "
            "when characteristics spread apart. "
            "At this point, it may seem that our work is complete. "
            "After all, if we can solve the equation analytically, "
            "why do we need numerical methods at all?"
        ):
            self.play(Write(title),                     run_time=rt(1.3))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.7))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. WHEN ANALYSIS IS ENOUGH
        # ─────────────────────────────────────────────────────────────────────
        enough_title = Text("When Analysis Is Sufficient",
                            font_size=30, weight=BOLD, color=WHITE)
        enough_title.to_edge(UP).shift(DOWN * 0.62)

        success = VGroup(
            VGroup(
                Text("✓", font_size=24, color=GREEN),
                Text("  Single Riemann problem  — exact shock speed from R-H condition.",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
            VGroup(
                Text("✓", font_size=24, color=GREEN),
                Text("  Single rarefaction  — explicit fan solution.",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
            VGroup(
                Text("✓", font_size=24, color=GREEN),
                Text("  Piecewise constant initial data with two regions.",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        success.center().shift(UP * 0.5)

        success_note = Text(
            "For these cases, the method of characteristics gives exact closed-form answers.",
            font_size=20, color="#8899cc",
        )
        success_note.next_to(success, DOWN, buff=0.38)

        # Block A: analytical methods can be enough — the Riemann callback
        with self.voiceover(
            "For some carefully constructed problems, "
            "analytical methods work remarkably well. "
            "Consider the simple Riemann problem "
            "we studied in the previous scenes. "
            "With only two constant traffic states, "
            "we were able to determine exactly "
            "whether a shock wave or a rarefaction wave would form. "
            "We even calculated the exact shock speed "
            "using the Rankine-Hugoniot condition, "
            "and described the rarefaction fan explicitly. "
            "In situations like these, "
            "the method of characteristics provides an exact solution — "
            "no approximation required."
        ):
            self.play(FadeIn(enough_title),                    run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: the checklist, as evidence
        with self.voiceover(
            "These are exactly the situations "
            "where exact solutions exist."
        ):
            self.play(
                LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in success],
                            lag_ratio=0.30),
                run_time=rt(0.8),
            )
            self.play(FadeIn(success_note, shift=UP * 0.1),   run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(enough_title, success, success_note)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 3. WHERE ANALYSIS FAILS
        # ─────────────────────────────────────────────────────────────────────
        fail_title = Text("Where Analysis Breaks Down",
                          font_size=30, weight=BOLD, color=WHITE)
        fail_title.to_edge(UP).shift(DOWN * 0.62)

        failures = VGroup(
            VGroup(
                Text("✗", font_size=24, color=RED),
                Text("  Arbitrary initial density profile  ρ(x, 0).",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
            VGroup(
                Text("✗", font_size=24, color=RED),
                Text("  Multiple shocks forming simultaneously.",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
            VGroup(
                Text("✗", font_size=24, color=RED),
                Text("  Shocks interacting and merging over time.",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
            VGroup(
                Text("✗", font_size=24, color=RED),
                Text("  Rarefaction fans overlapping with shocks.",
                     font_size=21, color="#cccccc"),
            ).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        failures.center().shift(UP * 0.5)

        fail_note = Text(
            "The method of characteristics relies on tracking every\n"
            "characteristic individually — once many waves interact,\n"
            "obtaining exact solutions becomes impractical.",
            font_size=19, color="#cc7777", line_spacing=1.3,
        )
        fail_note.next_to(failures, DOWN, buff=0.38)

        # Block A: real traffic is more complicated — the vivid picture
        with self.voiceover(
            "Unfortunately, real traffic is rarely this simple. "
            "Imagine collecting traffic density data "
            "from sensors installed along an actual highway. "
            "The density would not consist of just two constant values. "
            "Instead, it would vary continuously "
            "from one location to another. "
            "Some regions might already be congested. "
            "Others might still be flowing freely. "
            "New disturbances could appear at any moment. "
            "Multiple shock waves could develop simultaneously. "
            "Rarefaction waves could interact with those shocks. "
            "The traffic pattern quickly becomes far too complicated "
            "for analytical methods to handle."
        ):
            self.play(FadeIn(fail_title),                      run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in failures],
                            lag_ratio=0.25),
                run_time=rt(0.9),
            )

        self.wait(rt(0.3))

        # Block B: why characteristics are no longer enough
        with self.voiceover(
            "The method of characteristics "
            "is an incredibly powerful analytical tool. "
            "But it relies on our ability "
            "to follow every characteristic individually. "
            "Once many waves begin interacting, "
            "those characteristic curves "
            "become extremely difficult to track. "
            "For realistic traffic scenarios "
            "involving arbitrary initial conditions and interacting waves, "
            "obtaining exact analytical solutions becomes impractical — "
            "making numerical methods the preferred approach."
        ):
            self.play(FadeIn(fail_note, shift=UP * 0.1),       run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(fail_title, failures, fail_note)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 4. THE CENTRAL OBJECTIVE — EARNED TRANSITION
        # ─────────────────────────────────────────────────────────────────────
        obj_title = Text("The Central Objective of This Project",
                         font_size=32, weight=BOLD, color=WHITE)
        obj_title.to_edge(UP).shift(DOWN * 0.62)

        earned_txt = VGroup(
            Text("Characteristics work — for simple problems.", font_size=22, color="#cccccc"),
            Text("But real traffic rarely remains simple.", font_size=22, color="#cccccc"),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Shocks form. Rarefactions develop.", font_size=22, color="#cccccc"),
            Text("Multiple waves interact.", font_size=22, color="#cccccc"),
            Text("Analytical solutions become impossible.", font_size=22, color=RED, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        earned_txt.center().shift(UP * 1.1)

        arrow = Arrow(UP * 0.0, DOWN * 0.55, color=YELLOW, stroke_width=3, buff=0)
        arrow.next_to(earned_txt, DOWN, buff=0.18)

        numerical_lbl = Text(
            "Numerical methods are essential.",
            font_size=28, weight=BOLD, color=YELLOW,
        )
        numerical_lbl.next_to(arrow, DOWN, buff=0.20)

        box = SurroundingRectangle(numerical_lbl, color="#334466", buff=0.28)

        obj_note = VGroup(
            Text("This project approximates the LWR solution", font_size=20, color="#cccccc"),
            Text("using finite difference methods:", font_size=20, color="#cccccc"),
            Text("the Upwind Scheme and the Lax-Wendroff Scheme.", font_size=20, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        obj_note.next_to(box, DOWN, buff=0.35)

        # Block A: the key realization
        with self.voiceover(
            "At this point, we face an important decision. "
            "We can either limit ourselves "
            "to a few simple problems with exact solutions, "
            "or we can develop methods "
            "capable of solving realistic traffic scenarios. "
            "This is precisely why numerical methods were developed. "
            "Rather than solving the LWR equation exactly, "
            "numerical methods compute an approximate solution "
            "on a finite computational grid. "
            "As that grid becomes finer, "
            "that approximation becomes increasingly accurate."
        ):
            self.play(FadeIn(obj_title),                        run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in earned_txt],
                            lag_ratio=0.18),
                run_time=rt(0.9),
            )
            self.play(GrowArrow(arrow),                         run_time=rt(0.5))
            self.play(Write(numerical_lbl), Create(box),        run_time=rt(0.8))

        self.wait(rt(0.4))

        # Block B: connect to this project's objective
        with self.voiceover(
            "This brings us to the central objective of this project. "
            "Our goal is not to derive another analytical solution. "
            "Instead, we will approximate the solution of the LWR equation "
            "using finite difference methods. "
            "Specifically, we will study two classical numerical schemes: "
            "the Upwind scheme and the Lax-Wendroff scheme. "
            "We will investigate how each method approximates traffic flow, "
            "how accurately it captures shock waves and rarefaction waves, "
            "and the advantages and limitations of each approach."
        ):
            self.play(FadeIn(obj_note, shift=UP * 0.1),         run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(obj_title, earned_txt, arrow, numerical_lbl, box, obj_note)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4b. KEY TAKEAWAYS
        # ─────────────────────────────────────────────────────────────────────
        kt_title = Text("Key Takeaways", font_size=34, weight=BOLD, color="#e8b84b")
        kt_title.to_edge(UP).shift(DOWN * 0.62)

        kt_bullets = VGroup(
            Text("• Exact solutions exist only for simple initial conditions.",
                 font_size=22, color=WHITE),
            Text("• For realistic, interacting waves, exact methods become impractical.",
                 font_size=22, color=WHITE),
            Text("• Numerical methods approximate the solution on a finite",
                 font_size=22, color=YELLOW),
            Text("  computational grid.", font_size=22, color=YELLOW),
            Text("• Two classical schemes: Upwind and Lax-Wendroff.",
                 font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        kt_bullets.next_to(kt_title, DOWN, buff=0.55)

        with self.voiceover(
            "Before moving on, let's recap. "
            "Exact solutions exist only for simple initial conditions. "
            "For realistic, interacting waves, "
            "exact analytical methods become impractical. "
            "Numerical methods approximate the solution "
            "on a finite computational grid. "
            "We will study two classical schemes: "
            "the Upwind scheme and the Lax-Wendroff scheme."
        ):
            self.play(FadeIn(kt_title), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in kt_bullets],
                            lag_ratio=0.30),
                run_time=rt(1.7),
            )
            self.wait(rt(1.5))

        self.wait(rt(0.4))
        self.play(FadeOut(VGroup(kt_title, kt_bullets)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 5. TWO SCHEMES — PREVIEW ACT IV
        # ─────────────────────────────────────────────────────────────────────
        act4_title = Text("Act IV — Numerical Methods",
                          font_size=32, weight=BOLD, color=WHITE)
        act4_title.to_edge(UP).shift(DOWN * 0.62)

        schemes = VGroup(
            VGroup(
                Text("Scene 12", font_size=18, color="#888888"),
                Text("Grid Discretisation", font_size=20, weight=BOLD, color=WHITE),
                Text("Replacing continuous space and time with a finite grid.",
                     font_size=17, color="#aaaacc"),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(
                Text("Scene 13", font_size=18, color="#888888"),
                Text("The Upwind Scheme", font_size=20, weight=BOLD, color=YELLOW),
                Text("First-order, stable, upstream-biased differences.",
                     font_size=17, color="#aaaacc"),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(
                Text("Scene 14", font_size=18, color="#888888"),
                Text("The Lax-Wendroff Scheme", font_size=20, weight=BOLD, color=YELLOW),
                Text("Second-order accuracy via a Taylor-expanded correction.",
                     font_size=17, color="#aaaacc"),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(
                Text("Scene 15", font_size=18, color="#888888"),
                Text("Comparison", font_size=20, weight=BOLD, color=WHITE),
                Text("Accuracy, diffusion, dispersion — side by side.",
                     font_size=17, color="#aaaacc"),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        schemes.center().shift(DOWN * 0.05)

        closing_lbl = Text(
            "The challenge is no longer to understand the equation —\n"
            "it is to solve it efficiently and accurately.",
            font_size=25, color=YELLOW, line_spacing=1.3,
        )
        closing_lbl.center()

        # Block A: roadmap opens — grid discretisation
        with self.voiceover(
            "The remainder of this presentation "
            "focuses on the computational solution of the LWR equation. "
            "We will begin by discretising the continuous road "
            "into a computational grid."
        ):
            self.play(FadeIn(act4_title),                       run_time=rt(0.5))
            self.play(FadeIn(schemes[0], shift=RIGHT * 0.2),    run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: why the Upwind scheme
        with self.voiceover(
            "Remember that information in the LWR model "
            "travels along characteristics. "
            "Those characteristics have a direction "
            "determined by the wave speed. "
            "A good numerical method should respect that direction — "
            "instead of using information "
            "from the wrong side of the traffic stream, "
            "it should follow the direction "
            "in which information actually propagates. "
            "This simple but powerful idea "
            "leads naturally to the Upwind scheme."
        ):
            self.play(FadeIn(schemes[1], shift=RIGHT * 0.2),    run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block C: why the Lax-Wendroff scheme
        with self.voiceover(
            "While the Upwind scheme is robust and stable, "
            "it also introduces numerical diffusion, "
            "causing sharp traffic features to become smeared. "
            "To improve accuracy, we consider a second method: "
            "the Lax-Wendroff scheme. "
            "By incorporating additional information "
            "from a Taylor series expansion, "
            "it achieves second-order accuracy "
            "and preserves sharper solution profiles. "
            "However, as we will see later, "
            "this improvement comes with its own trade-offs."
        ):
            self.play(FadeIn(schemes[2], shift=RIGHT * 0.2),    run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block D: comparison, closing the roadmap
        with self.voiceover(
            "Finally, we will compare both methods "
            "using identical traffic scenarios, "
            "and evaluate their accuracy, stability, "
            "and ability to reproduce the physical behaviour "
            "predicted by the analytical theory."
        ):
            self.play(FadeIn(schemes[3], shift=RIGHT * 0.2),    run_time=rt(0.5))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(act4_title, schemes)),         run_time=rt(0.7))

        # Block E: closing statement
        with self.voiceover(
            "Everything we have learned so far has been preparation. "
            "We now understand the mathematics governing traffic flow. "
            "The challenge is no longer to understand the equation. "
            "The challenge is to solve it efficiently and accurately "
            "for realistic traffic conditions. "
            "That journey begins with a simple idea: "
            "replacing the continuous road with a computational grid. "
            "In the next scene, we'll see how that transformation is made."
        ):
            self.play(FadeIn(closing_lbl),                      run_time=rt(0.8))

        self.wait(rt(1.2))
        self.play(FadeOut(closing_lbl),                         run_time=rt(0.7))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene11_WhyNumerics",
    ])
