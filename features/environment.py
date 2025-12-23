# features/environment.py
import os
import django
from django.test import Client
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_corner.settings')
django.setup()

def before_all(context):
    """Выполняется перед всеми тестами"""
    # Создаем тестовый клиент Django
    context.client = Client()
    context.base_url = 'http://testserver'

    # Создаем тестовую базу данных
    connection.creation.create_test_db(verbosity=1)

def after_all(context):
    """Выполняется после всех тестов"""
    # Удаляем тестовую базу данных
    connection.creation.destroy_test_db('test_db', verbosity=1)

def before_feature(context, feature):
    """Выполняется перед каждым feature"""
    pass

def after_feature(context, feature):
    """Выполняется после каждого feature"""
    pass

def before_scenario(context, scenario):
    """Выполняется перед каждым сценарием"""
    # Сбрасываем состояние перед каждым сценарием
    context.user = None
    context.response = None
    context.current_page = None

def after_scenario(context, scenario):
    """Выполняется после каждого сценария"""
    # Очищаем данные после сценария
    from django.contrib.auth.models import User
    from books.models import Book, Author, Genre, Cart, CartItem, Order, OrderItem

    # Удаляем тестовые данные
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    Genre.objects.all().delete()
    User.objects.filter(username__in=['testuser123', 'existing', 'testuser']).delete()

# Функция для получения URL
def get_url(context, path):
    """Вспомогательная функция для получения полного URL"""
    return context.base_url + path
