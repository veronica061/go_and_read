from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from books.context_processors import cart_items_count
from books.models import Cart, CartItem, Book, Author, Genre

class ContextProcessorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Создаем тестовые данные
        genre = Genre.objects.create(name='Фантастика')
        author = Author.objects.create(name='Тестовый Автор')
        self.book = Book.objects.create(
            title='Тестовая Книга',
            author=author,
            genre=genre,
            price=500.00
        )

    def test_cart_items_count_authenticated(self):
        """Тест контекстного процессора для авторизованного пользователя"""
        request = self.factory.get('/')
        request.user = self.user

        # Создаем корзину с товарами
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, book=self.book, quantity=2)

        context = cart_items_count(request)
        self.assertEqual(context['cart_items_count'], 2)

    def test_cart_items_count_unauthenticated(self):
        """Тест контекстного процессора для неавторизованного пользователя"""
        request = self.factory.get('/')
        request.user = User()  # Анонимный пользователь

        context = cart_items_count(request)
        self.assertEqual(context['cart_items_count'], 0)

    def test_cart_items_count_empty_cart(self):
        """Тест контекстного процессора для пустой корзины"""
        request = self.factory.get('/')
        request.user = self.user

        # Создаем корзину без товаров
        Cart.objects.create(user=self.user)

        context = cart_items_count(request)
        self.assertEqual(context['cart_items_count'], 0)
