from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 4 — TRAFFIC FLOW
#  Render: manim -pql scene04_traffic_flow.py Scene04_TrafficFlow
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene04_TrafficFlow(VoiceoverScene):

    BG_COLOR  = "#0d1117"
    ASPHALT   = "#1e1e1e"
    GRASS_COL = "#1a3320"
    CAR_COLORS = [
        "#4a90e2", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#e67e22", "#5dade2",
    ]

    def _make_car(self, color: str, x: float, y: float) -> SVGMobject:
        car = self._car_template.copy()
        car[0].set_fill(color, opacity=1)
        car.move_to([x, y, 0])
        return car

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT I · Scene 4 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        self._car_template = SVGMobject("car.svg")
        self._car_template.height = 0.32

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE — CONNECT TO SCENES 2 AND 3
        # ─────────────────────────────────────────────────────────────────────
        title = Text("Traffic Flow", font_size=54, weight=BOLD, color=WHITE)
        sub   = Text("The third fundamental variable", font_size=28, color="#8899cc")
        sub.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            "In the previous scenes, we introduced two important quantities. "
            "Traffic density tells us how many vehicles occupy the road. "
            "Traffic velocity tells us how fast those vehicles are moving. "
            "But transportation engineers are usually interested in answering a different question. "
            "How many vehicles can actually pass through a point on the road?"
        ):
            self.play(Write(title), run_time=rt(1.4))
            self.play(FadeIn(sub, shift=UP * 0.15), run_time=rt(0.8))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(title, sub)), run_time=rt(0.6))

        # ─────────────────────────────────────────────────────────────────────
        # 2. DEFINITION — EVERYDAY MOTIVATION + NOTATION + UNITS
        # ─────────────────────────────────────────────────────────────────────
        def_title = Text("Traffic Flow  q",
                         font_size=38, weight=BOLD, color=YELLOW)
        def_title.to_edge(UP).shift(DOWN * 0.62)

        eq_def = MathTex(
            r"q(x,\,t)",
            r"=\; \text{number of vehicles crossing position }x"
            r"\text{ per unit time at time }t",
            font_size=27,
        )
        eq_def[0].set_color(YELLOW)
        eq_def.center().shift(UP * 0.6)

        units_line = MathTex(r"\text{Units: vehicles per hour \;\;(veh/h)}",
                             font_size=26, color="#aaaaaa")
        units_line.next_to(eq_def, DOWN, buff=0.50)

        with self.voiceover(
            "Imagine standing beside a highway with a stopwatch. "
            "Every time a vehicle passes in front of you, you count it. "
            "After one hour, you stop counting. "
            "The total number of vehicles that passed your position "
            "tells you something extremely useful: how busy that road is. "
            "This quantity is called traffic flow. "
            "Traffic flow measures the number of vehicles "
            "passing a fixed point during a given period of time. "
            "Unlike density, which looks at how many vehicles are on the road, "
            "traffic flow measures how many vehicles move through the road."
        ):
            self.play(FadeIn(def_title), run_time=rt(0.6))
            self.play(Write(eq_def), run_time=rt(1.5))
            self.play(FadeIn(units_line), run_time=rt(0.5))

        self.wait(rt(0.4))

        note_line = Text(
            "Also called traffic flux  —  the same q that appears in the LWR conservation law",
            font_size=21, color="#8899cc",
        )
        note_line.next_to(units_line, DOWN, buff=0.38)

        with self.voiceover(
            "We represent traffic flow using the symbol q of x and t. "
            "Just like density and velocity, "
            "traffic flow can vary from one location to another "
            "and change with time. "
            "Since we are counting vehicles crossing a point, "
            "the units are naturally expressed as vehicles per hour, "
            "or vehicles per second, depending on the application. "
            "In the LWR model, traffic flow is also called the flux — "
            "it is the q that appears directly in the conservation equation."
        ):
            self.play(FadeIn(note_line, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(0.6))
        self.play(FadeOut(VGroup(def_title, eq_def, units_line, note_line)),
                  run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 3. DERIVATION: q = ρ · v
        # ─────────────────────────────────────────────────────────────────────
        RY, RH, RW = -2.5, 1.2, 14.0

        road_rect = Rectangle(
            width=RW, height=RH,
            fill_color=self.ASPHALT, fill_opacity=1, stroke_width=0,
        ).move_to([0, RY, 0])
        grass_t = Rectangle(width=RW, height=3, fill_color=self.GRASS_COL,
                            fill_opacity=1, stroke_width=0
                            ).next_to(road_rect, UP, buff=0)
        grass_b = Rectangle(width=RW, height=3, fill_color=self.GRASS_COL,
                            fill_opacity=1, stroke_width=0
                            ).next_to(road_rect, DOWN, buff=0)
        top_edge = Line(LEFT * RW / 2, RIGHT * RW / 2, color=WHITE, stroke_width=2
                        ).move_to([0, RY + RH / 2, 0])
        bot_edge = Line(LEFT * RW / 2, RIGHT * RW / 2, color=WHITE, stroke_width=2
                        ).move_to([0, RY - RH / 2, 0])
        highway = VGroup(grass_b, grass_t, road_rect, top_edge, bot_edge)

        OBS_X = 2.0
        obs_line = DashedLine(
            start=[OBS_X, RY - RH / 2, 0],
            end=[OBS_X,   RY + RH / 2, 0],
            color=YELLOW, stroke_width=2.5, dash_length=0.18,
        )
        obs_lbl = Text("Observer", font_size=17, color=YELLOW)
        obs_lbl.next_to(obs_line, UP, buff=0.10)

        SEG_X0 = -4.0
        seg_cx  = (SEG_X0 + OBS_X) / 2
        seg_hl  = Rectangle(
            width=OBS_X - SEG_X0, height=RH,
            fill_color="#1a4a00", fill_opacity=0.55,
            stroke_color="#66cc33", stroke_width=1.5,
        ).move_to([seg_cx, RY, 0])

        arr_y  = RY + RH / 2 + 0.50
        seg_arr = DoubleArrow(
            start=[SEG_X0, arr_y, 0], end=[OBS_X, arr_y, 0],
            color="#66cc33", stroke_width=2.0, buff=0,
            max_tip_length_to_length_ratio=0.09,
        )
        seg_tex = MathTex(r"v \cdot \Delta t", font_size=26, color="#66cc33")
        seg_tex.next_to(seg_arr, UP, buff=0.12)

        cars_d = VGroup(*[
            self._make_car(self.CAR_COLORS[i], x=-3.4 + i * 1.2, y=RY)
            for i in range(5)
        ])

        sec_lbl = Text("The Observer Approach",
                       font_size=30, weight=BOLD, color=WHITE)
        sec_lbl.to_edge(UP).shift(DOWN * 0.52)

        # ── Block A: question + observer + why the green region ───────────────
        with self.voiceover(
            "Now comes an important question. "
            "What determines traffic flow? "
            "Can it be calculated using the quantities we already know? "
            "Imagine placing an observer beside the road. "
            "The observer remains completely stationary. "
            "Over a short period of time, "
            "every vehicle that reaches the observer is counted. "
            "During a small time interval, "
            "only vehicles that are close enough can actually reach the observer. "
            "Any vehicle outside this highlighted region simply cannot arrive in time. "
            "Therefore, every vehicle that crosses the observer "
            "must have started inside this section of road."
        ):
            self.play(FadeIn(sec_lbl), FadeIn(highway), run_time=rt(0.9))
            self.play(Create(obs_line), FadeIn(obs_lbl), run_time=rt(0.7))
            self.play(FadeIn(seg_hl), run_time=rt(0.5))

        # ── Block B: v·Δt — why that length, then cars appear ─────────────────
        with self.voiceover(
            "Suppose every vehicle is travelling at a speed of v. "
            "In a time interval of delta t, "
            "each vehicle travels a distance equal to speed multiplied by time. "
            "Therefore, every vehicle located within a distance v times delta t "
            "will reach the observer before the interval ends. "
            "That is exactly the length of the highlighted region."
        ):
            self.play(Create(seg_arr), FadeIn(seg_tex), run_time=rt(0.6))
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in cars_d], lag_ratio=0.1),
                run_time=rt(1.1),
            )

        # ── Block C: count vehicles + derivation + why divide by time ─────────
        deriv_lines = VGroup(
            MathTex(
                r"\text{vehicles in region} = \rho \cdot v \cdot \Delta t",
                font_size=27,
            ),
            MathTex(
                r"\therefore\; q \;=\; \frac{\rho \cdot v \cdot \Delta t}{\Delta t}"
                r"\;=\; \rho \cdot v",
                font_size=30, color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.38)
        deriv_lines.to_edge(UP).shift(DOWN * 0.72)

        with self.voiceover(
            "We already know that traffic density tells us "
            "the number of vehicles per unit length. "
            "Therefore, the total number of vehicles inside this region "
            "is simply density multiplied by the length of the region. "
            "The length is v times delta t, "
            "so the number of vehicles is rho times v times delta t. "
            "But remember — "
            "traffic flow is not the number of vehicles. "
            "Traffic flow is the number of vehicles per unit time. "
            "Therefore, we divide by the time interval delta t. "
            "Delta t cancels, and we are left with: "
            "q equals rho times v."
        ):
            self.play(
                VGroup(cars_d).animate.shift(RIGHT * 6.2),
                run_time=rt(2.2), rate_func=linear,
            )
            self.play(
                FadeOut(VGroup(sec_lbl, seg_hl, seg_arr, seg_tex)),
                run_time=rt(0.5),
            )
            self.play(Write(deriv_lines), run_time=rt(1.1))

        self.wait(rt(0.7))
        self.play(
            FadeOut(VGroup(deriv_lines, highway, obs_line, obs_lbl, cars_d)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 4. FORMULA HIGHLIGHT — MEANING AND PHYSICAL INTERPRETATION
        # ─────────────────────────────────────────────────────────────────────
        box_title = Text("The Fundamental Formula",
                         font_size=34, weight=BOLD, color=WHITE)
        box_title.to_edge(UP).shift(DOWN * 0.62)

        big_eq = MathTex(r"q \;=\; \rho \cdot v(\rho)", font_size=72, color=YELLOW)
        big_eq.center()

        unit_rows = VGroup(
            VGroup(MathTex(r"q",    font_size=26, color=YELLOW),
                   Text("  →  vehicles / hour", font_size=21, color="#cccccc")
                   ).arrange(RIGHT),
            VGroup(MathTex(r"\rho", font_size=26, color="#4a90e2"),
                   Text("  →  vehicles / km",   font_size=21, color="#cccccc")
                   ).arrange(RIGHT),
            VGroup(MathTex(r"v",    font_size=26, color="#2ecc71"),
                   Text("  →  km / h",           font_size=21, color="#cccccc")
                   ).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        unit_rows.next_to(big_eq, DOWN, buff=0.50)

        with self.voiceover(
            "Traffic flow equals density multiplied by velocity. "
            "This equation is surprisingly simple. "
            "Yet it captures an important physical idea. "
            "Traffic flow depends on two things. "
            "How many vehicles are available to move. "
            "And how fast those vehicles are moving. "
            "Both are equally important. "
            "A road with many slow-moving vehicles "
            "can carry the same flow as a road with fewer faster-moving vehicles."
        ):
            self.play(FadeIn(box_title), run_time=rt(0.6))
            self.play(Write(big_eq), run_time=rt(1.0))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in unit_rows],
                            lag_ratio=0.25),
                run_time=rt(0.9),
            )

        self.wait(rt(0.8))
        self.play(FadeOut(VGroup(box_title, big_eq, unit_rows)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 5. EXTREME CASES + THE BIG SURPRISE
        # ─────────────────────────────────────────────────────────────────────
        ext_title = Text("Does This Agree With Common Sense?",
                         font_size=32, weight=BOLD, color=WHITE)
        ext_title.to_edge(UP).shift(DOWN * 0.58)

        cases_data = [
            (r"\rho = 0 \;\Rightarrow\; q = \rho \cdot v = 0",
             GREEN, "No vehicles on road — nothing can pass the observer."),
            (r"\rho = \rho_{\max} \;\Rightarrow\; v = 0 \;\Rightarrow\;"
             r" q = \rho_{\max} \cdot 0 = 0",
             RED, "Gridlock — vehicles present but velocity is zero, so flow is zero."),
        ]

        case_rows = VGroup()
        for tex_str, col, note_str in cases_data:
            tex  = MathTex(tex_str, font_size=29, color=col)
            note = Text(note_str, font_size=19, color="#aaaaaa")
            case_rows.add(VGroup(tex, note).arrange(DOWN, aligned_edge=LEFT, buff=0.18))
        case_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        case_rows.center().shift(UP * 0.6)

        insight = MathTex(
            r"\text{Maximum flow } q_{\max} \text{ occurs at some intermediate density } \rho^*",
            font_size=27, color=YELLOW,
        )
        insight.next_to(case_rows, DOWN, buff=0.52)

        # Block A: empty road case
        with self.voiceover(
            "Let us test this equation. "
            "Does it agree with common sense? "
            "If there are no vehicles on the road, "
            "then no vehicles can pass the observer. "
            "Therefore, the traffic flow must be zero. "
            "And indeed — zero density gives zero flow."
        ):
            self.play(FadeIn(ext_title), run_time=rt(0.6))
            self.play(FadeIn(case_rows[0], shift=RIGHT * 0.2), run_time=rt(0.8))

        self.wait(rt(0.4))

        # Block B: gridlock case
        with self.voiceover(
            "Now imagine the opposite situation. "
            "The road is completely full. "
            "Vehicles are packed bumper-to-bumper. "
            "Although many vehicles are present, they cannot move. "
            "Their velocity becomes zero. "
            "Consequently, the traffic flow is once again zero."
        ):
            self.play(FadeIn(case_rows[1], shift=RIGHT * 0.2), run_time=rt(0.8))

        self.wait(rt(0.5))

        # Block C: the big surprise — maximum flow exists between the extremes
        with self.voiceover(
            "This leads to an interesting conclusion. "
            "Flow is zero when there are too few vehicles. "
            "Flow is also zero when there are too many vehicles. "
            "Therefore, somewhere between these two extremes, "
            "there must be a traffic density "
            "that produces the maximum possible flow. "
            "That maximum is the road's capacity — "
            "the peak throughput the road can carry. "
            "Finding exactly where that maximum occurs "
            "is what determines how roads should be designed and managed."
        ):
            self.play(Write(insight), run_time=rt(0.9))

        self.wait(rt(0.9))
        self.play(FadeOut(VGroup(ext_title, case_rows, insight)), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 6. TRANSITION TO GREENSHIELDS
        # ─────────────────────────────────────────────────────────────────────
        prev_title = Text("Next: The Greenshields Model",
                          font_size=36, weight=BOLD, color=WHITE)
        prev_eq    = MathTex(
            r"v(\rho) = v_{\max}\!\left(1 - \frac{\rho}{\rho_{\max}}\right)",
            font_size=46, color=YELLOW,
        )
        prev_desc  = Text(
            "An explicit formula for v(ρ)  →  everything else follows",
            font_size=24, color="#8899cc",
        )

        prev_title.center().shift(UP * 1.6)
        prev_eq.next_to(prev_title, DOWN, buff=0.45)
        prev_desc.next_to(prev_eq, DOWN, buff=0.38)

        with self.voiceover(
            "Up to this point, we know that flow depends on both density and velocity. "
            "But we still do not know exactly how velocity changes with density. "
            "To answer that question, "
            "we introduce one of the earliest and most influential models "
            "in traffic flow theory: "
            "the Greenshields model."
        ):
            self.play(Write(prev_title),      run_time=rt(0.9))
            self.play(Write(prev_eq),         run_time=rt(1.1))
            self.play(FadeIn(prev_desc, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(prev_title, prev_eq, prev_desc)), run_time=rt(0.8))
        self.wait(rt(0.3))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene04_TrafficFlow",
    ])
