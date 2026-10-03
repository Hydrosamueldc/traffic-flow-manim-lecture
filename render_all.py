"""
render_all.py  —  render every scene then concatenate into full_lecture.mp4

Usage:
    python render_all.py          # low quality  (480p15)  — fast preview
    python render_all.py -pqm     # medium quality (720p30)
    python render_all.py -pqh     # high quality  (1080p60)

Requirements:
    - manim
    - manim-voiceover
    - edge-tts           (free, no API key — pip install edge-tts)
    - ffmpeg              (must be on PATH)

First run will call the free Edge TTS voice to generate audio for every
voiceover block; subsequent renders reuse the cached audio from
media/voiceovers/, so re-renders after a text-only edit are much faster.
"""

import subprocess
import sys
import os

PYTHON = sys.executable


def resolve_ffmpeg() -> str:
    """Use ffmpeg on PATH if available, otherwise fall back to the copy
    manim already depends on via imageio-ffmpeg (no separate install needed)."""
    from shutil import which
    found = which("ffmpeg")
    if found:
        return found
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


FFMPEG = resolve_ffmpeg()

# ── scene manifest (in order) ──────────────────────────────────────────────────
SCENES = [
    ("scene01_traffic_problem.py",       "Scene01_TrafficProblem"),
    ("scene02_traffic_density.py",       "Scene02_TrafficDensity"),
    ("scene03_traffic_velocity.py",      "Scene03_TrafficVelocity"),
    ("scene04_traffic_flow.py",          "Scene04_TrafficFlow"),
    ("scene05_greenshields.py",          "Scene05_Greenshields"),
    ("scene06_fundamental_diagram.py",   "Scene06_FundamentalDiagram"),
    ("scene07_conservation.py",          "Scene07_Conservation"),
    ("scene08_characteristics.py",       "Scene08_Characteristics"),
    ("scene09_shock_waves.py",           "Scene09_ShockWaves"),
    ("scene10_rarefaction.py",           "Scene10_Rarefaction"),
    ("scene11_why_numerics.py",          "Scene11_WhyNumerics"),
    ("scene12_grid_discretization.py",   "Scene12_GridDiscretization"),
    ("scene13_upwind_scheme.py",         "Scene13_UpwindScheme"),
    ("scene14_lax_wendroff.py",          "Scene14_LaxWendroff"),
    ("scene15_experiments.py",           "Scene15_Experiments"),
    ("scene16_conclusion.py",            "Scene16_Conclusion"),
]

# ── quality flag ───────────────────────────────────────────────────────────────
QUALITY_FLAG = sys.argv[1] if len(sys.argv) > 1 else "-pql"

QUALITY_DIR = {
    "-pql": "480p15",
    "-pqm": "720p30",
    "-pqh": "1080p60",
    "-pq4k": "2160p60",
}.get(QUALITY_FLAG, "480p15")

OUTPUT_FILE = "full_lecture.mp4"


def render_scenes():
    for py_file, scene_name in SCENES:
        print(f"\n{'='*64}")
        print(f"  Rendering  {scene_name}")
        print(f"{'='*64}")
        # Retry a few times: transient TTS-service network errors and
        # OneDrive file-sync contention have both caused one-off failures
        # mid-batch in the past, even though the scene itself is fine.
        for attempt in range(1, 4):
            result = subprocess.run(
                [PYTHON, "-m", "manim", QUALITY_FLAG, py_file, scene_name],
            )
            if result.returncode == 0:
                break
            print(f"  ! {scene_name} failed (attempt {attempt}/3)")
        else:
            raise RuntimeError(f"{scene_name} failed after 3 attempts")


def concatenate():
    concat_list = "_concat_list.txt"
    missing = []

    with open(concat_list, "w") as f:
        for py_file, scene_name in SCENES:
            stem = py_file.replace(".py", "")
            path = os.path.join(
                "media", "videos", stem, QUALITY_DIR, f"{scene_name}.mp4"
            )
            if not os.path.exists(path):
                missing.append(path)
            f.write(f"file '{os.path.abspath(path)}'\n")

    if missing:
        os.remove(concat_list)
        raise FileNotFoundError(
            "These rendered videos were not found:\n" +
            "\n".join(f"  {p}" for p in missing)
        )

    print(f"\nConcatenating {len(SCENES)} scenes -> {OUTPUT_FILE} ...")
    # Video is copied as-is (fast, lossless — it was already fine).
    # Audio is re-encoded rather than raw-copied: naively concatenating 16
    # separately-encoded AAC streams with `-c copy` leaves timestamp
    # discontinuities between segments that some players (e.g. Windows
    # Movies & TV) fail to play back correctly — video shows, audio doesn't.
    # Re-encoding produces one continuous, clean audio stream instead.
    # +faststart moves the moov atom to the front for broad player/seek support.
    subprocess.run(
        [
            FFMPEG, "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
            "-movflags", "+faststart",
            OUTPUT_FILE, "-y",
        ],
        check=True,
    )
    os.remove(concat_list)
    print(f"\nDone!  ->  {os.path.abspath(OUTPUT_FILE)}")


if __name__ == "__main__":
    render_scenes()
    concatenate()
