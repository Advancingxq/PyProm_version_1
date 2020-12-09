def event_add(event, log):
    log.append(event)
    return log


def event_del(event, log):
    if event in log:
        log.remove(event)
    return log