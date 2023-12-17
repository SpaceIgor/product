from django.contrib import admin
from .models import Shop, Product, Category, ProductImage

# Register your models here


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    filter_horizontal = ('categories',)

    class Meta:
        model = Product

    # def get_prepopulated_fields(self, request, obj=None):
    #     prepopulated_fields = super().get_prepopulated_fields(request, obj)
    #
    #     shop_type = obj.shop.type if obj and obj.shop else None
    #
    #     if shop_type is None:
    #         prepopulated_fields = {}
    #     else:
    #         category_names = Category.objects.filter(shop=shop_type).values_list('name', flat=True)
    #         prepopulated_fields['categories'] = tuple(category_names)
    #
    #     return prepopulated_fields


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude', 'sales_commission')


