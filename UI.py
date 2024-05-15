from Pet import *

class UI:
    def create_pet(self):
        pet_name = input('Enter the name of your pet: ')
        pet_type = input('Enter the type of your pet: ')
        pet = Pet(pet_name, pet_type)
        return pet