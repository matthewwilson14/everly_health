from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" 
Test objectives
- Verify that volume-based discounts are applied correctly when buying five or more items.
- Verify that discounts are not applied when less than five items are purchased.
- Verify that manual promotion codes are applied correctly.
- Verify that the correct discount is applied when both the promotion code and volume-based discounts are used together.
 Higher savings to the consumer should be applied.
- Verify that the checkout process works as expected.

"""

def test_volume_based_discounts(num_items, promo):
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://www.everlywell.com/products/food-sensitivity/')
    driver.find_element(By.XPATH, '//select[@data-testid="productQuantity"]').send_keys(num_items)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="addToCartButton"]')))
    element.click()

    # Go to the checkout page
    driver.find_element(By.XPATH, '//a[@data-testid="checkout-link"]').click()

    # Wait for the cart
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="place-order-button"]')))
    element.click()
    if promo == "yes":
        driver.find_element(By.XPATH, '//input[@data-testid="promo-input"]').send_keys("promo1free")
        driver.find_element(By.XPATH, '//button[@data-testid="promo-button"]').click()
    # Validate the expected total and discount
    product_price = 199.00
    if num_items >= 5 and promo == "yes":
        if  0.15 * (product_price * num_items) < product_price:  #the higher savings should be applied
            discount = product_price
        else:
            discount = 0.15 * (product_price * num_items)
    elif promo == "yes":
        discount = 0.15 * (product_price * num_items)
    elif num_items >= 5:
        discount = product_price
    else:
        discount = 0

    expected_sub_total = (product_price * num_items) - discount
    sub_total = driver.find_element(By.XPATH, '//span[@data-testid="sub-total"]').text
    assert "$" + expected_sub_total == sub_total

    # enter payment address and payment info and place order
    driver.find_element(By.XPATH, '//input[@data-testid="email-checkout-input"]').send_keys("test123@gmail.com")
    driver.find_element(By.XPATH, '//input[@data-testid="first-name-checkout-input"]').send_keys("Matthew")
    driver.find_element(By.XPATH, '//input[@data-testid="last-name-checkout-input"]').send_keys("Wilson")
    driver.find_element(By.XPATH, '//input[@data-testid="address-one-checkout-input"]').send_keys("1426 Willow st")
    driver.find_element(By.XPATH, '//input[@data-testid="city-checkout-input"]').send_keys("Alameda")
    driver.find_element(By.XPATH, '//input[@data-testid="shipState"]').send_keys("CA")
    driver.find_element(By.XPATH, '//input[@data-testid="zip-code-checkout-input"]').send_keys("94501")
    driver.find_element(By.XPATH, '//input[@name="cardnumber"]').send_keys("1234-1234-1234-1234")
    driver.find_element(By.XPATH, '//input[@name="exp-date"]').send_keys("05/16")
    driver.find_element(By.XPATH, '//input[@name="cvc"]').send_keys("123")
    driver.find_element(By.XPATH, '//button[@data-testid="place-order-button"]').click()
    driver.find_element(By.XPATH, '//h1[@data-testid="confirmation-message"]').is_displayed()
    # Close the webdriver
    driver.quit()


# Test different quantities of items with 15% off promo code
test_volume_based_discounts(1, "no")
test_volume_based_discounts(4, "no")
test_volume_based_discounts(5, "no")
test_volume_based_discounts(9, "no")
test_volume_based_discounts(1, "yes")
test_volume_based_discounts(4, "yes")
test_volume_based_discounts(5, "yes")
test_volume_based_discounts(9, "yes")
