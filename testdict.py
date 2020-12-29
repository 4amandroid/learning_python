import json

with open('levels.json') as json_file:
            data = json.load(json_file)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
        
        
    
p = Struct(**data)
 
print(p.level2)   
'''def addition(p): 
    return p 
t=map(addition,p) 
print(type(t))
level2 = Struct(**t)
print(level2.brick_x)
#s = p.level2 
#t = Struct(**s)'''