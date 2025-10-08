from django.contrib import admin
from .models import CategoriaMenu, Plato, Inventario, MovimientoInventario, ConfiguracionSistema

@admin.register(CategoriaMenu)
class CategoriaMenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'orden', 'activa', 'cantidad_platos')
    list_filter = ('activa',)
    search_fields = ('nombre',)
    ordering = ('orden',)

    def cantidad_platos(self, obj):
        return obj.platos.count()
    cantidad_platos.short_description = 'Cantidad de Platos'

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'precio_con_impuesto', 'disponible', 'tiempo_preparacion')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'categoria__nombre')
    list_editable = ('precio', 'disponible')
    ordering = ('categoria__orden', 'orden')

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'cantidad_actual', 'unidad', 'cantidad_minima', 'costo_unitario', 'esta_bajo', 'activo')
    list_filter = ('categoria', 'unidad', 'activo')
    search_fields = ('nombre', 'categoria', 'proveedor')
    list_editable = ('cantidad_actual', 'cantidad_minima', 'costo_unitario')
    readonly_fields = ('esta_bajo',)

    def esta_bajo(self, obj):
        return obj.esta_bajo
    esta_bajo.boolean = True
    esta_bajo.short_description = '¿Stock Bajo?'

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('inventario', 'tipo', 'cantidad', 'cantidad_anterior', 'cantidad_nueva', 'usuario', 'created_at')
    list_filter = ('tipo', 'created_at')
    search_fields = ('inventario__nombre', 'usuario__username', 'motivo')
    readonly_fields = ('cantidad_anterior', 'cantidad_nueva', 'created_at')

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre_restaurante', 'impuesto', 'porcentaje_propina', 'telefono', 'horario_apertura', 'horario_cierre')
    list_editable = ('impuesto', 'porcentaje_propina', 'horario_apertura', 'horario_cierre')

    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not ConfiguracionSistema.objects.exists()