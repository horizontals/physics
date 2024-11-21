from math import sqrt
import matplotlib.pyplot as plt
from rainbow import rainbow



class DistanceException(Exception):
    pass

class Point:
    def __init__(self, position:list[float], velocity:list[float] = [0.,0.,0.], i_mass:float = 1., g_mass:float = 0., charge:float = 0., ex_force = [0.,0.,0.], is_fix:bool = False, need_history:bool = False, color = 'default'):
        self.position:list[float] = position
        self.velocity:list[float] = velocity
        self.force:list[float] = [0.,0.,0.]
        self.i_mass:float = i_mass
        self.g_mass:float = g_mass
        self.charge:float = charge
        self.is_fix:bool = is_fix
        self.ex_force:list[float] = ex_force
        self.need_history = need_history
        self.color = color
        if self.need_history:
            self.history:list[list,list,list] = [[self.position[0]],[self.position[1]],[self.position[2]]]
        

    def distance(self, point:"Point"):
        d = sqrt(sum([(point.position[i] - self.position[i]) ** 2 for i in range(3)]))
        if d==0:
            raise DistanceException()
        else:
            return d

    
    def update(self, points:set["Point"], unit_time):
        'include myself'
        if not(self.is_fix):
            self.force = [0.,0.,0.]
            for i in range(3):
                self.force[i] += self.ex_force[i]
                for e in points - {self}:
                    self.force[i] += (self.g_mass * e.g_mass - self.charge * e.charge) * (e.position[i] - self.position[i]) / self.distance(e) ** 3
            for i in range(3):
                self.velocity[i] += self.force[i] * unit_time / self.i_mass
            for i in range(3):
                self.position[i] += self.velocity[i] * unit_time
        if self.need_history:
            for i in range(3):
                self.history[i].append(self.position[i])
            

    def __str__(self):
        return f"""{self}"""


class Group:
    def __init__(self, *points, unit_time:float = 1., start_time:float = 0.):
        self.points:set[Point] = set(points)
        self.unit_time:float = unit_time
        self.total_time:float = start_time
        self.count:int = 0


    def update(self, unit_time:float = 1., count:int = 1):
        self.unit_time:float = unit_time
        self.total_time += self.unit_time
        for _ in range(count):
            self.count += 1
            for e in self.points:
                e.update(self.points, self.unit_time)
    
    def graph(self):
        fig = plt.figure(figsize=(6,6)) #図のサイズを決定
        ax = fig.add_subplot(projection='3d') #3d空間の作成
        ax.set_xlabel('x')
        ax.set_ylabel('y') # label
        ax.set_zlabel('z')
        for e,i in zip(self.points, range(len(self.points))):
            ax.scatter(*e.position, color=rainbow(i/len(self.points)))
            if e.need_history:
                if True:
                    ax.plot(*(e.history), color=rainbow(i/len(self.points)))
                else:
                    for i in range(self.count+1):
                        ax.plot(p.history[0][i:i+2],p.history[1][i:i+2],p.history[2][i:i+2],color=rainbow.rainbow(i/self.count))
        # ani = animation.ArtistAnimation(fig, ax, interval=100)
        plt.show()

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
# numpyを装備する。重くなってきた。
# unit_time, start_time はgroupが管理し、historyには適宜送る
# 色を指定できるようにする。'w'や、'rainbow'などを実装