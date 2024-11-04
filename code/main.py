from api_operations import (
    create_product, 
    get_products, 
    update_product, 
    delete_product)

from utilities import (
    check_api_with_retries,
    log_error_to_file,
    get_new_product_info,
    get_updated_product_info,
    get_product_to_delete,
    print_data
    )


def operation() -> None:
    '''Continuously executes CRUD operations based on user choice.'''
    while True:
        choice = input(
            'What operation would you like to perform?\n'
            '1- Insert product\n'
            '2- View all products\n'
            '3- Update product\n'
            '4- Delete product\n'
            '0- Exit\n'
            'Choose an option: \n'
        )
        try:
            choice = int(choice)
        except ValueError as e:
            print('Invalid input. Please try again.')
            continue

        if choice == 0:
            print('Thank you for using the API service.')
            break
        elif choice == 1:
            new_product = get_new_product_info()
            if new_product:
                create_product(new_product)
        elif choice == 2:
            products = get_products()
            if type(products) == list:
                print_data(products)
        elif choice == 3:
            product_to_update = get_updated_product_info()
            if product_to_update:
                update_product(product_to_update)
        elif choice == 4:
            product_to_delete = get_product_to_delete()
            if product_to_delete:
                delete_product(product_to_delete)
        else:
            print('Invalid input. Please try again.')
            

def main():
    """Main function to check API availability and execute operations."""
    if check_api_with_retries():
        operation()
    else:
        print('API is not available. Exiting program.')

if __name__ == '__main__':
    main()