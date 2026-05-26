#!/bin/bash
# Script de configuración inicial del proyecto Ferretería P

set -e

echo "======================================"
echo "  Ferretería P — Configuración inicial"
echo "======================================"

# 1. Crear entorno virtual
echo ""
echo "1. Creando entorno virtual..."
python -m venv venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate

# 2. Instalar dependencias
echo "2. Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Crear base de datos PostgreSQL
echo "3. Creando base de datos..."
psql -U postgres -c "CREATE DATABASE ferre_p;" 2>/dev/null || echo "   (La BD puede que ya exista, continuando...)"

# 4. Ejecutar migraciones
echo "4. Ejecutando migraciones..."
python manage.py migrate

# 5. Crear superusuario
echo ""
echo "5. Creando superusuario administrador..."
python manage.py createsuperuser

# 6. Collectstatic
echo "6. Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "======================================"
echo "  ¡Configuración completada!"
echo "  Inicie el servidor con:"
echo "  python manage.py runserver 127.0.0.1:8002"
echo "======================================"
