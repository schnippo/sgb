N = 5
sum = 0
with open("testlines", "r") as f:
    for line in f.readlines() [-N:]:
        sum += int(line)
    print(str(sum / N))

