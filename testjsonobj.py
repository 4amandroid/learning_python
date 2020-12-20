#import json
'''class Person():

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
    

#importing the module 
 
  
# opening the JSON file  
dict_ = open('levels.json',)  
  

     
# deserailizing the data 
dict_ = json.load(dict_)  
  
class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
         
        for key in dictionary:
            p = setattr(self, key, dictionary[key])
            for object in p:
                object = p(inputs)
    def __repr__(self):
        attrs = str([x for x in self.__dict__])
        return "<dict2obj: %s="">" % attrs        
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    ball_dict = {"color":"blue",
                 "size":"8 inches",
                 "material":"rubber"}
    ball = Dict2Obj(data1)

p = Dict2Obj(data1)
for object in p:
     object = p(inputs)
print(p.level2)
class OurObject:
    def __init__(self, /, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
x = json.dumps(dict_)
y = json.loads(x, object_hook=lambda d: OurObject(**d))
print(y)'''
import json
from types import SimpleNamespace

class Level:
    brick_y = []
    brick_break = []
    brick_x = []

    def Load(self, level_number: int):
        """
        load level by number using self generated number from array
        """
        with open('data2.json') as json_file:
            level = Level()
            level = json.loads(json_file.read(), object_hook=lambda d: SimpleNamespace(**d))
            # the problem is understanding the lambda expressions and what is SimpleNamespace, 
            # but isn't important at this stage. just assume as working blackbox
            return level[level_number]
        
        
l = Level()

# this is ugly shortcut for assigning all atributes at one line instead of one by one
# should be refactored later, not importatnt for now
l: Level = l.Load(0)
print('----------------brick_break------------')
print(l.brick_break)
print('----------------brick_x------------')
print(l.brick_x)
print('----------------brick_y------------')
print(l.brick_y)     