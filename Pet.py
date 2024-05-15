import random
import json

storage_file = 'pets.json'

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

# list of possible classes and stats associated
possible_species = [
    {
        'species': 'Orange Tabby',
        'strength': 6,
        'intelligence': 3,
        'agility': 10,
        'luck': 6
        },
    {
        'species': 'Pitbull',
        'strength': 10,
        'intelligence': 4,
        'agility': 7,
        'luck': 4
        },
    {
        'species': 'Buffalo',
        'strength': 15,
        'intelligence': 3,
        'agility': 4,
        'luck': 3
        },
    {
        'species': 'Crawfish',
        'strength': 1,
        'intelligence': 3,
        'agility': 6,
        'luck': 15
        },
    {
        'species': 'Owl',
        'strength': 3,
        'intelligence': 10,
        'agility': 7,
        'luck': 5
        },
    {
        'species': 'Deprived',
        'strength': 1,
        'intelligence': 1,
        'agility': 1,
        'luck': 1
        }
        
    ]

class Pet:
    id = 0
    name = ''
    gender = ''
    species = ''
    owner = ''
    age = 0
    food = 100
    energy = 100
    sanity = 100

    health = 100
    strength = 0
    intelligence = 0
    agility = 0
    luck = 0

    def __init__(self, name, species_name, owner):
        self.name = name
        for s in possible_species:
            if s['species'] == species_name:
                self.species = s['species']
                self.strength = s['strength']
                self.intelligence = s['intelligence']
                self.agility = s['agility']
                self.luck = s['luck']
                break
        
        self.owner = owner
        self.id = Pet.get_next_id()

    def __str__(self):
        return f'{self.name} is a {self.species} with {self.strength} strength, {self.intelligence} intelligence, {self.agility} agility, and {self.luck} luck.\nHealth: {self.health}\nFood: {self.food}\nEnergy: {self.energy}\nSanity: {self.sanity}'
    
    @staticmethod
    def create(name, species_name, owner):
        pet = Pet(name, species_name, owner)
        pet.update(storage_file)
        return pet

    def feed(self):
        self.food = clamp(self.food + 10, 0, 100)
        self.energy = clamp(self.energy + 5, 0, 100)
        self.sanity = clamp(self.sanity + 5, 0, 100)
        self.update(storage_file)

    def take_damage(self, damage):
        damage_taken = ((0.5+(1/self.strength)) * damage)
        self.health = clamp(self.health - damage_taken, 0, 100)
        # round to the nearest whole number
        self.health = round(self.health)
        self.update(storage_file)

    def roll_damage(self):
        # get random number between str-5 and str+5
        dmg = random.randint(self.strength - 5, self.strength + 5)
        clamped_dmg = clamp(dmg, 0, 100)
        return clamped_dmg

    def roll_crit(self):
        # get random number between 0 and 100
        # if the number is less than the luck stat, return True
        num = random.randint(0, 100)
        return num < self.luck
        
        # luck acts as a multiplier for the other stats

    def roll_evade(self):
        # get random number between 0 and 100
        # if the number is less than the agility stat, return True
        num = random.randint(0, 100)
        return num < self.agility
    
    def load_custom(self, data):
        self.name = data['name']
        self.gender = data['gender']
        self.species = data['species']
        self.owner = data['owner']
        self.age = data['age']
        self.health = data['health']
        self.food = data['food']
        self.energy = data['energy']
        self.sanity = data['sanity']
        self.strength = data['strength']
        self.intelligence = data['intelligence']
        self.agility = data['agility']
        self.luck = data['luck']
    
    def update(self, file=storage_file):
        data = Pet.get_data()
        pets = data['pets']
        for i in range(len(pets)):
            if pets[i]['id'] == self.id:
                pets[i] = self.__dict__()
                break
        else:
            pets.append(self.__dict__())
        with open(file, 'w') as f:
            json.dump(data, f)


    @staticmethod
    def get_data():
        try:
            with open(storage_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(storage_file, 'w') as f:
                json.dump({'pets': []}, f)
        with open(storage_file, 'r') as f:
            data = json.load(f)
            return data

    @staticmethod
    def get_pet(name):
        pets = Pet.get_all_pets()
        for pet in pets:
            if pet.name == name:
                return pet
        return None
    
    @staticmethod
    def get_pets(owner_id):
        pets = Pet.get_all_pets()
        return [p for p in pets if p.owner == owner_id]
        
    @staticmethod
    def get_next_id():
        with open(storage_file, 'r') as f:
            data = json.load(f)
            pets = data['pets']
            if len(pets) == 0:
                return 0
            return max([p['id'] for p in pets]) + 1
        
    def get_dead_pets(owner_id):
        pets = Pet.get_pets(owner_id)
        dead_pets = []
        for pet in pets:
            if pet.health <= 0:
                dead_pets.append(pet)
        return dead_pets
    
    def get_all_pets():
        pets_dict = Pet.get_data()
        pets = []
        for p in pets_dict['pets']:
            pet = Pet(None, None, None)
            pet.load_custom(p)
            pets.append(pet)
        return pets
        
    def check_ownership(self, owner_id):
        return self.owner == owner_id
    
    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'species': self.species,
            'owner': self.owner,
            'age': self.age,
            'health': self.health,
            'food': self.food,
            'energy': self.energy,
            'sanity': self.sanity,
            'strength': self.strength,
            'intelligence': self.intelligence,
            'agility': self.agility,
            'luck': self.luck
        }
    
    def __hash__(self) -> int:
        return hash(self.name) + hash(self.species) + hash(self.owner)
    
def distribute_numbers(N, C):
    # Generate C-1 random numbers to divide the range [0, N] into C parts
    divisions = sorted(random.sample(range(1, N), C - 1))
    divisions = [0] + divisions + [N]

    # Calculate the size of each category
    sizes = [divisions[i+1] - divisions[i] for i in range(C)]

    return sizes