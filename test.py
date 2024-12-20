n = 100
for i in range(2, n, 1):
    is_prime = True
    for j in range(2, i, 1):
        if 0 == (i % j):
            is_prime = False
            break
    if is_prime:
        print(i)