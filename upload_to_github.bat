@echo off
echo ========================================
echo AUTOMATED GitHub Upload
echo ========================================
echo.
echo This will open your browser to authenticate with GitHub
echo and then automatically push your code.
echo.
pause

echo.
echo Step 1: Opening GitHub authentication...
echo.

REM Try to push - this will trigger Windows Credential Manager or browser auth
git push -u origin main 2>&1

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! 
    echo ========================================
    echo.
    echo Your project is now live at:
    echo https://github.com/BalajiKoushik01/AI_video-generation
    echo.
    echo Opening repository in browser...
    start https://github.com/BalajiKoushik01/AI_video-generation
    echo.
    pause
    exit /b 0
) else (
    echo.
    echo ========================================
    echo Authentication Required
    echo ========================================
    echo.
    echo The push failed. This usually means you need to authenticate.
    echo.
    echo EASIEST SOLUTION: Use GitHub Desktop
    echo ----------------------------------------
    echo 1. Download: https://desktop.github.com/
    echo 2. Install and sign in
    echo 3. File -^> Add Local Repository
    echo 4. Select: %CD%
    echo 5. Click: Publish repository
    echo.
    echo ALTERNATIVE: Create Personal Access Token
    echo ----------------------------------------
    echo 1. Visit: https://github.com/settings/tokens
    echo 2. Click: Generate new token (classic)
    echo 3. Select scope: repo (full control)
    echo 4. Copy the token
    echo 5. Run this script again
    echo 6. When prompted for password, paste the token
    echo.
    echo Opening GitHub token page...
    start https://github.com/settings/tokens
    echo.
    pause
)
