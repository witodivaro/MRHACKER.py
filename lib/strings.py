def find_all(line, sub):
    start = 0
    while True:
        start = line.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)
