## IART 2018-19
Klotski

csv format

ex:
d;4;5 
p;2;3;1;n
t;n,1;n,0;n,0;n,0

1st elem: identifier: 
    d - table dimensions; 
    p - piece ; 
    t - table row

d;4;5 -> table size 4x5

piece line: 
    2 -> id -> int
    3;1 -> 3x1 dimensions
    n -> type: final = f ; temp = t ; normal = n

table line:
    n,1:
        n -> cell type: final= f ; parede = p ; normal = n
        1 -> id of piece; 0 -> empty
    n,0:
        n -> cell type: final= f ; parede = p ; normal = n
        0 -> empty