import time
start_time = time.time()
st = 0
while True:
    current = int(time.time() - start_time)
    if current != st:
        print(current)
        st = current
    # print(current)