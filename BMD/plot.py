import cv2
import csv

img = cv2.imread('map.png', 1)
yellow=(40,255,255)
green=(0,255,0)
red=(0,0,255)
orange=(0,165,255)
i=0
count=0
c=(0,255,255)

def color():
    global c
    #print(type(count))
    if count == '1' or count =='2':
        c=green
        print("green")
    if count == '3' or count == '4':
        c=yellow
        print("yellow")
    if count =='5' or count == '6':
        c=orange
        print("orange")
    if count == '7':
        c=red
        print("red")

with open('traffic.csv', 'rt') as traff:
    reader=csv.reader(traff)
    rows = list(reader)

n=0
count=rows[n][1]
color()

cv2.line(img,(990,280),(1397,291),c,2)
n += 1
count=rows[n][1]
print(count)
color()
cv2.line(img,(747,253),(990,280),c,2)
n += 1
count=rows[n][1]
print(count)
color()
cv2.line(img,(747,253),(632,243),c,2)
n += 1
count=rows[n][1]
print(count)
color()
cv2.line(img,(632,243),(484,322),c,2)
n += 1
count=rows[n][1]
print(count)
color()
cv2.line(img,(484,322),(415,510),c,2)
n += 1
count=rows[n][1]
print(count)
color()
cv2.line(img,(415,510),(440,593),c,2)
n += 1
count=rows[n][1]
print(count)
color()
cv2.line(img,(440,593),(417,687),c,2)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
