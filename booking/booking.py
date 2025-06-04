import time
from time import sleep

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

import booking.constants as const
from booking.hotel_filtering import HotelFiltering
from booking.hotel_report import HotelReport
from csv_processing.csv_processing import CsvProcessing


class Booking(uc.Chrome):
    def __init__(self, teardown=False, **kwargs):
        options = uc.ChromeOptions()
        options.add_argument("--disable=popup-blocking")

        super(Booking, self).__init__(options=options, enable_cdp_events=True, **kwargs)

        stealth(
            self,
            vendor="Google Inc.",
            platform="MacIntel",
            webgl_vendor="Apple Inc.",
            renderer="Apple M1",
            fix_hairline=True,
        )

        self.implicitly_wait(2)
        self.execute_script("""
                            Object.defineProperty(navigator, 'plugins', {
                                get: function() {
                                    return [1, 2, 3, 4, 5];
                                },
                            });
                        """)
        self.teardown = teardown

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def set_currency(self, currency=None):

        try:
            currency_btn = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']")
                )
            )
            currency_btn.click()

        except Exception as e:
            # Relocate element again right before click to avoid stale reference
            currency_btn = self.find_element(
                By.CSS_SELECTOR,
                "button[data-testid='header-currency-picker-trigger']"
            )

            WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']")
                )
            )
            currency_btn.click()

        try:
            currency_selection_btn = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//button[.//span[contains(@class, 'Picker_selection-text') and contains(text(), '{currency}')]]"
                    )
                )
            )
            currency_selection_btn.click()
        except Exception as e:
            print(f"Element not found -- currency selection: {e}")


    def select_destination(self, destination):
        destination_bar = self.find_element(By.NAME, "ss")
        time.sleep(1)
        destination_bar.send_keys(destination)

        time.sleep(1)
        first_result = self.find_element(By.ID, "autocomplete-result-0")
        first_result.click()


    def select_dates(self, check_in_date, check_out_date):
        check_in_selector = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[span[@data-date='{check_in_date}']]"))
        )
        check_in_selector.click()

        check_out_selector = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[span[@data-date='{check_out_date}']]"))
        )
        check_out_selector.click()

    def press_company_members_bar(self):
        self.find_element(By.CSS_SELECTOR, "button[aria-label*='Number of travelers and rooms.']").click()

    def select_adults(self, num_of_adults:int):
        time.sleep(0.5)

        groups = self.find_elements(By.XPATH, "//div[@class='e301a14002']")

        # Adults Section Buttons
        adult_decrease = groups[0].find_elements(By.XPATH, ".//button")[0]
        adult_increase = groups[0].find_elements(By.XPATH, ".//button")[1]

        adult_number_display = WebDriverWait(self, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='e301a14002'][1]//span[contains(@class, 'e32aa465fd')]"))
        )
        print(adult_number_display.text)

        current_adults = int(adult_number_display.text)
        while current_adults < num_of_adults:
            adult_increase.click()
            time.sleep(0.5)
            current_adults = int(adult_number_display.text)

        while current_adults > num_of_adults:
            adult_decrease.click()
            time.sleep(0.5)
            current_adults = int(adult_number_display.text)

    def select_rooms(self, num_of_rooms: int):
        time.sleep(0.5)

        groups = self.find_elements(By.XPATH, "//div[@class='e301a14002']")

        room_decrease = groups[2].find_elements(By.XPATH, ".//button")[0]
        room_increase = groups[2].find_elements(By.XPATH, ".//button")[1]

        room_number_display = groups[2].find_element(By.XPATH, ".//span[contains(@class, 'e32aa465fd')]")
        # print(room_number_display.text)

        current_rooms = int(room_number_display.text)
        while current_rooms < num_of_rooms:
            room_increase.click()
            time.sleep(0.5)
            current_rooms = int(room_number_display.text)

        while current_rooms > num_of_rooms:
            room_decrease.click()
            time.sleep(0.5)
            current_rooms = int(room_number_display.text)


    def hit_search_btn(self):
        sleep(1)
        self.find_element(By.XPATH, '//button[span[text()="Search"]]').click()
        print("Search button has been clicked!")

    def apply_filtering(self):
        hotel_filter = HotelFiltering(driver=self)
        hotel_filter.apply_star_ratings(3, 4, 5)
        hotel_filter.set_lowest_prices_first()

    def report_results(self):
        report = HotelReport(driver=self)
        report.extract_search_results()

        csv = CsvProcessing(report.name_list, report.price_list, report.star_rating_list)
        csv.save_data_into_csv()




# aria-label="Property card"











#========================= Select Number 0f Children ==================#

# def select_children(self, num_of_kids:int):
    #     time.sleep(0.5)
    #
    #     groups = self.find_elements(By.XPATH, "//div[@class='e301a14002']")
    #     children_decrease = groups[1].find_elements(By.XPATH, ".//button")[0]
    #     children_increase = groups[1].find_elements(By.XPATH, ".//button")[1]
    #
    #     children_number_display = WebDriverWait(self, 5).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, ".//span[contains(@class, 'e32aa465fd')]"))
    #     )
    #     print(children_number_display.text)
    #
    #     current_children = int(children_number_display.text)
    #     while current_children < num_of_kids:
    #         children_increase.click()
    #         time.sleep(0.5)
    #         current_children = int(children_number_display.text)
    #
    #     while current_children > num_of_kids:
    #         children_decrease.click()
    #         time.sleep(0.5)
    #         current_children = int(children_number_display.text)