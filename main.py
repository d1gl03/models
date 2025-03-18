from itertools import product

count = 0

for num in product('01234567', repeat=4):
    if num[0] == '0':
        continue
    freq = {}
    for digit in num:
        freq[digit] = freq.get(digit, 0) + 1
    if list(freq.values()).count(2) == 1 and list(freq.values()).count(1) == 3:
        count += 1

print(f"Количество чисел: {count}")