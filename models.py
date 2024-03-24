from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from faker import Faker
from sqlalchemy import Boolean
import bcrypt

 
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column( "name", String)
    option = Column("option" ,String)
    

    def __init__(self, name, option):
        self.name = name
        self.option = option
    
    def __repr__(self):
        return f"{self.id}). {self.name} {self.option}"

    @classmethod
    def create_user(cls, name, option):
        user = cls(name=name, option=option)
        session.add(user)
        session.commit()
        return user
   
    @classmethod
    def get_all(cls):
        return session.query(cls).all()
    
    @classmethod
    def filter_by_id(cls,user_id):
        return session.query(cls).filter(cls.id == user_id).first()

    


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, ForeignKey('users.name'))
    date = Column("date", String)
    time = Column("time" , String)
    number_of_guests = Column( "number_of_guests", Integer)
    deposit_paid = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Reservation(name :'{self.name}',date:'{self.date}',time:'{self.time}', number_of_guests:'{self.number_of_guests}, deposit_paid:'{self.deposit_paid}')>"

    @classmethod
    def create_reservation(cls, session, user_name, date, time, number_of_guests):
        reservation = cls(user_name=user_name, date=date, time=time, number_of_guests=number_of_guests)
        session.add(reservation)
        session.commit()
        return reservation

    @classmethod
    def get_all_reservations(cls, session):
        return session.query(cls).all()

    @classmethod
    def filter_reservation_by_id(cls, reservation_id):
        return session.query(cls).filter(cls.id == reservation_id).first()

    @classmethod
    def reservation_deposit_paid(cls, reservation_id):
        reservation = session.query(cls).filter(cls.id == reservation_id).first()

        if reservation:
            return reservation.deposit_paid
        else:
            return False

    @classmethod
    def cancel_reservation(cls, reservation_id):
        reservation = session.query(cls).filter(cls.id == reservation_id)

        if reservation:
            session.delete(reservation)
            session.commit()
            return True
        else:
            return False


class BulkingMenu(Base):
    __tablename__ = 'bulking_menus'

    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    description = Column("description", String)
    price = Column("price", Integer)
   

    @classmethod
    def create_menu_item(cls, session, name, description, price):
        bulking_menu_item = cls(name=name, description=description, price=price )
        session.add(bulking_menu_item)
        session.commit()
        return bulking_menu_item

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_bulking_menu_by_id(cls, session, bulking_menu_id):
        return session.query(cls).filter(cls.id == bulking_menu_id).first()
    
    @classmethod
    def select_menu_item(cls, session, bulking_menu_id):
        return session.query(cls).filter(cls.id == bulking_menu_id).first()

class CuttingMenu(Base):
    __tablename__ = 'cutting_menus'

    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    description = Column("description", String)
    price = Column("price", Integer)
   

    @classmethod
    def create_menu_item(cls, session, name, description, price):
       cutting_menu_item = cls(name=name, description=description, price=price )
       session.add(cutting_menu_item)
       session.commit()
       return cutting_menu_item

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_cutting_menu_by_id(cls, session, cutting_menu_id):
        return session.query(cls).filter(cls.id == cutting_menu_id).first()
    
    @classmethod
    def select_menu_item(cls, session, cutting_menu_id):
        return session.query(cls).filter(cls.id == cutting_menu_id).first()



class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, ForeignKey('users.name'))
    location = Column(String)
    street_name = Column(String)
    price = Column(Integer)
    bulking_menu_id= Column(Integer, ForeignKey('bulking_menus.id'))
    cutting_menu_id= Column(Integer, ForeignKey('cutting_menus.id'))

    bulking_menu = relationship("BulkingMenu")
    cutting_menu = relationship("CuttingMenu")


    @classmethod
    def create_delivery(cls, session, user_name, location, street_name, price ,bulking_menu_id=None, cutting_menu_id=None):
        delivery = cls(user_name=user_name, location=location, street_name=street_name, price=price,bulking_menu_id=bulking_menu_id, cutting_menu_id=cutting_menu_id)
        session.add(delivery)
        session.commit()
        return delivery

    @classmethod
    def get_all_deliveries(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_delivery_by_id(cls, session, delivery_id):
        return session.query(cls).filter(cls.id == delivery_id).first()
    
    
    
    @classmethod
    def checkout_station(cls, session, delivery_id, payment_info):
        delivery = cls.find_delivery_by_id(session, delivery_id)
        if delivery:
            if cls.process_payment(payment_info):
                delivery.payment_status = 'Paid & Ready For Delivery'
                session.commit()
                return True
            else:
                return False
        else:
            return False



    def display_with_menus(self):
        return f"Delivery Details: Location - {self.location}, Street Name - {self.street_name}, Price - {self.price}\n" \
               f"Bulking Menu: {self.bulking_menu}\nCutting Menu: {self.cutting_menu}"




engine = create_engine('sqlite:///gym_bro_restaurant.db')
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

bulking_menu_items = [
    {'name': 'Grilled Salmon', 'description': 'Grilled salmon fillet', 'price': 1200},
    {'name': 'Sweet Potato', 'description': 'Baked sweet potato', 'price': 600},
    {'name': 'Quinoa', 'description': 'Quinoa salad', 'price': 800},
    {'name': 'Lean Beef', 'description': 'Lean beef steak', 'price': 1400},
    {'name': 'Avocado', 'description': 'Fresh avocado slices', 'price': 700},
    {'name': 'Eggs', 'description': 'Scrambled eggs', 'price': 900},
    {'name': 'Greek Yogurt', 'description': 'Greek yogurt parfait', 'price': 600},
    {'name': 'Oatmeal', 'description': 'Steel-cut oatmeal', 'price': 500},
    {'name': 'Almonds', 'description': 'Roasted almonds', 'price': 400},
    {'name': 'Salmon Burger', 'description': 'Grilled salmon burger', 'price': 1000},
    {'name': 'Whole Wheat Pasta', 'description': 'Whole wheat pasta with marinara sauce', 'price': 800},
    {'name': 'Cottage Cheese', 'description': 'Low-fat cottage cheese', 'price': 500},
    {'name': 'Broccoli', 'description': 'Steamed broccoli florets', 'price': 600},
    {'name': 'Tuna', 'description': 'Grilled tuna steak', 'price': 1300},
    {'name': 'Spinach', 'description': 'Fresh spinach salad', 'price': 600},
    {'name': 'Whole Wheat Bread', 'description': 'Whole wheat bread slices', 'price': 400},
    {'name': 'Milk', 'description': 'Skim milk', 'price': 300},
    {'name': 'Peanut Butter', 'description': 'Natural peanut butter', 'price': 700},
    {'name': 'Banana', 'description': 'Fresh banana', 'price': 200},
    {'name': 'Cottage Cheese Pancakes', 'description': 'Whole wheat cottage cheese pancakes', 'price': 800},
]


for item in bulking_menu_items:
    BulkingMenu.create_menu_item(session, **item)

cutting_menu_items = [
    {'name': 'Grilled Chicken Salad', 'description': 'Fresh garden salad with grilled chicken', 'price': 800},
    {'name': 'Steamed Vegetables', 'description': 'Assorted steamed vegetables', 'price': 600},
    {'name': 'Tofu Stir-Fry', 'description': 'Tofu and vegetable stir-fry', 'price': 700},
    {'name': 'Egg White Omelette', 'description': 'Egg white omelette with vegetables', 'price': 500},
    {'name': 'Green Smoothie', 'description': 'Fresh green smoothie with spinach and kale', 'price': 400},
    {'name': 'Grilled Turkey Breast', 'description': 'Grilled turkey breast slices', 'price': 1000},
    {'name': 'Mixed Berry Salad', 'description': 'Mixed berry salad with vinaigrette dressing', 'price': 750},
    {'name': 'Vegetable Soup', 'description': 'Homemade vegetable soup', 'price': 450},
    {'name': 'Baked Salmon', 'description': 'Baked salmon fillet with lemon and herbs', 'price': 1200},
    {'name': 'Quinoa Salad', 'description': 'Quinoa salad with mixed vegetables', 'price': 850},
    {'name': 'Stir-Fried Shrimp', 'description': 'Stir-fried shrimp with garlic and broccoli', 'price': 1100},
    {'name': 'Cauliflower Rice', 'description': 'Cauliflower rice with spices', 'price': 600},
    {'name': 'Avocado Toast', 'description': 'Whole grain toast with avocado slices', 'price': 550},
    {'name': 'Zucchini Noodles', 'description': 'Zucchini noodles with marinara sauce', 'price': 700},
    {'name': 'Cucumber Salad', 'description': 'Cucumber salad with yogurt dressing', 'price': 400},
    {'name': 'Spinach Stuffed Chicken', 'description': 'Chicken breast stuffed with spinach and cheese', 'price': 900},
    {'name': 'Fruit Platter', 'description': 'Assorted fruit platter', 'price': 650},
    {'name': 'Veggie Wrap', 'description': 'Whole wheat veggie wrap', 'price': 500},
    {'name': 'Greek Yogurt Parfait', 'description': 'Greek yogurt parfait with granola and berries', 'price': 550},
    {'name': 'Grilled Vegetable Skewers', 'description': 'Assorted grilled vegetable skewers', 'price': 750},
]


for item in cutting_menu_items:
    CuttingMenu.create_menu_item(session, **item)

faker = Faker()
for _ in range(30):
   user = User(name=faker.name(), option=faker.random_element(elements=('CUTTING', 'BULKING')))
reservation = Reservation(user_name=user.name, date=faker.date(), time=faker.time(),
                          number_of_guests=faker.random_int(min=1, max=10))
reservation.deposit_paid = True  
session.add(reservation)


#Selecting menu item
bulking_menu_item = BulkingMenu.select_menu_item(session, bulking_menu_id=1)
print("Selected Bulking Meal:", bulking_menu_item)

cutting_menu_item = CuttingMenu.select_menu_item(session, cutting_menu_id=1)
print("Selected Cutting Meal:", cutting_menu_item)

session.commit()
session.close()