import cv2
from sklearn import svm
import os
import numpy as np
from sklearn.externals import joblib
from skimage.feature import hog
import sys

pos_img_dir = "../INRIAPerson/train_64x128_H96/pos/"
neg_img_dir = "../INRIAPerson/train_64x128_H96/neg/"
pos_test_img_dir = "../INRIAPerson/test_64x128_H96/pos/"
neg_test_img_dir = "../INRIAPerson/test_64x128_H96/neg/"

def shuffle_in_unison(a, b):
    a = np.array(a)
    b = np.array(b)
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


def crop_centre(img):
    h, w, d = img.shape
    l = (w - 64)/2
    t = (h - 128)/2
    #print (h, w, l, t)
    crop = img[t:t+128, l:l+64]
    return crop


def read_filenames():

    f_pos = []
    f_neg = []
    f_test_pos = []
    f_test_neg = []

    mypath_pos = pos_img_dir
    for (dirpath, dirnames, filenames) in os.walk(mypath_pos):
        f_pos.extend(filenames)
        break

    mypath_neg = neg_img_dir
    for (dirpath, dirnames, filenames) in os.walk(mypath_neg):
        f_neg.extend(filenames)
        break

    mypath_pos = pos_test_img_dir
    for (dirpath, dirnames, filenames) in os.walk(mypath_pos):
        f_test_pos.extend(filenames)
        break

    mypath_neg = neg_test_img_dir
    for (dirpath, dirnames, filenames) in os.walk(mypath_neg):
        f_test_neg.extend(filenames)
        break

    return f_pos, f_neg, f_test_pos, f_test_neg



def read_images(pos_files, neg_files, pos_test_files, neg_test_files):

    X = []
    Y = []
    X_test = []
    Y_test = []

    for img_file in pos_files:
        img = cv2.imread(pos_img_dir + img_file)
        #filename, file_extension = os.path.splitext(mypath_pos + img_file)
        #filename = os.path.basename(filename)
        cropped = crop_centre(img)
        cropped = cropped/255.0
        #gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #features = hog(cropped, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True)
        #joblib.dump(features, "features/pos/" + filename + ".feat")
        X.append(cropped)
        Y.append([1, 0])

    print "Read Positive images"

    # Loading Negative images

    for img_file in neg_files:
        img = cv2.imread(neg_img_dir + img_file)
        #filename, file_extension = os.path.splitext(mypath_neg + img_file)
        #filename = os.path.basename(filename)
        cropped = crop_centre(img)
        cropped = cropped/255.0
        #gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #features = hog(gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True)
        #joblib.dump(features, "features/neg/" + str(filename) + ".feat")
        X.append(cropped)
        Y.append([0, 1])

    print "Read Negative Images"

    for img_file in pos_test_files:
        img = cv2.imread(pos_test_img_dir + img_file)
        #filename, file_extension = os.path.splitext(mypath_pos + img_file)
        #filename = os.path.basename(filename)
        cropped = crop_centre(img)
        cropped = cropped/255.0
        #gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #features = hog(cropped, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True)
        #joblib.dump(features, "features/pos/" + filename + ".feat")
        X_test.append(cropped)
        Y_test.append([1, 0])

    print "Read Positive Test images"

    # Loading Negative images

    for img_file in neg_test_files:
        img = cv2.imread(neg_test_img_dir + img_file)
        #filename, file_extension = os.path.splitext(mypath_neg + img_file)
        #filename = os.path.basename(filename)
        cropped = crop_centre(img)
        cropped = cropped/255.0
        #gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #features = hog(gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True)
        #joblib.dump(features, "features/neg/" + str(filename) + ".feat")
        X_test.append(cropped)
        Y_test.append([0, 1])

    print "Read Negative Test Images"




    return X, Y, X_test, Y_test



def sliding_window(image, window_size, step_size):
    '''
    This function returns a patch of the input image `image` of size equal
    to `window_size`. The first image returned top-left co-ordinates (0, 0)
    and are increment in both x and y directions by the `step_size` supplied.
    So, the input parameters are -
    * `image` - Input Image
    * `window_size` - Size of Sliding Window
    * `step_size` - Incremented Size of Window

    The function returns a tuple -
    (x, y, im_window)
    where
    * x is the top-left x co-ordinate
    * y is the top-left y co-ordinate
    * im_window is the sliding window image
    '''
    for y in xrange(0, image.shape[0]-128, step_size[1]):
        for x in xrange(0, image.shape[1]-64, step_size[0]):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])




def hard_negative_mine(clf, f_neg, winSize, winStride):

    hard_negatives = []
    hard_negative_labels = []
    count = 0
    num = 0
    for imgfile in f_neg:
        #filename, file_extension = os.path.splitext(neg_img_dir + imgfile)
        #filename = os.path.basename(filename)
        img = cv2.imread(neg_img_dir + imgfile)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for (x, y, im_window) in sliding_window(gray, winSize, winStride):
            features = hog(im_window, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True)
            if (clf.predict([features]) == 1):
                hard_negatives.append(features)
                hard_negative_labels.append(0)
                #joblib.dump(features, "features/neg_mined/" + str(filename) + str(imgcount) + ".feat")
                count = count + 1

        num = num + 1

        #print "Images Done: " + str(num)
        sys.stdout.write("\r" + "Images Done: " + str((num/1218.0)*100) + "\tHard negatives: " + str(count))

        #print "Hard Negatives: " + str(count)
        if (num == 600):
            break
        sys.stdout.flush()

    return hard_negatives, hard_negative_labels


def read_dataset():


    pos_img_files, neg_img_files, pos_test_img_files, neg_test_img_files = read_filenames()

    print "Total Positive Images : " + str(len(pos_img_files))
    print "Total Negative Images : " + str(len(neg_img_files))
    print "Reading Images"

    X, Y, X_test, Y_test = read_images(pos_img_files, neg_img_files, pos_test_img_files, neg_test_img_files)



    # Randomize data

    #np.random.shuffle(X)
    #np.random.shuffle(Y)
    X_shuffled, Y_shuffled = shuffle_in_unison(X, Y)
    X_test_shuffled, Y_test_shuffled = shuffle_in_unison(X_test, Y_test)
    #np.random.shuffle(X_test)
    #np.random.shuffle(Y_test)
    print "Images Read"

    # Initializing classifiers

    return X_shuffled, Y_shuffled, X_test_shuffled, Y_test_shuffled


"""
print "Hard Negative Mining"

winStride = (8, 8)
winSize = (64, 128)
hard_negatives, hard_negative_labels = hard_negative_mine(clf, neg_img_files, winSize, winStride)
sys.stdout.write("\n")


X_final = np.concatenate((X, hard_negatives))
Y_final = np.concatenate((Y, hard_negative_labels))

print "Final Samples: " + str(len(X_final))
print "Retraining the classifier with final data"

clf.fit(X_final, Y_final)

print "Trained and Dumping"

joblib.dump(clf, 'person_final.pkl')
"""
