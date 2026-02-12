@echo off
chcp 65001>nul

set "PGPASSWORD="
set "HOST="
set "PORT="
set "DB="
set "USER="
set "DATA_DIR="
set "SCHEMA="

for %%F in ("%DATA_DIR%\2025_*.shp") do (
    echo 처리중: %%~nF
   
    ogr2ogr -f "PostgreSQL" ^
        "PG:host=%HOST% port=%PORT% dbname=%DB% user=%USER% password=%PGPASSWORD% options='-c search_path=public,%SCHEMA%'" ^
        "%%F" ^
        -s_srs EPSG:5179 ^
        -t_srs EPSG:5179 ^
        -oo ENCODING=CP949 ^
	-lco SCHEMA=%SCHEMA% ^
	-lco PRECISION=NO ^
        -nln "%%~nF" ^
        -nlt PROMOTE_TO_MULTI ^
        -lco GEOMETRY_NAME=geometry ^
        -lco LAUNDER=NO ^
        -overwrite -progress
)
echo 완료!
pause