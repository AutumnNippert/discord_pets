import random

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

    def __str__(self):
        return f'{self.name} is a {self.species} with {self.strength} strength, {self.intelligence} intelligence, {self.agility} agility, and {self.luck} luck.\nHealth: {self.health}\nFood: {self.food}\nEnergy: {self.energy}\nSanity: {self.sanity}'
    
    def feed(self):
        self.food = clamp(self.food + 10, 0, 100)
        self.energy = clamp(self.energy + 5, 0, 100)
        self.sanity = clamp(self.sanity + 5, 0, 100)

    def take_damage(self, damage):
        damage_taken = ((0.5+(1/self.strength)) * damage)
        self.health = clamp(self.health - damage_taken, 0, 100)
        # round to the nearest whole number
        self.health = round(self.health)

    def roll_damage(self):
        # get random number between str-5 and str+5
        dmg = random.randint(self.strength - 5, self.strength + 5)
        return clamp(dmg, 0, 100)

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
        self.species = data['species']
        self.health = data['health']
        self.strength = data['strength']
        self.intelligence = data['intelligence']
        self.agility = data['agility']
        self.luck = data['luck']