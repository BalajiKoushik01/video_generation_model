@echo off
cls
echo ========================================
echo   HOLLYWOOD STUDIO - GITHUB UPLOAD
echo ========================================
echo.
echo Your project is ready! Choose upload method:
echo.
echo 1. GitHub Desktop (EASIEST - Recommended)
echo 2. Personal Access Token
echo 3. Try automatic push (may prompt for login)
echo 4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto token
if "%choice%"=="3" goto autopush
if "%choice%"=="4" exit /b 0

:desktop
cls
echo ========================================
echo   METHOD 1: GitHub Desktop
echo ========================================
echo.
echo STEP 1: Download and Install
echo ----------------------------
echo Opening download page...
start https://desktop.github.com/
echo.
echo Please:
echo 1. Download and install GitHub Desktop
echo 2. Sign in with your GitHub account
echo.
pause
echo.
echo STEP 2: Add This Repository
echo ----------------------------
echo 1. Open GitHub Desktop
echo 2. Click: File -^> Add Local Repository
echo 3. Click: Choose... and select this folder:
echo    %CD%
echo 4. Click: Add Repository
echo.
pause
echo.
echo STEP 3: Publish
echo ---------------
echo 1. Click the "Publish repository" button
echo 2. Uncheck "Keep this code private" (if you want it public)
echo 3. Click "Publish repository"
echo.
echo Done! Your code is now on GitHub!
echo Visit: https://github.com/BalajiKoushik01/AI_video-generation
echo.
pause
exit /b 0

:token
cls
echo ========================================
echo   METHOD 2: Personal Access Token
echo ========================================
echo.
echo STEP 1: Create Token
echo --------------------
echo Opening GitHub token page...
start https://github.com/settings/tokens/new
echo.
echo On the GitHub page:
echo 1. Note: "Hollywood Studio Upload"
echo 2. Expiration: 90 days (or your preference)
echo 3. Check: [x] repo (full control)
echo 4. Scroll down and click "Generate token"
echo 5. COPY THE TOKEN (you won't see it again!)
echo.
pause
echo.
echo STEP 2: Push with Token
echo -----------------------
echo When you run the push command, you'll be prompted:
echo   Username: BalajiKoushik01
echo   Password: [paste your token here]
echo.
echo Press any key to start the push...
pause
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo SUCCESS! 
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo Visit: https://github.com/BalajiKoushik01/AI_video-generation
    start https://github.com/BalajiKoushik01/AI_video-generation
) else (
    echo.
    echo Push failed. Please try again or use GitHub Desktop.
)
echo.
pause
exit /b 0

:autopush
cls
echo ========================================
echo   METHOD 3: Automatic Push
echo ========================================
echo.
echo Attempting to push...
echo This may open a browser window for authentication.
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo SUCCESS! 
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo Visit: https://github.com/BalajiKoushik01/AI_video-generation
    start https://github.com/BalajiKoushik01/AI_video-generation
) else (
    echo.
    echo ========================================
    echo Authentication Required
    echo ========================================
    echo.
    echo The automatic push failed.
    echo Please use Method 1 (GitHub Desktop) or Method 2 (Token).
    echo.
    echo Restarting menu...
    timeout /t 3
    goto :eof
)
echo.
pause
exit /b 0
