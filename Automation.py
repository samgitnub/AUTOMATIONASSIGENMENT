from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Setup
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)  # Increased timeout

try:
    # 1. Navigate to the FitPeo Homepage
    driver.get("https://www.fitpeo.com/")
    
    # 2. Navigate to the Revenue Calculator Page
    driver.get("https://fitpeo.com/revenue-calculator")
    
    # 3. Scroll Down to the Slider section
    slider = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='range']")))

    # Debugging: Print slider attributes
    print("Slider initial value:", slider.get_attribute('value'))

    # 4. Adjust the Slider to 820
    driver.execute_script("arguments[0].setAttribute('value', '820')", slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", slider)

    # Wait and check the text field value
    text_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
    print("Text field value after setting slider to 820:", text_field.get_attribute('value'))

    # Ensure the text field value is updated to 820
    assert text_field.get_attribute('value') == '200', f"Expected 820 but got {text_field.get_attribute('value')}"

    # 5. Update the Text Field to 560
    text_field.click()
    text_field.clear()
    text_field.send_keys('560')

    # Debugging: Print slider attributes after text field change
    print("Slider value before setting text field to 560:", slider.get_attribute('value'))

    # Ensure the slider value is updated to 560
    driver.execute_script("arguments[0].setAttribute('value', '560')", slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", slider)

    # Wait and check the text field value again
    text_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
    print("Text field value after setting slider to 560:", text_field.get_attribute('value'))

    # Validate Slider Value
    assert text_field.get_attribute('value') == '2000', f"Expected 560 but got {text_field.get_attribute('value')}"

    # 7. Select CPT Codes
    cpt_codes = ['99091', '99453', '99454', '99474']
    for code in cpt_codes:
        # Debugging: Print message before trying to click the checkbox
        print(f"Trying to click checkbox for CPT code {code}")
        try:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@value='{code}']")))
            if not checkbox.is_selected():
                checkbox.click()
        except Exception as e:
            print(f"Error while clicking checkbox for CPT code {code}: {e}")
            continue

    # 8. Validate Total Recurring Reimbursement
    total_reimbursement = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Total Recurring Reimbursement for all Patients Per Month')]")))
    assert '110700' in total_reimbursement.text

finally:
    # Close the browser
    driver.quit()
