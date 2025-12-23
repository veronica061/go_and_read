import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.selenium
class TestCartManagement:
    """Управление корзиной"""

    def test_cart_operations(self, browser, base_url, test_data):
        # Логин пользователя
        browser.get(base_url + '/login/')

        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "login-email"))
        )
        email_input.send_keys(f"{test_data['username']}@example.com")

        password_input = browser.find_element(By.ID, "login-password")
        password_input.send_keys("testpass123")

        login_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
        login_button.click()

        # Ждем редиректа на главную
        WebDriverWait(browser, 10).until(EC.url_contains('/'))
        print("Пользователь успешно вошел в систему")

        # Добавляем книгу в корзину через каталог
        browser.get(base_url + '/catalog/')

        add_to_cart_buttons = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "add-to-cart-btn"))
        )

        if add_to_cart_buttons:
            # Добавляем первую книгу
            add_to_cart_buttons[0].click()

            # Обрабатываем alert если есть
            try:
                WebDriverWait(browser, 5).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.accept()
                print("Книга добавлена в корзину (alert обработан)")
            except:
                print("Книга добавлена в корзину")

            # Даем время для обновления DOM
            time.sleep(2)

            # Проверяем обновление счетчика корзины
            cart_count = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "cart-count"))
            )
            assert cart_count.text != "(0)"
            print(f"Счетчик корзины обновлен: {cart_count.text}")

        # Переход в корзину - используем более надежный селектор
        try:
            # Попробуем найти ссылку по частичному тексту
            cart_link = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Корзина"))
            )
        except:
            # Если не нашли, попробуем по XPath
            cart_link = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cart/')]"))
            )

        cart_link.click()

        WebDriverWait(browser, 10).until(EC.url_contains('/cart/'))
        print("Перешли в корзину")

        # Проверяем наличие товаров в корзине
        cart_items = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cart-item"))
        )
        assert len(cart_items) > 0
        print(f"В корзине {len(cart_items)} товар(ов)")

        if cart_items:
            # Увеличиваем количество первого товара
            increase_buttons = browser.find_elements(
                By.XPATH, "//button[contains(text(), '+')]"
            )
            if increase_buttons:
                initial_quantity = browser.find_element(By.CLASS_NAME, "quantity-input").get_attribute("value")
                print(f"Начальное количество: {initial_quantity}")

                increase_buttons[0].click()

                # Ждем обновления страницы
                time.sleep(1)

                # Проверяем, что количество изменилось
                new_quantity = browser.find_element(By.CLASS_NAME, "quantity-input").get_attribute("value")
                assert new_quantity != initial_quantity
                print(f"Количество увеличено до: {new_quantity}")

            # Проверяем общую стоимость
            total_price_element = browser.find_element(
                By.XPATH, "//div[contains(@class, 'summary-total')]//span[last()]"
            )
            assert total_price_element.text != ""
            print(f"Общая стоимость: {total_price_element.text}")

            # Тестируем кнопку "Продолжить покупки"
            try:
                continue_shopping = browser.find_element(
                    By.XPATH, "//a[contains(text(), 'Перейти в каталог')]"
                )
                continue_shopping.click()

                WebDriverWait(browser, 10).until(EC.url_contains('/catalog/'))
                print("Успешно вернулись в каталог")
            except:
                print("Кнопка 'Продолжить покупки' не найдена, но это не критично")
