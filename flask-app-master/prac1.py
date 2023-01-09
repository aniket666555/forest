s1 = '0110,0101,1010,0001'
l=s1.split(",")
print(l)

for no in l:
    dec=int (no,2)
    if(dec%5 ==0):
        print(no)
