numbers = []
binary = []
hexadecimal = []

with open("text.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            n = int(line)
            numbers.append(n)          
            binary.append(bin(n)[2:]) 
            hexadecimal.append(hex(n)[2:])  

# print(numbers)
# print(binary)
print(hexadecimal)
