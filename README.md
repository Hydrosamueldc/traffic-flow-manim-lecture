# Numerical Simulation of the LWR Traffic Flow Model

Animated companion to an undergraduate project on the numerical simulation of the Lighthill-Whitham-Richards (LWR) traffic-flow model using the Upwind and Lax-Wendroff finite-difference schemes.

## Watch

[Watch the full lecture on YouTube](https://youtu.be/AyCQ6vkNUt8)

## Why This Project

Traffic congestion is more than a delay: congestion waves can form and travel upstream even when there is no visible accident or road obstruction. This project uses mathematics to explain how that happens.

Rather than modelling individual vehicles, the LWR model treats traffic as a continuous flow. Vehicle conservation, combined with the Greenshields speed-density relationship, produces a nonlinear conservation law for traffic density. Its solutions can develop shock waves and rarefaction waves, which makes numerical methods essential.

## Study Focus

The project compares two classical finite-difference schemes for the one-dimensional LWR model:

- **Upwind scheme:** stable and non-oscillatory near shocks, but numerically diffusive.
- **Lax-Wendroff scheme:** more accurate for smooth density profiles, but can create nonphysical oscillations near sharp congestion fronts.

The comparison considers accuracy, CFL stability, shock resolution, convergence behaviour, density bounds, total variation, and computational cost.

## Benchmark Problems

The underlying study evaluates the methods using three traffic-flow scenarios:

1. A Riemann problem with a stationary shock wave.
2. A smooth initial density profile for convergence testing.
3. A localised traffic-jam scenario.

The results show that neither method is universally best. Upwind is the more reliable option for shock-dominated problems, while Lax-Wendroff is the more accurate option for smooth traffic-density profiles.

## Animated Lecture

The 16 Manim scenes introduce the mathematical ideas behind the study, including:

- Traffic density, velocity, and flow
- The Greenshields fundamental diagram
- The LWR conservation law and characteristics
- Shock and rarefaction waves
- Grid discretisation and the CFL condition
- Upwind and Lax-Wendroff schemes
- Comparative analysis and conclusions

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

## Author

Adegboyega Samuel

Department of Mathematics, University of Lagos
