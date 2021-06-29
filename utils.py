from math import pi

def degree_radian(degree) :
    return pi/2*(degree/90.0)

if   __name__ == "__main__" :
    degree=90.0
    print(degree_radian(degree))
    degree=180.0
    print(degree_radian(degree))
