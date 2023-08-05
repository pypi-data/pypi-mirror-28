=====
Usage
=====

There are two different ways to use this module

* Using class Shipfunk:
    * Search pickup points
    * Create package cards and tracking codes
* Using class ShipfunkUser:
    * Handle user accounts

Using Shipfunk class
--------------------

.. code-block:: python
    from shipfunk_python.shipfunk import Shipfunk

    # create object
    shipfunk_client = Shipfunk('your_apikey', 'order_number')

    # Define parameters in dictionary
    params = {
        'postal_code': 30100,
        'country': 'fi',
        'products': [{
            "amount": 1,
            "code": "product123",
            "name": "Test product",
            "weight": {
                "amount": 1,
                "unit": "kg"
            },
            "dimensions": {
                "unit": "cm",
                "width": "25",
                "depth": "15",
                "height": "3"
            },
        }]
    }

    # Call method with parameters
    prices = shipfunk_client._shipfunkClient.get_price(params)
