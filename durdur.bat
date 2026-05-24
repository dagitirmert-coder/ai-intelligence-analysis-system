@echo off
title GEOINT - Durdur

set "PG_BIN=C:\Program Files\PostgreSQL\18\bin"
set "PG_DATA=C:\Program Files\PostgreSQL\18\data"

echo PostgreSQL durduruluyor...
"%PG_BIN%\pg_ctl" stop -D "%PG_DATA%" -m fast >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo PostgreSQL durduruldu.
) else (
    echo PostgreSQL zaten calismiyordu.
)
pause
