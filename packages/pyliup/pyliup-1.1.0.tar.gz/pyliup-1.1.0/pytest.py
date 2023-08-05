def  tuxing() :
    n=1
    m=1
    while n<8 :
        t=(8-m)//2
        print(" "*t+"*"*m)
        n=n+1
        if n<5:
            m=m+2
        else:
            m=m-2
