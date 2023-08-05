def _(lines):
    ret = []
    switching = False
    last_line = ''
    for line in reversed(lines):
        indent = line[0]
        if line[2] == '>':
            if not switching:
                switching = True
                if last_line is '{':
                    line[2] = ''
                else:
                    line[2] = ';'
            else:
                line[2] = ''
        elif line[2] == ';' and switching:
            line[2] = ''
            switching = False
        ret.insert(0,line)
        last_line = ''.join(line[1]).strip()
    return ret
