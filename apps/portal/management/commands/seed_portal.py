import random
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.portal.models import Cliente, Movimiento

User = get_user_model()

NOMBRES = [
    "Establecimiento La Esperanza",
    "Agropecuaria San Jorge S.A.",
    "Hnos. Gutiérrez S.H.",
    "La Tordilla S.R.L.",
    "Don Aníbal e Hijos",
    "Campo El Ombú",
    "Sucesión Pérez",
    "Agrícola La Lucía S.A.",
    "Establecimiento Santa Rosa",
    "Los Algarrobos S.R.L.",
]
ESPECIES = ["soja", "maíz", "trigo", "sorgo", "girasol"]
COSECHAS = ["2023/24", "2024/25", "2025/26"]
PASSWORD = "demo1234"


class Command(BaseCommand):
    help = "Carga clientes y movimientos de prueba realistas en el portal."

    def add_arguments(self, parser):
        parser.add_argument("--clientes", type=int, default=8,
                            help="Cantidad de clientes a crear (default 8).")

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)
        n = min(options["clientes"], len(NOMBRES))
        numeros = [str(1001 + i) for i in range(n)]

        # Limpia un seed anterior (solo estos números), para poder re-ejecutar.
        Cliente.objects.filter(numero_cliente__in=numeros).delete()
        User.objects.filter(username__in=numeros).delete()

        for i in range(n):
            numero = numeros[i]
            user = User.objects.create_user(username=numero, password=PASSWORD)
            cliente = Cliente.objects.create(
                numero_cliente=numero,
                nombre=NOMBRES[i],
                email=f"cliente{numero}@example.com",
                telefono="3464-000000",
                user=user,
            )
            self._cargar_movimientos(cliente)

        self.stdout.write(self.style.SUCCESS(
            f"Listo. {n} clientes creados ({numeros[0]} a {numeros[-1]}). "
            f"Contraseña de todos: {PASSWORD}"
        ))

    def _cargar_movimientos(self, cliente):
        especies = random.sample(ESPECIES, k=random.randint(1, 3))
        cosechas = random.sample(COSECHAS, k=random.randint(1, len(COSECHAS)))
        for cosecha in cosechas:
            for especie in especies:
                for _ in range(random.randint(2, 6)):  # camionadas de ingreso
                    Movimiento.objects.create(
                        cliente=cliente, fecha=self._fecha(cosecha), cosecha=cosecha,
                        especie=especie, tipo=Movimiento.Tipo.INGRESO,
                        kilos=random.randint(20, 250) * 1000,
                    )
                if random.random() < 0.6:  # a veces una venta/retiro
                    Movimiento.objects.create(
                        cliente=cliente, fecha=self._fecha(cosecha), cosecha=cosecha,
                        especie=especie, tipo=Movimiento.Tipo.EGRESO,
                        kilos=random.randint(10, 120) * 1000,
                    )

    def _fecha(self, cosecha):
        anio = 2000 + int(cosecha.split("/")[1])
        return date(anio, random.choice([3, 4, 5, 11, 12]), random.randint(1, 28))
