import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

options = uc.ChromeOptions()
options.add_argument("--disable=popup-blocking")

driver =uc.Chrome(options=options, enable_cdp_events=True)
stealth(
    driver,
    vendor="Google Inc. ",
    platform="MacIntel",
    webgl_vendor="Apple Inc.",
    renderer="Apple M1",
    fix_hairline=True,
)

driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

driver.get("")
driver.implicitly_wait(2)

try:
    no_btn_for_popup_ad = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "at-cm-no-button"))
    )
    no_btn_for_popup_ad.click()
except Exception as e:
    print(f"Popup ad No Button not found or not clickable: {e} -- Just continuing...")

sum1 = driver.find_element(By.ID, "sum1")
sum2 = driver.find_element(By.ID, "sum2")

# Both do the same: 15
sum1.send_keys(Keys.NUMPAD1, Keys.NUMPAD5)
sum2.send_keys(15)

submit_btn = driver.find_element(
    By.CSS_SELECTOR,
    "button[onclick='return total()']"
)
submit_btn.click()

































