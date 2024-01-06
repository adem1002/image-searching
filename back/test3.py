import numpy as np
import cv2


def draw_contours( contour,title):
    img = np.zeros((500, 500), dtype=np.uint8)
    for i in range(len(contour)):
        img[contour[i][1], contour[i][0]] = 255   
    cv2.imshow(title, img)

def freeman_histogram(chain_code):
    histogram = np.zeros((8,), dtype=np.uint8)
    for i in range(len(chain_code)):
        histogram[chain_code[i]] += 1
    return histogram

def freeman_chain(img,title):
    FREEMAN = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
    gray =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 100)
    cv2.imshow("edges"+title, edges)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    x = contours[0].reshape(-1, 2)
    draw_contours(x,title)
    points = x
    chain_code = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        for j in range(len(FREEMAN)):
            if FREEMAN[j] == (dx, dy):
                chain_code.append(j)
                break
    return chain_code


def distance(d1,d2):
    return np.linalg.norm(np.array(d1)-np.array(d2) )

img1 = cv2.imread(r"back\images\1.jpg")
img1= cv2.resize(img1, (500, 500))

img2 = cv2.imread(r"back\images\2.jpg")
img2= cv2.resize(img2, (500, 500))

chain_code1 = freeman_chain(img1,"1")
chain_code2 = freeman_chain(img2,"2")
d1 = freeman_histogram(chain_code1)
d2 = freeman_histogram(chain_code2)
print(distance(d1, d2))

cv2.waitKey(0)