import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.selenium
class TestAuthentication:
    """Процесс аутентификации"""
    
    def test_auth_process(self, browser, base_url):
        # 1. Регистрация нового пользователя
        browser.get(base_url + '/register/')
        
        timestamp = str(int(time.time() * 1000))[-6:]
        username = f"selenium_user_{timestamp}"
        email = f"{username}@example.com"
        password = "SeleniumPass123"
        
        # Заполняем форму регистрации
        username_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "register-name"))
        )
        username_input.send_keys(username)
        
        email_input = browser.find_element(By.ID, "register-email")
        email_input.send_keys(email)
        
        password_input = browser.find_element(By.ID, "register-password")
        password_input.send_keys(password)
        
        confirm_input = browser.find_element(By.ID, "register-confirm")
        confirm_input.send_keys(password)
        
        # Отправляем форму
        submit_button = browser.find_element(
            By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]"
        )
        submit_button.click()
        
        # 2. Проверка автоматического входа и редиректа
        WebDriverWait(browser, 10).until(
            EC.url_contains('/')
        )
        
        user_greeting = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Привет,')]"))
        )
        assert username in user_greeting.text
        print("Пользователь успешно зарегистрирован и вошел в систему")
        
        # 3. Выход из системы
        logout_link = browser.find_element(By.LINK_TEXT, "Выйти")
        logout_link.click()
        
        # Проверяем редирект на главную
        WebDriverWait(browser, 10).until(
            EC.url_contains('/')
        )
        
        # Проверяем, что появились ссылки входа/регистрации
        login_link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Вход"))
        )
        register_link = browser.find_element(By.LINK_TEXT, "Регистрация")
        
        assert login_link.is_displayed()
        assert register_link.is_displayed()
        print("Пользователь успешно вышел из системы")
        
        # 4. Вход с созданными учетными данными
        login_link.click()
        
        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "login-email"))
        )
        email_input.send_keys(email)
        
        password_input = browser.find_element(By.ID, "login-password")
        password_input.send_keys(password)
        
        login_button = browser.find_element(
            By.XPATH, "//button[contains(text(), 'Войти')]"
        )
        login_button.click()
        
        # 5. Проверка успешного входа
        WebDriverWait(browser, 10).until(
            EC.url_contains('/')
        )
        
        user_greeting = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Привет,')]"))
        )
        assert username in user_greeting.text
        print("Пользователь успешно вошел в систему")
