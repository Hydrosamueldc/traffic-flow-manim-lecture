from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 2 — TRAFFIC DENSITY  (with voice narration)
#  Render: manim -pql scene02_traffic_density.py Scene02_TrafficDensity
#
#  Voice: Google TTS (gTTS) — free, requires internet on first render.
#         Audio is cached in media/voiceovers/ — subsequent renders are offline.
#  SVG car: car.svg must be in the same folder.
# ══════════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ANIMATION SPEED — change this number freely                            │
# │  1.0 = normal · 1.5 = 50% faster · 2.0 = double speed                 │
# │  (For voice speed, use your video player — VLC: ] key speeds up)       │
# └─────────────────────────────────────────────────────────────────────────┘
ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    """Scale a run_time value by ANIM_SPEED."""
    return seconds / ANIM_SPEED


class Scene02_TrafficDensity(VoiceoverScene):

    # ── palette ───────────────────────────────────────────────────────────────
    BG_COLOR  = "#0d1117"
    ASPHALT   = "#1e1e1e"
    LANE_MARK = "#f5c518"

    LOW_COL  = "#2ecc71"
    MED_COL  = "#f39c12"
    HIGH_COL = "#e74c3c"

    PAL_LOW  = ["#27ae60", "#1abc9c", "#27ae60", "#1abc9c"]
    PAL_MED  = ["#e67e22", "#f39c12", "#f1c40f", "#e67e22",
                "#f39c12", "#f1c40f", "#e67e22", "#f39c12"]
    PAL_HIGH = ["#e74c3c", "#c0392b"] * 8

    # ── road geometry ─────────────────────────────────────────────────────────
    ROAD_Y = -1.0
    ROAD_H =  1.8
    ROAD_W = 13.0
    SEG_X1 = -5.0
    SEG_X2 =  5.0

    # ── lane helpers ──────────────────────────────────────────────────────────

    def _upper_lane_y(self): return self.ROAD_Y + self.ROAD_H * 0.25

    def _lower_lane_y(self): return self.ROAD_Y - self.ROAD_H * 0.25

    # ── factories ─────────────────────────────────────────────────────────────

    def _make_car(self, color: str, x: float, lane: str = "upper") -> SVGMobject:
        y   = self._upper_lane_y() if lane == "upper" else self._lower_lane_y()
        car = self._car_template.copy()
        car[0].set_fill(color, opacity=1)
        car.move_to([x, y, 0])
        return car

    def _make_road(self) -> VGroup:
        road = Rectangle(
            width=self.ROAD_W, height=self.ROAD_H,
            fill_color=self.ASPHALT, fill_opacity=1, stroke_width=0,
        ).move_to([0, self.ROAD_Y, 0])

        top_e = Line(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                     color=WHITE, stroke_width=2)
        top_e.move_to([0, self.ROAD_Y + self.ROAD_H / 2, 0])

        bot_e = Line(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                     color=WHITE, stroke_width=2)
        bot_e.move_to([0, self.ROAD_Y - self.ROAD_H / 2, 0])

        centre = DashedLine(
            LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
            dash_length=0.40, dashed_ratio=0.45,
            color=self.LANE_MARK, stroke_width=1.5,
        ).move_to([0, self.ROAD_Y, 0])

        return VGroup(road, top_e, bot_e, centre)

    def _make_markers(self) -> VGroup:
        y_top = self.ROAD_Y + self.ROAD_H / 2
        y_bot = self.ROAD_Y - self.ROAD_H / 2

        m_left = DashedLine(
            [self.SEG_X1, y_bot - 0.45, 0], [self.SEG_X1, y_top + 0.25, 0],
            color=YELLOW, dash_length=0.13, dashed_ratio=0.5, stroke_width=2,
        )
        m_right = DashedLine(
            [self.SEG_X2, y_bot - 0.45, 0], [self.SEG_X2, y_top + 0.25, 0],
            color=YELLOW, dash_length=0.13, dashed_ratio=0.5, stroke_width=2,
        )
        arr = DoubleArrow(
            [self.SEG_X1, y_bot - 0.38, 0],
            [self.SEG_X2, y_bot - 0.38, 0],
            color=YELLOW, stroke_width=1.5, tip_length=0.13, buff=0,
        )
        L_lbl = Text("L  (unit length)", font_size=20, color=YELLOW)
        L_lbl.next_to(arr, DOWN, buff=0.10)

        return VGroup(m_left, m_right, arr, L_lbl)

    def _swap_rho(self, old_mob, new_text: str, color, row_shift: float):
        new_mob = Text(new_text, font_size=30, weight=BOLD, color=color)
        new_mob.to_edge(UP).shift(DOWN * row_shift)
        self.play(FadeOut(old_mob, run_time=0.3), FadeIn(new_mob, run_time=0.3))
        return new_mob

    # ── construct ─────────────────────────────────────────────────────────────

    def construct(self):
        self.camera.background_color = self.BG_COLOR

        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT I · Scene 2 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        # SVG car template loaded once; _make_car copies cheaply
        self._car_template = SVGMobject("car.svg")
        self._car_template.height = 0.34

        ROW1 = 0.50   # phase label row
        ROW2 = 1.20   # density counter row

        # ─────────────────────────────────────────────────────────────────────
        # 1. TITLE + DEFINITION
        # ─────────────────────────────────────────────────────────────────────
        title    = Text("Traffic Density", font_size=52, weight=BOLD, color=WHITE)
        rho_sym  = MathTex(r"\rho", font_size=72, color="#4a90e2")
        rho_name = Text("(rho)", font_size=26, color="#7788aa")
        rho_sym.next_to(title, RIGHT, buff=0.38)
        rho_name.next_to(rho_sym, RIGHT, buff=0.18)
        header = VGroup(title, rho_sym, rho_name).center()

        defn = Text(
            "The number of vehicles per unit length of road",
            font_size=27, color="#aaaacc",
        )
        defn.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
            "In the previous scene, we saw that traffic can exist in different states. "
            "Sometimes vehicles move freely, sometimes they slow down, "
            "and sometimes they come to a complete stop. "
            "But how do we describe these different traffic conditions mathematically? "
            "Before we can build any mathematical model, "
            "we first need a way to measure how crowded a road is. "
            "That measurement is called traffic density, "
            "and it is the most fundamental quantity in the LWR traffic flow model. "
            "Everything else we will study in this project is built upon this single idea."
        ):
            self.play(Write(title), run_time=1.2)
            self.play(FadeIn(VGroup(rho_sym, rho_name), shift=LEFT * 0.15))
            self.play(FadeIn(defn, shift=UP * 0.12))

        self.wait(0.5)
        self.play(FadeOut(VGroup(header, defn)), run_time=0.7)

        # ─────────────────────────────────────────────────────────────────────
        # 2. ROAD SEGMENT + MARKERS
        # ─────────────────────────────────────────────────────────────────────
        road    = self._make_road()
        markers = self._make_markers()

        with self.voiceover(
            "Imagine selecting a small section of road. "
            "We do not need to observe the entire highway. "
            "Instead, we focus on a fixed segment with a known length, "
            "which we will denote by L. "
            "Our question is simple: "
            "how many vehicles occupy this section of road at this particular moment? "
            "If we can answer that question, we have a way to measure how crowded the road is."
        ):
            self.play(FadeIn(road), run_time=0.7)
            self.play(Create(markers), run_time=1.0)

        rho_display = Text("ρ  =  —", font_size=30, color=GREY_B)
        rho_display.to_edge(UP).shift(DOWN * ROW2)
        self.play(FadeIn(rho_display))

        # ─────────────────────────────────────────────────────────────────────
        # 3A. LOW DENSITY
        # ─────────────────────────────────────────────────────────────────────
        phase_lbl = Text("Low Density", font_size=38, weight=BOLD, color=self.LOW_COL)
        phase_lbl.to_edge(UP).shift(DOWN * ROW1)

        low_slots = [(-4.0, "upper"), (-1.5, "lower"), (1.5, "upper"), (4.0, "lower")]
        low_cars  = VGroup(*[
            self._make_car(self.PAL_LOW[i], x, lane)
            for i, (x, lane) in enumerate(low_slots)
        ])

        info_low = Text(
            "Large spacing  ·  Vehicles travel freely  ·  ρ is small",
            font_size=22, color="#888888",
        )
        info_low.to_edge(DOWN).shift(UP * 0.42)

        with self.voiceover(
            "Here, only four vehicles occupy the entire road segment. "
            "The spacing between vehicles is large. "
            "Each driver has plenty of room to move "
            "without being influenced by the vehicle ahead. "
            "We therefore describe this as low traffic density."
        ):
            self.play(
                Write(phase_lbl, run_time=0.8),
                LaggedStart(*[FadeIn(c, scale=0.85) for c in low_cars],
                            lag_ratio=0.20, run_time=1.3),
            )
            rho_display = self._swap_rho(rho_display, "ρ  =  4 veh / L", self.LOW_COL, ROW2)
            self.play(FadeIn(info_low))

        self.wait(0.8)
        self.play(FadeOut(VGroup(phase_lbl, low_cars, info_low)))

        # ─────────────────────────────────────────────────────────────────────
        # 3B. MEDIUM DENSITY
        # ─────────────────────────────────────────────────────────────────────
        phase_lbl2 = Text("Medium Density", font_size=38, weight=BOLD, color=self.MED_COL)
        phase_lbl2.to_edge(UP).shift(DOWN * ROW1)

        med_xs   = [-4.2, -2.9, -1.6, -0.3, 1.0, 2.3, 3.6, 4.9]
        med_cars = VGroup(*[
            self._make_car(self.PAL_MED[i], x, "upper" if i % 2 == 0 else "lower")
            for i, x in enumerate(med_xs)
        ])

        info_med = Text(
            "Moderate spacing  ·  Speed begins to fall  ·  ρ ≈ ρ_jam / 2",
            font_size=22, color="#888888",
        )
        info_med.to_edge(DOWN).shift(UP * 0.42)

        with self.voiceover(
            "Now more vehicles enter the same road segment. "
            "The available space between vehicles becomes smaller. "
            "Drivers begin paying closer attention to the vehicle in front of them. "
            "At this stage, even a small change in speed "
            "can influence the surrounding traffic. "
            "We call this medium traffic density. "
            "Notice that the road itself has not changed — "
            "the length remains exactly the same. "
            "The only thing changing is the number of vehicles occupying that space."
        ):
            self.play(
                Write(phase_lbl2, run_time=0.8),
                LaggedStart(*[FadeIn(c, scale=0.85) for c in med_cars],
                            lag_ratio=0.10, run_time=1.3),
            )
            rho_display = self._swap_rho(rho_display, "ρ  =  8 veh / L", self.MED_COL, ROW2)
            self.play(FadeIn(info_med))

        self.wait(0.8)
        self.play(FadeOut(VGroup(phase_lbl2, med_cars, info_med)))

        # ─────────────────────────────────────────────────────────────────────
        # 3C. HIGH DENSITY
        # ─────────────────────────────────────────────────────────────────────
        phase_lbl3 = Text("High Density", font_size=38, weight=BOLD, color=self.HIGH_COL)
        phase_lbl3.to_edge(UP).shift(DOWN * ROW1)

        n_hi    = 15
        hi_xs   = [
            self.SEG_X1 + 0.4 + i * (self.SEG_X2 - self.SEG_X1 - 0.8) / (n_hi - 1)
            for i in range(n_hi)
        ]
        hi_cars = VGroup(*[
            self._make_car(self.PAL_HIGH[i], x, "upper" if i % 2 == 0 else "lower")
            for i, x in enumerate(hi_xs)
        ])

        info_hi = Text(
            "Minimal spacing  ·  Near standstill  ·  ρ approaching ρ_jam",
            font_size=22, color="#888888",
        )
        info_hi.to_edge(DOWN).shift(UP * 0.42)

        with self.voiceover(
            "Finally, even more vehicles occupy exactly the same section of road. "
            "The spacing becomes extremely small. "
            "Vehicles are almost bumper-to-bumper. "
            "Drivers have very little freedom to choose their own speed. "
            "This is called high traffic density. "
            "If even more vehicles attempt to enter the road, "
            "movement eventually becomes impossible."
        ):
            self.play(
                Write(phase_lbl3, run_time=0.8),
                LaggedStart(*[FadeIn(c, scale=0.85) for c in hi_cars],
                            lag_ratio=0.05, run_time=1.5),
            )
            rho_display = self._swap_rho(rho_display, "ρ  =  15 veh / L", self.HIGH_COL, ROW2)
            self.play(FadeIn(info_hi))

        self.wait(0.8)
        self.play(FadeOut(VGroup(phase_lbl3, hi_cars, info_hi)))

        # ─────────────────────────────────────────────────────────────────────
        # 4. FORMAL DEFINITION
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(VGroup(road, markers, rho_display)), run_time=0.7)

        defn_title = Text(
            "Formal Definition of Density",
            font_size=40, weight=BOLD, color=WHITE,
        )
        defn_title.to_edge(UP).shift(DOWN * 0.55)

        formula = MathTex(
            r"\rho(x,\,t) \;=\; \lim_{\Delta x \,\to\, 0}"
            r"\frac{N\!\left(x,\; x{+}\Delta x,\; t\right)}{\Delta x}",
            font_size=40,
        )
        formula.center().shift(UP * 0.55)

        var_rows = VGroup(
            Text("x  →  position along the road",          font_size=23, color="#aaaaaa"),
            Text("t  →  time",                              font_size=23, color="#aaaaaa"),
            Text("N  →  vehicle count in  [x,  x + Δx]",   font_size=23, color="#aaaaaa"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        var_rows.next_to(formula, DOWN, buff=0.50)

        range_txt = Text(
            "0   ≤   ρ   ≤   ρ_jam",
            font_size=34, weight=BOLD, color=YELLOW,
        )
        range_txt.next_to(var_rows, DOWN, buff=0.45)

        sub_range = Text(
            "ρ = 0  →  empty road          ρ = ρ_jam  →  gridlock",
            font_size=22, color="#888888",
        )
        sub_range.next_to(range_txt, DOWN, buff=0.25)

        with self.voiceover(
            "So far, we have described traffic qualitatively. "
            "To build a mathematical model, we need a precise numerical definition. "
            "Mathematically, traffic density measures the number of vehicles "
            "contained within a very small section of road. "
            "As the length of that section becomes infinitesimally small, "
            "we obtain a continuous quantity called the traffic density field. "
            "In this expression, "
            "x represents the position along the road, "
            "t represents time, "
            "and N represents the number of vehicles contained inside a small interval of road. "
            "Dividing the number of vehicles by the length of that interval "
            "gives the density at that location. "
            "Repeating this process everywhere along the highway "
            "produces a continuous description of traffic."
        ):
            self.play(FadeIn(defn_title))
            self.play(Write(formula), run_time=1.6)
            for row in var_rows:
                self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.45)

        with self.voiceover(
            "At first, this may seem unusual. "
            "After all, vehicles are individual objects. "
            "Cars are not a continuous fluid like water. "
            "However, when thousands of vehicles occupy a highway, "
            "tracking every single car becomes extremely difficult. "
            "Instead, we observe the overall behaviour of the traffic stream. "
            "In much the same way that fluid mechanics studies the motion of water "
            "without tracking every molecule, "
            "traffic flow theory studies the collective behaviour of vehicles "
            "by treating traffic as a continuous medium. "
            "This idea is known as the continuum assumption, "
            "and it forms the mathematical foundation of the LWR traffic flow model. "
            "Density cannot become negative. "
            "A density of zero represents an empty road. "
            "As more vehicles enter the road, the density increases. "
            "Eventually the road reaches its maximum possible density, "
            "known as the jam density. "
            "At this point, vehicles are packed as closely as physically possible, "
            "and traffic movement nearly stops."
        ):
            self.play(FadeIn(range_txt))
            self.play(FadeIn(sub_range))
            self.wait(1.5)

        self.play(
            FadeOut(VGroup(defn_title, formula, var_rows, range_txt, sub_range)),
            run_time=0.8,
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. CLOSING — LEAD INTO SCENE 3
        # ─────────────────────────────────────────────────────────────────────
        next_title = Text("Next: Traffic Velocity",
                          font_size=38, weight=BOLD, color=WHITE)
        next_eq = MathTex(r"v(\rho)", font_size=60, color=YELLOW)
        next_desc = Text(
            "How fast are those vehicles actually moving?",
            font_size=24, color="#8899cc",
        )

        next_title.center().shift(UP * 1.6)
        next_eq.next_to(next_title, DOWN, buff=0.45)
        next_desc.next_to(next_eq, DOWN, buff=0.38)

        with self.voiceover(
            "We have now introduced the first variable in the LWR traffic flow model: "
            "traffic density. "
            "Density tells us how crowded the road is. "
            "But knowing how many vehicles are on the road is only part of the story. "
            "We also need to know how fast those vehicles are moving. "
            "In the next scene, we introduce the second fundamental quantity: "
            "traffic velocity."
        ):
            self.play(Write(next_title), run_time=rt(0.9))
            self.play(Write(next_eq), run_time=rt(1.0))
            self.play(FadeIn(next_desc, shift=UP * 0.1), run_time=rt(0.6))

        self.wait(rt(1.5))
        self.play(FadeOut(VGroup(next_title, next_eq, next_desc)), run_time=rt(0.8))
        self.wait(rt(0.4))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene02_TrafficDensity",
    ])
