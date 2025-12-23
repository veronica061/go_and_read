import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.selenium
class TestCatalog:
    """Поиск и фильтрация книг"""

    def test_search_and_filter_books(self, browser, base_url, test_data):
        # Переход в каталог
        browser.get(base_url + '/catalog/')
        print("Перешли в каталог")

        # Ждем загрузки страницы
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "books-grid"))
        )

        # 1. Поиск книги
        search_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        search_term = "Тестовая"
        search_input.clear()
        search_input.send_keys(search_term)

        # Отправляем форму поиска
        search_input.submit()

        # Ждем обновления результатов
        time.sleep(2)

        # 2. Проверка результатов поиска
        search_results = browser.find_element(By.CLASS_NAME, "books-grid")
        book_cards_after_search = browser.find_elements(By.CLASS_NAME, "book-card")
        print(f"После поиска найдено {len(book_cards_after_search)} книг")

        # 3. Фильтрация по жанру
        genre_select = Select(browser.find_element(By.NAME, "genre"))
        available_genres = [option.text for option in genre_select.options if option.text]
        print(f"Доступные жанры: {available_genres}")

        if len(available_genres) > 1:
            # Выбираем первый непустой жанр
            genre_select.select_by_index(1)
            time.sleep(1)  # Ждем применения фильтра
            print("Применен фильтр по жанру")

        # 4. Сортировка
        sort_select = Select(browser.find_element(By.NAME, "sort"))
        sort_options = [option.text for option in sort_select.options if option.text]
        print(f"Доступные сортировки: {sort_options}")

        if "По цене (убывание)" in sort_options:
            sort_select.select_by_visible_text("По цене (убывание)")
            time.sleep(1)  # Ждем применения сортировки
            print("Применена сортировка по цене (убывание)")

        # 5. Проверяем отображение книг после фильтрации
        final_book_cards = browser.find_elements(By.CLASS_NAME, "book-card")
        print(f"После фильтрации отображается {len(final_book_cards)} книг")

        # 6. Проверяем элементы карточки книги
        if final_book_cards:
            book_card = final_book_cards[0]

            # Проверяем наличие основных элементов
            title_element = book_card.find_element(By.CLASS_NAME, "book-title")
            author_element = book_card.find_element(By.CLASS_NAME, "book-author")
            price_element = book_card.find_element(By.CLASS_NAME, "book-price")

            assert title_element.is_displayed(), "Заголовок книги не отображается"
            assert author_element.is_displayed(), "Автор книги не отображается"
            assert price_element.is_displayed(), "Цена книги не отображается"

            print(f"Карточка книги содержит: '{title_element.text}', автор: '{author_element.text}', цена: '{price_element.text}'")

            # Проверяем кнопку добавления в корзину
            try:
                add_to_cart_btn = book_card.find_element(By.CLASS_NAME, "add-to-cart-btn")
                assert add_to_cart_btn.is_displayed()
                print("Кнопка 'В корзину' отображается корректно")
            except:
                # Может быть ссылка для неавторизованных пользователей
                add_to_cart_link = book_card.find_element(By.XPATH, ".//a[contains(text(), 'В корзину')]")
                assert add_to_cart_link.is_displayed()
                print("Ссылка 'В корзину' отображается корректно")
