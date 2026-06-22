from django.contrib import admin

from .models import Cliente, Movimiento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("numero_cliente", "nombre", "email", "user")
    search_fields = ("numero_cliente", "nombre")


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("fecha", "cliente", "especie", "tipo", "kilos")
    list_filter = ("tipo", "especie", "cosecha")
    search_fields = ("cliente__numero_cliente", "cliente__nombre")