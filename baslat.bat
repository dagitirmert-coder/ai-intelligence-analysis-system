@echo off
title GEOINT Platform

set "PG_BIN=C:\Program Files\PostgreSQL\18\bin"
set "PG_DATA=C:\Program Files\PostgreSQL\18\data"
set "APP_DIR=%~dp0"

echo ============================================
echo   GEOINT Platform
echo ============================================
echo.

REM -- 1. Check PostgreSQL --
echo [1/3] PostgreSQL kontrol...
"%PG_BIN%\pg_isready" -h localhost -p 5432 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       PostgreSQL OK - zaten calisiyor.
    goto :check_db
)

echo       PostgreSQL baslatiliyor...
if not exist "%APP_DIR%data" mkdir "%APP_DIR%data"
"%PG_BIN%\pg_ctl" start -D "%PG_DATA%" -l "%APP_DIR%data\pg.log" -w >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo       [!] PostgreSQL baslatilamadi - SQLite kullanilacak.
    goto :start_app
)
echo       PostgreSQL baslatildi.

:check_db
REM -- 2. Create DB if needed --
echo [2/3] Veritabani kontrol...

"%PG_BIN%\psql" -h localhost -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='geoint'" 2>nul | findstr "1" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo       Kullanici olusturuluyor...
    "%PG_BIN%\psql" -h localhost -U postgres -c "CREATE USER geoint WITH PASSWORD 'geoint' CREATEDB;" >nul 2>&1
)

"%PG_BIN%\psql" -h localhost -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='geointdb'" 2>nul | findstr "1" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo       Veritabani olusturuluyor...
    "%PG_BIN%\psql" -h localhost -U postgres -c "CREATE DATABASE geointdb OWNER geoint;" >nul 2>&1
)

"%PG_BIN%\psql" -h localhost -U postgres -d geointdb -tAc "SELECT 1 FROM pg_extension WHERE extname='postgis'" 2>nul | findstr "1" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo       PostGIS yukleniyor...
    "%PG_BIN%\psql" -h localhost -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS postgis;" >nul 2>&1
    "%PG_BIN%\psql" -h localhost -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;" >nul 2>&1
    "%PG_BIN%\psql" -h localhost -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" >nul 2>&1
)

echo       Veritabani hazir.

:start_app
REM -- 3. Start application --
echo [3/3] Uygulama baslatiliyor...
if not exist "%APP_DIR%data" mkdir "%APP_DIR%data"
if not exist "%APP_DIR%data\reports" mkdir "%APP_DIR%data\reports"

echo.
echo ============================================
echo   http://localhost:8000
echo   Kapatmak icin CTRL+C
echo ============================================
echo.

cd /d "%APP_DIR%"
py app.py
