#coding=utf-8

#通过minidom解析xml文件
import xml.dom.minidom as xmldom
import numpy as np
#返回库所，变迁，关联矩阵


def read(xmlfilepath):

    places = []
    transitions = []
    places_id = {}
    transitions_id = {}

    domobj = xmldom.parse(xmlfilepath)
    elementobj = domobj.documentElement
    place_obj = elementobj.getElementsByTagName("place")
    transition_obj = elementobj.getElementsByTagName("transition")
    arc_obj = elementobj.getElementsByTagName("arc")

    for i in range(len(place_obj)):
        places.append(place_obj[i].getElementsByTagName("text")[0].firstChild.data)
        places_id[place_obj[i].getAttribute("id")] = i
    for i in range(len(transition_obj)):
        transitions.append(transition_obj[i].getElementsByTagName("text")[0].firstChild.data)
        transitions_id[transition_obj[i].getAttribute("id")] = i

    row = len(places)
    column = len(transitions)
    incidenceMatrix=np.zeros((row,column))

    for i in range(len(arc_obj)):
        source = arc_obj[i].getAttribute("source")
        target = arc_obj[i].getAttribute("target")
        # print(arc_obj[i].getElementsByTagName("text")[0].firstChild.data)
        if source in places_id:
            if incidenceMatrix[places_id[source]][transitions_id[target]] == 1:
                incidenceMatrix[places_id[source]][transitions_id[target]] = 2
            else:
                incidenceMatrix[places_id[source]][transitions_id[target]] = -1
        else:
            if incidenceMatrix[places_id[target]][transitions_id[source]] == -1:
                incidenceMatrix[places_id[target]][transitions_id[source]] = 2
            else:
                incidenceMatrix[places_id[target]][transitions_id[source]] = 1
            # incidenceMatrix[places_id[target]][transitions_id[source]] = 1
        # if arc_obj[i].getElementsByTagName("text")[0].firstChild.data=="out":
        #     incidenceMatrix[places_id[source]][transitions_id[target]] = -1
        # else:
        #     incidenceMatrix[places_id[target]][transitions_id[source]] = 1
    start = -1
    end = -1
    for i in range(row):
        f = 1
        for j in range(column):
            if incidenceMatrix[i][j] == 1:
                f = 0
                break
        if f == 1:
            start = i
            break
    for i in range(row):
        f = 1
        for j in range(column):
            if incidenceMatrix[i][j] == -1:
                f = 0
                break
        if f == 1:
            end = i
            break
    incidenceMatrix[[start, row - 2], :] = incidenceMatrix[[row - 2, start], :]
    incidenceMatrix[[end, row - 1], :] = incidenceMatrix[[row - 1, end], :]
    places[start] ,places[row - 2] = places[row - 2] ,places[start]
    places[end], places[row - 1] = places[row - 1], places[end]
    # temp = incidenceMatrix[start][:]
    # incidenceMatrix[start][:] = incidenceMatrix[row - 2][:]
    # incidenceMatrix[row - 2][:] = temp
    # temp = incidenceMatrix[end][:]
    # incidenceMatrix[end][:] = incidenceMatrix[row - 1][:]
    # incidenceMatrix[row - 1][:] = temp
    return (places, transitions, incidenceMatrix)




