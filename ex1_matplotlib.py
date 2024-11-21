import ex_world as w
a=w.Point([0,0,0], charge=1, is_fix=True)
p=w.Point([1,1,0], [0,0.7,0], charge=-1, need_history=True)
group=w.Group(a,p)
group.update(0.1, 1000)
group.graph()

b2=w.Point([0,0,0], [1,0,0], need_history=True, ex_force=[0,0,-1])
group2=w.Group(b2)
group2.update(1.,100)
group2.graph()