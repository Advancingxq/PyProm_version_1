import random


# 分别输入库所，变迁，关联矩阵，构造轨迹
def event_generate(place, transition, incidenceMatrix):
    start = len(place) - 2
    end = len(place) - 1
    event = []
    enableTransition = []
    placewithToken = []
    placewithToken.append(start)
    # (x,y) y is 0 representing the place or is transition
    for i in range(len(transition)):
        flag = 1
        for j in range(end + 1):
            if incidenceMatrix[j][i] == -1 and j not in placewithToken:
                flag = 0
                break
        if flag == 1 and i not in enableTransition:
            enableTransition.append(i)
    step = 1
    while True:
        if step == 1000:
            return [-1]
        a = random.choice(enableTransition)
        event.append(a)
        for j in range(end + 1):
            if incidenceMatrix[j][a] == -1:
                placewithToken.remove(j)
            elif incidenceMatrix[j][a] == 1:
                placewithToken.append(j)
            #处理单循环

        if end in placewithToken:
            break
        enableTransition.clear()
        for i in range(len(transition)):
            flag = 1
            for j in range(end + 1):
                if incidenceMatrix[j][i] == -1 and j not in placewithToken:
                    flag = 0
                    break
            if flag == 1 and i not in enableTransition:
                enableTransition.append(i)

        step += 1
    for i in range(len(event)):
        event[i] = transition[event[i]]
    return event


# 分别输入库所，变迁，关联矩阵，轨迹数量，构造日志
def stochastic_generate(place, transition, incidenceMatrix, num):
    log = []
    for i in range(num):
        temp = event_generate(place, transition, incidenceMatrix)
        if temp not in log:
            log.append(temp)
    if [-1] in log:
        log.remove([-1])
    return log
