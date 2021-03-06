from .pages.product_page import ProductPage
from .pages.base_page import BasePage
from .pages.basket_page import BasketPage
from .pages.login_page import LoginPage
import pytest
import time


class TestUserAddToBasketFromProductPage():
	@pytest.fixture(scope="function", autouse=True)
	def setup(self, browser):
		# открыть страницу регистрации
		self.link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
		self.page = BasePage(browser, self.link)
		self.page.open() 
		self.page.go_to_login_page()
		# зарегистрировать нового пользователя
		self.login_page = LoginPage(browser, browser.current_url)
		email = str(time.time()) + "@fakemail.org"
		self.login_page.register_new_user(email, "ybd5shla8")
		# проверить, что пользователь залогинен
		self.login_page.should_be_authorized_user()

	@pytest.mark.need_review
	def test_user_can_add_product_to_basket(self, browser):
		link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
		page = ProductPage(browser, link)
		page.open() 
		book_title = page.get_book_title() # получить название книги
		book_price = page.get_book_price() # получить цену книги
		page.add_to_basket() # добавить в корзину
		book_title_in_basket = page.book_title_in_basket() # получить название книги, которая добавлена в корзину
		book_price_in_basket = page.book_price_in_basket() # получить цену книги, которая добавлена в корзину
		# проверить, что название и цена книги, которую добавляли в корзину, совпадает с названием и ценой книги, которая добавлена в корзину
		page.books_are_equal(book_title, book_title_in_basket, book_price, book_price_in_basket)

	# НЕ добавляем товар в корзину и проверяем, что нет сообщения об успешном добавлении товара (это работающий тест)
	def test_user_cant_see_success_message(self, browser):
		link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
		page = ProductPage(browser, link)
		page.open() 
		page.should_not_be_success_message()

# незарегистрированный пользователь может добавить книги в корзину на страницах с промо-акцией
@pytest.mark.need_review
@pytest.mark.parametrize('link', ["http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
                                  pytest.param("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7", marks=pytest.mark.xfail), # этот тест падает. отметили его как xfail
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
                                  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9"])
def test_guest_can_add_product_to_basket(browser, link):
	link = link
	page = ProductPage(browser, link)
	page.open() 
	book_title = page.get_book_title() # получить название книги
	book_price = page.get_book_price() # получить цену книги
	page.add_to_basket() # добавить в корзину
	page.solve_quiz_and_get_code() # пройти задание в алерте
	time.sleep(2)
	book_title_in_basket = page.book_title_in_basket() # получить название книги, которая добавлена в корзину
	book_price_in_basket = page.book_price_in_basket() # получить цену книги, которая добавлена в корзину

# Добавляем товар в корзину и проверяем, что нет сообщения об успешном добавлении товара (это падающий тест - сообщение должно быть)
@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
	link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
	page = ProductPage(browser, link)
	page.open() 
	page.add_to_basket() # добавить в корзину
	# Проверяем, что нет сообщения об успехе с помощью is_not_element_present
	page.should_not_be_success_message()

# Проверяем, что сообщение об успешном добавлении товара в корзину исзечает (это падающий тест - сообщение не должно исчезать)
@pytest.mark.xfail
def test_message_disappeared_after_adding_product_to_basket(browser):
	link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
	page = ProductPage(browser, link)
	page.open() 
	page.add_to_basket() # добавить в корзину
	# Проверяем, что нет сообщения об успехе с помощью is_disappeared
	page.message_is_disappeared()

# Гость должен видеть ссылку на страницу логина
def test_guest_should_see_login_link_on_product_page(browser):
	link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
	page = ProductPage(browser, link)
	page.open()
	page.should_be_login_link()

# Гость может перейти на страницу логина
@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
	link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
	page = ProductPage(browser, link)
	page.open()
	page.go_to_login_page()

@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
	link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
	page = BasePage(browser, link)
	page.open()
	# Гость переходит в корзину по кнопке в шапке 
	page.go_to_basket_page()
	# Ожидаем, что в корзине нет товаров
	basket_page = BasketPage(browser, browser.current_url)
	basket_page.open()
	basket_page.should_not_be_items_in_basket() 
	# Ожидаем, что есть текст о том что корзина пуста
	basket_page.message_basket_is_empty()


