@echo off
REM Script để chạy migration với Alembic

cd /d C:\Users\Admin\Documents\PROJECT_IT\to-do_list

REM Activate venv
call .\venv\Scripts\activate.bat

REM Run migration
echo.
echo ========================================
echo Running: alembic upgrade head
echo ========================================
echo.

alembic upgrade head

echo.
echo ========================================
echo Migration completed!
echo ========================================
echo.
echo Bây giờ chạy: uvicorn app.main:app --reload
pause
