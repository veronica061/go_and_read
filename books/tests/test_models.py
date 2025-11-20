from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from books.models import Genre, Author, Book, Cart, CartItem, Order, OrderItem

class ModelTests(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.genre = Genre.objects.create(name='Фантастика')
        self.author = Author.objects.create(name='Тестовый Автор')
        self.book = Book.objects.create(
            title='Тестовая Книга',
            author=self.author,
            genre=self.genre,
            description='Тестовое описание',
            price=500.00,
            is_available=True
        )

    def test_genre_creation(self):
        """Тест создания жанра"""
        self.assertEqual(str(self.genre), 'Фантастика')
        self.assertEqual(Genre.objects.count(), 1)

    def test_author_creation(self):
        """Тест создания автора"""
        self.assertEqual(str(self.author), 'Тестовый Автор')
        self.assertEqual(Author.objects.count(), 1)

    def test_book_creation(self):
        """Тест создания книги"""
        self.assertEqual(str(self.book), 'Тестовая Книга - Тестовый Автор')
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.price, 500.00)
        self.assertTrue(self.book.is_available)

    def test_book_negative_price_validation(self):
        """Тест валидации отрицательной цены"""
        book = Book(
            title='Книга с отрицательной ценой',
            author=self.author,
            genre=self.genre,
            price=-100.00
        )
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_cart_creation(self):
        """Тест создания корзины"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), f"Корзина пользователя {self.user.username}")
        self.assertEqual(Cart.objects.count(), 1)

    def test_cart_item_creation(self):
        """Тест создания элемента корзины"""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2
        )
        self.assertEqual(str(cart_item), f"2 x {self.book.title}")
        self.assertEqual(cart_item.get_total_price(), 1000.00)

    def test_cart_total_price(self):
        """Тест расчета общей стоимости корзины"""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, book=self.book, quantity=2)

        # Создаем вторую книгу
        book2 = Book.objects.create(
            title='Вторая книга',
            author=self.author,
            genre=self.genre,
            price=300.00
        )
        CartItem.objects.create(cart=cart, book=book2, quantity=1)

        self.assertEqual(cart.get_total_price(), 1300.00)
        self.assertEqual(cart.get_total_items(), 3)

    def test_order_creation(self):
        """Тест создания заказа"""
        order = Order.objects.create(
            user=self.user,
            full_name='Тестовый Пользователь',
            address='Тестовый адрес',
            phone='+79999999999',
            payment_method='card',
            total_price=1000.00
        )
        self.assertEqual(str(order), f"Заказ #{order.id} - {self.user.username}")
        self.assertEqual(Order.objects.count(), 1)

    def test_order_item_creation(self):
        """Тест создания элемента заказа"""
        order = Order.objects.create(
            user=self.user,
            full_name='Тестовый Пользователь',
            address='Тестовый адрес',
            phone='+79999999999',
            payment_method='card',
            total_price=1000.00
        )
        order_item = OrderItem.objects.create(
            order=order,
            book=self.book,
            quantity=2,
            price=500.00
        )
        self.assertEqual(str(order_item), f"2 x {self.book.title}")
        self.assertEqual(order_item.get_total_price(), 1000.00)
