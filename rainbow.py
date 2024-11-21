def rainbow(phase:float)->tuple:
    'phase is 0 to 1'
    p=phase*6
    MIN=0.
    MAX=1.
    def ad(n:float)->int:
        # return min(int(256*n), MAX)
        return min(n,MAX)

    if 0 <= phase <= 1/6:
        return (MAX, ad(p), MIN)
    elif phase <=2/6:
        return (ad(2-p),MAX, MIN)
    elif phase <= 3/6:
        return (MIN, MAX, ad(p-2))
    elif phase <=4/6:
        return (MIN,ad(4-p),MAX)
    elif phase <= 5/6:
        return (ad(p-4),MIN,MAX)
    else:
        return (MAX,MIN,ad(6-p))

