import json


class Make_level:
    def __init__(self):
        self.LEVEL1_Y_BRICK = []
        self.LEVEL1_BREAKABLE_BRICK = []
        self.LEVEL1_X_BRICK = []
        self.level2_break = []
        self.level3_break = []

    def make(self):

        _count = -20
        _y = 40
        for _i in range(112):
            _count += 60
            if _count > 950:
                _count = 40
                _y += 60
            self.LEVEL1_X_BRICK.insert(_i, _count)
            self.LEVEL1_Y_BRICK.insert(_i, _y)
            self.LEVEL1_BREAKABLE_BRICK.insert(_i, 2)
            self.level2_break.insert(_i, 4)
            self.level3_break.insert(_i, 6)


make_level = Make_level()
make_level.make()
data = {}
data['level1'] = []
'''data['level2'] = []
data['level3'] = []
data['level4'] = []'''
data['level1'].append({
    'brick_x': make_level.LEVEL1_X_BRICK,
    'brick_y': make_level.LEVEL1_Y_BRICK,
    'brick_break': make_level.LEVEL1_BREAKABLE_BRICK
})
data['level2'] = []
data['level2'].append({
    'brick_x': make_level.LEVEL1_X_BRICK,
    'brick_y': make_level.LEVEL1_Y_BRICK,
    'brick_break': make_level.level2_break
})
data['level3'] = []
data['level3'].append({
    'brick_x': make_level.LEVEL1_X_BRICK,
    'brick_y': make_level.LEVEL1_Y_BRICK,
    'brick_break': make_level.level3_break
})
data['level4'] = []
data['level4'].append({
    'brick_x': make_level.LEVEL1_X_BRICK,
    'brick_y': make_level.LEVEL1_Y_BRICK,
    'brick_break': make_level.level3_break
})


with open('data2.txt', 'w') as outfile:
    json.dump(data, outfile)
print(make_level.LEVEL1_BREAKABLE_BRICK)
