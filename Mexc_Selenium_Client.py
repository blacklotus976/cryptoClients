from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
"""General Instructions
->The client requires all the buttons that the following functions use to be clearly visible with no interventions
->we usually firstly set the quantity before any other decisions just to look more random with no clues that we have programed everything
->continuation from above: so we will be able to press long/short button without needing any sleeps 
"""


"""run in cmd the following --after '>' character--, of course modify the path file like needed --as it is on your computer"""
'''>"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeUserData"'''

"""Initializing Driver"""
# Initialize Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress",
                                       "127.0.0.1:9222")  # Use the same port as in the remote debugging command
# print("\nextra SELENIUM logs")
# print("Initializing driver")
start = time.time()
driver = webdriver.Chrome(options=chrome_options)
# print(f"Driver initialized after {time.time() - start} seconds")
# print("\n")


"""Following function pre-loads the quantity --to have it ready
for testing purposes feel free to re-enable the commented print statements, they are helpful"""
def set_quantity(quantity):
    try:
        start = time.time()

        # Print the current URL
        #print("Current URL:", driver.current_url)

        # Print the page source (for debugging)
        #print("Page Source:", driver.page_source[:500])  # Print the first 500 characters of the page source

        #print("Waiting for quantity input field to be present")

        # Wait for the input field to be present
        quantity_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="off"]'))
            )
        #previous was : quantity_input = WebDriverWait(driver, 10).until(
               # EC.presence_of_element_located((By.CSS_SELECTOR, 'input.ant-input')) chnaged 01.08.24
            #)
        # Focus on the input field
        driver.execute_script("arguments[0].focus();", quantity_input)
        #print("Quantity input field focus

        #print("Sending quantity")
        quantity_input.clear()
        time.sleep(0.2)
        quantity_input.send_keys(str(quantity))
        #time.sleep(0.5)

        print(f"Quantity sent after {time.time() - start} seconds")
        # print("Pressing long")
    except Exception as e:
        exit("failed to send QUANTITY, error:{}".format(e))

"""Following function, opens position (just presses long/short) -- REQUIRES QUANTITY LOADED"""
def open_position_quantity_loaded(side):
    start = time.time()
    if side == 'LONG':
        button_selector = 'button.ant-btn.ant-btn-default.component_longBtn__BBkFR'
    elif side == 'SHORT':
        button_selector = 'button.ant-btn.ant-btn-default.component_shortBtn__s8HK4'
    else:
        exit("BAD SIDE REQUEST")
    try:
        openButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
                )
        openButton.click()
        print(f"Button pressed after {time.time() - start} seconds")

    except Exception as e:
            print(f"Error opening position: {e}")
            print("Exception details:", e)

"""Following function opens a position with a given quantity --slower than pre-loaded and fast opening"""
def open_position(side, quantity):
    #time.sleep(0.75)

    try:
        start = time.time()

        # Print the current URL
        print("Current URL:", driver.current_url)

        # Print the page source (for debugging)
        #print("Page Source:", driver.page_source[:500])  # Print the first 500 characters of the page source

        print("Waiting for quantity input field to be present")

            # Wait for the input field to be present
        quantity_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.ant-input'))
            )


            # Focus on the input field
        driver.execute_script("arguments[0].focus();", quantity_input)
        print("Quantity input field focused")

        print("Sending quantity")
        quantity_input.clear()
        time.sleep(0.2)
        quantity_input.send_keys(str(quantity))
        #time.sleep(0.5)

        print(f"Quantity sent after {time.time() - start} seconds")
        print("Pressing long")
    except Exception as e:
        exit("failed to send QUANTITY, error:{}".format(e))


    if side == 'LONG':
        button_selector = 'button.ant-btn.ant-btn-default.component_longBtn__BBkFR'
    elif side == 'SHORT':
        button_selector = 'button.ant-btn.ant-btn-default.component_shortBtn__s8HK4'
    else:
        exit("BAD SIDE REQUEST")
    #print("Pressing long")
    try:
        openButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
                )
        openButton.click()
        print(f"Button pressed after {time.time() - start} seconds")

    except Exception as e:
            print(f"Error opening position: {e}")
            print("Exception details:", e)

"""Following function partially closes a position by percentage"""
def partially_close_position(percentage):
    return NotImplemented

"""Following function force closes the position. Uses 'flash-close' button, 
REQUIRES IT TO BE VISIBLE, AND OF COURSE A POSITION TO BE OPEN"""
def close_all_positions():
    try:
        start = time.time()

        #print("Waiting for 'Flash Close' button to be present")

        # Wait for the "Flash Close" button to be present
        flash_close_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Flash Close']/ancestor::button"))
        )

        # Wait for the "Flash Close" button to be clickable
        flash_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Flash Close']/ancestor::button"))
        )

        # Click the "Flash Close" button
        flash_close_button.click()
        print(f"'Flash Close' button pressed after {time.time() - start} seconds")

    except Exception as e:
        print("didn't have anything to close")
        # print(f"Error closing all positions: {e}")
        # print("Exception details:", e)

"""Following function sets leverage"""
def set_leverage(leverage):
    return NotImplemented

"""Following function sets the right coin"""
def set_coin(coin):
    return NotImplemented

"""Following function checks if there are visual interventions -- SHOULD BE CONVERTED TO ASYNC MIDDLEWARE"""
def check_interventions():
    return NotImplemented


"""Following function checks as fast as possible last price directly from the website"""
def get_future_price():
    price_css_selector = 'span.market_bigPrice__yD9AA .PriceText_text__STO26'
    price_element = driver.find_element(By.CSS_SELECTOR, price_css_selector)

    # Get the price from the element

    price = price_element.text
    price = price.replace(',', '')
    # print(f"Current price: {price}")
    return price

# while True:
#     print(float(get_future_price()))



# open_position_quantity_loaded('LONG')
# time.sleep(1)
# set_quantity(90)