
def fibonacci(n):
    if n < 0:
        return -1
    elif n == 0 or n == 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
print("10 số đầu tiên của dãy số fibonacci: ")
sb = fibonacci(50)/fibonacci(51)

print(sb)

start = 16750
end = 39250

# 25000
muc1= 50
muc2= 61.8
kq =  (end - start)/100
print(kq * muc2 + start)
# print(start + 5605)
# print((start + end)* 0.618)
# print(0.618 * 100)
# print(start* 0.618)
# print((27100* 0.618/100))

