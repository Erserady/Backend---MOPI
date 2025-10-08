from django.contrib import admin
from .models import Caja, Factura, Pago, CierreCaja

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('numero_caja', 'estado', 'saldo_inicial', 'saldo_actual', 'usuario_apertura', 'fecha_apertura', 'fecha_cierre')
    list_filter = ('estado', 'fecha_apertura')
    search_fields = ('numero_caja', 'usuario_apertura__username')
    readonly_fields = ('saldo_actual', 'fecha_apertura', 'fecha_cierre')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'table', 'subtotal', 'impuestos', 'total', 'metodo_pago', 'estado', 'creado_por', 'created_at')
    list_filter = ('estado', 'metodo_pago', 'created_at')
    search_fields = ('numero_factura', 'table__mesa_id', 'creado_por__username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('orders',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'monto', 'metodo_pago', 'referencia', 'caja', 'creado_por', 'created_at')
    list_filter = ('metodo_pago', 'created_at')
    search_fields = ('factura__numero_factura', 'creado_por__username', 'referencia')
    readonly_fields = ('created_at',)

@admin.register(CierreCaja)
class CierreCajaAdmin(admin.ModelAdmin):
    list_display = ('caja', 'fecha_cierre', 'saldo_final', 'saldo_teorico', 'diferencia', 'cerrado_por')
    list_filter = ('fecha_cierre',)
    search_fields = ('caja__numero_caja', 'cerrado_por__username')
    readonly_fields = ('fecha_cierre',)