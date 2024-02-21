from django.contrib import admin
from .models import *
from django.utils.html import format_html
#-------------------------------------------------------------------------
class ProductImageItemInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ('product',)
    fields = ('alt', 'is_main','image','image_tag')
    readonly_fields = ('image_tag',)


    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 50px; height: auto;" />'.format(obj.image.url))

    image_tag.short_description = 'Image'
#-------------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}
#-------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image_tag','price','available','updated','is_new')
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('available','created')
    list_editable = ('price',)
    raw_id_fields = ('category',)
    actions = ('make_available','make_unavailable','add_specific_color')
    inlines = (ProductImageItemInline,)

    def make_available(self,request,queryset):
        rows = queryset.update(available=True)
        self.message_user(request,f'{rows} updated')

    def make_unavailable(self,request,queryset):
        rows = queryset.update(available=False)
        self.message_user(request,f'{rows} updated')

    def add_specific_color(self, request, queryset):
        color = Color.objects.get(en='custom')
        for product in queryset:
            product.colors.add(color)
        self.message_user(request, f'The specific color has been added to selected products.')

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 50px; height: auto;" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

    make_available.short_description = 'make all available'
    add_specific_color.short_description = 'Add specific color to selected products'
#-------------------------------------------------------------------------
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(Color)
