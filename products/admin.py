from django.contrib import admin
from .models import Category, Product, ProductImage, ProductComment


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')


class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')


class ProductCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
