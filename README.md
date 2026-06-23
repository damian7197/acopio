# Acopio — Sitio institucional + Portal de clientes

Plataforma web para un acopio de cereales: un **sitio institucional público** con
los servicios de la empresa y un **portal privado** donde cada productor consulta,
con su propio usuario, el cereal que tiene guardado.

**▶ Demo en vivo: https://acopio-bkjl.onrender.com**
_(es un plan gratuito: la primera carga tras un rato de inactividad puede tardar ~1 minuto)_

[![CI](https://github.com/damian7197/acopio/actions/workflows/ci.yml/badge.svg)](https://github.com/damian7197/acopio/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.x-092E20)

> Proyecto real desarrollado de forma individual para un acopio de cereales de
> Santa Fe, Argentina. El foco está puesto en un diseño robusto, el control de
> acceso por cliente y la calidad del código.


## El problema

En un acopio, cada productor entrega cereal que queda guardado a su nombre. Para
saber su saldo, hoy el cliente tiene que llamar o pasar por la oficina. Este portal
le permite consultarlo en línea en cualquier momento, mientras que el sitio público
funciona como cara institucional de la empresa.

El desafío técnico central es el **aislamiento de datos por cliente**: cada productor
debe ver únicamente su propia información, nunca la de otro.

## Funcionalidades

**Sitio institucional**
- Home con identidad de marca (paleta carbón + ámbar, tipografía slab).
- Páginas de servicios, nosotros y contacto.

**Portal de clientes** (requiere login)
- Ingreso con número de cliente y contraseña (altas provistas por administración).
- Resumen de cuenta corriente en kilos, por cosecha y especie.
- Historial de movimientos (ingresos y egresos).
- **Aislamiento por fila**: cada consulta se acota al usuario en el servidor,
  verificado por un test automatizado.

## Stack

- **Backend:** Python 3.12 · Django 5.x
- **Base de datos:** PostgreSQL
- **Frontend:** plantillas de Django · WhiteNoise · CSS propio
- **Calidad:** pytest · ruff · GitHub Actions (CI con PostgreSQL)
- **Infraestructura:** Docker · Render (deploy por blueprint)

## Arquitectura

```
acopio/
├── config/                 # Configuración del proyecto
│   ├── settings/           # base / development / production
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/           # Usuario custom (desde la migración 0)
│   ├── core/               # Utilidades compartidas
│   ├── sitio/              # Sitio institucional público
│   └── portal/             # Portal: Cliente, Movimiento, login, resumen, seed
├── templates/ · static/    # Plantillas y estáticos
├── Dockerfile · docker-compose.yml
├── render.yaml             # Infraestructura como código (Render)
└── .github/workflows/      # CI
```

**Decisiones de diseño**

- **Usuario custom desde el inicio**, para poder extenderlo sin migraciones dolorosas.
- **El portal es de solo lectura** sobre los datos de cereal: el sistema de gestión
  del acopio (Mahon / AMS Corporate) es la única fuente de verdad; el portal la
  proyecta, no la edita.
- **El aislamiento se aplica a nivel de queryset**, tomando el cliente del usuario
  logueado y nunca de la URL (prevención de IDOR).
- **La capa de ingesta está pensada desacoplada** de las vistas, para poder cambiar
  el origen de los datos (Excel, base) sin tocar el portal.

## Cómo correrlo localmente

Requisitos: Docker y Docker Compose.

```bash
git clone https://github.com/damian7197/acopio.git
cd acopio
cp .env.example .env
docker compose up --build
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_portal   # 8 clientes de prueba (clave: demo1234)
```

El sitio queda en http://localhost:8000 y el admin en http://localhost:8000/admin.
El portal, en http://localhost:8000/portal/ (login con un número de cliente, ej. `1001`).

## Tests

```bash
docker compose exec web pytest
docker compose exec web ruff check .
```

El test central (`apps/portal/tests.py`) verifica que **un cliente no pueda acceder
al resumen de otro**.

## Deploy

El despliegue está descrito como código en `render.yaml` (un servicio web Docker y
una base PostgreSQL, conectados). En Render se crea con **New → Blueprint** apuntando
al repositorio.

## Estado y roadmap

El MVP está construido: sitio institucional y portal con login, resumen y aislamiento,
sobre datos de prueba. Lo que sigue:

- [ ] Capa de ingesta real desde Mahon (AMS Corporate): importar el export del sistema
      a `Cliente` y `Movimiento`, reemplazando los datos de prueba.
- [ ] Reemplazar el contenido de relleno por textos, fotos y logo reales.

## Autor

Damian — Estudiante de Ingeniería en Sistemas (UCEL).

## Licencia

MIT — ver [`LICENSE`](LICENSE).