a = int(input("a: "))
b = int(input("b: "))
while b:
    prev_a = int(a)
    a = int(b)
    b = (prev_a % b)
print(a)