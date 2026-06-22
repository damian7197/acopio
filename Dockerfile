# Imagen para desarrollo. Para producción conviene instalar solo
# requirements.txt (sin las dependencias de desarrollo).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

EXPOSE 8000

# Por defecto: migra, recopila estáticos y levanta gunicorn (producción/Render).
# En desarrollo, docker-compose sobrescribe este comando por runserver.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
