@echo off
echo ======================================
echo   Ferreter^ia P - Configuracion inicial
echo ======================================

echo.
echo 1. Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo.
echo 2. Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 3. Creando base de datos PostgreSQL...
psql -U postgres -c "CREATE DATABASE ferre_p;" 2>nul || echo La BD puede que ya exista, continuando...

echo.
echo 4. Ejecutando migraciones...
python manage.py migrate

echo.
echo 5. Creando superusuario administrador...
python manage.py createsuperuser

echo.
echo 6. Recopilando archivos estaticos...
python manage.py collectstatic --noinput

echo.
echo ======================================
echo   !Configuracion completada!
echo   Inicie el servidor con:
echo   python manage.py runserver 127.0.0.1:8002
echo ======================================
pause
