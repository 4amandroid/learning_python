import json
class Person():

    def __init__(self, name, age):

        self.name = name

        self.age = age
     
class Level():
    def __init__(self):
        self.brick_x = []
        self.brick_y = []
        self.brick_break = []
        self.curtent_level = 0

    def load(self):
        _level = ['level1', 'level2', 'level3', 'level4']
        with open('levels.json') as json_file:
            data = json.loads(json_file)
            level_ = Level(**data) 
            print(level_.brick_x)
    

p = Level()
p.load
print(p.brick_x)
 
 
person_string = '{"name": "Bob", "age": 25}'


person_dict = json.loads(person_string)

person_object = Person(**person_dict)


print(person_object)
print(person_object.name)
print(person_object.age)
