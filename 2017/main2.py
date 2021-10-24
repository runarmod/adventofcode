import numpy as np
from io import StringIO


train_string = '''
111 13 12 1 161 335800
125 13 66 1 468 379100
46 6 127 2 961 118950
80 9 80 2 816 247200
33 10 18 2 297 107950
85 9 111 3 601 266550
24 10 105 2 1072 75850
31 4 66 1 417 93300
56 3 60 1 36 170650
49 3 147 2 179 149000
'''

test_string = '''
82 2 65 3 516 0
82 2 65 3 516 0
82 2 65 3 516 0
'''

def main():
    np.set_printoptions(precision=1)    # this just changes the output settings for easier reading

    # read in the training data and separate it to x_train and y_train
    x_train = np.asarray([line[:-1] for line in np.genfromtxt(StringIO(train_string), skip_header=1)])
    y = np.asarray([line[-1] for line in np.genfromtxt(StringIO(train_string), skip_header=1)])
    # fit a linear regression model to the data and get the coefficients
    c = np.asarray(np.linalg.lstsq(x_train, y)[0])

    # read in the test data and separate x_test from it
    x_test = np.asarray([line[:-1] for line in np.genfromtxt(StringIO(test_string), skip_header=1)])

    # print out the linear regression coefficients
    print(c)

    # this will print out the predicted prics for the two new cabins in the test data set
    print(x_test @ c)


main()
