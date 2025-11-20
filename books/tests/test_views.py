from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Genre, Author, Book, Cart, CartItem

class ViewTests(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
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
            price=500.00
        )

    def test_home_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/home.html')
        self.assertContains(response, 'Книжный уголок')

    def test_catalog_view(self):
        """Тест страницы каталога"""
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/catalog.html')
        self.assertContains(response, 'Тестовая Книга')

    def test_catalog_search(self):
        """Тест поиска в каталоге"""
        response = self.client.get(reverse('catalog') + '?search=Тестовая')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая Книга')

    def test_login_view_get(self):
        """Тест GET запроса страницы входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/login.html')

    def test_login_view_post_success(self):
        """Тест успешного входа"""
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        # После успешного входа должен быть редирект на главную
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_login_view_post_failure(self):
        """Тест неуспешного входа"""
        response = self.client.post(reverse('login'), {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный email или пароль')

    def test_register_view_get(self):
        """Тест GET запроса страницы регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/register.html')

    def test_register_view_post_success(self):
        """Тест успешной регистрации"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        # После успешной регистрации должен быть редирект на главную
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_cart_view_authenticated(self):
        """Тест корзины для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/cart.html')

    def test_cart_view_unauthenticated(self):
        """Тест корзины для неавторизованного пользователя"""
        response = self.client.get(reverse('cart'))
        # Должен быть редирект на страницу входа
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_add_to_cart_ajax_authenticated(self):
        """Тест добавления в корзину через AJAX"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_to_cart_ajax'), {
            'book_id': self.book.id,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True, 'cart_count': 1}
        )

    def test_add_to_cart_ajax_unauthenticated(self):
        """Тест добавления в корзину без авторизации"""
        response = self.client.post(reverse('add_to_cart_ajax'), {
            'book_id': self.book.id,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': False, 'error': 'Not authenticated'}
        )

    def test_reading_view(self):
        """Тест страницы чтения книги"""
        response = self.client.get(reverse('reading', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/reading.html')
        self.assertContains(response, 'Тестовая Книга')

    def test_reading_view_invalid_book(self):
        """Тест страницы чтения несуществующей книги"""
        response = self.client.get(reverse('reading', args=[999]))
        self.assertEqual(response.status_code, 404)

class PaymentViewTests(TestCase):
    def setUp(self):
        """Настройка для тестов оплаты"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.genre = Genre.objects.create(name='Фантастика')
        self.author = Author.objects.create(name='Тестовый Автор')
        self.book = Book.objects.create(
            title='Тестовая Книга',
            author=self.author,
            genre=self.genre,
            price=500.00
        )

        # Создаем корзину с товарами
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, book=self.book, quantity=2)

    def test_payment_view_authenticated_with_items(self):
        """Тест страницы оплаты с товарами в корзине"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/payment.html')

    def test_payment_view_authenticated_empty_cart(self):
        """Тест страницы оплаты с пустой корзиной"""
        self.client.login(username='testuser', password='testpass123')
        # Очищаем корзину
        self.cart.items.all().delete()
        response = self.client.get(reverse('payment'))
        # Должен быть редирект на корзину
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart'))

    def test_payment_view_unauthenticated(self):
        """Тест страницы оплаты без авторизации"""
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
