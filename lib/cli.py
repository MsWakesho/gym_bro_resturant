import getpass
from models import User, Reservation, BulkingMenu, CuttingMenu, Delivery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def main():
    print("*** Welcome To Gym Bro Restaurant ***")
    
    name = input("Enter your name: ")

    engine = create_engine('sqlite:///gym_bro_restaurant.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(name=name, option=None)  # You can modify this based on your User model
    session.add(user)
    session.commit()

    option = 0
    while option != 3:
        print(f"Hello {name}, Kindly Select Your Goal:")
        print("------------------------------------------")
        print("1) BULKING")
        print("2) CUTTING")
        print("3) CANCEL")
        option = int(input("*Your goal is: *"))

        if option == 1:
            print(f"Hello {name}, your goal is BULKING")
            print("------------------------------------------")
            print("**Select Your Option:**")
        
            bulking_option = 0
            while bulking_option != 4:  
                print("1) Book A Reservation")
                print("2) Bulking Menu")
                print("3) Food Delivery")
                print("4) BACK")
                bulking_option = int(input("Enter Your Option: "))

                # Booking a Bulking Reservation
                if bulking_option == 1:
                    print(f"{name}'s BULKING-CODED Reservation....")
                    print("------------------------------------------")

                    date = input("Enter Date (DD-MM-YYYY): ")
                    time = input("Enter Time (HH:MM): ")
                    number_of_guests = int(input("Enter Number Of Guests: "))

                    reservation = Reservation.create_reservation(session, user_name=name, date=date,
                                                                  time=time, number_of_guests=number_of_guests)
                    print(f"{name}'s BULKING Reservation successfully booked!")

                elif bulking_option == 2:
                    print("Retrieving The Bulking Menu...")
                    print("----------------------------------")
                    bulking_menu_items = BulkingMenu.get_all(session)
                    for index, item in enumerate(bulking_menu_items, start=1):
                        print(f"{index}. Name: {item.name},Description: {item.description}, Price:{item.price}")
                    selection = int(input("Enter the number of the meal you want to select:"))
                    selected_item= bulking_menu_items[selection -1]

                    print("Selected Meal:")
                    print(f"Name:{selected_item.name}, Description:{selected_item.description}, Price:{selected_item.price}")
                
                elif bulking_option == 3:
                    print("Gym Bro Delivery...")
                    print("--------------------------------")
                    delivery_option = input("Looking for delivery?(yes/no):").lower()

                    if delivery_option == 'yes':
                        location = input("Enter your location:")
                        street_name = input("Enter your street name:")
                        # Selecting The Meal
                        print("Select a bulking menu item for delivery:")
                        bulking_menu_items = BulkingMenu.get_all(session)
                        for index, item in enumerate(bulking_menu_items, start=1):
                            print(f"{index}.{item.name} - {item.price}")

                        selected_items = []
                        total_price = 0
                        while True:
                            selection = input("Enter the number of the menu item you want to select (or 'done' to finish): ")
                            if selection.lower() == 'done':
                                break
                            try:
                                index = int(selection)
                                if 1 <= index <= len(bulking_menu_items):
                                    selected_item = bulking_menu_items[index - 1]
                                    selected_items.append(selected_item)
                                    total_price += int(selected_item.price)
                                    print(f"{selected_item.name} - {selected_item.price} added to your order.")
                                else:
                                    print("Invalid selection. Please enter a valid number.") 
                            except ValueError:
                                print("Invalid input. Please enter a number or 'done'.")

                        print("Your order:")
                        for item in selected_items:
                            print(f"{item.name} - {item.price}")
                        print(f"Total price: {total_price}")

                        delivery = Delivery.create_delivery(session, user_name=name, location=location, street_name=street_name, price=total_price)
                        print("***Order Placed Successfully!***")
                    else:
                        print("No Delivery order placed. Returning to main menu")

        elif option == 2:
            print(f"Hello {name}, your goal is CUTTING")
            print("------------------------------------------")
            print("Select Your Option:")
        
            cutting_option = 0
            while cutting_option != 4:  
                print("1) Book A Reservation")
                print("2) Cutting Menu")
                print("3) Food Delivery")
                print("4) BACK")
                cutting_option = int(input("Enter Your Option: "))

                # Booking a Cutting Reservation
                if cutting_option == 1:
                    print(f"{name}'s CUTTING-CODED Reservation....")
                    print("------------------------------------------")

                    date = input("Enter Date (DD-MM-YYYY): ")
                    time = input("Enter Time (HH:MM): ")
                    number_of_guests = int(input("Enter Number Of Guests: "))

                    reservation = Reservation.create_reservation(session, user_name=name, date=date,
                                                                  time=time, number_of_guests=number_of_guests)
                    print(f"{name}'s CUTTING Reservation successfully booked!")

                elif cutting_option == 2:
                    print("Retrieving The Cutting Menu...")
                    print("----------------------------------")
                    cutting_menu_items = CuttingMenu.get_all(session)
                    for item in cutting_menu_items:
                        print(f"Name: {item.name},Description: {item.description}, Price:{item.price}")
                
                elif cutting_option == 3:
                    print("Gym Bro Delivery...")
                    print("--------------------------------")
                    delivery_option = input("Looking for delivery?(yes/no):").lower()

                    if delivery_option == 'yes':
                       location = input("Enter your location:")
                       street_name = input("Enter your street name:")
                       
                       print("Select a cutting meal for delivery:")
                       cutting_menu_items = CuttingMenu.get_all(session)
                       for index, item in enumerate(cutting_menu_items, start=1):
                            print(f"{index}.{item.name} - {item.price}")
                            
                            selected_items = []
                            total_price = 0  # Initialize total price
                            while True:
                                selection = input("Enter the number of the menu item you want to select (or 'done' to finish): ")
                                if selection.lower() == 'done':
                                    break
                                try:
                                    index = int(selection)
                                    if 1 <= index <= len(cutting_menu_items):
                                        selected_item = cutting_menu_items[index - 1]
                                        selected_items.append(selected_item)
                                        total_price += int(selected_item.price) # Add the price of the selected item to total price
                                        print(f"{selected_item.name} - {selected_item.price} added to your order.")
                                    else:
                                        print("Invalid selection. Please enter a valid number.") 
                                except ValueError:
                                    print("Invalid input. Please enter a number or 'done'.")

                            # Displaying the ordered items and total price
                            print("Your order:")
                            for item in selected_items:
                                print(f"{item.name} - {item.price}")
                            print(f"Total price: {total_price}")

                            # Create delivery record with total price
                            delivery = Delivery.create_delivery(session, user_name=name, location=location, street_name=street_name, price=total_price)
                            print("***Order Placed Successfully!***")
                    else:
                            print("No Delivery order placed. Returning to main menu")


        elif option == 3:
            print(f"Oops! {name}, You Terminated The Process")

        else:
            print("Invalid Option, Kindly Select Again")

    session.close()
    
if __name__ == "__main__":
    main()