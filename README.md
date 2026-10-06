# Traffic Flow Manim Lecture

An animated, 16-scene introduction to traffic-flow theory and numerical methods, built with Manim. Topics include density, velocity, flow, the Greenshields model, conservation laws, characteristics, shock waves, rarefaction waves, and finite-difference schemes.

## Watch

[Watch the full lecture on YouTube](https://youtu.be/AyCQ6vkNUt8)

## Requirements

- Python 3.10 or newer
- FFmpeg available on your PATH

Install the Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Render

Render the full lecture at low quality for a quick preview:

```powershell
python render_all.py
```

Use `-pqm` for 720p or `-pqh` for 1080p:

```powershell
python render_all.py -pqh
```

Individual scenes can also be rendered directly with Manim. For example:

```powershell
manim -pqh scene01_traffic_problem.py Scene01_TrafficProblem
```

Rendered videos, audio, and TeX assets are generated under `media/` and intentionally excluded from version control.
