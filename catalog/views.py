# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Wishlist

# ============== HOME ==============
def home_view(request):
    featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)
    return render(request, "home.html", {"featured": featured, "categories": categories})


# ============== CATEGORY PRODUCTS ==============
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, "product_list.html", {"category": category, "products": products})


# ============== PRODUCT DETAIL ==============
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]

    in_wishlist = False
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist and product in wishlist.products.all():
            in_wishlist = True

    return render(request, "product_detail.html", {
        "product": product,
        "related": related,
        "in_wishlist": in_wishlist
    })


# ============== SEARCH ==============
def search_view(request):
    query = request.GET.get("q")
    products = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )
    return render(request, "product_list.html", {"products": products, "query": query})


# ============== CART VIEWS ==============
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart_detail.html", {"cart": cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    messages.success(request, f"{product.name} added to your cart.")
    return redirect("catalog:cart_detail")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("catalog:cart_detail")


# ============== CHECKOUT & ORDERS ==============
@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")

        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            shipping_address=shipping_address,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price,
            )
        cart.items.all().delete()
        messages.success(request, "Order placed successfully!")
        return redirect("catalog:order_detail", order.id)

    return render(request, "checkout.html", {"cart": cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})


# ============== WISHLIST ==============
@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, "wishlist.html", {"products": products})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.info(request, f"{product.name} removed from wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"{product.name} added to wishlist.")

    return redirect(product.get_absolute_url())
