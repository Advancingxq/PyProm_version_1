import pnml_read
import graphviz as gv


def show(xmlfilepath, output_file):
    (place, transition, incidenceMatrix) = pnml_read.read(xmlfilepath)
    pn = gv.Digraph(format='png')
    pn.attr(rankdir='LR')  # left to righ layout - default is top down
    # pn.node('start')
    # pn.node('end')
    row = len(place)
    column = len(transition)
    for i in range(row):
        if not (1 in incidenceMatrix[i] or -1 in incidenceMatrix[i]):
            continue
        pn.node(place[i], shape='circle')
        for j in range(column):
            if incidenceMatrix[i][j] == 1:
                pn.node(transition[j], shape='box')
                pn.edge(transition[j], place[i])
            elif incidenceMatrix[i][j] == -1:
                pn.node(transition[j], shape='box')
                pn.edge(place[i], transition[j])
            #处理单循环的情况
            elif incidenceMatrix[i][j] == 2:
                pn.node(transition[j], shape='box')
                pn.edge(transition[j], place[i])
                pn.edge(place[i], transition[j])
    pn.render(output_file)
def show1(place, transition, incidenceMatrix, output_file):
    pn = gv.Digraph(format='png')
    pn.attr(rankdir='LR')  # left to righ layout - default is top down
    # pn.node('start')
    # pn.node('end')
    row = len(place)
    column = len(transition)
    for i in range(row):
        if not (1 in incidenceMatrix[i] or -1 in incidenceMatrix[i]):
            continue
        pn.node(place[i], shape='circle')
        for j in range(column):
            if incidenceMatrix[i][j] == 1:
                pn.node(transition[j], shape='box')
                pn.edge(transition[j], place[i])
            elif incidenceMatrix[i][j] == -1:
                pn.node(transition[j], shape='box')
                pn.edge(place[i], transition[j])
            # 处理单循环的情况
            elif incidenceMatrix[i][j] == 2:
                pn.node(transition[j], shape='box')
                pn.edge(transition[j], place[i])
                pn.edge(place[i], transition[j])
    pn.render(output_file)