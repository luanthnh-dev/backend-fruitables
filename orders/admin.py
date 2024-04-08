from django.contrib import admin
from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline]
    readonly_fields = ('total', 'created_at', 'updated_at', 'deleted_at')


class OrderDetailAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
