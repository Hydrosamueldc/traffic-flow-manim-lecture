from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 8 — METHOD OF CHARACTERISTICS
#  Render: manim -pql scene08_characteristics.py Scene08_Characteristics
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene08_Characteristics(VoiceoverScene):

    BG_COLOR = "#0d1117"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT II · Scene 8 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Method of Characteristics",
                     font_size=50, weight=BOLD, color=WHITE)
        sub   = Text("How information travels through traffic",
                     font_size=26, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "We have now derived the LWR equation — "
            "a mathematical model that describes "
            "how traffic density changes over both space and time. "
            "Naturally, the next question is: "
            "can we solve this equation? "
            "For simple traffic situations, the answer is yes. "
            "There is an elegant analytical technique "
            "called the method of characteristics. "
            "But before we learn how this method solves the equation, "
            "we first need to understand what a characteristic actually is."
        ):
            self.play(Write(title),                     run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15),     run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)),           run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. WHAT IS A CHARACTERISTIC? — INTUITION BEFORE DERIVATION
        # ─────────────────────────────────────────────────────────────────────
        intro_title = Text("What Is a Characteristic?",
                           font_size=34, weight=BOLD, color=WHITE)
        intro_title.to_edge(UP).shift(DOWN * 0.62)

        # Road (horizontal line)
        PKT_Y = -1.55
        road = Line(LEFT * 5.6, RIGHT * 5.6, color=GREY_B, stroke_width=2.5)
        road.move_to([0, PKT_Y, 0])

        x_road_lbl = MathTex(r"x\;\text{(position)}", font_size=21, color=GREY_B)
        x_road_lbl.next_to(road.get_end(), RIGHT * 0.3)

        # Tick at t = 0
        P_START = np.array([-4.0, PKT_Y, 0])
        P_END   = np.array([ 3.5, PKT_Y, 0])

        tick_start = Line(P_START, P_START + UP * 0.22, color=GREY_B, stroke_width=1.5)
        lbl_t0     = MathTex(r"t=0", font_size=17, color="#888888"
                             ).next_to(P_START + UP * 0.22, UP * 0.35)

        tick_end   = Line(P_END,   P_END   + UP * 0.22, color=GREY_B, stroke_width=1.5)
        lbl_tT     = MathTex(r"t=T", font_size=17, color="#888888"
                             ).next_to(P_END + UP * 0.22, UP * 0.35)

        # The disturbance (coloured dot)
        packet = Dot(P_START, radius=0.24, color=YELLOW)
        trail  = TracedPath(packet.get_center,
                            stroke_color=YELLOW, stroke_width=2.8, stroke_opacity=0.55)

        # Labels alongside the road
        info_lbl = Text("small\ndisturbance", font_size=17, color=YELLOW, line_spacing=1.2)
        info_lbl.next_to(P_START, DOWN * 1.1)

        path_lbl = Text("characteristic curve:\nthe path of this disturbance",
                        font_size=17, color=YELLOW, line_spacing=1.2)
        path_lbl.move_to([(P_START[0] + P_END[0]) / 2, PKT_Y - 0.88, 0])

        # Right-side explanation text
        explain = VGroup(
            Text("One driver taps the brakes.", font_size=21, color=WHITE),
            Text("It affects the next driver, then the next.", font_size=21, color=WHITE),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("The disturbance does not stay put —", font_size=21, color=WHITE),
            Text("it travels through the traffic stream.", font_size=21, color=WHITE),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("The path it follows is called", font_size=21, color=YELLOW),
            Text("a characteristic curve.", font_size=21, weight=BOLD, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        explain.move_to(RIGHT * 3.3 + UP * 0.55)

        # Block A: road animation
        with self.voiceover(
            "Imagine you are watching traffic from above. "
            "Suddenly, one driver taps the brakes. "
            "That tiny action affects the driver behind. "
            "Then the next driver. "
            "Then the next. "
            "Notice something interesting: "
            "the disturbance does not stay where it started. "
            "It travels through the traffic stream. "
            "The path followed by that disturbance "
            "is called a characteristic curve. "
            "Every point on the road generates its own characteristic — "
            "its own path through space-time."
        ):
            self.play(FadeIn(intro_title),                     run_time=rt(0.5))
            self.play(Create(road), FadeIn(x_road_lbl),        run_time=rt(0.5))
            self.play(FadeIn(tick_start), FadeIn(lbl_t0),      run_time=rt(0.4))
            self.play(FadeIn(packet), FadeIn(info_lbl),        run_time=rt(0.4))
            self.add(trail)
            self.play(
                packet.animate.move_to(P_END),
                run_time=rt(2.6), rate_func=linear,
            )
            self.play(FadeIn(tick_end), FadeIn(lbl_tT),        run_time=rt(0.4))
            self.play(FadeIn(path_lbl, shift=UP * 0.1),        run_time=rt(0.5))
            self.play(FadeIn(explain, shift=LEFT * 0.1),       run_time=rt(0.5))

        self.wait(rt(0.5))

        # Block B: transition to x-t plane
        # Small x-t diagram on the left to show the characteristic as a line
        st_mini = Axes(
            x_range=[-4.5, 4.2, 1],
            y_range=[0,    3.5, 1],
            x_length=5.2,
            y_length=3.9,
            axis_config={
                "color":           GREY_B,
                "include_tip":     True,
                "tip_width":       0.18,
                "tip_height":      0.22,
                "include_numbers": False,
            },
        )
        st_mini.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.15)

        st_x = Text("x", font_size=21, color=GREY_B)
        st_x.next_to(st_mini.x_axis.get_end(), RIGHT * 0.4)
        st_t = Text("t", font_size=21, color=GREY_B)
        st_t.next_to(st_mini.y_axis.get_end(), UP * 0.4)

        char_line_mini = Line(
            st_mini.c2p(-4.0, 0), st_mini.c2p(3.5, 3.0),
            color=YELLOW, stroke_width=3,
        )
        dot_mini_0 = Dot(st_mini.c2p(-4.0, 0), radius=0.11, color=YELLOW)
        dot_mini_T = Dot(st_mini.c2p( 3.5, 3.0), radius=0.11, color=YELLOW)
        char_mini_lbl = Text("characteristic", font_size=19, weight=BOLD, color=YELLOW)
        char_mini_lbl.next_to(st_mini.c2p(3.5, 3.0), RIGHT * 0.4)

        xt_note = VGroup(
            Text("In the (x, t) plane, the path", font_size=21, color=WHITE),
            Text("of the disturbance is a line.", font_size=21, color=WHITE),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("Its slope = 1 / c(ρ).", font_size=21, color=YELLOW),
            Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0),
            Text("The derivation will show us", font_size=21, color="#aaaacc"),
            Text("exactly what that slope must be.", font_size=21, color="#aaaacc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        xt_note.move_to(RIGHT * 3.3 + UP * 0.45)

        road_grp = VGroup(road, x_road_lbl, tick_start, lbl_t0,
                          packet, trail, info_lbl,
                          tick_end, lbl_tT, path_lbl, explain)

        with self.voiceover(
            "Watching cars move along a road is useful. "
            "But it becomes difficult to see "
            "how this information evolves over time. "
            "So mathematicians use a different picture. "
            "Instead of drawing the road itself, "
            "we draw position along the horizontal axis, "
            "and time along the vertical axis. "
            "In this new picture, "
            "the motion of the disturbance becomes a straight line. "
            "That line is the characteristic. "
            "Its slope in the x-t plane "
            "tells us the speed at which the disturbance travels. "
            "The central question is: "
            "what determines that slope? "
            "The derivation will give us the precise answer."
        ):
            self.play(FadeOut(road_grp),                        run_time=rt(0.7))
            self.play(Create(st_mini), FadeIn(st_x, st_t),      run_time=rt(0.7))
            self.play(FadeIn(dot_mini_0),                       run_time=rt(0.3))
            self.play(Create(char_line_mini), FadeIn(dot_mini_T), run_time=rt(0.9))
            self.play(FadeIn(char_mini_lbl, shift=LEFT * 0.1),  run_time=rt(0.5))
            self.play(FadeIn(xt_note, shift=LEFT * 0.1),        run_time=rt(0.5))

        self.wait(rt(0.5))
        mini_grp = VGroup(intro_title, st_mini, st_x, st_t,
                          char_line_mini, dot_mini_0, dot_mini_T,
                          char_mini_lbl, xt_note)
        self.play(FadeOut(mini_grp), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 3. DERIVING THE CHARACTERISTIC EQUATION
        # ─────────────────────────────────────────────────────────────────────
        deriv_title = Text("Deriving the Characteristic Curves",
                           font_size=32, weight=BOLD, color=WHITE)
        deriv_title.to_edge(UP).shift(DOWN * 0.62)

        idea_txt = Text(
            "Suppose density is constant along some curve  x(t)  in (x, t) space.",
            font_size=23, color="#cccccc",
        )
        idea_txt.next_to(deriv_title, DOWN, buff=0.50)

        step1 = MathTex(
            r"\frac{d\rho}{dt}\bigg|_{x(t)}"
            r"\;=\;\frac{\partial\rho}{\partial t}"
            r"+\frac{dx}{dt}\,\frac{\partial\rho}{\partial x}"
            r"\;=\;0",
            font_size=26,
        )
        step1.next_to(idea_txt, DOWN, buff=0.42)

        step2 = MathTex(
            r"\text{LWR: }\quad"
            r"\frac{\partial\rho}{\partial t}"
            r"+ f'(\rho)\,\frac{\partial\rho}{\partial x} = 0",
            font_size=25, color="#8899cc",
        )
        step2.next_to(step1, DOWN, buff=0.38)

        step3 = MathTex(
            r"\therefore\quad\frac{dx}{dt} \;=\; f'(\rho) \;=\; c(\rho)",
            font_size=34, color=YELLOW,
        )
        step3.next_to(step2, DOWN, buff=0.40)
        step3_box = SurroundingRectangle(step3, color="#334466", buff=0.28)

        # Block A
        with self.voiceover(
            "We have identified the path followed by a disturbance. "
            "Now we would like to determine exactly how fast that path moves. "
            "Suppose that, as we move along the path of the disturbance, "
            "the traffic density never changes. "
            "In other words, "
            "we are following the same packet of traffic information. "
            "If the density remains constant, "
            "then its total rate of change along that path must be zero. "
            "The density depends on both position and time. "
            "But position itself changes as we move along the characteristic. "
            "Therefore, to calculate the total change in density, "
            "we must use the chain rule. "
            "That gives us: "
            "partial rho over partial t, "
            "plus the speed of the curve times partial rho over partial x, "
            "and this sum equals zero."
        ):
            self.play(FadeIn(deriv_title),                   run_time=rt(0.6))
            self.play(FadeIn(idea_txt, shift=DOWN * 0.1),    run_time=rt(0.6))
            self.play(Write(step1),                          run_time=rt(1.0))

        self.wait(rt(0.3))

        # Block B
        with self.voiceover(
            "Now compare with the LWR equation. "
            "It says the same two terms must sum to zero — "
            "but the coefficient of the spatial derivative is f-prime of rho, "
            "the wave speed c of rho. "
            "These two equations match if and only if "
            "the curve moves at speed f-prime of rho. "
            "That is the characteristic equation. "
            "This result is remarkable. "
            "The LWR equation itself "
            "tells us how fast traffic information travels. "
            "It is very important not to confuse two different speeds. "
            "Vehicles move with the traffic velocity v. "
            "Disturbances move with the characteristic speed c of rho. "
            "These are completely different quantities. "
            "A driver may move forward, "
            "while the disturbance created by that driver "
            "travels backward through the traffic stream."
        ):
            self.play(FadeIn(step2, shift=UP * 0.1),         run_time=rt(0.6))
            self.wait(rt(0.5))
            self.play(Write(step3), Create(step3_box),        run_time=rt(0.9))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(deriv_title, idea_txt, step1, step2, step3_box)),
            step3.animate.move_to(UP * 2.85).scale(0.78),
            run_time=rt(0.9),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4. TWO KEY PROPERTIES
        # ─────────────────────────────────────────────────────────────────────
        prop1_grp = VGroup(
            MathTex(r"\mathbf{1.}", font_size=26, color=YELLOW),
            Text("Along each characteristic, traffic density is constant.",
                 font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.22)
        prop1_rect = SurroundingRectangle(prop1_grp, color="#334455", buff=0.22)
        prop1 = VGroup(prop1_rect, prop1_grp)
        prop1.center().shift(UP * 1.35)

        prop2_top = VGroup(
            MathTex(r"\mathbf{2.}", font_size=26, color=YELLOW),
            Text("Since density is constant, c(ρ) is constant —",
                 font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.22)
        prop2_bot = Text(
            "so characteristics are straight lines in (x, t) space.",
            font_size=22, color=WHITE,
        )
        prop2_bot.next_to(prop2_top, DOWN, buff=0.10).align_to(prop2_top[1], LEFT)
        prop2_grp = VGroup(prop2_top, prop2_bot)
        prop2_rect = SurroundingRectangle(prop2_grp, color="#334455", buff=0.22)
        prop2 = VGroup(prop2_rect, prop2_grp)
        prop2.next_to(prop1, DOWN, buff=0.38)

        with self.voiceover(
            "This gives us two immediate consequences. "
            "First: density is constant along each characteristic — "
            "that is exactly what we assumed, and the LWR equation confirms it. "
            "Second: because density is constant, "
            "the wave speed c of rho is also constant along the characteristic. "
            "A curve with constant slope is a straight line. "
            "So every characteristic is a straight line in (x, t) space. "
            "The slope equals one over c of rho. "
            "Every straight line acts like a highway "
            "carrying one particular density value "
            "through space and time."
        ):
            self.play(FadeIn(prop1, shift=DOWN * 0.1), run_time=rt(0.7))
            self.wait(rt(0.4))
            self.play(FadeIn(prop2, shift=DOWN * 0.1), run_time=rt(0.7))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(step3, prop1, prop2)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 5. SPACE-TIME DIAGRAM — FREE FLOW AND CONGESTED CHARACTERISTICS
        # ─────────────────────────────────────────────────────────────────────
        st_ax = Axes(
            x_range=[-3.2, 3.5, 1],
            y_range=[0,    3.2, 1],
            x_length=5.5,
            y_length=4.4,
            axis_config={
                "color":           GREY_B,
                "include_tip":     True,
                "tip_width":       0.18,
                "tip_height":      0.22,
                "include_numbers": False,
            },
        )
        st_ax.to_edge(LEFT).shift(RIGHT * 0.55 + DOWN * 0.25)

        x_lbl_st = Text("x  (position)", font_size=20, color=GREY_B)
        x_lbl_st.next_to(st_ax.x_axis.get_end(), RIGHT * 0.4)
        t_lbl_st = Text("t  (time)", font_size=20, color=GREY_B)
        t_lbl_st.next_to(st_ax.y_axis.get_end(), UP * 0.4)

        st_title = Text("Space-Time Diagram",
                        font_size=26, weight=BOLD, color=WHITE)
        st_title.to_edge(UP).shift(DOWN * 0.52)

        C_FREE = 0.6
        C_CONG = -0.4
        T_MAX  = 3.0

        def char_line(x0, c, clr, alpha=0.85):
            return Line(
                st_ax.c2p(x0, 0),
                st_ax.c2p(x0 + c * T_MAX, T_MAX),
                color=clr, stroke_width=2.0, stroke_opacity=alpha,
            )

        free_chars = VGroup(*[char_line(x0, C_FREE, GREEN)  for x0 in [-3,-2,-1,0,1,2]])
        cong_chars = VGroup(*[char_line(x0, C_CONG, RED)    for x0 in [-2,-1,0,1,2,3]])

        panel_free = VGroup(
            Dot(radius=0.08, color=GREEN),
            Text("  Free flow:  c > 0  (forward)", font_size=19, color="#cccccc"),
        ).arrange(RIGHT, buff=0.10)
        panel_free.move_to(RIGHT * 3.3 + UP * 1.8)

        panel_cong = VGroup(
            Dot(radius=0.08, color=RED),
            Text("  Congested:  c < 0  (backward)", font_size=19, color="#cccccc"),
        ).arrange(RIGHT, buff=0.10)
        panel_cong.next_to(panel_free, DOWN, buff=0.38)

        interp = VGroup(
            Text("Think of each characteristic as an", font_size=19, color="#aaaacc"),
            Text("invisible conveyor belt for information.", font_size=19, color="#aaaacc"),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        interp.next_to(panel_cong, DOWN, buff=0.38)

        # Block A: free-flow characteristics
        with self.voiceover(
            "Let us draw the space-time plane. "
            "The horizontal axis is position x "
            "and the vertical axis is time t, increasing upward. "
            "Each characteristic is a straight line. "
            "In a region of free-flowing traffic, "
            "density is low and the wave speed is positive. "
            "The characteristics lean to the right — "
            "density information travels forward in both space and time."
        ):
            self.play(FadeIn(st_title), run_time=rt(0.5))
            self.play(Create(st_ax), FadeIn(x_lbl_st, t_lbl_st), run_time=rt(0.7))
            self.play(
                LaggedStart(*[Create(l) for l in free_chars], lag_ratio=0.13),
                run_time=rt(1.0),
            )
            self.play(FadeIn(panel_free, shift=LEFT * 0.1), run_time=rt(0.5))

        self.wait(rt(0.3))

        # Block B: congested characteristics
        with self.voiceover(
            "In a congested region, "
            "density is high and the wave speed is negative. "
            "The characteristics lean to the left. "
            "Changes in density travel backward — "
            "against the direction of vehicle motion. "
            "Remember from Scene Six: "
            "cars move forward, but disturbances move backward. "
            "You can think of each characteristic "
            "as an invisible conveyor belt "
            "carrying information through the traffic stream. "
            "The cars themselves may move in one direction, "
            "but the information follows the characteristics."
        ):
            self.play(
                LaggedStart(*[Create(l) for l in cong_chars], lag_ratio=0.13),
                run_time=rt(1.0),
            )
            self.play(FadeIn(panel_cong, shift=LEFT * 0.1), run_time=rt(0.5))
            self.play(FadeIn(interp, shift=UP * 0.1),        run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(
            FadeOut(VGroup(st_title, st_ax, x_lbl_st, t_lbl_st,
                           free_chars, cong_chars,
                           panel_free, panel_cong, interp)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5b. KEY TAKEAWAYS
        # ─────────────────────────────────────────────────────────────────────
        kt_title = Text("Key Takeaways", font_size=34, weight=BOLD, color="#e8b84b")
        kt_title.to_edge(UP).shift(DOWN * 0.62)

        kt_bullets = VGroup(
            Text("• A characteristic is a curve along which density stays constant.",
                 font_size=22, color=WHITE),
            Text("• Its speed is c(ρ) = f'(ρ), the characteristic (wave) speed.",
                 font_size=22, color=YELLOW),
            Text("• This is not the speed of the vehicles.", font_size=22, color=WHITE),
            Text("  It is the speed of traffic information.", font_size=22, color=WHITE),
            Text("• c(ρ) > 0 in free flow; c(ρ) < 0 in congestion.",
                 font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        kt_bullets.next_to(kt_title, DOWN, buff=0.55)

        with self.voiceover(
            "Before moving on, let's recap. "
            "A characteristic is a curve along which density stays constant. "
            "Its speed is c of rho, the characteristic speed. "
            "This is not the speed of the vehicles. "
            "It is the speed of traffic information. "
            "The characteristic speed is positive in free flow, "
            "and negative in congestion."
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
        # 6. PREVIEW — SCENE 9: SHOCK WAVES
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: Shock Waves",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_eq    = MathTex(
            r"\rho(x,0) = \begin{cases}"
            r"\rho_L & x < 0 \\"
            r"\rho_R & x > 0"
            r"\end{cases}",
            font_size=46, color=YELLOW,
        )
        prev_desc  = Text(
            "What happens when characteristics from different regions collide?",
            font_size=23, color="#8899cc",
        )
        prev_title.center().shift(UP * 1.7)
        prev_eq.next_to(prev_title, DOWN, buff=0.45)
        prev_desc.next_to(prev_eq,  DOWN, buff=0.38)

        with self.voiceover(
            "So far, everything seems beautifully simple. "
            "Every disturbance follows its own characteristic. "
            "But what happens if two different disturbances "
            "try to occupy the same point at the same time? "
            "Can one location have two different density values? "
            "Clearly not. "
            "Something has to give. "
            "Nature resolves this contradiction "
            "by creating a shock wave. "
            "In the next scene, we'll see exactly how that happens."
        ):
            self.play(Write(prev_title),                     run_time=rt(0.9))
            self.play(Write(prev_eq),                        run_time=rt(1.1))
            self.play(FadeIn(prev_desc, shift=UP * 0.1),     run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(prev_title, prev_eq, prev_desc)), run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene08_Characteristics",
    ])
