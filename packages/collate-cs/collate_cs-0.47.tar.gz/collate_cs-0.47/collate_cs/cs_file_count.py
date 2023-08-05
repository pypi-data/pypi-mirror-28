def _(files):
    if len(files) == 0:
        return 0
    ret = 0
    for file in files:
        if file[-3:] == '.cs':
            ret = ret + 1
    return ret
