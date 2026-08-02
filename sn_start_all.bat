@echo off
REM SuperNinja - Start All Windows Components
REM =============================================
REM 
REM Prerequisites:
REM   1. Python 3 installed (python.org)
REM   2. pip install requests
REM   3. Unreal Engine 5 with Python Editor Script Plugin enabled
REM   4. All 3 Python files in the SAME folder
REM
REM Steps:
REM   1. Open 3 command prompts
REM   2. Run this batch file (starts bridge + companion)
REM   3. In Unreal, open Python console and run the Unreal client
REM
REM =============================================

echo ============================================
echo   SuperNinja Windows Starter
echo ============================================
echo.

REM Start the local bridge in a new window
echo [1/2] Starting Local Bridge on port 8765...
start "SuperNinja Bridge" cmd /k python sn_local_bridge_phase2.py

REM Wait a moment for bridge to start
timeout /t 2 /nobreak >nul

REM Start the companion in a new window  
echo [2/2] Starting Companion (polling cloud server)...
start "SuperNinja Companion" cmd /k python sn_companion_phase2.py

echo.
echo ============================================
echo   Both services started!
echo.
echo   Bridge:    http://127.0.0.1:8765
echo   Cloud URL: https://launched-excessive-sends-joshua.trycloudflare.com
echo.
echo   Now open Unreal Editor and run:
echo   exec(open(r"PATH_TO\sn_unreal_nonblocking_phase2.py", "r", encoding="utf-8-sig").read())
echo.
echo   Or use the Python console in UE5 and paste the script.
echo ============================================
pause