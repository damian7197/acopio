import pytest


@pytest.mark.skip(reason="Pendiente: implementar cuando exista el modelo de cuenta corriente")
def test_un_cliente_no_ve_el_resumen_de_otro():
    """Test de aislamiento (el más importante del portal).

    Un usuario autenticado NUNCA debe poder acceder al resumen de cuenta
    de otro cliente, ni cambiando un id en la URL. Se implementa cuando
    exista el modelo de datos del cereal.
    """
    ...
