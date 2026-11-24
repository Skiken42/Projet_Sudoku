# Les importations
import numpy as np
import random as rd
import time

size_mat = 9

# Compteur de noeuds explorés par les solveurs
noeuds = 0


# Vérifie si val peut être placé sur la ligne i
def valid_row(mat, i, val):
    for x in range(0, size_mat):
        if mat[i, x] == val:
            return False
    return True


# Vérifie si val peut être placé sur la colonne j
def valid_column(mat, j, val):
    for x in range(0, size_mat):
        if mat[x, j] == val:
            return False
    return True


# Vérifie si val peut être placé dans le carré 3x3 de la case (i,j)
def valid_square(mat, i, j, val):
    start_row = (i // 3) * 3
    start_col = (j // 3) * 3
    for k in range(0, 3):
        for l in range(0, 3):
            if mat[start_row + k, start_col + l] == val:
                return False
    return True


def is_valid(mat, i, j, val):
    return valid_row(mat, i, val) and valid_column(mat, j, val) and valid_square(mat, i, j, val)


# Vérifie qu'aucune valeur déjà placée n'est en conflit avec une autre
def grid_is_consistent(mat):
    for i in range(size_mat):
        for j in range(size_mat):
            val = mat[i, j]
            if val != 0:
                if val < 1 or val > 9:
                    return False
                # On retire la case pour ne pas la comparer à elle-même
                mat[i, j] = 0
                ok = is_valid(mat, i, j, val)
                mat[i, j] = val
                if not ok:
                    return False
    return True


# Vérifie que la grille est pleine et respecte toutes les contraintes
def is_solution(mat):
    for i in range(size_mat):
        for j in range(size_mat):
            if mat[i, j] == 0:
                return False
    return grid_is_consistent(mat)


# Remplit les 3 carrés de la diagonale (ils sont indépendants entre eux)
def generate_diagonal():
    mat = np.zeros((size_mat, size_mat), dtype=np.int_)
    for b in range(0, 3):
        values = list(range(1, 10))
        rd.shuffle(values)
        k = 0
        for i in range(0, 3):
            for j in range(0, 3):
                mat[3 * b + i, 3 * b + j] = values[k]
                k = k + 1
    return mat


def fill(mat):
    for i in range(9):
        for j in range(9):
            if mat[i, j] == 0:
                l_candidates = list(range(1, size_mat + 1))
                rd.shuffle(l_candidates)
                for n in l_candidates:
                    if is_valid(mat, i, j, n):
                        mat[i, j] = n
                        if fill(mat):
                            return True
                        else:
                            mat[i, j] = 0  # backtrack, on tombe dans un cas impossible
                return False
    return True


def remove(mat, n):
    l_tested = []

    # On met dans l_tested tous les couples (i,j) différents de zero
    for i in range(9):
        for j in range(9):
            if mat[i, j] != 0:
                l_tested.append((i, j))
    if n > len(l_tested):
        print("Erreur : pas assez de valeurs dans la grille")
        return mat
    rd.shuffle(l_tested)
    removed = 0
    for i, j in l_tested:
        if removed == n:
            break
        value = mat[i, j]
        mat[i, j] = 0
        if count_solutions(mat.copy()) == 1:
            removed += 1
        else:
            mat[i, j] = value
    if removed < n:
        print("Attention : seulement " + str(removed) + " cases retirées sur " + str(n) + " demandées")
    return mat


def count_solutions(mat, limit=2):
    # Une grille de départ incohérente n'a aucune solution
    if not grid_is_consistent(mat):
        return 0
    return count(mat, limit)


def count(mat, limit):
    # Chercher une case vide
    for i in range(9):
        for j in range(9):
            if mat[i, j] == 0:
                c = 0
                for k in range(1, 10):
                    if is_valid(mat, i, j, k):
                        mat[i, j] = k
                        c += count(mat, limit - c)
                        mat[i, j] = 0
                        if c >= limit:
                            return c
                return c
    return 1


def generate_sudoku(n):
    mat = generate_diagonal()
    fill(mat)
    remove(mat, n)
    return mat


# SOLVEUR 1 : backtracking simple

def backtracking(mat):
    global noeuds
    noeuds = noeuds + 1
    for i in range(9):
        for j in range(9):
            if mat[i, j] == 0:
                for n in range(1, 10):
                    if is_valid(mat, i, j, n):
                        mat[i, j] = n
                        if backtracking(mat):
                            return True
                        mat[i, j] = 0  # backtrack
                return False
    return True


def solve_backtracking(mat):
    global noeuds
    noeuds = 0
    mat = mat.copy()
    if not grid_is_consistent(mat):
        return None
    if backtracking(mat):
        return mat
    return None


# SOLVEUR 2 : backtracking + propagation de contraintes (forward checking + MRV)
# Chaque case a un domaine : la liste des valeurs encore possibles

# Renvoie la liste des cases qui partagent une contrainte avec (i,j) (20 car 8 ligne, 8 colonne 4 dans le carre)
def peers(i, j):
    l = []
    for x in range(9):
        if x != j:
            l.append((i, x))
        if x != i:
            l.append((x, j))
    start_row = (i // 3) * 3
    start_col = (j // 3) * 3
    for k in range(0, 3):
        for m in range(0, 3):
            r = start_row + k
            c = start_col + m
            if r != i and c != j:
                l.append((r, c))
    return l


# Copie les domaines pour pouvoir revenir en arrière
def copy_domains(dom):
    # dico dom sous la forme : dom = { (0,0): [4, 7],   (0,1): [9],   (0,2): [1, 2, 5] }
    new = {}
    for cell in dom:
        # list sinon on ne travaille pas sur une copie on pointe sur dom[cell]
        new[cell] = list(dom[cell])
    return new


# Affecte v à la case puis retire v du domaine de toutes les cases voisines
def assign(dom, cell, v):
    # veirfie bien que v est une valeure possible dans le dom de la cellule
    if v not in dom[cell]:
        return False
    dom[cell] = [v]
    to_propagate = [cell]
    while len(to_propagate) > 0:
        #on prend la derniere de la liste on pop et on propage sur les voisins 
        #(on les previens qu'on vient de psoer la valeur et on l'enleve de leur dom
        c = to_propagate.pop()
        val = dom[c][0]
        for p in peers(c[0], c[1]):
            if val in dom[p]:
                dom[p].remove(val)
                # Domaine vide : mauvais choix on s'arrête
                if len(dom[p]) == 0:
                    return False
                # Une seule valeur possible : on la propage à son tour
                if len(dom[p]) == 1:
                    to_propagate.append(p)
                # sinon plusieurs choix, on continue
    return True


# Crée les domaines de départ à partir de la grille
def init_domains(mat):
    dom = {}
    for i in range(9):
        for j in range(9):
            dom[(i, j)] = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if mat[i, j] != 0:
                if not assign(dom, (i, j), int(mat[i, j])):
                    return None
    return dom


# Heuristique MRV : choisit la case non fixée qui a le moins de valeurs possibles (la plus contrainte)
def select_mrv(dom):
    best = None
    for cell in dom:
        if len(dom[cell]) > 1:
            # quel est la case qui a le moins de valeurs possible
            if best is None or len(dom[cell]) < len(dom[best]):
                best = cell
    return best


def backtracking_propagation(dom):
    global noeuds
    noeuds = noeuds + 1
    cell = select_mrv(dom)
    # Plus aucune case à choisir toutes les cases sont fixées
    if cell is None:
        return dom
    # on propage à partir de la meilleure case : 
    for v in dom[cell]:
        #copie du domaine sinon on pointe vers le même endroit et on peux pas revenir en arriere si echoue
        new = copy_domains(dom)
        if assign(new, cell, v):
            res = backtracking_propagation(new)
            if res is not None:
                return res
    return None  # backtrack


def solve_propagation(mat):
    global noeuds
    noeuds = 0

    #grille valide
    if not grid_is_consistent(mat.copy()):
        return None

    # domaine
    dom = init_domains(mat)
    if dom is None:
        return None
    res = backtracking_propagation(dom)
    if res is None:
        return None
    # on reconvertit de dom vers une matrice pour l'afficher et manipuler plus simplement
    sol = np.zeros((size_mat, size_mat), dtype=np.int_)
    for i in range(9):
        for j in range(9):
            sol[i, j] = res[(i, j)][0]
    return sol


# Affichage

def show_grid(mat):
    for i in range(size_mat):
        for j in range(size_mat):
            print(mat[i, j], end=" ")
        print()


def solvable(mat):
    c = count_solutions(mat.copy())
    if c == 1:
        print("Solution unique")
    elif c > 1:
        print("Solutions multiples")
    else:
        print("Non solvable")


def test(nom, grille):
    mat = np.array(grille)
    print("Grille : " + nom)
    show_grid(mat)
    solvable(mat)

    debut = time.perf_counter()
    sol = solve_backtracking(mat)
    temps = (time.perf_counter() - debut) * 1000
    print("Backtracking simple : " + str(round(temps, 1)) + " ms, " + str(noeuds) + " noeuds")

    debut = time.perf_counter()
    sol = solve_propagation(mat)
    temps = (time.perf_counter() - debut) * 1000
    print("Backtracking + propagation : " + str(round(temps, 1)) + " ms, " + str(noeuds) + " noeuds")

    if sol is None:
        print("Pas de solution")
    else:
        print("Solution :")
        show_grid(sol)
        print("Solution valide : " + str(is_solution(sol)))
    print()


# Grilles de test (0 = case vide)

facile = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
          [9, 0, 0, 3, 0, 5, 0, 0, 1],
          [0, 0, 1, 8, 0, 6, 4, 0, 0],
          [0, 0, 8, 1, 0, 2, 9, 0, 0],
          [7, 0, 0, 0, 0, 0, 0, 0, 8],
          [0, 0, 6, 7, 0, 8, 2, 0, 0],
          [0, 0, 2, 6, 0, 9, 5, 0, 0],
          [8, 0, 0, 2, 0, 3, 0, 0, 9],
          [0, 0, 5, 0, 1, 0, 3, 0, 0]]

moyenne = [[0, 0, 0, 0, 0, 0, 9, 0, 7],
           [0, 0, 0, 4, 2, 0, 1, 8, 0],
           [0, 0, 0, 7, 0, 5, 0, 2, 6],
           [1, 0, 0, 9, 0, 4, 0, 0, 0],
           [0, 5, 0, 0, 0, 0, 0, 4, 0],
           [0, 0, 0, 5, 0, 7, 0, 0, 9],
           [9, 2, 0, 1, 0, 8, 0, 0, 0],
           [0, 3, 4, 0, 5, 9, 0, 0, 0],
           [5, 0, 7, 0, 0, 0, 0, 0, 0]]

difficile = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 3, 6, 0, 0, 0, 0, 0],
             [0, 7, 0, 0, 9, 0, 2, 0, 0],
             [0, 5, 0, 0, 0, 7, 0, 0, 0],
             [0, 0, 0, 0, 4, 5, 7, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 3, 0],
             [0, 0, 1, 0, 0, 0, 0, 6, 8],
             [0, 0, 8, 5, 0, 0, 0, 1, 0],
             [0, 9, 0, 0, 0, 0, 4, 0, 0]]

vide = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Deux 5 sur la première ligne
incoherente = [[5, 5, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# La dernière case de la première ligne ne peut prendre aucune valeur
sans_solution = [[1, 2, 3, 4, 5, 6, 7, 8, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 9],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]


# Programme principal

test("Facile", facile)
test("Moyenne", moyenne)
test("Difficile", difficile)
test("Vide", vide)
test("Incoherente", incoherente)
test("Sans solution", sans_solution)
test("Generee", generate_sudoku(55))