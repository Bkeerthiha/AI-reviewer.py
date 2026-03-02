
def add(a, b, c, d, e):
    return a + b + c + d + e

def long_function():
    total = 0
    for i in range(10):
        total += i
        for j in range(5):
            total += j
            for k in range(3):
                total += k

    for x in range(5):
        total += x
    for y in range(5):
        total += y
    for z in range(5):
        total += z

    return total

def nested_function():
    if True:
        if True:
            if True:
                if True:
                    print("Deep nesting")
