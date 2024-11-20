from math import sqrt

class DistanceException(Exception):
    pass

class Point:
    unit_time:float = 1.
    def __init__(self, position:list[float], velocity:list[float] = [0.,0.,0.], i_mass:float = 1., g_mass:float = 0., charge:float = 0., is_fix:bool = False, need_history:bool=False):
        self.position:list[float] = position
        self.velocity:list[float] = velocity
        self.force:list[float] = [0.,0.,0.]
        self.i_mass:float = i_mass
        self.g_mass:float = g_mass
        self.charge:float = charge
        self.is_fix:bool = is_fix
        self.ex_force:list[float] = [0.,0.,0.]
        self.need_history = need_history
        if self.need_history:
            self.history = [[self.position[0]],[self.position[1]],[self.position[2]]]

    def distance(self, point:"Point"):
        d = sqrt(sum([(point.position[i] - self.position[i]) ** 2 for i in range(3)]))
        if d==0:
            raise DistanceException()
        else:
            return d

    
    def update(self, points:set["Point"]):
        'include myself'
        if not(self.is_fix):
            self.force = [0.,0.,0.]
            for i in range(3):
                for e in points - {self}:
                    self.force[i] += (self.g_mass * e.g_mass - self.charge * e.charge) * (e.position[i] - self.position[i]) / self.distance(e) ** 3 + self.ex_force[i]
            for i in range(3):
                self.velocity[i] += self.force[i] * self.unit_time / self.i_mass
            for i in range(3):
                self.position[i] += self.velocity[i] * self.unit_time
        if self.need_history:
            for i in range(3):
                self.history[i].append(self.position[i])
            

    def __str__(self):
        return f"""{self}"""


class Group:
    def __init__(self, *points, start_time:float = 0.):
        self.points:set[Point] = set(points)
        self.total_time:float = start_time
        
    def update(self):
        self.total_time += Point.unit_time
        for e in self.points:
            e.update(self.points)

if __name__ == '__main__':
    a=Point([5,0,0], charge=1, is_fix=True)
    b=Point([-5,0,0], charge=1, is_fix=True)
    p=Point([1,0,0], charge=1)
    group=Group(a,b,p)
    while True:
        group.update()
        print(p.position)

# 今後の展望
# need_history==tureならhistoryをもち、[x[],y[],z[]]型、[x[],y[],z[],t[]]型、[pos[]]型などを持つ
# 外力については、関数を変数として持つ
# matplotlibを組み込む
# numpyを装備する
