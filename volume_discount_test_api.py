import requests

"""
Test objectives
-Retrieve the items in the user’s shopping cart and asserts the subtotal price returned is correct.
-Ensure our internal API’s cannot be leveraged maliciously to apply discounts to the shopping cart.
-The proper status code is returned when attempting to apply a 100% discount via the promoCode endpoint.
-The contents of the shopping cart have not been affected after a failed discount request via the shoppingCart endpoint.
"""

def test_shopping_cart():
    # Set up the headers and API endpoint
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAAAAA1234567890'
    }
    endpoint = 'https://everlywell.com/v9/shoppingCart'

    # Make the API request and validate the response
    response = requests.get(endpoint, headers=headers)
    data = response.json()
    assert response.status_code == 200

    # Calculate the expected subtotal based on the items and discount
    expected_subtotal = sum(item['price'] * item['quantity'] for item in data['items'])
    expected_subtotal -= data['discount']
    assert data['subTotal'] == expected_subtotal

    shopping_cart_endpoint = 'https://everlywell.com/v9/shoppingCart'
    promo_code_endpoint = 'https://everlywell.com/v9/promoCode'

    # Retrieve the current shopping cart to get the initial items and subtotal
    response = requests.get(shopping_cart_endpoint, headers=headers)
    shopping_cart_data = response.json()
    assert response.status_code == 200

    # Attempt to apply a 100% discount via the promo code endpoint and validate the response
    payload = {{
        "userId": 12345,
        "sessionId": "7x78634",
        "items": [
            {

                "name": "FIT Test",
                "quantity": 1,
                "price": 40.00
            },
            {
                "name": "Allergy Test",
                "quantity": 1,
                "price": 60.00
            }
        ],
        "discount": 100.00,
        "subTotal": 0.00
    }}
    response = requests.post(promo_code_endpoint, headers=headers, json=payload)
    assert response.status_code == 400

    # Verify contents of shopping cart have not been affected after the failed discount request using shoppingCart endpoint.
    response = requests.get(shopping_cart_endpoint, headers=headers)
    after_failed_discount_shopping_cart_data = response.json()
    assert response.status_code == 200
    assert shopping_cart_data == after_failed_discount_shopping_cart_data
