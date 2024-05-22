"""Wrote additional code to discount the product prices by 10% if the current time of day is before 11:00 a.m."""
import csv
from datetime import datetime

def read_dictionary(filename, key_column_index):
    """Read the contents of a CSV file into a compound
    dictionary and return the dictionary.

    Parameters
        filename: the name of the CSV file to read.
        key_column_index: the index of the column
            to use as the keys in the dictionary.
    Return: a compound dictionary that contains
        the contents of the CSV file.
    """
    compound_dict = {}
    
    with open(filename, mode="rt") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            key = row[key_column_index]
            compound_dict[key] = row

    return compound_dict

def apply_discount(price, discount_rate):
    return price * (1 - discount_rate)

def main():
    try:
        products_dict = read_dictionary('products.csv', 0)
        
        print("Inkom Emporium\n")
        
        with open('request.csv', mode="rt") as file:
            reader = csv.reader(file)
            next(reader)
            
            subtotal = 0
            total_items = 0
            
            current_time = datetime.now().time()
            discount_rate = 0.10 if current_time < datetime.strptime("11:00:00", "%H:%M:%S").time() else 0.0
            
            for row in reader:
                product_number = row[0]
                quantity = int(row[1])

                product_info = products_dict[product_number]
                
                product_name = product_info[1]
                product_price = float(product_info[2])
                
                if discount_rate > 0:
                    product_price = apply_discount(product_price, discount_rate)
                
                total_items += quantity
                subtotal += product_price * quantity
                print(f"{product_name}: {quantity} @ {product_price:.2f}")
            
            sales_tax_rate = 0.06
            sales_tax = subtotal * sales_tax_rate
            total = subtotal + sales_tax
            
            print(f"\nNumber of Items: {total_items}")
            print(f"Subtotal: {subtotal:.2f}")
            print(f"Sales Tax: {sales_tax:.2f}")
            print(f"Total: {total:.2f}")
            
            current_datetime = datetime.now()
            print("\nThank you for shopping at the Inkom Emporium.")
            print(current_datetime.strftime('%a %b %d %H:%M:%S %Y'))
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("The file was not found.")
    except PermissionError as e:
        print(f"Error: {e}")
        print("You do not have permission to access the file.")
    except KeyError as e:
        print("Error: unknown product ID in the request.csv file")
        print(e)

if __name__ == "__main__":
    main()