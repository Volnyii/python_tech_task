import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

"""
Необходимо Перейти на сайт https://ptable.com/?lang=ru и получить все элементы
периодической таблицы в виде списка экземпляров класса ChemicalElement
Экземпляр класса должен содержать в себе следующие атрибуты:
atomic: Порядковый номер в таблице
name: Название элемента
weight:атомная масса элемента
"""

"""Constants"""
DRIVER_PATH = os.path.dirname(os.path.abspath(__file__)) + "chromedriver_mac_arm64/chromedriver"
URL_LINK = "https://ptable.com/?lang=ru"
print(DRIVER_PATH)


class WebDriver:
    """Initialize web driver in different modes: headless or not"""

    def __init__(self, driver_path: str, headless_mode: bool = True):
        self.__driver_path = driver_path
        self.__headless_mode_status = headless_mode

    @property
    def initialize_driver(self):
        service = Service(self.__driver_path)
        return webdriver.Chrome(service=service, options=self.enable_headless_mode)

    @property
    def enable_headless_mode(self):
        chrome_options = Options()
        if self.__headless_mode_status:
            chrome_options.add_argument("--headless")
            return chrome_options


class PageUtils:
    """Base methods-helpers for all pages in project"""

    def __init__(self):
        self.__driver = driver

    def _open_page(self, url):
        self.__driver.get(url)
        return self

    def _find_element(self, *locator):
        return self.__driver.find_element(*locator)

    def _get_text_from_element(self, *locator):
        return self._find_element(*locator).text

    def _get_attribute(self, *locator):
        return self._find_element(*locator).text

    def _find_elements_by_selector(self, *locator) -> list:
        return self.__driver.find_elements(*locator)

    def close_browser(self):
        self.__driver.quit()
        return self


class PtableLocators:
    """Locators for page Ptable"""
    LAST_OBJECT_ON_PAGE = (By.XPATH, '//*[@id="CompoundArrows"]')
    ELEMENT_SELECTOR = (By.CSS_SELECTOR, '[data-atomic]')


class ElementLocators:
    """Locators for chemical elements"""
    ATOMIC = (By.TAG_NAME, "b")
    NAME = (By.TAG_NAME, "em")
    WEIGHT = (By.TAG_NAME, "data")
    WEIGHT_ATTRIBUTE = "data-abridged"


class PtablePage(PageUtils):
    """Description ptable page"""

    def __init__(self):
        super().__init__()
        self._locators = PtableLocators
        self.__chemical_element_list = None

    def open_ptable_page(self):
        self._open_page(URL_LINK)
        return self

    def find_last_element_on_page(self):
        self._find_element(*self._locators.LAST_OBJECT_ON_PAGE)
        return self

    def collect_chemical_elements_list(self):
        chemical_elements_list = []
        objects_with_data_atomic_list = self._find_elements_by_selector(*self._locators.ELEMENT_SELECTOR)
        for object in objects_with_data_atomic_list:
            chemical_elements_list.append(ChemicalElement(object))
        self.__chemical_element_list = chemical_elements_list
        return self

    def print_information_about_all_elements(self):
        if self.__chemical_element_list is None:
            raise Exception("First fill out the list of elements using the method 'collect_chemical_elements_list'!")
        for chemical_element in self.__chemical_element_list:
            chemical_element.print_element_info()
        return self


class ChemicalElement:
    """Filling an element entity with data:
    atomic: Serial number in table
    name: Element name
    weight: Atomic mass of element"""

    def __init__(self, element: WebElement):
        super().__init__()
        self.__element = element
        self.__locators = ElementLocators
        self.__atomic = self.__get_atomic
        self.__name = self.__get_name
        self.__weight = self.__get_weight

    @property
    def __get_atomic(self):
        return self.__element.find_element(*self.__locators.ATOMIC).text

    @property
    def __get_name(self):
        return self.__element.find_element(*self.__locators.NAME).text

    @property
    def __get_weight(self):
        return self.__element.find_element(*self.__locators.WEIGHT).get_attribute(self.__locators.WEIGHT_ATTRIBUTE)

    def print_element_info(self):
        print(f"Serial number in table: {self.__atomic}", f"Element name: {self.__name}",
              f"Atomic mass of element: {self.__atomic}", sep=", ", end=";\n")


if __name__ == "__main__":
    """"Driver initialization"""
    driver = (WebDriver(DRIVER_PATH)
              .initialize_driver)

    """Test 1"""
    (PtablePage()
     .open_ptable_page()
     .find_last_element_on_page()
     .collect_chemical_elements_list()
     .print_information_about_all_elements()
     .close_browser())
