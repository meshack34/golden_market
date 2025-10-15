from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductImage,
    Review,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Wishlist,
)

# -------------------------
# CATEGORY ADMIN
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("is_active", "parent")


# -------------------------
# PRODUCT IMAGE INLINE
# -------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# -------------------------
# PRODUCT ADMIN
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "is_featured")
    list_filter = ("is_active", "is_featured", "category")
    search_fields = ("name", "description", "sku")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


# -------------------------
# REVIEW ADMIN
# -------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username")


# -------------------------
# CART ADMIN
# -------------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at", "total_items", "total_price")
    inlines = [CartItemInline]


# -------------------------
# ORDER ADMIN
# -------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "status", "total_amount", "paid", "created_at")
    list_filter = ("status", "paid", "created_at")
    search_fields = ("order_id", "user__username")
    inlines = [OrderItemInline]


# -------------------------
# WISHLIST ADMIN
# -------------------------
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    filter_horizontal = ("products",)
