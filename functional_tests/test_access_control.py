import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.selenium
class TestAccessControl:
    """Оформление заказа без авторизации"""
    
    def test_unauthorized_access(self, browser, base_url):
        # Убедимся, что пользователь не авторизован (выход если нужно)
        browser.get(base_url + '/logout/')
        
        # 1. Попытка доступа к корзине
        browser.get(base_url + '/cart/')
        
        # 2. Проверка редиректа на страницу входа
        WebDriverWait(browser, 10).until(
            EC.url_contains('/login/')
        )
        assert "login" in browser.current_url
        print("Корзина недоступна без авторизации")
        
        # 3. Попытка прямого доступа к оплате
        browser.get(base_url + '/payment/')
        
        # 4. Проверка редиректа на страницу входа
        WebDriverWait(browser, 10).until(
            EC.url_contains('/login/')
        )
        assert "login" in browser.current_url
        print("Оплата недоступна без авторизации")
        
        # 5. Попытка добавить в корзину из каталога
        browser.get(base_url + '/catalog/')
        
        add_to_cart_links = browser.find_elements(
            By.XPATH, "//a[contains(text(), 'В корзину')]"
        )
        if add_to_cart_links:
            add_to_cart_links[0].click()
            
            # 6. Проверка редиректа на страницу входа
            WebDriverWait(browser, 10).until(
                EC.url_contains('/login/')
            )
            assert "login" in browser.current_url
            print("Добавление в корзину недоступно без авторизации")
