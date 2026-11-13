# Les importations
import numpy as np
import random as rd

size_mat = 9
def valid_row(mat,i,val):
    can_place = True
    for x in range(0,size_mat):
        if mat[[i],[x]] == val:
            can_place = False
    return can_place

def valid_column(mat,j,val):
    can_place = True
    for x in range(0,size_mat):
        if mat[[x],[j]] == val:
            can_place = False
    return can_place

def number_to_place(mat,i,j):
    number = list(range(1,size_mat,1))
    return number

def valid_square(mat, i,j, val):
    start_row = (i // 3) * 3
    start_col = (j // 3) *3
    for k in range (0,3):
        for l in range (0,3):
            if mat[start_row+k, start_col+l] == val:
                return False
    return True
def genereate_diagonal():
    mat = np.zeros((size_mat,size_mat))
    for i in range (0, 3):
        for j in range(0, 3):
            n=rd.randint(1,9)
            while not (valid_square(mat, i, j, n)):
                n=rd.randint(1,9)
            mat[i, j] = n
            n=rd.randint(1,9)
            while not (valid_square(mat, i+3, j+3, n)):
                n=rd.randint(1,9)
            mat[i+3, j+3] = n
            n=rd.randint(1,9)
            while not (valid_square(mat, i+6, j+6, n)):
                n=rd.randint(1,9)
            mat[i+6, j+6] = n
    return mat   

def show_grid(mat):
    for i in range (size_mat):
        for j in range (size_mat):
            print(mat[i,j], end=" ")
        print()


show_grid(genereate_diagonal())