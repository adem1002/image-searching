
import numpy as np
import cv2


# form
def form_method(image):
    contours = get_contours(image)
    descriptors = []
    for contour in contours:
        descriptors.append(freeman_chain_code(contour.reshape(-1, 2).tolist()))
    return descriptors


def get_contours(image, acceptable_size=0.8):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresholded_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY) 

    contours, _ = cv2.findContours(thresholded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_contour = max(contours, key=cv2.contourArea)
    max_ = cv2.contourArea(largest_contour)*acceptable_size
    return list(filter(lambda x: cv2.contourArea(x) >= max_, contours))


def freeman_chain_code(contour, size=192):
    directions = [(1, 0), (1, -1), (0, -1), (-1, -1),
                  (-1, 0), (-1, 1), (0, 1), (1, 1)]
    start_point = min(contour, key=lambda point: np.linalg.norm(point))
    start_index = contour.index(start_point)

    chain_code = []
    current_point = start_point

    for i in range(len(contour) - 1):
        next_point = contour[(start_index + i + 1) % len(contour)]
        direction_vector = (next_point[0] - current_point[0], next_point[1] - current_point[1])
        direction_index = directions.index(direction_vector)
        chain_code.append(direction_index)
        current_point = next_point

    return interpolation(np.array(chain_code, dtype=np.float32)/8, size).tolist()



def interpolation(d, size):
    s = len(d)
    m = size/s
    index_array = np.arange(size)
    trans_array = index_array/m
    cond = (trans_array >= 0) & (trans_array < s)
    floor_array = np.floor(trans_array).astype('int32')[cond]
    floor_array_ = floor_array + 1
    semi_cond = floor_array_ >= s
    floor_array_[semi_cond] = floor_array[semi_cond]
    eps_array = (trans_array[cond] - floor_array)
    m_eps_array = 1 - eps_array
    result = np.zeros((size, ))
    result[index_array[cond]] = m_eps_array*d[floor_array] + eps_array*d[floor_array_]
    return result


def distance_freeman_descriptor(d1, d2):
    distance1 = np.abs(d1 - d2)
    distance2 = 1 - distance1
    return np.linalg.norm(np.minimum(distance1, distance2))


def _distance_hausdorff(p, X):
    return min([distance_freeman_descriptor(p, q) for q in X])


def distance_hausdorff(X, Y):
    return max(max([_distance_hausdorff(np.array(p), Y) for p in X]), max([_distance_hausdorff(np.array(p), X) for p in Y]))





# color

def distance(d1,d2):
    return np.linalg.norm(np.array(d1)-np.array(d2) )


def color_method(image):
    result = np.zeros((8, 8, 3), dtype=np.uint8)
    width, height = image.shape[:2]
    pas_w, pas_h = width / 8, height / 8
    for i in range(8):
        for j in range(8):
            result[i, j] = np.mean(image[int(i * pas_w):int((i + 1) * pas_w), int(j * pas_h):int((j + 1) * pas_h), :],
                                axis=(0, 1))
    result = cv2.cvtColor(result, cv2.COLOR_BGR2YCrCb)
    return (result.flatten().astype('float') / 255 ).tolist()


def image_search(query_image, database, method='color_descriptor'):
    query_feature = None

    if method == 'color_descriptor':
        pass
        # query_feature = color_descriptor(query_image)

    # elif method == 'freeman_chain':
    #     query_feature = freeman_chain(query_image)

    # elif method == 'dct_descriptor':
    #     query_feature = dct_descriptor(query_image)

    # elif method == 'cld_descriptor':
    #     query_feature = cld_descriptor(query_image, rows=4, cols=4)

    elif method == 'color_method':
        query_feature = color_method(query_image)

    results = []

    for index, (image, _) in enumerate(database):
        if method == 'color_descriptor':
            pass

        elif method == 'color_method':
            image_feature = color_method(image)
            similarity = distance(query_feature, image_feature)

        results.append((index, similarity))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def draw_contours( contour,title):
        contour= contour.reshape(-1, 2)
        img = np.zeros((500, 500), dtype=np.uint8)
        for i in range(len(contour)):
            img[contour[i][1], contour[i][0]] = 255   
        cv2.imshow(title, img)

if __name__ == "__main__":
  
    database = [
        (cv2.resize(cv2.imread(r"back\images\1.jpg"), (512, 512)), "Label 1"),
        (cv2.resize(cv2.imread(r"back\images\2.jpg"), (512, 512)), "Label 2"),
        (cv2.resize(cv2.imread(r"back\images\3.jpg"), (512, 512)), "Label 3"),
        (cv2.resize(cv2.imread(r"back\images\4.jpg"), (512, 512)), "Label 4"),
        (cv2.resize(cv2.imread(r"back\images\5.jpg"), (512, 512)), "Label 5"),
        (cv2.resize(cv2.imread(r"back\images\6.jpg"), (512, 512)), "Label 6"),
        (cv2.resize(cv2.imread(r"back\images\7.jpg"), (512, 512)), "Label 7"),
        (cv2.resize(cv2.imread(r"back\images\8.jpg"), (512, 512)), "Label 8"),
        (cv2.resize(cv2.imread(r"back\images\9.jpg"), (512, 512)), "Label 9"),
        (cv2.resize(cv2.imread(r"back\images\10.jpg"), (512, 512)), "Label 10"),
        (cv2.resize(cv2.imread(r"back\images\11.jpg"), (512, 512)), "Label 11"),
        (cv2.resize(cv2.imread(r"back\images\12.jpg"), (512, 512)), "Label 12"),
        (cv2.resize(cv2.imread(r"back\images\13.jpg"), (512, 512)), "Label 1"),
        (cv2.resize(cv2.imread(r"back\images\14.png"), (512, 512)), "Label 2"),
        (cv2.resize(cv2.imread(r"back\images\15.png"), (512, 512)), "Label 3"),

     
        
    ]

    # Load a query image
    query_image = cv2.resize(cv2.imread(r"back\images\a1.jpg"), (512, 512))

    # Perform image search using color descriptor
    color_method_results = image_search(query_image, database, method='color_method')
    print("Color Method Results:", color_method_results)

    img1 = cv2.imread(r"back\images\4.jpg")
    img1= cv2.resize(img1, (500, 500))

    img2 = cv2.imread(r"back\images\3.jpg")
    img2= cv2.resize(img2, (500, 500))
 
    d1 = form_method(img1)
    d2 = form_method(img2)
    c1 = get_contours(img1)[0]
    c2 = get_contours(img2)[0]
    draw_contours(c1,"1")
    draw_contours(c2,"2")

    print(distance_hausdorff(d1, d2))

    cv2.waitKey(0)