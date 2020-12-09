import graphviz as gv
import numpy as np

# 获取日志
from pnml_generate import PNML


def get_log(input_file):
    log = []
    with open(input_file, "r") as f:
        for line in f.readlines():
            line = line.split()
            if line not in log:
                log.append(line)
    return log


# Tw
def get_Tw(log):
    return list(set(item for sub in log for item in sub))


# 邻接关系
def get_directLink(log):
    dL = []
    for event in log:
        for i in range(0, len(event) - 1):
            if (event[i], event[i + 1]) not in dL:
                dL.append((event[i], event[i + 1]))
    return dL


# 因果关系
def get_causalities(log):
    dL = get_directLink(log)
    causalities = []
    for item in dL:
        if (item[1], item[0]) not in dL:
            causalities.append(item)
    return causalities


# 非因果关系
def get_noCausalities(log):
    Tw = get_Tw(log)
    dL = get_directLink(log)
    noCausalities = []
    for item1 in Tw:
        for item2 in Tw:
            if (item1, item2) not in dL and (item2, item1) not in dL:
                if (item1, item2) not in noCausalities:
                    noCausalities.append((item1, item2))
    return noCausalities


# Ti
def get_Ti(log):
    return list(set(event[0] for event in log))


# To
def get_To(log):
    return list(set(event[-1] for event in log))


# Xw
def get_Xw(log):
    Xw = []
    Tw = get_Tw(log)
    Sets = []
    noCausalities = get_noCausalities(log)
    causalities = get_causalities(log)
    for i in range(1, (1 << len(Tw))):
        Set = []
        for j in range(0, 32):
            if (i >> j) & 1 == 1:
                Set.append(Tw[j])
        Sets.append(Set)
    flag = 1
    for i in range(0, len(Sets)):
        for j in range(0, len(Sets)):
            flag = 1
            for item1 in Sets[i]:
                if flag == 0:
                    break
                for item2 in Sets[i]:
                    if (item1, item2) not in noCausalities:
                        flag = 0
                        break
            for item1 in Sets[j]:
                if flag == 0:
                    break
                for item2 in Sets[j]:
                    if (item1, item2) not in noCausalities:
                        flag = 0
                        break
            for item1 in Sets[i]:
                if flag == 0:
                    break
                for item2 in Sets[j]:
                    if (item1, item2) not in causalities:
                        flag = 0
                        break
            if flag == 0:
                continue
            Xw.append((Sets[i], Sets[j]))
    return Xw


# Yw
def get_Yw(log):
    Xw = get_Xw(log)
    Yw = []
    for item1 in Xw:
        num = 0
        for item2 in Xw:
            if set(item1[0]).issubset(item2[0]) and set(item1[1]).issubset(item2[1]):
                num += 1
        if num == 1:
            Yw.append(item1)
    return Yw


# 输出三元组（库所，变迁，关联矩阵）
def get_incidenceMatrix(log):
    Yw = get_Yw(log)
    Tw = get_Tw(log)
    row = len(Yw) + 2
    column = len(Tw)
    place = []
    for item in Yw:
        place.append(str(item))
    place.append(str('start'))
    place.append(str('end'))
    incidenceMatrix = np.zeros((row, column))
    for i in range(0, row-2):
        for item in Yw[i][0]:
            transition_ind = -1
            for ind in range(0, column):
                if Tw[ind] == item:
                    transition_ind = ind
                    break
            incidenceMatrix[i][transition_ind] = 1
        for item in Yw[i][1]:
            transition_ind = -1
            for ind in range(0, column):
                if Tw[ind] == item:
                    transition_ind = ind
                    break
            incidenceMatrix[i][transition_ind] = -1
    Ti = get_Ti(log)
    To = get_To(log)
    for item in Ti:
        transition_ind = -1
        for ind in range(0, column):
            if Tw[ind] == item:
                transition_ind = ind
                break
        incidenceMatrix[row - 2][transition_ind] = -1
    for item in To:
        transition_ind = -1
        for ind in range(0, column):
            if Tw[ind] == item:
                transition_ind = ind
                break
        incidenceMatrix[row - 1][transition_ind] = 1
    return (place, Tw, incidenceMatrix)

#得到pnml格式的WF网
def get_WFnet(log, netName):
    (place, Tw, incidenceMatrix)=get_incidenceMatrix(log)
    # return PNML('Untitled',place, Tw, incidenceMatrix)
    return PNML(netName, place, Tw, incidenceMatrix)
# 输出模型
def show(log, output_file):
    Yw = get_Yw(log)
    Ti = get_Ti(log)
    To = get_To(log)
    pn = gv.Digraph(format='png')
    pn.attr(rankdir='LR')  # left to righ layout - default is top down
    pn.node('start')
    pn.node('end')
    for item in Yw:
        pn.node(str(item), shape='circle')
        for i in item[0]:
            pn.edge(i, str(item))
            pn.node(i, shape='box')
        for i in item[1]:
            pn.edge(str(item), i)
            pn.node(i, shape='box')
    for i in Ti:
        pn.edge('start', i)
    for o in To:
        pn.edge(o, 'end')
    pn.render(output_file)
