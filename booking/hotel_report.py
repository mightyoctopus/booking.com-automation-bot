from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class HotelReport:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.name_list = []
        self.price_list = []
        self.star_rating_list = []
        self.report_form = []

    def extract_search_results(self):
        try:
            listing_boxes = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label="Property card"]'))
            )
            print(f"Listing Boxes: {len(listing_boxes)} listings")

            for listing in listing_boxes:
                try:
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", listing)

                    name_element = listing.find_element(By.XPATH, './/h2[@data-testid="header-title"]')
                    name = name_element.text.strip()
                    # print("NAME: ", name)
                    self.name_list.append(name)

                    price_element = listing.find_element(By.XPATH, './/span[@data-testid="price-and-discounted-price"]')
                    price = price_element.text.strip()
                    # print("PRICE: ", price)
                    self.price_list.append(price)

                    try:
                        star_rating_element = listing.find_element(By.XPATH, './/span[@data-testid="rating-stars"]')
                        aria_label_element = star_rating_element.get_attribute("aria-label").strip().split(" ")
                        star_rating = aria_label_element[0] if aria_label_element[0] else "N/A"
                        self.star_rating_list.append(star_rating)
                    except NoSuchElementException:
                        star_rating = "N/A"
                        # print("Star rating not found, just set to N/A")
                        self.star_rating_list.append(star_rating)

                    # print("Star Rating: ", star_rating)

                except (StaleElementReferenceException, NoSuchElementException) as e:
                    print(f"Failed to extract listing value: {e}")

        except Exception as e:
            print("Error occurred during extracting search results", e)


    # def format_report_data(self):
    #     for n in range(len(self.name_list)):
    #         self.report_form.append(
    #             (self.name_list[n], self.price_list[n], self.star_rating_list[n])
    #         )
    #     print("Report data has been formatted!")
