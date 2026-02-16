from fastapi import FastAPI
from abc import ABC, abstractmethod
from enum import Enum
from datetime import date

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Dorm:
    def __init__(self, name):
        self.__name = name
        self.__building_list = []
        self.__applicant_list = []
        self.__resident_list = []
        self.__os_staff_list = []
        self.__maintenace_technician_list = []
        self.__system_admin_list = []

    def add_resident(self, resident):
        self.__resident_list.append(resident)
        
    def add_operation_staff(self, operation_staff):
        self.__os_staff_list.append(operation_staff)

    def verify_identity(self,email,password):
        for os in self.__os_staff_list:
            if os.password == password and os.email == email:
                return os
        return None

class User:
    def __init__(self,name,id, email, phone_number):
        self.__name = name
        self.__id = id
        self.__email = email
        self.__phone_number = phone_number
        self.__strike = 0

    # get User artibute
    @property
    def name(self):
        return self.__name
    
    @property
    def id(self):
        return self.__id
    
    @property
    def email(self):
        return self.__email
    
    @property
    def phone_number(self):
        return self.__phone_number

    #method User
    def request_booking_room(self,user_id, sign_contract_time, building, room_id):
        pass

    def show_booking_status(self,book):
        pass

    def send_contract_info(self):
        pass

    def cancel_booking(self,book):
        pass

class AccountStatus(Enum):
    Applicant = 1

    Active = 2
    
    Suspended = 3
    
    Closed = 4

class Resident(User):
    def __init__(self,name,id, email, phone_number):
        super().__init__(name,id, email, phone_number)
        self.__move_in_date = date.today()
        self.__booking_list = []
        self.__discount_list = []
        self.__invoice_list = []
        self.__payment = None
        self.__receipt_list = []
        self.__status = AccountStatus.Active.name

    # get Resident artibute (Resident สืบทอดมาจาก User ทำให้ get artibute name,id,email,phone_number ได้เหมือนกัน)
    def move_in_date(self):
        return self.__move_in_date
    
    def status(self):
        return self.__status

    # method Resident
    def request_maintanance(self):
        pass

    def cancel_maintenance(self,mt):
        pass

    def show_maintenance_ticket(self):
        pass

    def cancel_contract(self,contract):
        pass

class Staff:
    def __init__(self,building_responsibility,role_id):
        self.__building_responsibility = building_responsibility
        self.__role_id = role_id

    #get artibute Staff
    @property
    def building_responsibility(self):
        return self.__building_responsibility
    
    @property
    def role_id(self):
        return self.__role_id
    
    #method Staff
    def logout(self):
        pass

class Operation_Staff(Staff):
    
    # FIX 2: Fixed calculation logic to return numbers, not Objects
    def calculate_net_amount(self, total_cost, discount_cost):
        return total_cost - discount_cost

    def create_invoice(self,resident_info, invoice_type, room_cost, electricity_cost, water_cost, 
                       parking_slot_cost, share_facility_cost, maintenance_cost):
        
        # 1. Sum up all costs
        total_services = (room_cost + electricity_cost + water_cost + 
                          parking_slot_cost + share_facility_cost + maintenance_cost)
        
        # 2. Calculate Discount Value
        

        # 3. Calculate Net Amount
        net_amount = self.calculate_net_amount(total_services)
        
        # 4. Create and Return the Invoice Object
        new_invoice = Invoice(
            invoice_type, room_cost, electricity_cost, water_cost, 
            parking_slot_cost, share_facility_cost, maintenance_cost, 
            total_services, net_amount
        )
        
        
        return new_invoice
    

class Invoice:
    def __init__(self,resident_info, invoice_type, room_cost, electricity_cost, water_cost, 
                 parking_slot_cost, share_facility_cost, maintenance_cost, 
                 total_before_discount, net_amount):
        self.__resident_info = resident_info
        self.__invoice_type = invoice_type
        self.__room_cost = room_cost
        self.__electricity_cost = electricity_cost
        self.__water_cost = water_cost
        self.__parking_slot_cost = parking_slot_cost
        self.__share_facility_cost = share_facility_cost
        self.__maintenance_cost = maintenance_cost
        self.__total_before_discount = total_before_discount
        self.__net_amount = net_amount

    def __str__(self):
        return (f"--- Invoice ---\n"
                f"Type: {self.__invoice_type}\n"
                f"Discount Applied: {self.__discount_cost}\n"
                f"Net Amount To Pay: {self.__net_amount}")

# --- Discount Logic Refactored ---

class Discount(ABC):
    def __init__(self, type_name):
        self.__type = type_name

    @abstractmethod
    def calculate_discount(self, target_amount):
        pass

    # FIX 3: Static Factory Method to create the correct subclass
    @staticmethod
    def create_discount(type_name):
        if type_name == "STUDENT":
            return Student_Discount(type_name)
        elif type_name == "EARLY":
            return Early_Discount(type_name)
        elif type_name == "LONGTERM":
            return Long_Term_Discount(type_name)
        return None

class Student_Discount(Discount):
    # นักศึกษา: ลดค่าเช่า 3% (ต้องยืนยันสถานะทุกเทอม)
    # องค์กร: ลดค่าเช่า 8% แต่ขั้นต่ำ 5 ห้อง และสัญญารายปี
    @staticmethod
    def calculate_discount(self, room_cost):
        return room_cost * 0.03

class Early_Discount(Discount):
    # ชำระบิลก่อนวันที่ 5 ของเดือน ลดค่าบริการส่วนกลาง 100 บาท
    @staticmethod
    def calculate_discount(self, target_amount=0):
        return 100

class Long_Term_Discount(Discount):
    # ทำสัญญา 12 เดือน ลดค่าเช่า 5% ตลอดสัญญา
    @staticmethod
    def calculate_discount(self, room_cost):
        return room_cost * 0.05

# --- Testing ---

def test():
    print("="*70)
    dorm = Dorm("Ducky")
    
    # 1. Create Resident
    kenny = Resident("123456", "ken", "ken@gmail.com", "1234567890")
    print(f"Resident created: {kenny.special_condition}")

    # 2. Create Staff
    gong = Operation_Staff("676767", "gong_inwzaa", "gong@gmail.com", "0812345678", "A01", "AdminRole")
    gong.password_setting("67766776")
    
    dorm.add_resident(kenny)
    dorm.add_operation_staff(gong)
    gonginwzaa = dorm.verify_identity("gong@gmail.com","67766776")
    
    # 3. Create Discount Object using Factory
    # We use the resident's condition to ask the Factory for the correct object
    discount_obj = Discount.create_discount(kenny.special_condition)
    
    # 4. Create Invoice
    # We pass the discount object into the function
    gonginwzaa.create_invoice(
        kenny,
        invoice_type="normal",
        room_cost=6500,
        electricity_cost=500,
        water_cost=50,
        parking_slot_cost=800,
        share_facility_cost=500,
        maintenance_cost=0,
        discount_obj=discount_obj
    )
    print("="*70)
if __name__ == "__main__":
        test()