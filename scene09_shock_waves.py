from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 9 — SHOCK WAVES
#  Render: manim -pql scene09_shock_waves.py Scene09_ShockWaves
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


# Greenshields (normalised): f(ρ) = ρ(1 − ρ),  c(ρ) = 1 − 2ρ
def f(rho):
    return rho * (1 - rho)


def c_speed(rho):
    return 1 - 2 * rho


class Scene09_ShockWaves(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT II · Scene 9 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Shock Waves", font_size=56, weight=BOLD, color=WHITE)
        sub   = Text("When characteristics collide and solutions break down",
                     font_size=25, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "In the previous scene, we discovered a beautiful way "
            "to solve the LWR equation. "
            "Every traffic disturbance followed its own characteristic curve. "
            "As long as those characteristics remained separate, "
            "the solution was smooth, predictable, and easy to interpret. "
            "But real traffic is rarely that well behaved. "
            "Disturbances do not always move away from one another. "
            "Sometimes, they move toward each other. "
            "And when they do, something remarkable happens: "
            "the elegant solution we just developed suddenly breaks down. "
            "In this scene, we will discover why that happens, "
            "how mathematics resolves the problem, "
            "and how it explains one of the most familiar phenomena "
            "on our roads — the sudden appearance of a traffic jam."
        ):
            self.play(Write(title),                     run_time=rt(1.3))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. CHARACTERISTICS INTERSECT — THE BREAKDOWN
        # ─────────────────────────────────────────────────────────────────────
        sec_title = Text("When Characteristics Intersect",
                         font_size=32, weight=BOLD, color=WHITE)
        sec_title.to_edge(UP).shift(DOWN * 0.62)

        # Space-time axes
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

        # Two bundles of characteristics heading toward each other
        # Left region: ρ_L = 0.2 → c = 0.6 (forward lean)
        # Right region: ρ_R = 0.7 → c = -0.4 (backward lean)
        T_MAX = 3.0

        def char(x0, speed, clr, alpha=0.80):
            return Line(
                st_ax.c2p(x0, 0),
                st_ax.c2p(x0 + speed * T_MAX, T_MAX),
                color=clr, stroke_width=2.0, stroke_opacity=alpha,
            )

        left_chars  = VGroup(*[char(x0, 0.6,  GREEN) for x0 in [-3, -2, -1]])
        right_chars = VGroup(*[char(x0, -0.4, RED)   for x0 in [1,  2,  3]])

        # Highlight the collision region
        collision_dot = Dot(st_ax.c2p(0, 0), radius=0.12, color=YELLOW)
        collision_lbl = Text("initial boundary", font_size=17, color=GREY_B)
        collision_lbl.next_to(st_ax.c2p(0, 0), DOWN * 0.8)

        # Right panel explanation
        explain_break = VGroup(
            Text("Left  (low density):", font_size=19, weight=BOLD, color=GREEN),
            Text("   c > 0  →  characteristics lean right", font_size=19, color=GREEN),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Right  (high density):", font_size=19, weight=BOLD, color=RED),
            Text("   c < 0  →  characteristics lean left", font_size=19, color=RED),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("They converge toward x = 0.", font_size=19, color=YELLOW),
            Text("Where they meet, the density", font_size=19, color=YELLOW),
            Text("would need two values at once.", font_size=19, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        explain_break.move_to(RIGHT * 3.3 + UP * 0.35)

        # Block A: the two regions, characteristics converge
        with self.voiceover(
            "Imagine two different traffic conditions on the same road. "
            "On the left, traffic is light. "
            "Vehicles have plenty of space, "
            "so information travels forward through the traffic stream. "
            "On the right, traffic is much denser. "
            "Drivers are closely packed together, "
            "and disturbances travel in the opposite direction. "
            "As time passes, "
            "the characteristics from both regions move toward one another. "
            "Eventually, they intersect."
        ):
            self.play(FadeIn(sec_title),                        run_time=rt(0.5))
            self.play(Create(st_ax), FadeIn(x_lbl, t_lbl),     run_time=rt(0.7))
            self.play(FadeIn(collision_dot), FadeIn(collision_lbl), run_time=rt(0.4))
            self.play(
                LaggedStart(*[Create(l) for l in left_chars],  lag_ratio=0.18),
                run_time=rt(0.8),
            )
            self.play(
                LaggedStart(*[Create(l) for l in right_chars], lag_ratio=0.18),
                run_time=rt(0.8),
            )

        self.wait(rt(0.5))

        # Block B: why is this a problem? — define the classical solution
        with self.voiceover(
            "At first glance, this may not seem like a problem. "
            "But mathematically, it creates a contradiction. "
            "Remember what a characteristic represents: "
            "each characteristic carries one specific traffic density. "
            "If two different characteristics intersect, "
            "they attempt to assign two different density values "
            "to the same point in space and time. "
            "But that is impossible — "
            "a single location on the road "
            "cannot simultaneously have two different traffic densities. "
            "This tells us something important: "
            "the smooth solution obtained using the method of characteristics "
            "is no longer valid. "
            "We say that the classical solution has broken down. "
            "A classical solution simply means a solution "
            "that remains smooth and continuous everywhere. "
            "Once characteristics intersect, "
            "that smooth description is no longer possible."
        ):
            self.play(FadeIn(explain_break, shift=LEFT * 0.1),  run_time=rt(0.6))

        self.wait(rt(0.5))
        self.play(
            FadeOut(VGroup(sec_title, st_ax, x_lbl, t_lbl,
                           left_chars, right_chars,
                           collision_dot, collision_lbl, explain_break)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 3. THE RIEMANN PROBLEM + WEAK SOLUTION
        # ─────────────────────────────────────────────────────────────────────
        riem_title = Text("The Riemann Problem",
                          font_size=32, weight=BOLD, color=WHITE)
        riem_title.to_edge(UP).shift(DOWN * 0.62)

        ic_eq = MathTex(
            r"\rho(x,0) = \begin{cases}"
            r"\rho_L & x < 0 \\"
            r"\rho_R & x > 0"
            r"\end{cases}",
            font_size=38, color=YELLOW,
        )
        ic_eq.center().shift(UP * 1.3)

        ic_note = Text(
            "A step-function initial condition with two constant states.",
            font_size=21, color="#aaaacc",
        )
        ic_note.next_to(ic_eq, DOWN, buff=0.30)

        weak_title = Text("The Weak Solution", font_size=22, weight=BOLD, color=WHITE)
        weak_title.next_to(ic_note, DOWN, buff=0.38)

        weak_txt = VGroup(
            Text("Since the smooth solution no longer exists,", font_size=20, color="#cccccc"),
            Text("we allow density to change abruptly —", font_size=20, color="#cccccc"),
            Text("a discontinuity, called a weak solution.", font_size=20, color=YELLOW),
            Text("This moving boundary is called a shock wave.", font_size=20, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        weak_txt.next_to(weak_title, DOWN, buff=0.22)

        # Block A: the Riemann problem — kept brief
        with self.voiceover(
            "To study this phenomenon, "
            "mathematicians begin with the simplest possible traffic configuration. "
            "Suppose the road is divided into two regions. "
            "On the left, the traffic density is constant. "
            "On the right, the traffic density is also constant, but different. "
            "The boundary between these two regions "
            "creates what is known as the Riemann problem. "
            "Although this initial condition is simple, "
            "it captures the essential behaviour of traffic "
            "when two different traffic states interact."
        ):
            self.play(FadeIn(riem_title),                   run_time=rt(0.5))
            self.play(Write(ic_eq),                         run_time=rt(1.0))
            self.play(FadeIn(ic_note, shift=UP * 0.1),      run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: the weak solution
        with self.voiceover(
            "Since the smooth solution no longer exists, "
            "we need a new mathematical description. "
            "Instead of forcing the density to change continuously, "
            "we allow it to change abruptly. "
            "This abrupt change is called a discontinuity. "
            "The solution that permits such discontinuities "
            "is known as a weak solution. "
            "Physically, this discontinuity represents the boundary "
            "between two different traffic states. "
            "That moving boundary is called a shock wave."
        ):
            self.play(FadeIn(weak_title),                   run_time=rt(0.4))
            self.play(
                LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in weak_txt],
                            lag_ratio=0.25),
                run_time=rt(0.8),
            )

        self.wait(rt(0.5))
        self.play(
            FadeOut(VGroup(riem_title, ic_eq, ic_note, weak_title, weak_txt)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4. RANKINE-HUGONIOT CONDITION — DERIVATION
        # ─────────────────────────────────────────────────────────────────────
        rh_title = Text("The Rankine-Hugoniot Condition",
                        font_size=32, weight=BOLD, color=WHITE)
        rh_title.to_edge(UP).shift(DOWN * 0.62)

        rh_question = Text(
            "At what speed does the shock travel?",
            font_size=25, color="#cccccc",
        )
        rh_question.next_to(rh_title, DOWN, buff=0.45)

        rh_deriv = VGroup(
            MathTex(r"\text{Conservation requires:}\quad"
                    r"\frac{d}{dt}\int_{\Omega}\rho\,dx + [f(\rho)]_{\text{jump}} = 0",
                    font_size=22, color="#888888"),
            MathTex(r"\Downarrow", font_size=26, color=GREY_B),
            MathTex(r"s\,(\rho_R - \rho_L) \;=\; f(\rho_R) - f(\rho_L)",
                    font_size=28, color="#cccccc"),
            MathTex(r"\Downarrow", font_size=26, color=GREY_B),
        ).arrange(DOWN, buff=0.28)
        rh_deriv.next_to(rh_question, DOWN, buff=0.38)

        rh_result = MathTex(
            r"s \;=\; \frac{f(\rho_R) - f(\rho_L)}{\rho_R - \rho_L}",
            font_size=40, color=YELLOW,
        )
        rh_result.next_to(rh_deriv, DOWN, buff=0.28)
        rh_box = SurroundingRectangle(rh_result, color="#334466", buff=0.26)

        rh_words = Text(
            "The shock speed  s  equals the slope of the secant\n"
            "on the flux diagram between the two states.",
            font_size=19, color="#8899cc", line_spacing=1.3,
        )
        rh_words.next_to(rh_box, DOWN, buff=0.30)

        # Block A: a new question
        with self.voiceover(
            "Once a shock wave forms, "
            "another important question naturally follows: "
            "how fast does the shock move? "
            "Unlike ordinary vehicles, the shock is not a physical object. "
            "It is a moving boundary between two traffic states. "
            "Yet this boundary has its own speed, "
            "and that speed can be calculated."
        ):
            self.play(FadeIn(rh_title),                     run_time=rt(0.5))
            self.play(FadeIn(rh_question, shift=DOWN * 0.1), run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: the Rankine-Hugoniot derivation
        with self.voiceover(
            "The answer comes from the same physical principle "
            "that led us to the LWR equation: "
            "the conservation of vehicles. "
            "Even though the traffic density changes abruptly across the shock, "
            "vehicles still cannot appear or disappear. "
            "Conservation must still hold. "
            "Applying this conservation principle across the discontinuity "
            "leads to one of the most important equations "
            "in traffic flow theory: "
            "the Rankine-Hugoniot condition. "
            "This equation tells us that the shock speed "
            "depends only on the traffic states "
            "immediately to its left and right. "
            "Once those two states are known, "
            "the motion of the shock is completely determined."
        ):
            self.play(Write(rh_deriv[0]),                   run_time=rt(0.8))
            self.play(FadeIn(rh_deriv[1]),                  run_time=rt(0.3))
            self.play(Write(rh_deriv[2]),                   run_time=rt(0.7))
            self.play(FadeIn(rh_deriv[3]),                  run_time=rt(0.3))
            self.play(Write(rh_result), Create(rh_box),     run_time=rt(0.9))
            self.play(FadeIn(rh_words, shift=UP * 0.1),     run_time=rt(0.5))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(rh_title, rh_question, rh_deriv, rh_words)),
            rh_result.animate.move_to(UP * 2.7).scale(0.70),
            FadeOut(rh_box),
            run_time=rt(0.9),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. SHOCK IN THE SPACE-TIME DIAGRAM
        # ─────────────────────────────────────────────────────────────────────
        # ρ_L = 0.2, ρ_R = 0.7 (normalised Greenshields f(ρ) = ρ(1-ρ))
        RHO_L = 0.2;  RHO_R = 0.7
        S_SHOCK = (f(RHO_R) - f(RHO_L)) / (RHO_R - RHO_L)   # = (0.21-0.16)/0.5 = 0.1

        st2 = Axes(
            x_range=[-3.2, 3.5, 1],
            y_range=[0,    3.2, 1],
            x_length=5.5,
            y_length=4.3,
            axis_config={
                "color": GREY_B, "include_tip": True,
                "tip_width": 0.18, "tip_height": 0.22, "include_numbers": False,
            },
        )
        st2.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.25)
        x2 = Text("x", font_size=20, color=GREY_B).next_to(st2.x_axis.get_end(), RIGHT * 0.4)
        t2 = Text("t", font_size=20, color=GREY_B).next_to(st2.y_axis.get_end(), UP * 0.4)

        C_L = c_speed(RHO_L)    # 0.6
        C_R = c_speed(RHO_R)    # -0.4

        left_chars2 = VGroup(*[
            Line(st2.c2p(x0, 0), st2.c2p(x0 + C_L * T_MAX, T_MAX),
                 color=GREEN, stroke_width=2.0, stroke_opacity=0.75)
            for x0 in [-3, -2, -1]
        ])
        right_chars2 = VGroup(*[
            Line(st2.c2p(x0, 0), st2.c2p(x0 + C_R * T_MAX, T_MAX),
                 color=RED, stroke_width=2.0, stroke_opacity=0.75)
            for x0 in [1, 2, 3]
        ])

        shock_line = Line(
            st2.c2p(0, 0), st2.c2p(S_SHOCK * T_MAX, T_MAX),
            color=YELLOW, stroke_width=4,
        )
        shock_lbl = VGroup(
            Text("shock", font_size=19, weight=BOLD, color=YELLOW),
            MathTex(r"s = 0.1", font_size=18, color=YELLOW),
        ).arrange(DOWN, buff=0.08)
        shock_lbl.next_to(st2.c2p(S_SHOCK * T_MAX, T_MAX), RIGHT * 0.5)

        # Right panel: numeric example
        numeric = VGroup(
            Text("Example  (normalised Greenshields):", font_size=18, weight=BOLD, color=WHITE),
            Rectangle(width=0.01, height=0.06, stroke_opacity=0, fill_opacity=0),
            MathTex(r"\rho_L = 0.2,\quad f(\rho_L) = 0.16", font_size=20, color=GREEN),
            MathTex(r"\rho_R = 0.7,\quad f(\rho_R) = 0.21", font_size=20, color=RED),
            Rectangle(width=0.01, height=0.06, stroke_opacity=0, fill_opacity=0),
            MathTex(
                r"s = \frac{0.21 - 0.16}{0.7 - 0.2} = \frac{0.05}{0.5} = 0.1",
                font_size=19, color=YELLOW,
            ),
            Rectangle(width=0.01, height=0.06, stroke_opacity=0, fill_opacity=0),
            Text("Shock moves slowly forward.", font_size=19, color="#aaaacc"),
            Text("The dense region grows into the free-flow region.", font_size=19, color="#aaaacc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        numeric.move_to(RIGHT * 3.3 + DOWN * 0.15)

        with self.voiceover(
            "Let's apply this equation to the normalised Greenshields model "
            "introduced earlier. "
            "Suppose the density on the left is 0.2, "
            "while the density on the right is 0.7. "
            "Using the corresponding traffic flow values, "
            "the Rankine-Hugoniot condition gives a shock speed of 0.1. "
            "In the space-time diagram, this appears as the yellow line. "
            "Notice that the characteristics approach the shock "
            "from both sides, but they never cross it. "
            "The shock itself becomes the moving boundary "
            "separating the two traffic states."
        ):
            self.play(Create(st2), FadeIn(x2, t2),         run_time=rt(0.7))
            self.play(
                LaggedStart(*[Create(l) for l in left_chars2],  lag_ratio=0.18),
                LaggedStart(*[Create(l) for l in right_chars2], lag_ratio=0.18),
                run_time=rt(0.9),
            )
            self.play(Create(shock_line), run_time=rt(0.9))
            self.play(FadeIn(shock_lbl),  run_time=rt(0.4))
            self.play(FadeIn(numeric, shift=LEFT * 0.1), run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(st2, x2, t2, left_chars2, right_chars2,
                           shock_line, shock_lbl, numeric, rh_result)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 6. PHANTOM JAMS — RECONNECT TO SCENE 1
        # ─────────────────────────────────────────────────────────────────────
        phant_title = Text("The Phantom Traffic Jam",
                           font_size=34, weight=BOLD, color=WHITE)
        phant_title.to_edge(UP).shift(DOWN * 0.62)

        scene1_recall = Text(
            "Recall from Scene 1: a jam that appears with no visible cause.",
            font_size=22, color="#aaaacc",
        )
        scene1_recall.center().shift(UP * 1.5)

        explanation = VGroup(
            Text("A small density disturbance can create", font_size=22, color=WHITE),
            Text("converging characteristics — and a shock.", font_size=22, color=WHITE),
            Rectangle(width=0.01, height=0.06, stroke_opacity=0, fill_opacity=0),
            Text("The shock propagates backward", font_size=22, color=YELLOW),
            Text("against the flow of traffic.", font_size=22, color=YELLOW),
            Rectangle(width=0.01, height=0.06, stroke_opacity=0, fill_opacity=0),
            Text("Cars move forward.", font_size=22, weight=BOLD, color=GREEN),
            Text("The jam propagates backward.", font_size=22, weight=BOLD, color=RED),
            Rectangle(width=0.01, height=0.06, stroke_opacity=0, fill_opacity=0),
            Text("This is the phantom jam — fully explained",  font_size=22, color=WHITE),
            Text("by the Rankine-Hugoniot condition.", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        explanation.next_to(scene1_recall, DOWN, buff=0.45)

        with self.voiceover(
            "We can now return to the question we asked "
            "at the very beginning of this presentation. "
            "Why can a traffic jam appear "
            "even when there is no accident, no roadworks, "
            "and no visible obstruction? "
            "The answer is now clear. "
            "A small disturbance — "
            "perhaps caused by one driver braking slightly — "
            "causes characteristics to converge. "
            "When those characteristics intersect, a shock wave forms. "
            "That shock propagates backward through the traffic stream, "
            "even though every vehicle continues moving forward. "
            "Drivers arriving at the shock "
            "experience what appears to be a traffic jam "
            "with no obvious cause ahead. "
            "This is the phenomenon known as a phantom traffic jam. "
            "What once seemed mysterious "
            "is now completely explained "
            "by the mathematics of the LWR model."
        ):
            self.play(FadeIn(phant_title),                      run_time=rt(0.5))
            self.play(FadeIn(scene1_recall, shift=DOWN * 0.1),  run_time=rt(0.5))
            self.wait(rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in explanation],
                            lag_ratio=0.14),
                run_time=rt(1.1),
            )

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(phant_title, scene1_recall, explanation)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 6b. KEY TAKEAWAYS
        # ─────────────────────────────────────────────────────────────────────
        kt_title = Text("Key Takeaways", font_size=34, weight=BOLD, color="#e8b84b")
        kt_title.to_edge(UP).shift(DOWN * 0.62)

        kt_bullets = VGroup(
            Text("• When characteristics converge, density becomes multi-valued.",
                 font_size=22, color=WHITE),
            Text("• Nature resolves this with a shock — a moving discontinuity.",
                 font_size=22, color=RED),
            Text("• The shock speed s is given by the Rankine-Hugoniot condition.",
                 font_size=22, color=YELLOW),
            Text("• Notice this is simply the slope of the secant joining the",
                 font_size=22, color=WHITE),
            Text("  two states on the fundamental diagram.", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        kt_bullets.next_to(kt_title, DOWN, buff=0.55)

        with self.voiceover(
            "Before moving on, let's recap. "
            "When characteristics converge, density becomes multi-valued. "
            "Nature resolves this with a shock — a moving discontinuity. "
            "The shock speed s is given by the Rankine-Hugoniot condition. "
            "Notice this is simply the slope of the secant "
            "joining the two states on the fundamental diagram."
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
        # 7. PREVIEW — SCENE 10: RAREFACTION WAVES
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Rarefaction Waves",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_q     = Text(
            "What happens when characteristics diverge instead of converge?",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.3)
        prev_q.next_to(prev_title, DOWN, buff=0.40)

        with self.voiceover(
            "So far, we have studied one possible outcome "
            "of the LWR equation. "
            "Characteristics move toward one another. "
            "They intersect. "
            "A shock wave forms. "
            "But convergence is not the only possibility. "
            "Sometimes characteristics spread apart instead of colliding. "
            "Instead of creating a shock, "
            "they produce a completely different type of solution "
            "known as a rarefaction wave. "
            "In the next scene, we'll explore how rarefaction waves form, "
            "and why they represent the opposite behaviour of shock waves."
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
        __file__, "Scene09_ShockWaves",
    ])
