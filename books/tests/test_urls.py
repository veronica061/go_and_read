from django.test import TestCase
from django.urls import reverse, resolve
from books import views

class URLTests(TestCase):
    def test_home_url(self):
        """Тест URL главной страницы"""
        url = reverse('home')
        self.assertEqual(url, '/')
        self.assertEqual(resolve(url).func, views.home)

    def test_catalog_url(self):
        """Тест URL каталога"""
        url = reverse('catalog')
        self.assertEqual(url, '/catalog/')
        self.assertEqual(resolve(url).func, views.catalog)

    def test_login_url(self):
        """Тест URL входа"""
        url = reverse('login')
        self.assertEqual(url, '/login/')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_register_url(self):
        """Тест URL регистрации"""
        url = reverse('register')
        self.assertEqual(url, '/register/')
        self.assertEqual(resolve(url).func, views.user_register)

    def test_cart_url(self):
        """Тест URL корзины"""
        url = reverse('cart')
        self.assertEqual(url, '/cart/')
        self.assertEqual(resolve(url).func, views.cart_view)

    def test_payment_url(self):
        """Тест URL оплаты"""
        url = reverse('payment')
        self.assertEqual(url, '/payment/')
        self.assertEqual(resolve(url).func, views.payment)

    def test_reading_url(self):
        """Тест URL чтения книги"""
        url = reverse('reading', args=[1])
        self.assertEqual(url, '/reading/1/')
        self.assertEqual(resolve(url).func, views.reading)
