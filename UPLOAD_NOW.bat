@echo off
color 0A
cls
echo.
echo  ╔════════════════════════════════════════════════════════════╗
echo  ║                                                            ║
echo  ║     HOLLYWOOD STUDIO - READY TO UPLOAD TO GITHUB!         ║
echo  ║                                                            ║
echo  ╚════════════════════════════════════════════════════════════╝
echo.
echo  ✅ Project Status:
echo     • Deep cleaned (1.26 GB freed)
echo     • 30 Python files ready
echo     • Git committed (2 commits)
echo     • Remote configured
echo.
echo  🎯 Target: https://github.com/BalajiKoushik01/AI_video-generation
echo.
echo  ════════════════════════════════════════════════════════════
echo.
echo  📋 CHOOSE YOUR METHOD:
echo.
echo     1 │ GitHub Desktop (EASIEST - 2 minutes)
echo       │ Download, sign in, add folder, publish
echo.
echo     2 │ Personal Access Token (Quick)
echo       │ Create token, paste when prompted
echo.
echo     3 │ Manual Instructions
echo       │ Show detailed step-by-step guide
echo.
echo     4 │ Exit
echo.
echo  ════════════════════════════════════════════════════════════
echo.
set /p choice="  Enter your choice (1-4): "

if "%choice%"=="1" goto method1
if "%choice%"=="2" goto method2
if "%choice%"=="3" goto method3
if "%choice%"=="4" exit /b 0
goto :eof

:method1
cls
echo.
echo  ╔════════════════════════════════════════════════════════════╗
echo  ║  METHOD 1: GitHub Desktop (Recommended)                   ║
echo  ╚════════════════════════════════════════════════════════════╝
echo.
echo  📥 STEP 1: Download GitHub Desktop
echo  ────────────────────────────────────────────────────────────
echo     Opening download page in your browser...
echo.
start https://desktop.github.com/
timeout /t 2 >nul
echo     ✓ Download and install GitHub Desktop
echo     ✓ Sign in with your GitHub account (BalajiKoushik01)
echo.
pause
echo.
echo  📁 STEP 2: Add This Repository
echo  ────────────────────────────────────────────────────────────
echo     In GitHub Desktop:
echo.
echo     1. Click: File → Add Local Repository
echo     2. Click: Choose...
echo     3. Navigate to and select:
echo        %CD%
echo     4. Click: Add Repository
echo.
pause
echo.
echo  🚀 STEP 3: Publish to GitHub
echo  ────────────────────────────────────────────────────────────
echo     1. Click the blue "Publish repository" button
echo     2. Repository name: AI_video-generation
echo     3. Uncheck "Keep this code private" (if public)
echo     4. Click "Publish repository"
echo.
echo     ✅ DONE! Your code is now on GitHub!
echo.
echo     Opening your repository...
timeout /t 2 >nul
start https://github.com/BalajiKoushik01/AI_video-generation
echo.
pause
exit /b 0

:method2
cls
echo.
echo  ╔════════════════════════════════════════════════════════════╗
echo  ║  METHOD 2: Personal Access Token                          ║
echo  ╚════════════════════════════════════════════════════════════╝
echo.
echo  🔑 STEP 1: Create Personal Access Token
echo  ────────────────────────────────────────────────────────────
echo     Opening GitHub token creation page...
echo.
start https://github.com/settings/tokens/new
timeout /t 2 >nul
echo.
echo     On the GitHub page, fill in:
echo.
echo     Note: Hollywood Studio Upload
echo     Expiration: 90 days (or your preference)
echo     Select scopes: ✓ repo (full control)
echo.
echo     Then click "Generate token" at the bottom
echo.
echo     ⚠️  IMPORTANT: Copy the token immediately!
echo         You won't be able to see it again.
echo.
pause
echo.
echo  🚀 STEP 2: Push with Token
echo  ────────────────────────────────────────────────────────────
echo.
echo     When prompted:
echo       Username: BalajiKoushik01
echo       Password: [paste your token]
echo.
echo     Press any key to start the push...
pause
echo.
echo     Pushing to GitHub...
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    color 0A
    echo.
    echo  ╔════════════════════════════════════════════════════════════╗
    echo  ║  ✅ SUCCESS! Your code is now on GitHub!                  ║
    echo  ╚════════════════════════════════════════════════════════════╝
    echo.
    timeout /t 2 >nul
    start https://github.com/BalajiKoushik01/AI_video-generation
) else (
    color 0C
    echo.
    echo  ╔════════════════════════════════════════════════════════════╗
    echo  ║  ⚠️  Push Failed - Authentication Issue                   ║
    echo  ╚════════════════════════════════════════════════════════════╝
    echo.
    echo     Please try Method 1 (GitHub Desktop) instead.
    echo     It's easier and handles authentication automatically.
    echo.
)
pause
exit /b 0

:method3
cls
echo.
echo  ╔════════════════════════════════════════════════════════════╗
echo  ║  MANUAL UPLOAD INSTRUCTIONS                                ║
echo  ╚════════════════════════════════════════════════════════════╝
echo.
echo  Your project is at:
echo  %CD%
echo.
echo  ════════════════════════════════════════════════════════════
echo  OPTION A: GitHub Desktop (Easiest)
echo  ════════════════════════════════════════════════════════════
echo.
echo  1. Download: https://desktop.github.com/
echo  2. Install and sign in
echo  3. File → Add Local Repository → Select this folder
echo  4. Click "Publish repository"
echo.
echo  ════════════════════════════════════════════════════════════
echo  OPTION B: Command Line with Token
echo  ════════════════════════════════════════════════════════════
echo.
echo  1. Create token: https://github.com/settings/tokens/new
echo     - Check "repo" scope
echo     - Copy the token
echo.
echo  2. Open PowerShell here and run:
echo     git push -u origin main
echo.
echo  3. When prompted:
echo     Username: BalajiKoushik01
echo     Password: [your token]
echo.
echo  ════════════════════════════════════════════════════════════
echo.
echo  Opening both pages in browser...
start https://desktop.github.com/
timeout /t 1 >nul
start https://github.com/settings/tokens/new
echo.
pause
exit /b 0
