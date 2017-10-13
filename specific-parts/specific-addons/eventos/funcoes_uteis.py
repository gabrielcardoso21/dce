def float_to_time(f):
    time = ''
    i = int(f)
    if i < 10:
        time += '0'
    time += str(i)
    time += ':'
    f -= i
    f *= 60
    i = '{0:.0f}'.format(f)
    if int(i) < 10:
        time += '0'
    time += i
    return time
