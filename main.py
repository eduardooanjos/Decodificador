def decrypt_rsa(cipher_blocks, d, n):
    return [pow(c, d, n) for c in cipher_blocks]


def to_text(blocks):
    chars = []
    for value in blocks:
        if 0 <= value <= 255:
            chars.append(chr(value))
        else:
            chars.append(f"[{value}]")
    return "".join(chars)


def read_cipher_blocks(path):
    blocks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                blocks.append(int(line))
    return blocks


if __name__ == "__main__":
    n = int(input("Digite n: ").strip())
    d = int(input("Digite d: ").strip())

    cipher_blocks = read_cipher_blocks("text.txt")
    plain_blocks = decrypt_rsa(cipher_blocks, d, n)

    print("Blocos descriptografados:")
    print(plain_blocks)

    print("Texto (ASCII quando possível):")
    print(to_text(plain_blocks))

