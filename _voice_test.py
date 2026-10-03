from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class VoiceTest(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        t = Text("Traffic Density", font_size=48, color=WHITE)
        with self.voiceover("Traffic density measures the number of vehicles per unit length of road."):
            self.play(Write(t))
        self.wait(1)
