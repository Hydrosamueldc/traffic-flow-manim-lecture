from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 3 — TRAFFIC VELOCITY
#  Render: manim -pql scene03_traffic_velocity.py Scene03_TrafficVelocity
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene03_TrafficVelocity(VoiceoverScene):

    BG_COLOR  = "#0d1117"
    ASPHALT   = "#1e1e1e"
    GRASS_COL = "#1a3320"
    CAR_COLORS = [
        "#4a90e2", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#e67e22", "#5dade2",
    ]
    ROAD_Y = -1.5
    ROAD_H = 1.5
    ROAD_W = 14.0

    def _make_car(self, color: str, x: float, y: float) -> SVGMobject:
        car = self._car_template.copy()
        car[0].set_fill(color, opacity=1)
        car.move_to([x, y, 0])
        return car

    def _make_highway(self) -> VGroup:
        road = Rectangle(
            width=self.ROAD_W, height=self.ROAD_H,
            fill_color=self.ASPHALT, fill_opacity=1, stroke_width=0,
        ).move_to([0, self.ROAD_Y, 0])
        grass_top = Rectangle(width=self.ROAD_W, height=4,
                              fill_color=self.GRASS_COL, fill_opacity=1,
                              stroke_width=0).next_to(road, UP, buff=0)
        grass_bot = Rectangle(width=self.ROAD_W, height=4,
                              fill_color=self.GRASS_COL, fill_opacity=1,
                              stroke_width=0).next_to(road, DOWN, buff=0)
        top_edge = Line(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                        color=WHITE, stroke_width=2
                        ).move_to([0, self.ROAD_Y + self.ROAD_H / 2, 0])
        bot_edge = Line(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                        color=WHITE, stroke_width=2
                        ).move_to([0, self.ROAD_Y - self.ROAD_H / 2, 0])
        return VGroup(grass_bot, grass_top, road, top_edge, bot_edge)

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT I · Scene 3 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        self._car_template = SVGMobject("car.svg")
        self._car_template.height = 0.32

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE — CONNECT TO SCENE 2
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Traffic Velocity", font_size=54, weight=BOLD, color=WHITE)
        sub   = Text("The second fundamental variable", font_size=28, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "In the previous scene, we learned how to measure how crowded a road is "
            "using traffic density. "
            "But knowing how many vehicles are on the road is only part of the story. "
            "Imagine two highways with exactly the same number of vehicles. "
            "On one highway, traffic is moving smoothly at high speed. "
            "On the other, vehicles are barely moving. "
            "Clearly, density alone cannot completely describe traffic. "
            "We also need another quantity: how fast are the vehicles moving?"
        ):
            self.play(Write(title), run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15), run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. DEFINITION — WHAT IS VELOCITY AND WHY AVERAGE?
        # ─────────────────────────────────────────────────────────────────────
        def_title = Text("Traffic Velocity", font_size=40, weight=BOLD, color=YELLOW)
        def_title.to_edge(UP).shift(DOWN * 0.6)

        eq = MathTex(
            r"v(x,\,t)",
            r"=\; \text{average speed of vehicles at position }x\text{, time }t",
            font_size=29,
        )
        eq[0].set_color(YELLOW)
        eq.center().shift(UP * 0.7)

        units_line = MathTex(r"\text{Units: km/h \quad (or m/s)}",
                             font_size=26, color="#aaaaaa")
        units_line.next_to(eq, DOWN, buff=0.45)

        with self.voiceover(
            "This quantity is called traffic velocity. "
            "In everyday life, velocity simply tells us how fast something is moving. "
            "In traffic flow theory, however, we are not interested in the speed "
            "of one particular vehicle. "
            "Suppose one driver is travelling at one hundred kilometres per hour "
            "while another nearby is travelling at sixty. "
            "Which one should represent the traffic? Neither. "
            "Instead, we consider the average behaviour of all nearby vehicles. "
            "This average speed is what we call the traffic velocity."
        ):
            self.play(FadeIn(def_title), run_time=rt(0.6))
            self.play(Write(eq), run_time=rt(1.5))
            self.play(FadeIn(units_line), run_time=rt(0.5))

        self.wait(rt(0.4))

        # Explain what x and t mean
        note_line = Text(
            "v(x, t) varies continuously in both space and time",
            font_size=23, color="#8899cc",
        )
        note_line.next_to(units_line, DOWN, buff=0.38)

        var_note = VGroup(
            Text("x  →  location along the road", font_size=21, color="#aaaaaa"),
            Text("t  →  the moment of observation", font_size=21, color="#aaaaaa"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        var_note.next_to(note_line, DOWN, buff=0.32)

        with self.voiceover(
            "We denote traffic velocity by v of x and t. "
            "The symbol x tells us where we are along the road. "
            "The symbol t tells us when we are observing the traffic. "
            "This means that traffic velocity can change "
            "from one location to another and from one moment to the next. "
            "Just like density, velocity is not a single number. "
            "It is a function that varies continuously in both space and time."
        ):
            self.play(FadeIn(note_line, shift=UP * 0.1), run_time=rt(0.6))
            for row in var_note:
                self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=rt(0.5))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(def_title, eq, units_line, note_line, var_note)),
                  run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 3. VISUAL DISCOVERY — THREE DENSITY LEVELS
        # ─────────────────────────────────────────────────────────────────────
        highway = self._make_highway()
        sec_lbl = Text("What determines how fast vehicles can move?",
                       font_size=28, weight=BOLD, color=WHITE)
        sec_lbl.to_edge(UP).shift(DOWN * 0.52)

        with self.voiceover(
            "But what actually determines how fast vehicles can move? "
            "Think about driving on an empty highway. "
            "Let us observe what happens as we gradually increase the number of vehicles."
        ):
            self.play(FadeIn(sec_lbl), FadeIn(highway), run_time=rt(0.9))

        # ── LOW DENSITY ───────────────────────────────────────────────────────
        low_lbl = Text("Low Density  →  High Velocity", font_size=26, color=GREEN)
        low_lbl.to_edge(DOWN).shift(UP * 0.5)

        cars_low = VGroup(*[
            self._make_car(self.CAR_COLORS[i], x=-5.5 + i * 3.2, y=self.ROAD_Y)
            for i in range(4)
        ])
        arr_low = VGroup(*[
            Arrow(
                start=car.get_right() + RIGHT * 0.05,
                end=car.get_right() + RIGHT * 1.15,
                color=GREEN, stroke_width=2.5, buff=0,
                max_tip_length_to_length_ratio=0.28,
            )
            for car in cars_low
        ])

        with self.voiceover(
            "There are only a few vehicles on the road. "
            "Large gaps separate one vehicle from the next. "
            "Drivers have plenty of space to accelerate. "
            "They are rarely forced to react to other vehicles. "
            "As a result, traffic moves close to the maximum allowed speed."
        ):
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in cars_low], lag_ratio=0.15),
                FadeIn(low_lbl, shift=UP * 0.1),
                run_time=rt(1.2),
            )
            self.play(
                LaggedStart(*[GrowArrow(a) for a in arr_low], lag_ratio=0.12),
                run_time=rt(0.9),
            )
            self.play(
                VGroup(cars_low, arr_low).animate.shift(RIGHT * 5.0),
                run_time=rt(2.0), rate_func=linear,
            )

        self.play(FadeOut(VGroup(cars_low, arr_low, low_lbl)), run_time=rt(0.5))

        # ── MEDIUM DENSITY ────────────────────────────────────────────────────
        med_lbl = Text("Medium Density  →  Reduced Velocity", font_size=26, color=YELLOW)
        med_lbl.to_edge(DOWN).shift(UP * 0.5)

        cars_med = VGroup(*[
            self._make_car(self.CAR_COLORS[i % 8], x=-5.2 + i * 1.75, y=self.ROAD_Y)
            for i in range(7)
        ])
        arr_med = VGroup(*[
            Arrow(
                start=car.get_right() + RIGHT * 0.04,
                end=car.get_right() + RIGHT * 0.58,
                color=YELLOW, stroke_width=2.2, buff=0,
                max_tip_length_to_length_ratio=0.35,
            )
            for car in cars_med
        ])

        with self.voiceover(
            "Now more vehicles enter the road. "
            "The available space between vehicles becomes smaller. "
            "Drivers begin adjusting their speed to match the vehicles ahead. "
            "Although traffic is still moving, drivers no longer have complete freedom. "
            "Average speed begins to decrease."
        ):
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in cars_med], lag_ratio=0.08),
                FadeIn(med_lbl, shift=UP * 0.1),
                run_time=rt(1.2),
            )
            self.play(
                LaggedStart(*[GrowArrow(a) for a in arr_med], lag_ratio=0.07),
                run_time=rt(0.9),
            )
            self.play(
                VGroup(cars_med, arr_med).animate.shift(RIGHT * 2.8),
                run_time=rt(2.0), rate_func=linear,
            )

        self.play(FadeOut(VGroup(cars_med, arr_med, med_lbl)), run_time=rt(0.5))

        # ── HIGH DENSITY ──────────────────────────────────────────────────────
        high_lbl = Text("High Density  →  Near-Zero Velocity", font_size=26, color=RED)
        high_lbl.to_edge(DOWN).shift(UP * 0.5)

        cars_high = VGroup(*[
            self._make_car(self.CAR_COLORS[i % 8], x=-6.0 + i * 1.1, y=self.ROAD_Y)
            for i in range(11)
        ])
        arr_high = VGroup(*[
            Arrow(
                start=car.get_right() + RIGHT * 0.02,
                end=car.get_right() + RIGHT * 0.28,
                color=RED, stroke_width=2, buff=0,
                max_tip_length_to_length_ratio=0.50,
            )
            for car in cars_high
        ])

        with self.voiceover(
            "Finally, the road becomes heavily congested. "
            "Vehicles are packed closely together. "
            "Every driver is constantly reacting to the vehicle in front. "
            "The available space almost disappears. "
            "As the density approaches its maximum possible value, "
            "the average speed approaches zero."
        ):
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in cars_high], lag_ratio=0.06),
                FadeIn(high_lbl, shift=UP * 0.1),
                run_time=rt(1.3),
            )
            self.play(
                LaggedStart(*[GrowArrow(a) for a in arr_high], lag_ratio=0.05),
                run_time=rt(0.8),
            )
            self.play(
                VGroup(cars_high, arr_high).animate.shift(RIGHT * 0.7),
                run_time=rt(2.2), rate_func=linear,
            )

        self.play(
            FadeOut(VGroup(sec_lbl, highway, cars_high, arr_high, high_lbl)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4. THE BIG OBSERVATION
        # ─────────────────────────────────────────────────────────────────────
        obs_lines = VGroup(
            Text("The road did not change.",         font_size=30, color="#888888"),
            Text("The weather did not change.",      font_size=30, color="#888888"),
            Text("The speed limit did not change.",  font_size=30, color="#888888"),
            Text("Only one quantity changed:",       font_size=30, color=WHITE),
            Text("the traffic density.",             font_size=30, color=YELLOW, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40)
        obs_lines.center().shift(UP * 0.3)

        conclusion = Text(
            "Yet the average speed changed automatically.",
            font_size=28, color="#aaaacc",
        )
        conclusion.next_to(obs_lines, DOWN, buff=0.52)

        with self.voiceover(
            "From these three situations, we notice something remarkable. "
            "We never changed the road. "
            "We never changed the weather. "
            "We never changed the speed limit. "
            "The only quantity that changed was the traffic density. "
            "Yet the average speed changed automatically. "
            "This tells us something fundamental: "
            "velocity depends on density."
        ):
            for line in obs_lines:
                self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=rt(0.5))
                self.wait(rt(0.12))
            self.play(FadeIn(conclusion, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(obs_lines, conclusion)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 5. THE v(ρ) RELATIONSHIP
        # ─────────────────────────────────────────────────────────────────────
        rel_title = Text("The Velocity–Density Relationship",
                         font_size=34, weight=BOLD, color=WHITE)
        rel_title.to_edge(UP).shift(DOWN * 0.58)

        key_eq = MathTex(
            r"v \;=\; v(\rho)",
            font_size=58, color=YELLOW,
        )
        key_eq.center().shift(UP * 0.8)

        key_desc = Text(
            "Once the traffic density is known,\n"
            "the average traffic velocity can also be determined.",
            font_size=24, color="#aaaacc", line_spacing=1.4,
        )
        key_desc.next_to(key_eq, DOWN, buff=0.45)

        with self.voiceover(
            "Instead of treating velocity as an independent quantity, "
            "we can express it as a function of density. "
            "In other words, "
            "once the traffic density is known, "
            "the average traffic velocity can also be determined. "
            "We write this as v equals v of rho."
        ):
            self.play(FadeIn(rel_title), run_time=rt(0.6))
            self.play(Write(key_eq), run_time=rt(1.0))
            self.play(FadeIn(key_desc, shift=UP * 0.1), run_time=rt(0.7))

        self.wait(rt(0.6))
        self.play(FadeOut(key_desc), run_time=rt(0.5))

        # ── Why does this function decrease? ─────────────────────────────────
        why_lines = VGroup(
            Text("Every additional vehicle reduces the available space.",
                 font_size=24, color="#cccccc"),
            Text("Less space means more interaction between drivers.",
                 font_size=24, color="#cccccc"),
            Text("More interaction means lower speeds.",
                 font_size=24, color="#cccccc"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        why_lines.next_to(key_eq, DOWN, buff=0.50)

        therefore = MathTex(
            r"\text{As } \rho \text{ increases,} \quad v(\rho) \text{ decreases.}",
            font_size=32, color=YELLOW,
        )
        therefore.next_to(why_lines, DOWN, buff=0.38)

        with self.voiceover(
            "Why is this function decreasing? "
            "Because every additional vehicle reduces the amount of available space. "
            "Less available space means more interaction between drivers. "
            "More interaction means lower speeds. "
            "Therefore, as density increases, velocity decreases."
        ):
            for line in why_lines:
                self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=rt(0.55))
                self.wait(rt(0.12))
            self.play(Write(therefore), run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(why_lines, therefore)), run_time=rt(0.5))

        # ── Physical interpretation: three cases ──────────────────────────────
        table_data = [
            (r"\rho = 0",                r"v = v_{\max}",  GREEN,  "Empty road — drivers travel at free-flow speed"),
            (r"0 < \rho < \rho_{\max}",  r"v \downarrow",  YELLOW, "More vehicles — average speed gradually decreases"),
            (r"\rho = \rho_{\max}",      r"v = 0",         RED,    "Jam density — traffic can no longer move"),
        ]

        rows = VGroup()
        for rho_str, v_str, col, desc_str in table_data:
            rho_tex  = MathTex(rho_str,           font_size=27)
            arr_sym  = MathTex(r"\Rightarrow",     font_size=27, color="#555555")
            v_tex    = MathTex(v_str,              font_size=27, color=col)
            desc_txt = Text(desc_str,              font_size=19, color="#cccccc")
            row = VGroup(rho_tex, arr_sym, v_tex, desc_txt).arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        rows.next_to(key_eq, DOWN, buff=0.48)

        with self.voiceover(
            "When the road is empty, drivers can travel at the free-flow speed. "
            "As vehicles begin to enter the road, average speed gradually decreases. "
            "Eventually, when the road reaches the jam density, "
            "traffic can no longer move. "
            "The average velocity becomes zero."
        ):
            for row in rows:
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=rt(0.65))
                self.wait(rt(0.18))

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(rel_title, key_eq, rows)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 6. WHY THIS MATTERS
        # ─────────────────────────────────────────────────────────────────────
        matters_title = Text("Why This Matters",
                             font_size=36, weight=BOLD, color=WHITE)
        matters_title.to_edge(UP).shift(DOWN * 0.62)

        matters_lines = VGroup(
            Text(
                "This relationship is one of the most important assumptions\n"
                "in traffic flow theory.",
                font_size=24, color="#cccccc", line_spacing=1.4,
            ),
            MathTex(
                r"\text{Once } \rho \text{ is known,} \quad v = v(\rho) "
                r"\text{ follows automatically.}",
                font_size=28, color=YELLOW,
            ),
            Text(
                "An entire traffic stream can be described\n"
                "using only one unknown quantity: the traffic density ρ.",
                font_size=24, color="#cccccc", line_spacing=1.4,
            ),
        ).arrange(DOWN, buff=0.50)
        matters_lines.center().shift(DOWN * 0.15)

        with self.voiceover(
            "This relationship between density and velocity "
            "is one of the most important assumptions in traffic flow theory. "
            "It allows us to describe an entire traffic stream "
            "using only one unknown quantity: the traffic density. "
            "Once the density is known at every location and every moment, "
            "the velocity follows automatically. "
            "This is what makes the LWR model mathematically tractable."
        ):
            self.play(FadeIn(matters_title), run_time=rt(0.6))
            for item in matters_lines:
                self.play(FadeIn(item, shift=UP * 0.1), run_time=rt(0.7))
                self.wait(rt(0.2))

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(matters_title, matters_lines)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 7. TRANSITION TO SCENE 4 — TRAFFIC FLOW
        # ─────────────────────────────────────────────────────────────────────
        preview_title = Text("Next: Traffic Flow  q",
                             font_size=36, weight=BOLD, color=WHITE)
        flow_eq  = MathTex(r"q \;=\; \rho \cdot v(\rho)", font_size=52, color=YELLOW)
        flow_desc = Text(
            "How many vehicles pass a point on the road every second?",
            font_size=24, color="#8899cc",
        )

        preview_title.center().shift(UP * 1.5)
        flow_eq.next_to(preview_title, DOWN, buff=0.45)
        flow_desc.next_to(flow_eq, DOWN, buff=0.38)

        with self.voiceover(
            "We now understand two fundamental quantities: "
            "how many vehicles occupy the road, "
            "and how fast they are moving. "
            "The next question is: "
            "how many vehicles pass a point on the road every second? "
            "That quantity is called traffic flow, "
            "and it combines both density and velocity into a single measure. "
            "Let us see how."
        ):
            self.play(Write(preview_title), run_time=rt(0.9))
            self.play(Write(flow_eq),       run_time=rt(0.9))
            self.play(FadeIn(flow_desc, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(preview_title, flow_eq, flow_desc)), run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene03_TrafficVelocity",
    ])
