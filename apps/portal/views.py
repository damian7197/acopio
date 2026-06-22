from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Cliente


@login_required
def resumen(request):
    # El cliente sale SIEMPRE del usuario logueado, nunca de la URL.
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        return render(request, "portal/sin_cuenta.html")

    # .movimientos ya viene filtrado a este cliente por el related_name.
    movimientos = cliente.movimientos.all()

    # Saldo neto (ingresos - egresos) por cosecha y especie.
    acumulado = {}
    for m in movimientos:
        clave = (m.cosecha, m.especie)
        signo = 1 if m.tipo == m.Tipo.INGRESO else -1
        acumulado[clave] = acumulado.get(clave, 0) + signo * m.kilos

    saldos = [
        {"cosecha": cosecha, "especie": especie, "kilos": kilos}
        for (cosecha, especie), kilos in sorted(acumulado.items())
    ]

    return render(request, "portal/resumen.html", {
        "cliente": cliente,
        "saldos": saldos,
        "movimientos": movimientos,
    })
