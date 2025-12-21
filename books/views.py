from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Book, Cart, CartItem, Order, OrderItem, Genre
from .forms import LoginForm, RegisterForm, OrderForm

def home(request):
    featured_books = Book.objects.filter(is_available=True)[:4]
    return render(request, 'books/home.html', {
        'featured_books': featured_books
    })

def catalog(request):
    books = Book.objects.filter(is_available=True)
    genres = Genre.objects.all()
    return render(request, 'books/catalog.html', {
        'books': books,
        'genres': genres,
    })

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Упрощенная логика входа
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except User.DoesNotExist:
                pass
            form.add_error(None, 'Неверный email или пароль')
    else:
        form = LoginForm()
    return render(request, 'books/login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'books/register.html', {'form': form})

# Упрощенные функции с проверкой аутентификации
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'books/cart.html', {'cart': cart})

def update_cart_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif action == 'remove':
            cart_item.delete()

        return redirect('cart')

def payment(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = get_object_or_404(Cart, user=request.user)

    if cart.items.count() == 0:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.book.price
                )

            cart.items.all().delete()
            return render(request, 'books/payment_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'books/payment.html', {
        'form': form,
        'cart': cart
    })

def reading(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/reading.html', {'book': book})

def add_to_cart_ajax(request):
    if request.method == 'POST' and request.user.is_authenticated:
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))

        book = get_object_or_404(Book, id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, book=book,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_items()
        })

    return JsonResponse({'success': False, 'error': 'Not authenticated'})
