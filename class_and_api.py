from fastapi import FastAPI
from abc import ABC, abstractmethod
from enum import Enum
from datetime import date

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
