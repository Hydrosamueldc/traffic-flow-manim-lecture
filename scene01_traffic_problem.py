from manim import *
from manim_voiceover import VoiceoverScene
from edge_tts_service import EdgeTTSService

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 1 — THE TRAFFIC PROBLEM  (with voice narration)
#  Render: manim -pql scene01_traffic_problem.py Scene01_TrafficProblem
# ══════════════════════════════════════════════════════════════════════════════

ANIM_SPEED = 1.4


def rt(seconds: float) -> float:
    return seconds / ANIM_SPEED


class Scene01_TrafficProblem(VoiceoverScene):

    BG_COLOR  = "#0d1117"
    ASPHALT   = "#1e1e1e"
    GRASS_COL = "#1a3320"
    LANE_MARK = "#f5c518"

    CAR_COLORS = [
        "#4a90e2", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#e67e22", "#5dade2",
    ]

    ROAD_Y = -0.5
    ROAD_H = 2.0
    ROAD_W = 17.0

    def _upper_lane_y(self): return self.ROAD_Y + self.ROAD_H * 0.25

    def _lower_lane_y(self): return self.ROAD_Y - self.ROAD_H * 0.25

    def _make_car(self, color: str, x: float, lane: str = "upper") -> SVGMobject:
        y   = self._upper_lane_y() if lane == "upper" else self._lower_lane_y()
        car = self._car_template.copy()
        car[0].set_fill(color, opacity=1)
        car.move_to([x, y, 0])
        return car

    def _make_highway(self) -> VGroup:
        road = Rectangle(
            width=self.ROAD_W, height=self.ROAD_H,
            fill_color=self.ASPHALT, fill_opacity=1, stroke_width=0,
        ).move_to([0, self.ROAD_Y, 0])

        grass_top = Rectangle(width=self.ROAD_W, height=5,
                              fill_color=self.GRASS_COL, fill_opacity=1,
                              stroke_width=0).next_to(road, UP, buff=0)
        grass_bot = Rectangle(width=self.ROAD_W, height=5,
                              fill_color=self.GRASS_COL, fill_opacity=1,
                              stroke_width=0).next_to(road, DOWN, buff=0)

        top_edge = Line(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                        color=WHITE, stroke_width=2.5)
        top_edge.move_to([0, self.ROAD_Y + self.ROAD_H / 2, 0])

        bot_edge = Line(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                        color=WHITE, stroke_width=2.5)
        bot_edge.move_to([0, self.ROAD_Y - self.ROAD_H / 2, 0])

        centre = DashedLine(LEFT * self.ROAD_W / 2, RIGHT * self.ROAD_W / 2,
                            dash_length=0.50, dashed_ratio=0.45,
                            color=self.LANE_MARK, stroke_width=2)
        centre.move_to([0, self.ROAD_Y, 0])

        return VGroup(grass_bot, grass_top, road, top_edge, bot_edge, centre)

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        self.set_speech_service(EdgeTTSService())

        progress_lbl = Text("ACT I · Scene 1 of 16", font_size=16, color="#666677")
        progress_lbl.to_corner(UL, buff=0.22)
        self.add(progress_lbl)

        self._car_template = SVGMobject("car.svg")
        self._car_template.height = 0.36

        # ─────────────────────────────────────────────────────────────────────
        # 1. ACADEMIC TITLE CARD
        # ─────────────────────────────────────────────────────────────────────
        uni_lbl = Text(
            "University of Lagos  ·  Department of Mathematics",
            font_size=20, color="#7788aa",
        )
        uni_lbl.to_edge(UP).shift(DOWN * 0.55)

        proj_line1 = Text(
            "Numerical Simulation of the",
            font_size=36, weight=BOLD, color=WHITE,
        )
        proj_line2 = Text(
            "LWR Traffic Flow Model",
            font_size=46, weight=BOLD, color=YELLOW,
        )
        proj_sub = Text(
            "Using Upwind and Lax-Wendroff Finite Difference Schemes",
            font_size=24, color="#8899cc",
        )
        proj_line1.center().shift(UP * 1.05)
        proj_line2.next_to(proj_line1, DOWN, buff=0.18)
        proj_sub.next_to(proj_line2, DOWN, buff=0.38)

        by_lbl = Text(
            "Adegboyega Samuel  ·  Matric No: 210806134",
            font_size=18, color="#556677",
        )
        by_lbl.to_edge(DOWN).shift(UP * 0.55)

        with self.voiceover(
            "This presentation accompanies a final-year undergraduate project "
            "submitted to the Department of Mathematics at the University of Lagos. "
            "The project numerically simulates the Lighthill-Whitham-Richards traffic flow model "
            "and compares two finite difference methods for solving it — "
            "the Upwind scheme and the Lax-Wendroff scheme. "
            "What follows builds the complete mathematical framework, "
            "step by step, from first principles. "
            "No prior knowledge of traffic theory is assumed."
        ):
            self.play(FadeIn(uni_lbl), run_time=rt(0.6))
            self.play(Write(proj_line1), run_time=rt(0.9))
            self.play(Write(proj_line2), run_time=rt(0.8))
            self.play(FadeIn(proj_sub, shift=UP * 0.12), run_time=rt(0.7))
            self.play(FadeIn(by_lbl), run_time=rt(0.5))

        self.wait(rt(1.0))
        self.play(
            FadeOut(VGroup(uni_lbl, proj_line1, proj_line2, proj_sub, by_lbl)),
            run_time=rt(0.8),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 2. GLOBAL TRAFFIC CONTEXT — THREE SCENARIOS
        # ─────────────────────────────────────────────────────────────────────
        highway = self._make_highway()

        with self.voiceover(
            "Traffic congestion costs the global economy over a trillion dollars every year. "
            "In cities like Lagos, Beijing, and Los Angeles, commuters lose hundreds of hours "
            "sitting in gridlock. Usually there is an obvious cause."
        ):
            self.play(FadeIn(highway), run_time=rt(0.9))

        # ── Scenario A: Accident ─────────────────────────────────────────────
        sc_lbl_a = Text("Scenario 1  —  Road Accident",
                        font_size=30, weight=BOLD, color=RED)
        sc_lbl_a.to_edge(UP).shift(DOWN * 0.45)

        # Collision marker on the road
        x_mark = Text("✕", font_size=60, color=RED, weight=BOLD)
        x_mark.move_to([4.8, self._upper_lane_y(), 0])

        stopped_a = VGroup(*[
            self._make_car(self.CAR_COLORS[i % len(self.CAR_COLORS)],
                           x=-6.5 + i * 0.82, lane="upper")
            for i in range(8)
        ])

        info_a = Text(
            "A collision blocks the road.  The cause is clear.  Clear it and traffic resumes.",
            font_size=21, color="#cccccc",
        )
        info_a.to_edge(DOWN).shift(UP * 0.42)

        with self.voiceover(
            "An accident brings traffic to an immediate standstill. "
            "The cause is visible — a physical obstruction. "
            "Remove the obstruction, and traffic resumes. "
            "Traffic engineers can model and manage this."
        ):
            self.play(FadeIn(sc_lbl_a), Write(x_mark), run_time=rt(0.7))
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in stopped_a],
                            lag_ratio=0.08, run_time=rt(1.0)),
            )
            self.play(FadeIn(info_a, shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(sc_lbl_a, stopped_a, x_mark, info_a)),
                  run_time=rt(0.5))

        # ── Scenario B: Roadworks ────────────────────────────────────────────
        sc_lbl_b = Text("Scenario 2  —  Roadworks",
                        font_size=30, weight=BOLD, color=ORANGE)
        sc_lbl_b.to_edge(UP).shift(DOWN * 0.45)

        cones = VGroup(*[
            Triangle(color=ORANGE, fill_color=ORANGE,
                     fill_opacity=0.9, stroke_width=0)
            .scale(0.22)
            .move_to([x, self._upper_lane_y(), 0])
            for x in [1.6, 2.4, 3.2, 4.0, 4.8]
        ])

        warn_tri = Triangle(color=ORANGE, fill_color="#1c0a00",
                            fill_opacity=1, stroke_width=3).scale(0.42)
        warn_exc = Text("!", font_size=24, color=ORANGE, weight=BOLD)
        warn_exc.move_to(warn_tri.get_center() + DOWN * 0.06)
        warning_grp = VGroup(warn_tri, warn_exc).move_to([3.2, 1.15, 0])

        rw_cars = VGroup(*[
            self._make_car(self.CAR_COLORS[i % len(self.CAR_COLORS)],
                           x=-6.5 + i * 1.05, lane="upper")
            for i in range(6)
        ])

        info_b = Text(
            "A lane closure creates a predictable bottleneck — planned, visible, and manageable.",
            font_size=21, color="#cccccc",
        )
        info_b.to_edge(DOWN).shift(UP * 0.42)

        with self.voiceover(
            "Roadworks narrow the road and create a predictable bottleneck. "
            "Again, the cause is visible. "
            "Schedule it at off-peak hours, add signage, and the disruption is manageable."
        ):
            self.play(FadeIn(sc_lbl_b), FadeIn(cones), FadeIn(warning_grp),
                      run_time=rt(0.7))
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in rw_cars],
                            lag_ratio=0.1, run_time=rt(1.0)),
            )
            self.play(FadeIn(info_b, shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.5))
        self.play(FadeOut(VGroup(sc_lbl_b, cones, warning_grp, rw_cars, info_b)),
                  run_time=rt(0.5))

        # ── Scenario C: Phantom Jam ──────────────────────────────────────────
        sc_lbl_c = Text("Scenario 3  —  No Obvious Cause",
                        font_size=30, weight=BOLD, color=WHITE)
        sc_lbl_c.to_edge(UP).shift(DOWN * 0.45)

        free_cars = VGroup(*[
            self._make_car(self.CAR_COLORS[i % len(self.CAR_COLORS)],
                           x=-7.5 + i * 2.1, lane="upper")
            for i in range(5)
        ])

        q_mark = Text("?", font_size=100, color=RED, weight=BOLD)
        q_mark.move_to([5.0, 0.3, 0])

        info_c = Text(
            "No accident.   No roadworks.   No reason anyone can see.",
            font_size=21, color="#ff8888",
        )
        info_c.to_edge(DOWN).shift(UP * 0.42)

        with self.voiceover(
            "But there is a third kind of traffic jam — and it is the most puzzling. "
            "No accident. No roadworks. The road ahead is completely clear. "
            "Yet traffic grinds to a halt. "
            "Drivers sit for minutes, sometimes much longer. "
            "Then, just as suddenly, everything clears — as though nothing had happened."
        ):
            self.play(FadeIn(sc_lbl_c), run_time=rt(0.5))
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.8) for c in free_cars],
                            lag_ratio=0.12, run_time=rt(1.0)),
            )
            self.play(free_cars.animate.shift(RIGHT * 2.5),
                      run_time=rt(1.8), rate_func=linear)
            self.play(FadeIn(q_mark), run_time=rt(0.4))
            self.play(FadeIn(info_c, shift=UP * 0.1), run_time=rt(0.5))

        self.wait(rt(0.6))
        self.play(
            FadeOut(VGroup(sc_lbl_c, free_cars, q_mark, info_c, highway)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 3. THE QUESTIONS
        # ─────────────────────────────────────────────────────────────────────
        q1 = Text("Where did that jam come from?",
                  font_size=36, weight=BOLD, color=WHITE)
        q2 = Text("How does a traffic jam form with no physical cause?",
                  font_size=28, color="#aaaacc")
        q3 = Text("Can mathematics explain — and predict — this behaviour?",
                  font_size=28, color=YELLOW)

        qs = VGroup(q1, q2, q3).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        qs.center()

        with self.voiceover(
            "These events are called phantom traffic jams. "
            "They are not random, and they are not unexplained. "
            "They are compression waves — disturbances that form spontaneously "
            "in dense traffic and propagate backward against the direction of vehicle motion. "
            "Understanding them mathematically is exactly what this project is about."
        ):
            for q in qs:
                self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=rt(0.65))
                self.wait(rt(0.3))

        self.wait(rt(0.8))
        self.play(FadeOut(qs), run_time=rt(0.7))

        # ─────────────────────────────────────────────────────────────────────
        # 4. PROJECT FRAMING — LWR MODEL + TWO SCHEMES
        # ─────────────────────────────────────────────────────────────────────
        frame_title = Text("In This Project",
                           font_size=40, weight=BOLD, color=WHITE)
        frame_title.to_edge(UP).shift(DOWN * 0.65)

        lwr_tag = Text(
            "The Lighthill–Whitham–Richards (LWR) Model",
            font_size=26, weight=BOLD, color=YELLOW,
        )
        lwr_tag.center().shift(UP * 1.45)

        lwr_eq = MathTex(
            r"\frac{\partial \rho}{\partial t}"
            r"+ \frac{\partial f(\rho)}{\partial x} = 0",
            font_size=54, color=YELLOW,
        )
        lwr_eq.next_to(lwr_tag, DOWN, buff=0.38)

        lwr_note = Text(
            "Traffic density ρ(x, t) modelled as a continuous field — a nonlinear conservation law",
            font_size=20, color="#8899cc",
        )
        lwr_note.next_to(lwr_eq, DOWN, buff=0.32)

        sep = Line(LEFT * 5.0, RIGHT * 5.0, color=GREY_B, stroke_width=1.0)
        sep.next_to(lwr_note, DOWN, buff=0.38)

        schemes_lbl = Text("Two numerical methods are compared:",
                           font_size=21, color="#8899cc")
        schemes_lbl.next_to(sep, DOWN, buff=0.28)

        up_row = VGroup(
            Text("Upwind Scheme", font_size=25, weight=BOLD, color="#4a90e2"),
            Text("  —  first-order, stable, diffusive", font_size=20, color="#aaaaaa"),
        ).arrange(RIGHT, aligned_edge=DOWN)

        lw_row = VGroup(
            Text("Lax-Wendroff Scheme", font_size=25, weight=BOLD, color="#2ecc71"),
            Text("  —  second-order, accurate, dispersive", font_size=20, color="#aaaaaa"),
        ).arrange(RIGHT, aligned_edge=DOWN)

        scheme_rows = VGroup(up_row, lw_row).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        scheme_rows.next_to(schemes_lbl, DOWN, buff=0.26)

        with self.voiceover(
            "In the 1950s, Lighthill, Whitham, and Richards proposed "
            "a model that treats traffic not as a collection of individual vehicles, "
            "but as a continuous fluid. "
            "Vehicle density evolves according to this conservation equation — "
            "a nonlinear hyperbolic PDE. "
            "Because realistic traffic scenarios produce shock waves — "
            "sharp density discontinuities — no closed-form solution exists. "
            "Numerical methods are essential. "
            "This project implements and compares two: "
            "the first-order Upwind scheme, and the second-order Lax-Wendroff scheme."
        ):
            self.play(FadeIn(frame_title), run_time=rt(0.6))
            self.play(FadeIn(lwr_tag), run_time=rt(0.7))
            self.play(Write(lwr_eq), run_time=rt(1.0))
            self.play(FadeIn(lwr_note, shift=UP * 0.1), run_time=rt(0.6))
            self.play(Create(sep), run_time=rt(0.4))
            self.play(FadeIn(schemes_lbl), run_time=rt(0.4))
            self.play(FadeIn(up_row, shift=RIGHT * 0.15), run_time=rt(0.6))
            self.play(FadeIn(lw_row, shift=RIGHT * 0.15), run_time=rt(0.6))

        self.wait(rt(0.8))
        self.play(
            FadeOut(VGroup(frame_title, lwr_tag, lwr_eq, lwr_note,
                           sep, schemes_lbl, scheme_rows)),
            run_time=rt(0.7),
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. ROADMAP CHECKLIST — WHAT THIS PRESENTATION COVERS
        # ─────────────────────────────────────────────────────────────────────
        roadmap_title = Text("What This Presentation Covers",
                             font_size=34, weight=BOLD, color=WHITE)
        roadmap_title.to_edge(UP).shift(DOWN * 0.65)

        topics = [
            ("Traffic Density  ρ",                                  "#4a90e2"),
            ("Traffic Velocity  v",                                 "#4a90e2"),
            ("Traffic Flow  q  =  ρ · v",                          "#4a90e2"),
            ("The Greenshields Speed–Density Model",                "#f39c12"),
            ("The Fundamental Diagram",                             "#f39c12"),
            ("Conservation of Vehicles — the LWR Equation",        "#e74c3c"),
            ("Upwind vs Lax-Wendroff: Simulations & Comparison",   "#2ecc71"),
        ]

        checklist = VGroup()
        for text, color in topics:
            box = Square(side_length=0.26, color="#445566",
                         fill_opacity=0, stroke_width=1.5)
            lbl = Text(text, font_size=22, color=color)
            row = VGroup(box, lbl).arrange(RIGHT, buff=0.30)
            checklist.add(row)

        checklist.arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        checklist.center().shift(DOWN * 0.22)

        with self.voiceover(
            "Here is the structure of what follows. "
            "We begin with the three fundamental traffic variables: density, velocity, and flow. "
            "These are the building blocks of any macroscopic traffic model. "
            "We then introduce the Greenshields model — "
            "an empirical relationship between speed and density. "
            "From it, we derive the fundamental diagram, which governs road capacity. "
            "The conservation of vehicles principle then yields the LWR partial differential equation. "
            "The presentation closes with numerical simulations "
            "and a direct comparison of the two schemes."
        ):
            self.play(FadeIn(roadmap_title), run_time=rt(0.6))
            for item in checklist:
                self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=rt(0.48))
                self.wait(rt(0.08))

        self.wait(rt(1.2))
        self.play(FadeOut(VGroup(roadmap_title, checklist)), run_time=rt(0.8))
        self.wait(rt(0.4))


if __name__ == "__main__":
    import subprocess
    subprocess.run([
        r"C:\Users\PC\anaconda3\python.exe", "-m", "manim", "-pql",
        __file__, "Scene01_TrafficProblem",
    ])
