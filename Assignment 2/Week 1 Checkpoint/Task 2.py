def patch_item_price(price: dict, patch: dict) -> dict:
    """
    This function updates the price dictionary using the patch dictionary and returns the updated
    price dictionary.

    Parameters:
        price(dict) : A dictionary containing the supermarket's prices for all items they carry (Contains str
                      keys and float values)
        patch(dict): A dictionary containing departments as keys and values as another dictionary. The inner dictionary
                    contains the names and prices of the items for that particular department. (str keys and float values)

    Returns:
        Updated price dictionary using the patch dictionary
    """
    price.update(patch)
    return price


def is_valid_sale(price: dict, patch: dict, department: str, item_sold: str, quantity_sold: int,
                  sale_total: float) -> bool:
    """
    This function checks whether a particular sale is valid or not and returns a boolean result
    Parameters:
        price(dict) : A dictionary containing the supermarket's prices for all items they carry (Contains str
                      keys and float values)
        patch(dict): A dictionary containing departments as keys and values as another dictionary. The inner dictionary
                    contains the names and prices of the items for that particular department. (str keys and float values)
        department(str): A string containing the name of the department of which the sale is a part of
        item_sold(str): A string containing the name of the item sold
        quantity_sold(int): An integer value describing the quantity of the item sold
        sale_total(float): A float value describing the price at which the item was sold

    Returns:
        A boolean value indicating whether a particular sale is valid or invalid
    """
    # If department is in patch dict and item sold is in the department's dict
    if department in patch and item_sold in patch[department]:
        return patch[department][item_sold] * quantity_sold == sale_total
    elif item_sold in price:
        return price[item_sold] * quantity_sold == sale_total
    # Case when price at which it was supposed to be sold does not match the price at which it was sold
    else:
        return False


def get_unique_departments(sales: list) -> set:
    """
    This function is used to get all the unique departments from the sales list and return them as a set

    Parameters:
        sales(list): A list of lists containing the list of sales done by each department

    Returns:
        A set containing all the unique departments from the sales list
    """
    unique_departments = set()
    for sale in sales:
        department = sale[0]
        # Add the department to unique_department set
        unique_departments.add(department)
    return unique_departments


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


def generate_sales_reports(price: dict, patch: dict, sales: list) -> list:
    """
        This function returns a dictionary summarising the day's business by item

        Parameters:
            price(dict): A dictionary containing the supermarket's prices for all item's they carry
                        (Contains str keys and float values)
            patch(dict): A dictionary containing departments as keys and values as another dictionary.
                        The inner dictionary contains the names and prices of the items for that particular department.
                        (str keys and float values)
            sales(list): A list of records of sale

        Returns:
            List: A list summarising department, total sales of the department for all items and the invalid sales
                    of the department
        """
    all_items = dict()
    sales_report = {}
    invalid_sales = {}

    # Initialise and empty dict for all departments, empty list for all departments
    for department in get_unique_departments(sales):
        sales_report[department] = {}
        invalid_sales[department] = []

        # Get all the items for a department in the price dict and patch dict
        all_items[department] = set(items for items in price)
        if department in patch:
            all_items[department].update(keys for keys in patch[department].keys())

        # Initialise the sales_report dict for each department and item of that department
        for item in all_items[department]:
            sales_report[department][item] = [0, 0, 0.0, 0]

    for sale in sales:
        department, item_sold, quantity_sold, sale_total = sale

        # If the sale is valid, increment quantity_sold, number of sales and sale total
        if is_valid_sale(price, patch, department, item_sold, quantity_sold, sale_total):
            sales_report[department][item_sold][0] += quantity_sold
            sales_report[department][item_sold][1] += 1
            sales_report[department][item_sold][2] += sale_total
        else:
            # If sale is invalid, add the sale list to invalid sales of that department
            invalid_sales[department].append(sale[1:])
            if item_sold not in sales_report[department]:
                sales_report[department][item_sold] = [0, 0, 0.0, 0]
            # For all invalid sales, increment number of transactions and number of invalid transactions
            sales_report[department][item_sold][1] += 1
            sales_report[department][item_sold][3] += 1

    for department in sales_report:
        # Calculating the average price per sale for each item in each department
        for item_sold, sale_info in sales_report[department].items():
            sales_report[department][item_sold] = calculate_average_price_per_sale(sale_info)

    sales_summary_by_department = []

    """Get the final result by creating tuples of departments, sales summary of respective departments and 
    invalid sales of respective departments"""
    
    for department in get_unique_departments(sales):
        sales_summary_by_department.append((department, sales_report[department], invalid_sales[department]))
    return sales_summary_by_department


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    patch = {
        "dep2": {"carrot": 2.5}
    }
    sales = [
        ["dep1", "apple", 1, 2.0],
        ["dep1", "apple", 3, 6.0],
        ["dep1", "orange", 1, 2.0],
        ["dep1", "carrot", 1, 8.0],
        ["dep2", "orange", 3, 9.0],
        ["dep2", "carrot", 2, 5.0],
        ["dep2", "apricot", 1, 9.0],
        ["dep3", "apricot", 1, 9.0],
    ]
    print(generate_sales_reports(price, patch, sales))

