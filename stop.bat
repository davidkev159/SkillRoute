@echo off
echo Stopping SkillRoute...
taskkill /FI "WINDOWTITLE eq SkillRoute API*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq SkillRoute Frontend*" /T /F >nul 2>&1
echo Done. (If a window didn't close, close it manually.)
pause
