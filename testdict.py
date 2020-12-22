import json

with open('levels.json') as json_file:
            data = json.load(json_file)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
         
    
p = Struct(**data)
 
print(type(p.level2))   
t=map(p) 
#s = p.level2 
#t = Struct(**s)