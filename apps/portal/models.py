from django.conf import settings
from django.db import models


class Cliente(models.Model):
    """Productor del acopio.

    Es una proyección del cliente que ya existe en Mahon. El número de
    cliente es la clave del negocio y, además, se usa como nombre de
    usuario para el login.

    El vínculo con el usuario es opcional (null=True): se pueden importar
    clientes desde Mahon aunque todavía no tengan cuenta en el portal; la
    cuenta se crea después, solo para los que la van a usar.
    """

    numero_cliente = models.CharField("número de cliente", max_length=20, unique=True)
    nombre = models.CharField("nombre o razón social", max_length=200)
    email = models.EmailField(blank=True)
    telefono = models.CharField("teléfono", max_length=40, blank=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cliente",
    )

    class Meta:
        ordering = ["numero_cliente"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return f"{self.numero_cliente} — {self.nombre}"


class Movimiento(models.Model):
    """Movimiento de cuenta corriente de un cliente."""

    class Tipo(models.TextChoices):
        INGRESO = "ingreso", "Ingreso"
        EGRESO = "egreso", "Egreso"

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="movimientos")
    fecha = models.DateField()
    cosecha = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    kilos = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "movimiento"
        verbose_name_plural = "movimientos"

    def __str__(self):
        return f"{self.cliente.numero_cliente} - {self.especie} ({self.kilos} kg) el {self.fecha}"