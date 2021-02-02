#  Разработано: Meyer Dmitriy
#  Поддержка и сопровождение:
#  [Email] - meyerwork22@gmail.com
#  [Telegram] - https://t.me/meyerwork

from selenium import webdriver
import os
import time
from selenium.common.exceptions import NoSuchElementException


def set_browser_settings():   # НАСТРОЙКИ БРАУЗЕРА
    ua = '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) 
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'''   # юзерагент, вставляется одной строкой
    option = webdriver.FirefoxOptions()
    option.set_preference('dom.webdriver.enabled', False)  # скрывает автоматизацию
    # headless = option.add_argument("--headless")   # работа в фоновом режиме без запуска окна браузера (# = ВЫКЛ)
    return option

def account_get():
    directory = os.getcwd()  # путь к рабочей директории
    file = open(directory + '/accounts.txt', 'r')  # файл с аккаунтами
    return file

def account_login(_browser, _email, _password):   # ЛОГИНИМСЯ В АКК
    _browser.find_element_by_id('email').send_keys(_email)
    _browser.find_element_by_id('password').send_keys(_password)
    _browser.find_element_by_id('login-btn').click()
    time.sleep(2)

def account_quit(_browser):   # ВЫХОДИМ ИЗ АККАУНТА
    print('Выходим из аккаунта')
    _browser.find_element_by_id('header-profile').click()
    logoutBtn = _browser.find_element_by_id('logout-button')
    _browser.execute_script("arguments[0].click();", logoutBtn)
    time.sleep(5)

def check_modal(_browser):   # ПРОВЕРЯЕМ МОДАЛКУ С НОВЫМ СОГЛАШЕНИЕМ ООП (если не нужна, то комментить блок)
    try:
        modalOOP = _browser.find_element_by_xpath('//div[@class="flavr-message"]/h1')
    except NoSuchElementException:
        print('Модалки нет')
        time.sleep(1)
    else:
        if (modalOOP.is_displayed()):
            acceptBtn = _browser.find_element_by_xpath('//button[@rel="btn-accept"]')
            acceptBtn.click()
            print('Закрыли окно ОПП')
            time.sleep(2)
            _browser.get('https://www.eldarya.ru/')  # обновляем страницу чтобы убрать все вспл.окна
            time.sleep(1)
        else:
            print('Модалки нет')
            time.sleep(1)

def check_present(_browser, _email):   # ПРОВЕРЯЕМ НАЛИЧИЕ ПОДАРКА
    getGift = _browser.find_element_by_xpath(
        '//div[@id="daily-gift-container"]')  # элемент всегда есть в коде страницы, после нажатия на подарок становится display:none
    if (getGift.is_displayed()):
        getGift.click()
        time.sleep(3)
        thanksBtn = _browser.find_element_by_xpath('//button[@class="flavr-button default"]')
        thanksBtn.click()
        print('Забрали подарок для ', _email)
    else:
        print('Здесь подарка нет :(')
        time.sleep(1)

def check_winter_event(_browser):   # ПРОВЕРЯЕМ НАЛИЧИЕ ОКНА ЗИМНЕГО ИВЕНТА
    try:
        winter_event = _browser.find_element_by_xpath('//button["@id=go-to-event-button"]')
    except NoSuchElementException:
        print('Окна с ивентом нет')
        time.sleep(1)
    else:
        if (winter_event.is_displayed()):
            winter_event.click()
            print('Перешли в ивент')
            time.sleep(2)
            _browser.refresh()
            time.sleep(1)
        else:
            print('Окна с ивентом нет')
            time.sleep(1)

def browser_clear_cookies_and_refresh(_browser, _url):   # ЧИСТИМ КУКИ И ПЕРЕЗАХОДИМ НА СТРАНИЦУ
    print('Чистим куки')
    _browser.delete_all_cookies()
    _browser.get(_url)
    time.sleep(10)
    print('*' * 10)

def main():
    # ЗАПУСК БРАУЗЕРА
    set_browser_settings()
    url = 'https://www.eldarya.ru/login'  # адрес сайта, куда пойдем
    browser = webdriver.Firefox(options=set_browser_settings())
    browser.get(url)  # переход на страницу из переменной url
    time.sleep(2)

    # ПЕРЕБОР АККАУНТОВ ИЗ СПИСКА + ДЕЙСТВИЯ
    for line in account_get().readlines():
        line = line.strip()
        account = line.split(';')
        email = account[0]
        password = account[1]
        print('Акк:', email, ';', password)

        account_login(browser, email, password)
        check_modal(browser)
        check_winter_event(browser)
        check_present(browser, email)
        account_quit(browser)
        browser_clear_cookies_and_refresh(browser, url)

    browser.quit()  # Закрываем процесс webdriver
    print('Акки закончились! Программа завершена!', sep='')

main()   # Запуск программы