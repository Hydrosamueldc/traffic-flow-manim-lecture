from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 16 — COMPARATIVE ANALYSIS, CONCLUSION & PROJECT CLOSING
#  Render: manim -pql scene16_conclusion.py Scene16_Conclusion
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene16_Conclusion(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT IV · Scene 16 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Comparative Analysis & Conclusion",
                     font_size=42, weight=BOLD, color=WHITE)
        sub   = Text("What have we actually learned?",
                     font_size=25, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "Throughout this project, "
            "we have developed two classical numerical methods "
            "for solving the LWR traffic flow model, "
            "and established a framework "
            "for evaluating their performance. "
            "We can now compare their theoretical properties, "
            "and reflect on what this study has achieved."
        ):
            self.play(Write(title),                     run_time=rt(1.3))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. COMPARISON TABLE
        # ─────────────────────────────────────────────────────────────────────
        table_title = Text("Upwind vs Lax-Wendroff",
                           font_size=30, weight=BOLD, color=WHITE)
        table_title.to_edge(UP).shift(DOWN * 0.60)

        header = VGroup(
            Text("Property", font_size=19, weight=BOLD, color="#888888"),
            Text("Upwind", font_size=19, weight=BOLD, color="#4a90e2"),
            Text("Lax-Wendroff", font_size=19, weight=BOLD, color="#ff8844"),
        )
        header[0].move_to(LEFT * 3.6)
        header[1].move_to(LEFT * 0.3)
        header[2].move_to(RIGHT * 3.0)
        header.next_to(table_title, DOWN, buff=0.42)

        divider = Line(LEFT * 5.6, RIGHT * 5.6, color=GREY_B, stroke_width=1)
        divider.next_to(header, DOWN, buff=0.18)

        def trow(label, u, lw):
            l = Text(label, font_size=17, color="#cccccc").move_to(LEFT * 3.6)
            a = Text(u,     font_size=17, color="#aac8ff").move_to(LEFT * 0.3)
            b = Text(lw,    font_size=17, color="#ffcaa8").move_to(RIGHT * 3.0)
            return VGroup(l, a, b)

        rows = VGroup(
            trow("Accuracy",           "first-order",         "second-order"),
            trow("Stability",          "CFL ≤ 1",              "CFL ≤ 1"),
            trow("Shock resolution",   "diffusive (smears)",   "sharper, may oscillate"),
            trow("Oscillations",       "none",                 "possible (dispersion)"),
            trow("Stencil",            "3 points, simple",     "5 points, moderate"),
            trow("Computational cost", "lower",                "moderately higher"),
        ).arrange(DOWN, buff=0.30)
        rows.next_to(divider, DOWN, buff=0.35)

        with self.voiceover(
            "Every property in this table "
            "traces back to a decision we made "
            "in Scenes Thirteen and Fourteen. "
            "The Upwind scheme is first-order accurate "
            "because it truncates the Taylor expansion early. "
            "The Lax-Wendroff scheme is second-order "
            "because it keeps one more term. "
            "Both share the same CFL stability limit, "
            "because both are still bound "
            "by the same characteristic speed. "
            "And the shock behaviour of each — "
            "diffusive versus oscillatory — "
            "is the direct, unavoidable consequence "
            "of that one choice about how many terms to keep."
        ):
            self.play(FadeIn(table_title), run_time=rt(0.5))
            self.play(FadeIn(header), Create(divider), run_time=rt(0.6))
            self.play(
                LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows],
                            lag_ratio=0.20),
                run_time=rt(1.1),
            )

        self.wait(rt(0.8))
        self.play(
            FadeOut(VGroup(table_title, header, divider, rows)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 3. KEY OBSERVATIONS
        # ─────────────────────────────────────────────────────────────────────
        obs_title = Text("Key Observations",
                         font_size=32, weight=BOLD, color=WHITE)
        obs_title.to_edge(UP).shift(DOWN * 0.62)

        up_head = Text("The Upwind Scheme", font_size=22, weight=BOLD, color="#4a90e2")
        up_body = VGroup(
            Text("Extremely stable and computationally efficient.", font_size=19, color="#cccccc"),
            Text("Its simplicity makes it attractive for many", font_size=19, color="#cccccc"),
            Text("engineering applications.", font_size=19, color="#cccccc"),
            Text("But numerical diffusion causes sharp traffic", font_size=19, color="#cccccc"),
            Text("fronts to become progressively smeared.", font_size=19, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        up_grp = VGroup(up_head, up_body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        lw_head = Text("The Lax-Wendroff Scheme", font_size=22, weight=BOLD, color="#ff8844")
        lw_body = VGroup(
            Text("Provides significantly higher accuracy and", font_size=19, color="#cccccc"),
            Text("preserves important traffic features more effectively.", font_size=19, color="#cccccc"),
            Text("The price paid for this improvement is the", font_size=19, color="#cccccc"),
            Text("appearance of small oscillations near strong", font_size=19, color="#cccccc"),
            Text("discontinuities.", font_size=19, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        lw_grp = VGroup(lw_head, lw_body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        obs = VGroup(up_grp, lw_grp).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        obs.next_to(obs_title, DOWN, buff=0.45)

        with self.voiceover(
            "The Upwind scheme proved extremely stable "
            "and computationally efficient throughout this project. "
            "Its simplicity makes it attractive "
            "for many engineering applications. "
            "However, numerical diffusion causes sharp traffic fronts "
            "to become progressively smeared. "
            "The Lax-Wendroff scheme, by contrast, "
            "provides significantly higher accuracy "
            "and preserves important traffic features more effectively. "
            "The price paid for that improvement "
            "is the appearance of small oscillations "
            "near strong discontinuities."
        ):
            self.play(FadeIn(obs_title), run_time=rt(0.5))
            self.play(FadeIn(up_grp, shift=RIGHT * 0.15), run_time=rt(0.8))
            self.play(FadeIn(lw_grp, shift=RIGHT * 0.15), run_time=rt(0.8))

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(obs_title, obs)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 4. WHICH ONE IS BETTER?
        # ─────────────────────────────────────────────────────────────────────
        which_title = Text("Which One Is Better?",
                           font_size=32, weight=BOLD, color=WHITE)
        which_title.to_edge(UP).shift(DOWN * 0.62)

        neither_note = Text(
            "Neither method is universally superior.\n"
            "Their suitability depends on the problem being solved.\n"
            "The choice should always be guided by the objectives\n"
            "of the simulation, rather than by accuracy alone.",
            font_size=21, color="#cccccc", line_spacing=1.4,
        )
        neither_note.next_to(which_title, DOWN, buff=0.50)

        need_stab = VGroup(
            Text("Need robustness and stability?", font_size=21, color="#aaaacc"),
            Arrow(LEFT * 0.4, RIGHT * 0.4, color="#4a90e2", stroke_width=3, buff=0),
            Text("Upwind", font_size=24, weight=BOLD, color="#4a90e2"),
        ).arrange(DOWN, buff=0.22)

        need_acc = VGroup(
            Text("Need sharper accuracy on smooth flow?", font_size=21, color="#aaaacc"),
            Arrow(LEFT * 0.4, RIGHT * 0.4, color="#ff8844", stroke_width=3, buff=0),
            Text("Lax-Wendroff", font_size=24, weight=BOLD, color="#ff8844"),
        ).arrange(DOWN, buff=0.22)

        choices = VGroup(need_stab, need_acc).arrange(RIGHT, buff=1.4)
        choices.next_to(neither_note, DOWN, buff=0.7)

        with self.voiceover(
            "So which scheme is better? "
            "Neither method is universally superior. "
            "Their suitability depends "
            "on the problem being solved. "
            "The choice of numerical method "
            "should always be guided "
            "by the objectives of the simulation, "
            "rather than by accuracy alone. "
            "If the priority is robustness and stability — "
            "especially when jams and shocks are expected — "
            "the Upwind scheme is the natural choice. "
            "If the priority is sharper accuracy "
            "on smoother, more gradual flow, "
            "and the extra computation is affordable, "
            "the Lax-Wendroff scheme performs better. "
            "That is exactly what numerical analysts say "
            "about this family of methods in general."
        ):
            self.play(FadeIn(which_title), run_time=rt(0.5))
            self.play(FadeIn(neither_note, shift=UP * 0.1), run_time=rt(0.7))
            self.play(FadeIn(need_stab, shift=UP * 0.1), run_time=rt(0.6))
            self.play(FadeIn(need_acc,  shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(which_title, neither_note, choices)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 5. THE CONTRIBUTION OF THIS PROJECT
        # ─────────────────────────────────────────────────────────────────────
        contrib_title = Text("The Contribution of This Project",
                             font_size=30, weight=BOLD, color=WHITE)
        contrib_title.to_edge(UP).shift(DOWN * 0.62)

        contrib_body = VGroup(
            Text("The objective of this study was to investigate", font_size=21, color="#cccccc"),
            Text("the numerical simulation of the LWR traffic flow model", font_size=21, color="#cccccc"),
            Text("using the Upwind and Lax-Wendroff finite difference schemes.", font_size=21, color="#cccccc"),
            Rectangle(width=0.01, height=0.10, stroke_opacity=0, fill_opacity=0),
            Text("Through analytical derivation, computational methodology,", font_size=21, color="#cccccc"),
            Text("and a framework for numerical evaluation, this project", font_size=21, color="#cccccc"),
            Text("investigated how both methods approximate traffic flow", font_size=21, color="#cccccc"),
            Text("and highlighted their respective strengths and limitations.", font_size=21, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        contrib_body.next_to(contrib_title, DOWN, buff=0.5)

        with self.voiceover(
            "The objective of this study "
            "was to investigate the numerical simulation "
            "of the LWR traffic flow model "
            "using the Upwind and Lax-Wendroff finite difference schemes. "
            "Through analytical derivation, "
            "computational methodology, "
            "and a framework for numerical evaluation, "
            "this project investigated "
            "how both methods approximate traffic flow, "
            "and highlighted their respective strengths and limitations."
        ):
            self.play(FadeIn(contrib_title), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in contrib_body],
                            lag_ratio=0.15),
                run_time=rt(1.0),
            )

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(contrib_title, contrib_body)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 6. FUTURE WORK
        # ─────────────────────────────────────────────────────────────────────
        future_title = Text("Future Work",
                            font_size=30, weight=BOLD, color=WHITE)
        future_title.to_edge(UP).shift(DOWN * 0.62)

        future_body = Text(
            "Future work may include extending the present\n"
            "implementation to more realistic traffic scenarios,\n"
            "such as multi-lane highway models, adaptive mesh\n"
            "refinement, higher-order numerical methods,\n"
            "and validation using real traffic measurements.",
            font_size=21, color="#cccccc", line_spacing=1.4,
        )
        future_body.next_to(future_title, DOWN, buff=0.55)

        with self.voiceover(
            "Future work may include extending "
            "the present implementation "
            "to more realistic traffic scenarios — "
            "such as multi-lane highway models, "
            "adaptive mesh refinement, "
            "higher-order numerical methods, "
            "and validation using real traffic measurements."
        ):
            self.play(FadeIn(future_title), run_time=rt(0.5))
            self.play(FadeIn(future_body, shift=UP * 0.1), run_time=rt(0.8))

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(future_title, future_body)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 7. A BROADER SIGNIFICANCE
        # ─────────────────────────────────────────────────────────────────────
        sig_title = Text("A Broader Significance",
                         font_size=30, weight=BOLD, color=WHITE)
        sig_title.to_edge(UP).shift(DOWN * 0.62)

        sig_body = VGroup(
            Text("The mathematics in this project reaches", font_size=21, color="#cccccc"),
            Text("far beyond highways.", font_size=21, color="#cccccc"),
            Rectangle(width=0.01, height=0.10, stroke_opacity=0, fill_opacity=0),
            Text("Hyperbolic conservation laws also govern:", font_size=21, weight=BOLD, color=YELLOW),
            Text("fluid dynamics  ·  gas dynamics  ·  environmental modelling", font_size=19, color="#aaaacc"),
            Rectangle(width=0.01, height=0.10, stroke_opacity=0, fill_opacity=0),
            Text("By studying numerical methods for the LWR model,", font_size=21, color="#cccccc"),
            Text("we are also learning techniques that apply to a much", font_size=21, color="#cccccc"),
            Text("broader class of real-world problems.", font_size=21, color="#cccccc"),
        ).arrange(DOWN, buff=0.18)
        sig_body.next_to(sig_title, DOWN, buff=0.5)

        with self.voiceover(
            "Beyond traffic engineering, "
            "the mathematical ideas explored in this project "
            "extend far beyond highways. "
            "Hyperbolic conservation laws arise "
            "in fluid dynamics, gas dynamics, "
            "environmental modelling, "
            "and many other areas of science and engineering. "
            "By studying numerical methods for the LWR model, "
            "we are also learning techniques "
            "that apply to a much broader class "
            "of real-world problems."
        ):
            self.play(FadeIn(sig_title), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in sig_body],
                            lag_ratio=0.15),
                run_time=rt(1.1),
            )

        self.wait(rt(0.7))
        self.play(FadeOut(VGroup(sig_title, sig_body)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 8. FINAL CLOSING — RETURN TO SCENE 1
        # ─────────────────────────────────────────────────────────────────────
        closing_text = VGroup(
            Text("We began this journey by asking a simple question.", font_size=23, color="#cccccc"),
            Text("Why can traffic jams appear without any visible cause?", font_size=23, weight=BOLD, color=WHITE),
            Rectangle(width=0.01, height=0.10, stroke_opacity=0, fill_opacity=0),
            Text("Along the way, we transformed that everyday observation", font_size=23, color="#cccccc"),
            Text("into mathematics. We derived the LWR traffic flow model.", font_size=23, color="#cccccc"),
            Text("We explored shock waves and rarefaction waves.", font_size=23, color="#cccccc"),
            Text("We developed numerical methods capable of simulating", font_size=23, color="#cccccc"),
            Text("complex traffic behaviour.", font_size=23, color="#cccccc"),
            Rectangle(width=0.01, height=0.10, stroke_opacity=0, fill_opacity=0),
            Text("What began as a simple question about traffic became", font_size=23, color="#cccccc"),
            Text("a journey through applied mathematics, numerical", font_size=23, color="#cccccc"),
            Text("analysis, and scientific computing.", font_size=23, color="#cccccc"),
        ).arrange(DOWN, buff=0.16)
        closing_text.scale(0.85)

        with self.voiceover(
            "We began this journey by asking a simple question. "
            "Why can traffic jams appear without any visible cause? "
            "Along the way, "
            "we transformed that everyday observation into mathematics. "
            "We derived the LWR traffic flow model. "
            "We explored shock waves and rarefaction waves. "
            "We developed numerical methods "
            "capable of simulating complex traffic behaviour. "
            "What began as a simple question about traffic "
            "became a journey through applied mathematics, "
            "numerical analysis, "
            "and scientific computing. "
            "Thank you for joining me on that journey."
        ):
            self.play(
                LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in closing_text],
                            lag_ratio=0.18),
                run_time=rt(2.0),
            )

        self.wait(rt(1.2))
        self.play(FadeOut(closing_text), run_time=rt(0.8))

        # ─────────────────────────────────────────────────────────────────────
        # 9. VISUAL MONTAGE — EVERY IDEA, ONE LAST TIME
        # ─────────────────────────────────────────────────────────────────────
        topics_col1 = ["Traffic", "Density", "Velocity", "Flow",
                       "Greenshields", "Fundamental Diagram",
                       "LWR Equation", "Characteristics"]
        topics_col2 = ["Shock Waves", "Rarefaction Waves", "Why Numerics?",
                       "Discretisation", "Upwind Scheme",
                       "Lax-Wendroff Scheme", "Simulation Framework", "Conclusion"]

        def build_chain(items):
            parts = []
            for i, t in enumerate(items):
                parts.append(Text(t, font_size=16, color="#8899cc"))
                if i < len(items) - 1:
                    parts.append(Text("↓", font_size=14, color="#445566"))
            return VGroup(*parts).arrange(DOWN, buff=0.10)

        montage_col1 = build_chain(topics_col1)
        montage_col2 = build_chain(topics_col2)
        montage = VGroup(montage_col1, montage_col2).arrange(RIGHT, buff=1.4)
        montage.center()

        collapse_lbl = Text(
            "Traffic Flow Simulation\nUsing Numerical Methods",
            font_size=34, weight=BOLD, color=YELLOW, line_spacing=1.3,
        )
        collapse_lbl.center()

        with self.voiceover(
            "Every idea in this project "
            "connects to the next — "
            "from a single traffic jam, "
            "to a complete framework "
            "for simulating traffic flow."
        ):
            self.play(
                LaggedStart(*[FadeIn(m) for m in montage],
                            lag_ratio=0.4),
                run_time=rt(1.3),
            )
            self.wait(rt(0.8))
            self.play(FadeOut(montage), run_time=rt(0.5))
            self.play(FadeIn(collapse_lbl, scale=0.9), run_time=rt(0.7))

        self.wait(rt(1.0))
        self.play(FadeOut(collapse_lbl), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 10. TITLE CARD — PROJECT & THANKS
        # ─────────────────────────────────────────────────────────────────────
        proj_title = Text(
            "Numerical Simulation of the LWR Traffic Flow Model",
            font_size=28, weight=BOLD, color=WHITE,
        )
        proj_sub = Text(
            "Using Upwind and Lax-Wendroff Finite Difference Schemes",
            font_size=22, color="#8899cc",
        )
        proj_sub.next_to(proj_title, DOWN, buff=0.28)

        author = Text("Adegboyega Samuel", font_size=24, weight=BOLD, color=YELLOW)
        matric = Text("Matric No: 210806134", font_size=19, color="#cccccc")
        dept   = Text("Department of Mathematics, University of Lagos", font_size=19, color="#cccccc")
        author_grp = VGroup(author, matric, dept).arrange(DOWN, buff=0.14)
        author_grp.next_to(proj_sub, DOWN, buff=0.55)

        supervisor = Text("Supervisor: Dr. J. S. Aroloye", font_size=19, color="#aaaacc")
        supervisor.next_to(author_grp, DOWN, buff=0.35)

        thanks = Text("Thank you.", font_size=34, weight=BOLD, color=WHITE)

        with self.voiceover(
            "This has been a numerical simulation "
            "of the LWR traffic flow model, "
            "using the Upwind and Lax-Wendroff finite difference schemes. "
            "Thank you for watching."
        ):
            self.play(Write(proj_title),                    run_time=rt(1.2))
            self.play(FadeIn(proj_sub, shift=UP * 0.1),      run_time=rt(0.6))
            self.play(FadeIn(author_grp, shift=UP * 0.1),    run_time=rt(0.7))
            self.play(FadeIn(supervisor, shift=UP * 0.1),    run_time=rt(0.5))

        self.wait(rt(1.0))
        self.play(
            FadeOut(VGroup(proj_title, proj_sub, author_grp, supervisor)),
            run_time=rt(0.7),
        )
        self.play(Write(thanks), run_time=rt(1.0))
        self.wait(rt(1.5))
        self.play(FadeOut(thanks), run_time=rt(0.8))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene16_Conclusion",
    ])
