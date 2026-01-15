from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Category, SubCategory, Product


# -------- Product Admin Form --------
class ProductAdminForm(forms.ModelForm):
    default_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'style': 'width:40px;height:40px;padding:0;border:none;'
        })
    )

    class Meta:
        model = Product
        fields = '__all__'



# -------- Product Admin --------
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'subcategory', 'price', 'display_colors')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def display_colors(self, obj):
        if not obj.colors:
            return "-"
        html = ""
        for color in obj.colors:
            html += (
                f'<span style="display:inline-block;'
                f'width:18px;height:18px;'
                f'border-radius:50%;'
                f'background:{color};'
                f'border:1px solid #999;'
                f'margin-right:4px;"></span>'
            )
        return mark_safe(html)



# -------- Register Models --------
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)

admin.site.site_header = "Pearl Vibe Admin Panel"
admin.site.site_title = "Pearl Vibe Admin"
admin.site.index_title = "Administration"
