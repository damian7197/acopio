# Acopio — Sitio institucional + Portal de clientes

Plataforma web para un acopio de cereales: un **sitio institucional público** con los
servicios de la empresa y un **portal privado** donde cada productor consulta, con su
propio usuario, el cereal que tiene guardado.

> Proyecto real desarrollado de forma individual para un acopio de cereales en la zona
> núcleo (Santa Fe, Argentina). El foco está puesto en un diseño robusto y en el control
> de acceso por cliente.

<!-- Reemplazá estos badges cuando tengas el repo público -->
![CI](https://github.com/USUARIO/acopio/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.x-092E20)

---

## El problema

En un acopio, cada productor entrega cereal que queda guardado a su nombre. Hoy, para
saber su saldo, el cliente tiene que llamar o pasar por la oficina. Este portal le permite
consultarlo en cualquier momento, mientras que el sitio público funciona como cara
institucional de la empresa.

El desafío técnico central es el **aislamiento de datos por cliente**: cada productor
debe ver únicamente su propia información, nunca la de otro.

## Funcionalidades

- **Sitio institucional**: servicios, ubicación, contacto. Páginas públicas y rápidas.
- **Portal de clientes** (requiere login):
  - Saldo de cereal guardado, por especie y campaña.
  - Historial de movimientos / pesadas.
  - (Roadmap) Comprobantes descargables.
- **Control de acceso por fila**: todas las consultas se acotan al usuario en el servidor.
- **Panel de administración** para la gestión interna.

## Stack

- **Backend**: Python 3.12 · Django 5.x
- **Base de datos**: PostgreSQL
- **Frontend**: plantillas de Django (+ WhiteNoise para estáticos)
- **Calidad**: pytest · ruff · GitHub Actions (CI)
- **Deploy**: Render / VPS (ver sección *Despliegue*)

## Arquitectura del proyecto

```
acopio/
├── config/                 # Configuración del proyecto
│   ├── settings/
│   │   ├── base.py         # Settings comunes
│   │   ├── development.py  # Settings de desarrollo
│   │   └── production.py   # Settings de producción
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/               # Modelos y utilidades compartidas
│   ├── accounts/           # Usuario custom + autenticación
│   ├── sitio/              # Sitio institucional público
│   └── portal/             # Portal de clientes (cuenta de granos)
├── templates/              # Plantillas HTML
├── static/                 # CSS, JS, imágenes
├── docs/                   # Relevamiento y documentación
├── .github/workflows/      # CI
├── .env.example            # Variables de entorno (plantilla)
├── requirements.txt
└── manage.py
```

> **Decisión de diseño**: la app `accounts` define un **modelo de usuario custom desde el
> inicio** (cambiarlo después en Django es muy costoso). El vínculo Usuario ↔ Productor es
> de muchos-a-muchos, porque un mismo productor puede operar con varios CUIT.

> **Decisión de diseño**: el portal es **de solo lectura** sobre los datos de cereal. El
> dato oficial vive en el sistema de gestión del acopio; el portal lo proyecta, no lo edita.

## Cómo correrlo localmente

### Opción rápida: con Docker (recomendada)

Requisitos: Docker y Docker Compose.

```bash
cp .env.example .env             # los valores por defecto ya sirven para Docker
docker compose up --build        # levanta Postgres + Django y corre migraciones
docker compose exec web python manage.py createsuperuser
```

La app queda en http://localhost:8000 y el admin en http://localhost:8000/admin.

### Opción sin Docker

Requisitos: Python 3.12 y PostgreSQL.

```bash
git clone https://github.com/USUARIO/acopio.git
cd acopio

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt -r requirements-dev.txt

cp .env.example .env             # completá las variables
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Tests

```bash
pytest
ruff check .
```

> El test clave del proyecto verifica que **un usuario no pueda acceder a los datos de
> otro cliente** (prevención de IDOR). Vive en `apps/portal/tests.py`.

## Despliegue

- **Demo / aprendizaje**: Render free tier (con datos ficticios). Tener en cuenta que la
  base gratuita de Render expira a los 30 días y los servicios web gratuitos se duermen.
- **Producción**: Render pago **o** un VPS propio, siempre con backups automatizados de la
  base y HTTPS.

## Documentación

- [`docs/relevamiento-acopio.md`](docs/relevamiento-acopio.md) — relevamiento de
  requisitos hecho con la dueña del acopio.

## Autor

Damian — Estudiante de Ingeniería en Sistemas (UCEL).

## Licencia

MIT — ver [`LICENSE`](LICENSE).
