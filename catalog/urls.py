# catalog/urls.py
from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("search/", views.search_view, name="search"),

    # Cart
    path("cart/", views.cart_view, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    # Checkout / Orders
    path("checkout/", views.checkout_view, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

    # Wishlist
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
]
