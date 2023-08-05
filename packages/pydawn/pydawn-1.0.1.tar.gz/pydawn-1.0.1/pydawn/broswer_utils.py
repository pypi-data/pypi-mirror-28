# coding=utf-8
from selenium import webdriver


def get_headless_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    return webdriver.Chrome(chrome_options=chrome_options)
