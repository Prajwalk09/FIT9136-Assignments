def is_valid_sale(price: dict, item_type: str, item_quantity: int, sale_total: float) -> bool:
    """
    Checks whether a particular sale is valid or not.
    Parameters:
        price(dict) : A dictionary containing the supermarket's prices for all items they carry (Contains str keys and float values)
        item_type (str) : Specifies the type of the item.
        item_quantity (int) : Specifies the number of units sold.
        sale_total (float) : Specifies the total sale price.

    Returns:
        bool: True if the sale is valid, False otherwise
    """
    if item_type not in price.keys():
        return False

    # Checking if the current sold price is equal to the price at which that particular item was supposed to be sold.
    actual_price = item_quantity * price.get(item_type)
    return actual_price == sale_total


def flag_invalid_sales(price: dict, sales: list) -> list:
    """
    This function returns a list of all sales that are invalid.
    Parameters:
            price(dict): A dictionary containing the supermarket's prices for all item's they carry (Contains str keys and float values)
            sales(list): A list of records of sale

    Returns:
        list: A list of all sales which were invalid as per the rules of is_valid_sale function
    """
    invalid_sales = []
    for sale in sales:
        item_type, item_quantity, sale_total = sale[:]
        if not is_valid_sale(price, item_type, item_quantity, sale_total):
            invalid_sales.append(sale)
    return invalid_sales


def generate_sales_report(price: dict, sales: list) -> dict:
    """
    This function returns a dictionary summarising the day's business by item

    Parameters:
        price(dict): A dictionary containing the supermarket's prices for all item's they carry (Contains str keys and float values)
        sales(list): A list of records of sale

    Returns:
        Dictionary: a dictionary summarising the day's business by item (for only sales that are valid)
    """
    sales_report = {}
    invalid_sales = flag_invalid_sales(price, sales)

    # Generating sales report for invalid sales
    for sale in invalid_sales:
        item_type = sale[0]
        # If the key(item_type) not in sales_report dictionary already, add it to the dictionary and initialise values
        if item_type not in sales_report:
            sales_report[item_type] = [0, 0, 0.0, 0]

        # Incrementing the total sale count and invalid sale count by 1
        sales_report[item_type][1] += 1
        sales_report[item_type][3] += 1

    # Generate valid sale list
    valid_sales = [sale for sale in sales if sale not in invalid_sales]
    for sale in valid_sales:
        item_type, item_quantity, sale_total = sale

        """If the key(item_type) not in sales_report dictionary already, 
        add it to the dictionary and initialize values."""
        if item_type not in sales_report:
            sales_report[item_type] = [0, 0, 0.0, 0]
        # Update item_quantity, total_sale_count and sale_total
        sales_report[item_type][0] += item_quantity
        sales_report[item_type][1] += 1
        sales_report[item_type][2] += sale_total

    for item in price.keys():
        # Add all those items to the sales_report summary which are in price but not in sales_report already
        if item not in sales_report:
            sales_report[item] = [0, 0.0, 0, 0]

    # Calculating the average sale price per sale for each item
    for item, sale_info in sales_report.items():
        sales_report[item] = calculate_average_price_per_sale(sale_info)

    return sales_report


def calculate_average_price_per_sale(sale_info: list) -> tuple:
    """
    This function calculates and returns the average sale price per sale

    Parameters:
        sale_info(list): A list containing the information about each item sold.

    Returns:
        A tuple containing information about each item sold and average sale price per sale.
    """
    total_sale_count, invalid_sale_count = sale_info[1], sale_info[-1]
    total_sale_price = sale_info[2]
    valid_sale_count = total_sale_count - invalid_sale_count
    # Calculate the average sale price if and only if any valid number of sales have been made.
    if valid_sale_count:
        average_sale_price = total_sale_price / valid_sale_count
        sale_info[2] = average_sale_price

    # Return the updated sale information as a tuple
    return tuple(sale_info)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    sales = [
        ["apple", 1, 2.0],
        ["apple", 3, 6.0],  # Two sales of apples have an average price of 4 per sale
        ["orange", 1, 2.0],
        ["carrot", 1, 8.0],  # Two sales of apples have an average price of 4 per sale
    ]
    print(generate_sales_report(price, sales))

    print(f"Is valid sale {is_valid_sale.__doc__}")
    print(f"Flag invalid sale {flag_invalid_sales.__doc__}")
    print(f"Generate sales report {generate_sales_report.__doc__}")
    print(f"Calculate average sale {calculate_average_price_per_sale.__doc__}")
