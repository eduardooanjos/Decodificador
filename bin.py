numbers = []

with open("text.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            numbers.append(bin(int(line))[2:]) 

print(numbers)
