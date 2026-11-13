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
    mat = np.zeros(size,size)
    for i in range (0, 2):
        for j in range(0, 2):
            mat[i][j]
def generate_sudoku(size, difficulty):
    
    for i in range (0,8):
        for j in range (0,8):
def 















































































































































print("Ligne de séparation")

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