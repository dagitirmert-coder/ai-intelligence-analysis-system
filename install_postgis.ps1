# PostGIS Installation Script for PostgreSQL 18
# Run as Administrator: Right-click → Run with PowerShell (as Admin)

$SRC = "C:\Users\Mert\postgis_temp\postgis-bundle-pg18-3.6.2x64"
$PG = "C:\Program Files\PostgreSQL\18"

Write-Host "=== Installing PostGIS 3.6.2 for PostgreSQL 18 ===" -ForegroundColor Green

# 1. Copy extension control + SQL files
Write-Host "1. Copying extension files..." -ForegroundColor Yellow
Copy-Item -Path "$SRC\share\extension\*" -Destination "$PG\share\extension\" -Force
Write-Host "   OK: share/extension" -ForegroundColor Green

# 2. Copy contrib SQL files
Write-Host "2. Copying contrib files..." -ForegroundColor Yellow
if (Test-Path "$SRC\share\contrib") {
    Copy-Item -Path "$SRC\share\contrib\*" -Destination "$PG\share\contrib\" -Force -Recurse
    Write-Host "   OK: share/contrib" -ForegroundColor Green
}

# 3. Copy lib files (PostGIS .dll modules)
Write-Host "3. Copying lib files..." -ForegroundColor Yellow
Copy-Item -Path "$SRC\lib\*" -Destination "$PG\lib\" -Force
Write-Host "   OK: lib" -ForegroundColor Green

# 4. Copy bin DLL dependencies
Write-Host "4. Copying bin DLLs..." -ForegroundColor Yellow
Copy-Item -Path "$SRC\bin\*.dll" -Destination "$PG\bin\" -Force
Copy-Item -Path "$SRC\bin\*.exe" -Destination "$PG\bin\" -Force -ErrorAction SilentlyContinue
Write-Host "   OK: bin" -ForegroundColor Green

# 5. Copy GDAL data
Write-Host "5. Copying GDAL data..." -ForegroundColor Yellow
if (Test-Path "$SRC\gdal-data") {
    if (-not (Test-Path "$PG\gdal-data")) { New-Item -ItemType Directory -Path "$PG\gdal-data" | Out-Null }
    Copy-Item -Path "$SRC\gdal-data\*" -Destination "$PG\gdal-data\" -Force
    Write-Host "   OK: gdal-data" -ForegroundColor Green
}

# 6. Restart PostgreSQL
Write-Host "6. Restarting PostgreSQL..." -ForegroundColor Yellow
& "$PG\bin\pg_ctl.exe" -D "C:\Users\Mert\pgdata" restart 2>&1 | Out-Null
Start-Sleep -Seconds 3

# 7. Test PostGIS
Write-Host "7. Testing PostGIS extension..." -ForegroundColor Yellow
$result = & "$PG\bin\psql.exe" -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS postgis; SELECT PostGIS_Version();" 2>&1
Write-Host $result

Write-Host "`n=== PostGIS Installation Complete ===" -ForegroundColor Green
Write-Host "Now run: python app.py" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
