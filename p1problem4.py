#Austin Wang, June 30, 2020
#Problem 4 of Problem Set 1

import numpy as np #imported to pass in numpy arrays
import copy #imported to use deepcopy for testing speed of algos

#function to return determinant in a 2 X 2 matrix
def det2By2(matrix):
    #apply the formula to the function
    return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

#function to return determinant in a 3 X 3 matrix
def det3By3(matrix):
    #store the top row as variables, for multiplication later
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[0][2]
    #cut the bottom two rows to submatrices
    subA = matrix[1:, 1:]
    subB = matrix[1:, 0::2]
    subC = matrix[1:, :2]
    #apply formula for calculating determinant in a 3 by 3 matrix (given)
    return a * det2By2(subA) - b * det2By2(subB) + c * det2By2(subC)

#challenge problem
def detNByN(matrixList): #does not work with numpy... value shape error?
    det = 0 #initialize det as 0
    if (len(matrixList) == 2): #base case with 2x2 matrix
        return det2By2(matrixList) #det2X2 method from earlier
    for i in range(0, len(matrixList)): #interate through indexes list with length of matrix
        matrixCopy = copy.deepcopy(matrixList) #deepcopy the matrix so not affected by change
        matrixCopy = matrixCopy[1:] #remove the top row in the copy
        for j in range(0, len(matrixCopy)): #iterate through the length of submatrix
            matrixCopy[j] = matrixCopy[j][:i] + matrixCopy[j][i+1:] #slice off unnecessary column
            #'+' between matrixCopy[j][:i], matrixCopy[j][i+1:]
            #allows for all rows to be added when assigning it into the array
        if (i % 2 == 0): #alternate the sign
            sign = 1
        else:
            sign = -1
        #recursive function with submatrix * top row index number * sign
        det += sign * detNByN(matrixCopy) * matrixList[0][i] #add/sub product (alternating sign)
    #return final determinant
    return det

def convertNumpyToList(matrix): #helper function to avoid numpy shapes error
    return matrix.tolist() #not the best solution :(

#test cases for 2 by 2 Matrix Determinant
print('2 X 2 Matrices Test')
matrix1 = np.array([[1, 2],
                    [3, 4]]) #det = -2
print(matrix1)
print(det2By2(matrix1)) #returns -2
print(int(round(np.linalg.det(matrix1)))) #test with numpy method

matrix2 = np.array([[5, 3],
                    [2, 1]]) #det = -1
print(matrix2)
print(det2By2(matrix2)) #returns -1
print(int(round(np.linalg.det(matrix2)))) #test with numpy method

matrix3 = np.array([[-1, 0],
                    [0, -1]]) #det = 1
print(matrix3)
print(det2By2(matrix3)) #returns 1
print(int(round(np.linalg.det(matrix3)))) #test with numpy method

#test cases for 3 by 3 Matrix Determinant
print('3 X 3 Matrices Test')
matrix4 = np.array([[4, -1, 1],
                    [4, 5, 3],
                    [-2, 0, 0]]) #det = 16
print(matrix4)
print(det3By3(matrix4)) #returns 16
print(int(round(np.linalg.det(matrix4)))) #test with numpy method

matrix5 = np.array([[2, 0, -2],
                    [0, -1, 1],
                    [4, -2, 2]]) #det = -8
print(matrix5)
print(det3By3(matrix5)) #returns -8
print(int(round(np.linalg.det(matrix5)))) #test with numpy method

matrix6 = np.array([[2, 3, 0],
                    [5, -1, -1],
                    [-1, 0, 4]]) #det = -65
print(matrix6)
print(det3By3(matrix6)) #returns -65
print(int(round(np.linalg.det(matrix6)))) #test with numpy method

#testing N by N determinant function
print('N x N Matrices Test')
matrix7 = np.array([[1, 2, 3, 4, 1],
                    [0, -1, 2, 4, 2],
                    [0, 0, 4, 0, 0],
                    [-3, -6, -9, -12, 4],
                    [0, 0, 1, 1, 1]]) #det = 28
print(matrix7)
print(detNByN(convertNumpyToList(matrix7))) #returns 28
print(int(round(np.linalg.det(matrix7)))) #test with numpy method

matrix8 = np.array([[2, 3, 0],
                    [5, -1, -1],
                    [-1, 0, 4]]) #det = -65
print(matrix8)
print(detNByN(convertNumpyToList(matrix8))) #returns -65
print(int(round(np.linalg.det(matrix8)))) #test with numpy method

matrix9 = np.array([[5, 3],
                    [2, 1]]) #det = -1
print(matrix9)
print(detNByN(convertNumpyToList(matrix9))) #returns -1
print(int(round(np.linalg.det(matrix9)))) #test with numpy method
