from django.test import TestCase
from django.contrib.auth.models import User
from books.forms import LoginForm, RegisterForm, OrderForm

class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )

    def test_login_form_valid(self):
        """Тест валидной формы входа"""
        form_data = {
            'email': 'existing@example.com',
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_email(self):
        """Тест формы входа с неверным email"""
        form_data = {
            'email': 'wrong@example.com',
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())  # Форма валидна, но пользователь не найден

    def test_register_form_valid(self):
        """Тест валидной формы регистрации"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_password_mismatch(self):
        """Тест формы регистрации с несовпадающими паролями"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_register_form_existing_username(self):
        """Тест формы регистрации с существующим именем пользователя"""
        form_data = {
            'username': 'existinguser',  # Уже существует
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_order_form_valid(self):
        """Тест валидной формы заказа"""
        form_data = {
            'full_name': 'Тестовый Пользователь',
            'address': 'Тестовый адрес доставки',
            'phone': '+79999999999',
            'payment_method': 'card'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        """Тест невалидной формы заказа"""
        form_data = {
            'full_name': '',  # Обязательное поле
            'address': 'Тестовый адрес',
            'phone': '+79999999999',
            'payment_method': 'card'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
