from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 10 — RAREFACTION WAVES
#  Render: manim -pql scene10_rarefaction.py Scene10_Rarefaction
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


# Normalised Greenshields: f(ρ) = ρ(1 − ρ),  c(ρ) = 1 − 2ρ
def f(rho):
    return rho * (1 - rho)


def c_speed(rho):
    return 1 - 2 * rho


class Scene10_Rarefaction(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT II · Scene 10 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Rarefaction Waves", font_size=52, weight=BOLD, color=WHITE)
        sub   = Text("When characteristics diverge and density smoothly transitions",
                     font_size=24, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "In the previous scene, we studied what happens "
            "when characteristics move toward one another. "
            "They intersect. "
            "The classical solution breaks down. "
            "A shock wave forms. "
            "But traffic does not always become more congested. "
            "Sometimes, the opposite happens. "
            "Instead of moving toward one another, "
            "characteristics move apart. "
            "Instead of compression, traffic experiences expansion. "
            "This produces a completely different type of wave "
            "known as a rarefaction wave. "
            "In this scene, we'll discover how rarefaction waves form, "
            "how they differ from shock waves, "
            "and why they represent smooth traffic recovery "
            "rather than sudden congestion."
        ):
            self.play(Write(title),                     run_time=rt(1.3))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. DIVERGING CHARACTERISTICS
        # ─────────────────────────────────────────────────────────────────────
        sec_title = Text("Diverging Characteristics",
                         font_size=32, weight=BOLD, color=WHITE)
        sec_title.to_edge(UP).shift(DOWN * 0.62)

        # Space-time axes
        T_MAX = 3.0
        st_ax = Axes(
            x_range=[-3.2, 3.5, 1],
            y_range=[0,    3.2, 1],
            x_length=5.5,
            y_length=4.3,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.18, "tip_height": 0.22, "include_numbers": False,
            },
        )
        st_ax.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.25)
        x_lbl = Text("x", font_size=20, color=GREY_B
                     ).next_to(st_ax.x_axis.get_end(), RIGHT * 0.4)
        t_lbl = Text("t", font_size=20, color=GREY_B
                     ).next_to(st_ax.y_axis.get_end(), UP * 0.4)

        # ρ_L = 0.7 (congested, c < 0), ρ_R = 0.2 (free-flow, c > 0)
        # Characteristics on the left lean LEFT (diverge away from x=0)
        # Characteristics on the right lean RIGHT (diverge away from x=0)
        RHO_L = 0.7;  C_L = c_speed(RHO_L)   # -0.4
        RHO_R = 0.2;  C_R = c_speed(RHO_R)   #  0.6

        left_chars = VGroup(*[
            Line(st_ax.c2p(x0, 0), st_ax.c2p(x0 + C_L * T_MAX, T_MAX),
                 color=RED, stroke_width=2.0, stroke_opacity=0.80)
            for x0 in [-3, -2, -1]
        ])
        right_chars = VGroup(*[
            Line(st_ax.c2p(x0, 0), st_ax.c2p(x0 + C_R * T_MAX, T_MAX),
                 color=GREEN, stroke_width=2.0, stroke_opacity=0.80)
            for x0 in [1, 2, 3]
        ])

        # The fan: characteristics from x=0 with c in [C_L, C_R]
        N_FAN = 7
        fan_chars = VGroup(*[
            Line(
                st_ax.c2p(0, 0),
                st_ax.c2p(c_val * T_MAX, T_MAX),
                color=interpolate_color(RED, GREEN, k / (N_FAN - 1)),
                stroke_width=2.0, stroke_opacity=0.75,
            )
            for k, c_val in enumerate(np.linspace(C_L, C_R, N_FAN))
        ])

        fan_lbl = Text("expansion fan", font_size=18, weight=BOLD, color="#ffdd88")
        fan_lbl.next_to(st_ax.c2p(0, 3.0), UP * 0.4)

        # Gap annotation (the empty region before the fan fills it)
        gap_lbl = Text("gap — no characteristics\nfrom initial data",
                       font_size=16, color=GREY_B, line_spacing=1.2)
        gap_lbl.move_to(st_ax.c2p(0.0, 1.5) + RIGHT * 0.15)

        explain1 = VGroup(
            Text("Left  (high density):", font_size=19, weight=BOLD, color=RED),
            Text("   c < 0  →  lean left  (diverge)", font_size=19, color=RED),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Right  (low density):", font_size=19, weight=BOLD, color=GREEN),
            Text("   c > 0  →  lean right (diverge)", font_size=19, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        explain1.move_to(RIGHT * 3.3 + UP * 0.95)

        explain2 = VGroup(
            Text("A gap opens — filled by the fan:", font_size=19, color=YELLOW),
            Text("density varies continuously from", font_size=19, color=YELLOW),
            Text("ρ_L to ρ_R across the fan.", font_size=19, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        explain2.next_to(explain1, DOWN, buff=0.32)

        phys_note = VGroup(
            Text("Unlike a shock, this is a gradual transition.", font_size=19, color="#aaaacc"),
            Text("Drivers accelerate smoothly as space opens up.", font_size=19, color="#aaaacc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        phys_note.next_to(explain2, DOWN, buff=0.34)

        # Block A: reverse the states — characteristics diverge
        with self.voiceover(
            "Let us begin by reversing the situation "
            "from the previous scene. "
            "This time, the left side of the road "
            "contains high-density traffic. "
            "The right side contains low-density traffic. "
            "Because wave speed depends on density, "
            "the characteristics now move away from each other "
            "instead of toward each other. "
            "As time passes, they spread apart. "
            "Unlike the shock wave case, "
            "the characteristics never collide."
        ):
            self.play(FadeIn(sec_title),                       run_time=rt(0.5))
            self.play(Create(st_ax), FadeIn(x_lbl, t_lbl),    run_time=rt(0.7))
            self.play(
                LaggedStart(*[Create(l) for l in left_chars],  lag_ratio=0.18),
                LaggedStart(*[Create(l) for l in right_chars], lag_ratio=0.18),
                run_time=rt(0.8),
            )
            self.play(FadeIn(explain1, shift=LEFT * 0.1),      run_time=rt(0.6))

        self.wait(rt(0.5))

        # Block B: the empty gap — resolved by the expansion fan
        with self.voiceover(
            "Instead, something unexpected happens. "
            "A gap begins to appear between them. "
            "At first glance, this gap seems impossible. "
            "No characteristic from the initial traffic states "
            "enters this region. "
            "So how can the solution exist there? "
            "Nature cannot simply leave part of the traffic undefined. "
            "The LWR equation resolves this problem "
            "in a remarkable way. "
            "Instead of introducing a discontinuity, "
            "the solution is filled by infinitely many new characteristics. "
            "Each one carries a slightly different traffic density. "
            "Together, these characteristics fill the gap completely. "
            "This family of spreading characteristics "
            "is called an expansion fan, or rarefaction fan."
        ):
            self.play(FadeIn(gap_lbl, shift=UP * 0.1),         run_time=rt(0.4))
            self.play(FadeIn(explain2, shift=LEFT * 0.1),      run_time=rt(0.5))
            self.play(
                LaggedStart(*[Create(l) for l in fan_chars], lag_ratio=0.12),
                run_time=rt(1.0),
            )
            self.play(FadeIn(fan_lbl),                         run_time=rt(0.5))

        self.wait(rt(0.4))

        # Block C: physical meaning — gradual, not abrupt
        with self.voiceover(
            "Unlike a shock wave, "
            "where traffic density changes abruptly, "
            "a rarefaction wave represents a gradual transition. "
            "Drivers do not experience a sudden change "
            "in traffic conditions. "
            "Instead, they accelerate smoothly "
            "as more space becomes available."
        ):
            self.play(FadeIn(phys_note, shift=UP * 0.1),       run_time=rt(0.6))

        self.wait(rt(0.5))
        self.play(
            FadeOut(VGroup(sec_title, st_ax, x_lbl, t_lbl,
                           left_chars, right_chars, fan_chars, fan_lbl,
                           gap_lbl, explain1, explain2, phys_note)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 3. THE RAREFACTION SOLUTION
        # ─────────────────────────────────────────────────────────────────────
        sol_title = Text("The Rarefaction Solution",
                         font_size=32, weight=BOLD, color=WHITE)
        sol_title.to_edge(UP).shift(DOWN * 0.62)

        sol_eq = MathTex(
            r"\rho(x,t) = \begin{cases}"
            r"\rho_L              & x < c(\rho_L)\,t \\"
            r"(c)^{-1}(x/t)      & c(\rho_L)\,t \leq x \leq c(\rho_R)\,t \\"
            r"\rho_R              & x > c(\rho_R)\,t"
            r"\end{cases}",
            font_size=30, color=YELLOW,
        )
        sol_eq.center().shift(UP * 1.0)

        sol_note = VGroup(
            Text("Inside the fan, density at position x and time t", font_size=20, color="#cccccc"),
            Text("is the density whose wave speed equals x/t.", font_size=20, color="#cccccc"),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("The density varies continuously — no shocks, no jumps.", font_size=20, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        sol_note.next_to(sol_eq, DOWN, buff=0.38)

        # Block A: what the solution describes, before showing it
        with self.voiceover(
            "We can now describe the traffic density "
            "everywhere in the space-time plane. "
            "Outside the expansion fan, "
            "the traffic remains exactly as it was initially. "
            "The left side keeps its original density. "
            "The right side also keeps its original density. "
            "Only inside the fan "
            "does the density change continuously "
            "from one traffic state to the other."
        ):
            self.play(FadeIn(sol_title),                       run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: reveal the equation briefly — no derivation
        with self.voiceover(
            "Inside the fan, "
            "each position corresponds to one particular characteristic. "
            "The traffic density at that location "
            "is simply the density whose wave speed "
            "matches the ratio of distance to time. "
            "For the normalised Greenshields model, "
            "this relationship simplifies to a linear expression, "
            "producing a smooth transition across the entire fan."
        ):
            self.play(Write(sol_eq),                           run_time=rt(1.2))
            self.play(
                LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in sol_note],
                            lag_ratio=0.25),
                run_time=rt(0.8),
            )

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(sol_title, sol_eq, sol_note)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 4. TRAFFIC LIGHT EXAMPLE
        # ─────────────────────────────────────────────────────────────────────
        ex_title = Text("Traffic Light Example",
                        font_size=32, weight=BOLD, color=WHITE)
        ex_title.to_edge(UP).shift(DOWN * 0.62)

        setup = VGroup(
            Text("A traffic light turns green.", font_size=22, weight=BOLD, color=GREEN),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Before:  dense queue at x < 0  (ρ = ρ_j,  v = 0)", font_size=20, color=RED),
            Text("After:   empty road at x > 0  (ρ = 0,  v = v_f)", font_size=20, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        setup.center().shift(UP * 1.3)

        result = VGroup(
            Text("This is exactly a Riemann problem with diverging characteristics.", font_size=20, color="#cccccc"),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("The solution is a rarefaction fan.", font_size=20, color=YELLOW),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("The region of acceleration spreads:", font_size=20, color="#cccccc"),
            Text("  →  rightward into the empty road  (forward rarefaction)", font_size=20, color=GREEN),
            Text("  →  leftward into the waiting queue  (backward release)", font_size=20, color=RED),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Vehicles accelerate smoothly — no shock, no jump.", font_size=20, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        result.next_to(setup, DOWN, buff=0.35)

        # Block A: the everyday scenario
        with self.voiceover(
            "Rarefaction waves are not just mathematical objects. "
            "We experience them every day. "
            "Imagine waiting at a red traffic light. "
            "Behind the light, "
            "vehicles are densely packed together. "
            "Ahead, the road is almost empty."
        ):
            self.play(FadeIn(ex_title),                            run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in setup],
                            lag_ratio=0.2),
                run_time=rt(0.7),
            )

        self.wait(rt(0.3))

        # Block B: the release, framed as the Riemann problem
        with self.voiceover(
            "The moment the signal turns green, "
            "the first vehicle begins to move. "
            "Then the second. "
            "Then the third — "
            "one after another, the vehicles accelerate smoothly. "
            "This is exactly a Riemann problem "
            "with diverging characteristics, "
            "and the solution is a rarefaction fan. "
            "The region of acceleration spreads forward "
            "into the empty road, "
            "and backward into the waiting queue, "
            "as each driver reacts in turn to the one ahead. "
            "No shock, no jump — just smooth acceleration."
        ):
            self.play(
                LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in result],
                            lag_ratio=0.15),
                run_time=rt(1.0),
            )

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(ex_title, setup, result)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 5. SUMMARY — SHOCK vs RAREFACTION
        # ─────────────────────────────────────────────────────────────────────
        comp_title = Text("Shock vs Rarefaction",
                          font_size=32, weight=BOLD, color=WHITE)
        comp_title.to_edge(UP).shift(DOWN * 0.62)

        header = VGroup(
            Text("Shock Wave", font_size=21, weight=BOLD, color=RED),
            Text("Rarefaction Wave", font_size=21, weight=BOLD, color=GREEN),
        ).arrange(RIGHT, buff=2.0)
        header.next_to(comp_title, DOWN, buff=0.40)

        divider = Line(UP * 2.5, DOWN * 1.2, color=GREY_B, stroke_width=1)
        divider.next_to(header, DOWN, buff=0.22).align_to(header, UP)
        divider.move_to([0, divider.get_center()[1], 0])

        def make_pair(left_str, right_str):
            l = Text(left_str, font_size=18, color="#ffaaaa")
            r = Text(right_str, font_size=18, color="#aaffaa")
            return VGroup(l.move_to(LEFT * 2.8), r.move_to(RIGHT * 2.8))

        rows = VGroup(
            make_pair("characteristics converge",  "characteristics diverge"),
            make_pair("density jumps abruptly",    "density changes smoothly"),
            make_pair("Rankine-Hugoniot gives s",  "fan solution gives ρ(x,t)"),
            make_pair("requires weak solution",    "classical solution valid"),
            make_pair("phantom jam, merge shock",  "traffic light green phase"),
        ).arrange(DOWN, buff=0.34)
        rows.next_to(header, DOWN, buff=0.55)

        # Block A: the comparison, told as a story
        with self.voiceover(
            "We can now compare the two fundamental wave types "
            "of the LWR model. "
            "A shock wave forms when characteristics converge. "
            "Traffic compresses. "
            "Density changes abruptly. "
            "The solution contains a moving discontinuity. "
            "In contrast, a rarefaction wave forms "
            "when characteristics diverge. "
            "Traffic expands. "
            "Density changes smoothly. "
            "No discontinuity is present, "
            "and the classical solution remains valid "
            "throughout the expansion fan."
        ):
            self.play(FadeIn(comp_title),                      run_time=rt(0.5))
            self.play(FadeIn(header), Create(divider),         run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows],
                            lag_ratio=0.22),
                run_time=rt(1.0),
            )

        self.wait(rt(0.3))

        # Block B: why this distinction matters for the project
        with self.voiceover(
            "Together, shock waves and rarefaction waves "
            "describe the two fundamental ways traffic evolves. "
            "One represents compression. "
            "The other represents expansion. "
            "Any realistic traffic simulation "
            "must be capable of capturing both behaviours accurately. "
            "This requirement becomes one of the most important tests "
            "for any numerical method."
        ):
            self.wait(rt(0.3))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(comp_title, header, divider, rows)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 5b. KEY TAKEAWAYS
        # ─────────────────────────────────────────────────────────────────────
        kt_title = Text("Key Takeaways", font_size=34, weight=BOLD, color="#e8b84b")
        kt_title.to_edge(UP).shift(DOWN * 0.62)

        kt_bullets = VGroup(
            Text("• When characteristics diverge, a gap opens with no defined density.",
                 font_size=22, color=WHITE),
            Text("• The solution is filled by infinitely many characteristics —",
                 font_size=22, color=GREEN),
            Text("  this is called a rarefaction (expansion) fan.", font_size=22, color=GREEN),
            Text("• Shocks are sharp; rarefactions are smooth and self-similar.",
                 font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        kt_bullets.next_to(kt_title, DOWN, buff=0.55)

        with self.voiceover(
            "Before moving on, let's recap. "
            "When characteristics diverge, "
            "a gap opens with no defined density. "
            "The solution is filled by infinitely many characteristics — "
            "this is called a rarefaction, or expansion fan. "
            "Shocks are sharp; rarefactions are smooth and self-similar."
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
        # 6. PREVIEW — SCENE 11: WHY NUMERICAL METHODS?
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Why Numerical Methods?",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_q     = Text(
            "Characteristics work — until the problem becomes too complex.",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.3)
        prev_q.next_to(prev_title, DOWN, buff=0.40)

        with self.voiceover(
            "We have now completed the analytical theory "
            "of the LWR traffic model. "
            "We understand how characteristics "
            "carry traffic information. "
            "We know how shock waves form "
            "when characteristics intersect. "
            "We know how rarefaction waves emerge "
            "when characteristics diverge. "
            "For simple problems like the Riemann problem, "
            "these analytical solutions are elegant and exact. "
            "But real highways are rarely so simple. "
            "Traffic densities vary continuously along the road. "
            "Multiple shock waves can form. "
            "Rarefaction fans can overlap. "
            "New interactions appear constantly. "
            "Under these conditions, "
            "finding exact analytical solutions becomes impractical. "
            "This brings us to the central objective of this project. "
            "Instead of solving the LWR equation exactly, "
            "we will approximate its solution numerically. "
            "In the next scene, we'll discover why numerical methods "
            "are essential, and how they allow us "
            "to simulate realistic traffic flow."
        ):
            self.play(Write(prev_title),                     run_time=rt(0.9))
            self.play(FadeIn(prev_q, shift=UP * 0.1),        run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(prev_title, prev_q)),       run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene10_Rarefaction",
    ])
