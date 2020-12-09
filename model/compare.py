import numpy as np
from munkres import Munkres


def calculate_commonality(preSet1, postSet1, preSet2, postSet2):
    cartesianProduct1 = set()
    for item1 in preSet1:
        for item2 in postSet1:
            cartesianProduct1.add((item1, item2))
    cartesianProduct2 = set()
    for item1 in preSet2:
        for item2 in postSet2:
            cartesianProduct2.add((item1, item2))
    return (len(cartesianProduct1 & cartesianProduct2) + len(preSet1 & preSet2) + len(postSet1 & postSet2)) \
           / (max(len(cartesianProduct1), len(cartesianProduct2)) \
              + max(len(preSet1), len(preSet2)) + max(len(postSet1), len(postSet2)))


def place_hungarian(place1, transition1, incidenceMatrix1, place2, transition2, incidenceMatrix2):
    row = len(place1)
    column = len(place2)
    profit = np.zeros((row, column))
    for i in range(0, row):
        for j in range(0, column):
            preSet_place1 = set()
            postSet_place1 = set()
            for k in range(0, len(transition1)):
                if incidenceMatrix1[i][k] == 1:
                    preSet_place1.add(transition1[k])
                elif incidenceMatrix1[i][k] == -1:
                    postSet_place1.add(transition1[k])
                #处理单循环的情况下
                elif incidenceMatrix1[i][k] == 2:
                    preSet_place1.add(transition1[k])
                    postSet_place1.add(transition1[k])
            preSet_place2 = set()
            postSet_place2 = set()
            for k in range(0, len(transition2)):
                if incidenceMatrix2[j][k] == 1:
                    preSet_place2.add(transition2[k])
                elif incidenceMatrix2[j][k] == -1:
                    postSet_place2.add(transition2[k])
                #处理单循环的情况下
                elif incidenceMatrix2[j][k] == 2:
                    preSet_place2.add(transition2[k])
                    postSet_place2.add(transition2[k])
            profit[i][j] = calculate_commonality(preSet_place1, postSet_place1, preSet_place2, postSet_place2)
    cost_matrix = []
    for item in profit:
        cost_row = []
        for subitem in item:
            cost_row += [1.0 - subitem]
        cost_matrix += [cost_row]

    m = Munkres()
    indexes = m.compute(cost_matrix)
    total = 0
    for x, y in indexes:
        total += profit[x][y]
    return 2 * total / (len(place1) + len(place2))
