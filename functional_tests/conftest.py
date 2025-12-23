import pytest
import time
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from books.models import Genre, Author, Book

@pytest.fixture(scope="function")
def browser():
    """Фикстура для создания браузера"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Раскомментируйте для запуска без GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.implicitly_wait(10)

        yield driver
        driver.quit()
    except Exception as e:
        pytest.skip(f"Не удалось запустить браузер: {e}")

@pytest.fixture
def test_data(db):
    """Фикстура для тестовых данных с уникальными именами"""
    timestamp = str(int(time.time() * 1000))[-6:]
    username = f'testuser_{timestamp}'

    user = User.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password='testpass123'
    )

    genre = Genre.objects.create(name=f'Фантастика_{timestamp}')
    author = Author.objects.create(name=f'Тестовый Автор_{timestamp}')

    book = Book.objects.create(
        title=f'Тестовая Книга_{timestamp}',
        author=author,
        genre=genre,
        price=500.00,
        is_available=True
    )

    return {
        'user': user,
        'genre': genre,
        'author': author,
        'book': book,
        'username': username
    }

@pytest.fixture
def base_url(live_server):
    """Фикстура для базового URL тестового сервера"""
    return live_server.url
