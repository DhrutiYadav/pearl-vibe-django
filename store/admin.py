from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import Category, SubCategory, Product, Order, OrderItem
from .models import Customer, ShippingAddress, OrderSummary, Invoice


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")


# -------- Product Admin Form --------
class ProductAdminForm(forms.ModelForm):
    colors_input = forms.CharField(required=False, label="Colors")

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the input but keep the form-row visible
        self.fields["colors_input"].widget = forms.TextInput(
            attrs={"style": "display:none;"}
        )

        if self.instance and self.instance.colors:
            self.initial["colors_input"] = ",".join(self.instance.colors)

    def clean(self):
        cleaned_data = super().clean()
        raw_colors = self.data.getlist("colors_picker[]")

        if raw_colors:
            cleaned_data["colors"] = raw_colors

        return cleaned_data


# -------- Product Admin --------
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "subcategory", "price", "image_preview", "display_colors")
    readonly_fields = ("color_preview", "image_preview")
    exclude = ("colors",)  # hide raw JSON field

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}
        js = ("admin/js/multi_color_picker.js",)

    def save_model(self, request, obj, form, change):
        # Read final colors from hidden input (after add/delete)
        raw_colors = request.POST.get("colors_input", "")

        if raw_colors:
            obj.colors = [c.strip() for c in raw_colors.split(",") if c.strip()]
        else:
            obj.colors = []

        super().save_model(request, obj, form, change)

    def display_colors(self, obj):
        if not obj.colors:
            return "-"
        html = "".join(
            f"""
            <span class="color-chip" data-color="{c.strip()}"
                  style="display:inline-flex;align-items:center;
                  width:22px;height:22px;border-radius:50%;
                  background:{c.strip()};
                  border:1px solid #999;
                  margin-right:6px;cursor:pointer;">
            </span>
            """
            for c in obj.colors
        )
        return mark_safe(html)

    display_colors.short_description = "Colors"

    def color_preview(self, obj):
        if not obj.colors:
            return "-"
        html = "".join(
            f"""
            <span class="color-chip removable" data-color="{c.strip()}"
                  style="display:inline-flex;
                  align-items:center;
                  justify-content:center;
                  width:26px;height:26px;
                  border-radius:50%;
                  background:{c.strip()};
                  border:1px solid #666;
                  margin-right:6px;
                  cursor:pointer;
                  position:relative;">
                  <span style="color:white;font-size:14px;font-weight:bold;">×</span>
            </span>
            """
            for c in obj.colors
        )
        return mark_safe(html)

    color_preview.short_description = "Colors Preview"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" height="70" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Image"

    fields = (
        "subcategory",
        "name",
        "price",
        "image",
        "image_preview",  # 👈 preview right after image
        "digital",
        "description",
        "colors_input",
        "color_preview",
        "sizes",
    )


# -------- Order Admin --------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "complete", "date_ordered")
    list_filter = ("complete",)
    search_fields = ("customer__user__username",)
    inlines = [OrderItemInline]


# -------- OrderItem Admin --------
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "size", "color")
    list_filter = ("product", "size", "color")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "email")
    search_fields = ("name", "email", "user__username")


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order", "city", "state", "zipcode")
    list_filter = ("city", "state")
    search_fields = ("customer__name", "city", "zipcode")


class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ("order", "subtotal", "tax", "shipping_cost", "total", "updated_at")
    readonly_fields = ("updated_at",)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "order", "issued_date", "paid")
    list_filter = ("paid",)
    search_fields = ("invoice_number",)


# -------- Register Models --------
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(OrderSummary, OrderSummaryAdmin)
admin.site.register(Invoice, InvoiceAdmin)

admin.site.site_header = "Pearl Vibe"
admin.site.site_title = "Pearl Vibe"
admin.site.index_title = "Administration"
