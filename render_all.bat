@echo off
setlocal

echo.
echo  ==========================================================
echo   LWR Traffic Animation  --  Full Render Script
echo   Run from Anaconda Prompt inside the ManimProjects folder
echo  ==========================================================
echo.

:: ── Quality ───────────────────────────────────────────────────────────────
:: Change QUAL and QUAL_DIR together:
::   low   (-ql)  480p15   <- default, fast
::   medium(-qm)  720p30
::   high  (-qh)  1080p60
set QUAL=l
set QUAL_DIR=480p15

:: ── Force re-render ────────────────────────────────────────────────────────
:: Set FORCE=1 to re-render every scene even if the MP4 already exists.
:: Set FORCE=0 to skip scenes that are already rendered (safe resume after error).
set FORCE=0

echo  Quality : %QUAL_DIR%
if "%FORCE%"=="1" (echo  Mode    : FORCE re-render all) else (echo  Mode    : Skip already-rendered scenes)
echo.

:: ══════════════════════════════════════════════════════════════
::  RENDER SCENES
:: ══════════════════════════════════════════════════════════════

call :maybe_render scene01_traffic_problem    Scene01_TrafficProblem    "[1/7]"
call :maybe_render scene02_traffic_density    Scene02_TrafficDensity    "[2/7]"
call :maybe_render scene03_traffic_velocity   Scene03_TrafficVelocity   "[3/7]"
call :maybe_render scene04_traffic_flow       Scene04_TrafficFlow       "[4/7]"
call :maybe_render scene05_greenshields       Scene05_Greenshields      "[5/7]"
call :maybe_render scene06_fundamental_diagram Scene06_FundamentalDiagram "[6/7]"
call :maybe_render scene07_conservation       Scene07_Conservation      "[7/7]"

::call :maybe_render scene08_characteristics   Scene08_Characteristics   "[8/15]"
::call :maybe_render scene09_shock_waves        Scene09_ShockWaves        "[9/15]"
::call :maybe_render scene10_rarefaction        Scene10_Rarefaction       "[10/15]"
::call :maybe_render scene11_numerical_grid     Scene11_NumericalGrid     "[11/15]"
::call :maybe_render scene12_upwind             Scene12_Upwind            "[12/15]"
::call :maybe_render scene13_lax_wendroff       Scene13_LaxWendroff       "[13/15]"
::call :maybe_render scene14_comparison         Scene14_Comparison        "[14/15]"
::call :maybe_render scene15_conclusion         Scene15_Conclusion        "[15/15]"

:: ══════════════════════════════════════════════════════════════
::  BUILD FFMPEG FILE LIST
::  Add each scene's line here as you build new scenes.
:: ══════════════════════════════════════════════════════════════

echo.
echo Building concat list...
(
echo file 'media/videos/scene01_traffic_problem/%QUAL_DIR%/Scene01_TrafficProblem.mp4'
echo file 'media/videos/scene02_traffic_density/%QUAL_DIR%/Scene02_TrafficDensity.mp4'
echo file 'media/videos/scene03_traffic_velocity/%QUAL_DIR%/Scene03_TrafficVelocity.mp4'
echo file 'media/videos/scene04_traffic_flow/%QUAL_DIR%/Scene04_TrafficFlow.mp4'
echo file 'media/videos/scene05_greenshields/%QUAL_DIR%/Scene05_Greenshields.mp4'
echo file 'media/videos/scene06_fundamental_diagram/%QUAL_DIR%/Scene06_FundamentalDiagram.mp4'
echo file 'media/videos/scene07_conservation/%QUAL_DIR%/Scene07_Conservation.mp4'
) > filelist.txt

:: ══════════════════════════════════════════════════════════════
::  CONCATENATE
:: ══════════════════════════════════════════════════════════════

echo Concatenating into LWR_Full_Animation.mp4 ...
ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy LWR_Full_Animation.mp4
if %errorlevel% neq 0 (
  echo.
  echo FAILED: FFmpeg could not concatenate. Check all MP4 files exist.
  pause & exit /b 1
)

echo.
echo  ==========================================================
echo   Done!  LWR_Full_Animation.mp4 is ready.
echo  ==========================================================
echo.
start LWR_Full_Animation.mp4
endlocal
exit /b 0

:: ══════════════════════════════════════════════════════════════
::  SUBROUTINE: render only if MP4 is missing (or FORCE=1)
::  Usage: call :maybe_render <file_stem> <ClassName> <label>
:: ══════════════════════════════════════════════════════════════
:maybe_render
set _STEM=%~1
set _CLASS=%~2
set _LABEL=%~3
set _MP4=media\videos\%_STEM%\%QUAL_DIR%\%_CLASS%.mp4

if "%FORCE%"=="0" if exist "%_MP4%" (
  echo %_LABEL% %_CLASS% -- already rendered, skipping.
  exit /b 0
)

echo %_LABEL% Rendering %_CLASS% ...
manim -q%QUAL% %_STEM%.py %_CLASS%
if %errorlevel% neq 0 (
  echo.
  echo FAILED: %_CLASS%
  echo Tip: run the scene individually first to check for errors:
  echo   manim -pql %_STEM%.py %_CLASS%
  pause & exit /b 1
)

:: Short pause between scenes to avoid gTTS rate-limiting
timeout /t 4 /nobreak >nul
exit /b 0
