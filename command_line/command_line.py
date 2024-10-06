from math import*
xbeg=-10
xend=8
dx=1
print("Значение функции на интервале от -10 до 8")
print("x\ty")
for x in range(xbeg,xend+1):
    if x<=-8: print(x,"\t",-3)
    elif x>-8 and x<=-3: print(x,"\t",0.6*x+1.2)
    elif x>-3 and x<=3: print(x,"\t",-sqrt(9-x**2))
    elif x>3 and x<=5: print(x,"\t",x-3)
    elif x>5 and x<=8: print(x,"\t",3)