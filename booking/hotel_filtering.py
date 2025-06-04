# This file includes a class with instance methods
# that will be responsible for filtering hotel conditions.
# e.g. search 5-star hotels etc
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


class HotelFiltering:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_ratings(self, *star_values):
        star_filter_box = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-filters-group='class']"))
        )
        time.sleep(1)
        star_filter_child_elements = star_filter_box.find_elements(By.CSS_SELECTOR, "*")
        print(len(star_filter_child_elements))

        for star_value in star_values:
            for star_element in star_filter_child_elements:
                if str(star_element.get_attribute("innerHTML")).strip() == f"{star_value} stars":
                    print("Star element found: ", str(star_element.get_attribute("innerHTML")).strip())

                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.element_to_be_clickable(star_element)
                        )

                        ActionChains(self.driver).move_to_element(star_element).perform()
                        time.sleep(1)

                        # Try a normal click first and if it fails, execute javascript and click its element.
                        try:
                            star_element.click()
                        except ElementClickInterceptedException:
                            print("Normal click failed. Using JS click instead.")
                            self.driver.execute_script("arguments[0].click();", star_element)

                    except StaleElementReferenceException as e:
                        print(f"Element updated, so it needs to find the element again: {e}")


    def set_lowest_prices_first(self):

        ## Click the Sort By button
        try:
            sort_by_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='sorters-dropdown-trigger']"))
            )
            ActionChains(self.driver).move_to_element(sort_by_btn).perform()
            time.sleep(1)

            try:
                sort_by_btn.click()
            except ElementClickInterceptedException:
                print("Normal click failed. Using JS click instead.")
                self.driver.execute_script("arguments[0].click();", sort_by_btn)
        except StaleElementReferenceException as e:
            print(f"Element updated, so it needs to find the element again: {e}")

        # Click lowest price first button in the sort by menu
        try:
            lowest_first_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Price (lowest first)']"))
            )
            lowest_first_btn.click()
            print("Lowest_price_first_btn clicked!")
        except Exception as e:
            print(f"Failed to click lowest price first btn: {e}")
