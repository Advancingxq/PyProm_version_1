path = 'F:/prom/logs_test/exercise1.txt'
log = []
with open(path, "r") as f:
    for line in f.readlines():
        line = line.split()
        if line not in log:
            log.append(line)
event = sorted(list(set(item for sub in log for item in sub)))
# 获得直接相连关系direct link
DL = []
for trace in log:
    for i in range(1,len(trace)):
        if (trace[i-1], trace[i]) not in DL:
            DL.append((trace[i-1], trace[i]))
# 获得因果关系causalities
causality = []
for item in DL:
    if (item[1], item[0]) not in DL:
        causality.append(item)
# 获得并发关系
concurrency = []
for item in DL:
    if (item[1], item[0]) in DL:
        concurrency.append(item)
# 打印因果足迹矩阵
print('  '+'  '.join(event))
for item0 in event:
    tmp = [item0]
    for item1 in event:
        if (item0, item1) in causality:
            tmp.append('->')
        elif (item0, item1) in concurrency:
            tmp.append('||')
        else:
            if (item1, item0) in causality:
                tmp.append('<-')
            else:
                tmp.append('# ')
    tmp = ' '.join(tmp)
    print(tmp)
