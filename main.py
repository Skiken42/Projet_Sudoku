# Les importations
import numpy as np
import random as rd

size_mat = 9
def valid_row(mat,i,val):
    can_place = True
    for x in range(0,size_mat):
        if mat[i,x] == val:
            can_place = False
    return can_place

def valid_column(mat,j,val):
    can_place = True
    for x in range(0,size_mat):
        if mat[x,j] == val:
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

def is_valid(mat,i,j,val):
    return valid_row(mat,i,val) and valid_column(mat,j,val) and valid_square(mat,i,j,val)
def genereate_diagonal():
    mat = np.zeros((size_mat,size_mat), dtype=np.int_)
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


def fill(mat):
    for i in range(9):
        for j in range(9):
            if mat[i, j] == 0:
                l_candidates = list(range(1,size_mat+1))
                rd.shuffle(l_candidates)
                for n in l_candidates:
                    if is_valid(mat,i,j,n):
                        mat[i,j] = n
                        if fill(mat):
                            return True
                        else:
                            mat[i,j] = 0 #backtrack, on tombe dans un cas impossible
                return False
    return True

def remove(mat, n):
    l_tested = []

    # On met dans l tested tous les couples (i,j) différents de zero
    for i in range(9):
        for j in range(9):
            if mat[i, j] != 0:
                l_tested.append((i, j))
    if n > len(l_tested):
        print("Pas assez de val dans la grille")
    rd.shuffle(l_tested)
    removed = 0
    for i, j in l_tested:
        if removed != n:
            value = mat[i, j]
            mat[i, j] = 0
            if count_solutions(mat.copy()) == 1:
                removed += 1
            else:
                mat[i, j] = value
    return mat

def count_solutions(mat, limit=2):
    # Chercher une case vide
    for i in range(9):
        for j in range(9):
            if mat[i, j] == 0:
                count = 0
                for k in range(1, 10):
                    if is_valid(mat, i, j, k):
                        mat[i, j] = k
                        count += count_solutions(mat, limit - count)
                        mat[i, j] = 0
                        if count >= limit:
                            return count
                return count
    return 1

def generate_sudoku(n):
    mat = genereate_diagonal()
    fill(mat)
    remove(mat, n)
    return mat

def show_grid(mat):
    for i in range (size_mat):
        for j in range (size_mat):
            print(mat[i,j], end=" ")
        print()

def solvable(mat):
    c = count_solutions(mat)
    if c == 1:
        print("Solution unique")
    elif c >1:
        print("Solution multiples")
    else:
        print("Non Solvable")
mat=generate_sudoku(59)
show_grid(mat)
solvable(mat)