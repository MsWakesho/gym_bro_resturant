import getpass
from models import User, Reservation, CuttingMenu, BulkingMenu, Delivery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def main():
    print("*** Welcome To Gym Bro Restaurant ***")
    
    name = input("Enter your name: ")
    password = getpass.getpass("Enter your password: ")

    print("Password Confirmed!")

    engine = create_engine('sqlite:///gym_bro_restaurant.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(name=name, password=password, option=None)  # You can modify this based on your User model
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
                    print("")

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

        elif option == 3:
            print(f"Oops! {name}, You Terminated The Process")

        else:
            print("Invalid Option, Kindly Select Again")

    session.close()

if __name__ == "__main__":
    main()
