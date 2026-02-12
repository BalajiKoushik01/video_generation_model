@echo off
cls
echo ========================================
echo   CREATE GITHUB REPOSITORY
echo ========================================
echo.
echo The repository needs to be created on GitHub first.
echo.
echo Opening GitHub in your browser...
echo.
timeout /t 2 >nul

start https://github.com/new

echo.
echo ========================================
echo   FOLLOW THESE STEPS:
echo ========================================
echo.
echo 1. Repository name: AI_video-generation
echo 2. Description: Hollywood Studio - AI Video Generation Pipeline
echo 3. Public or Private: Choose your preference
echo 4. DO NOT initialize with README, .gitignore, or license
echo 5. Click "Create repository"
echo.
echo ========================================
echo.
pause

echo.
echo Now pushing your code to GitHub...
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo Opening repository...
    timeout /t 2 >nul
    start https://github.com/BalajiKoushik01/AI_video-generation
) else (
    echo.
    echo ========================================
    echo   PUSH FAILED
    echo ========================================
    echo.
    echo Please make sure:
    echo 1. You created the repository on GitHub
    echo 2. Repository name is exactly: AI_video-generation
    echo 3. You did NOT initialize it with any files
    echo.
    echo Then run this script again.
)

echo.
pause
