#!/usr/bin/env python3
"""
MD5 Cracker para Penetration Testing
Autor: HackerAI
Uso: python md5_cracker.py hash.txt wordlist.txt
"""

import hashlib
import sys
import argparse
import time
from pathlib import Path

def md5_hash(text):
    """Gera hash MD5 de string"""
    return hashlib.md5(text.encode()).hexdigest().lower()

def crack_from_wordlist(target_hash, wordlist_path, show_progress=True):
    """Crack usando wordlist"""
    print(f"[+] Testando wordlist: {wordlist_path}")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[-] Wordlist não encontrada: {wordlist_path}")
        return None
    
    total = len(lines)
    for i, line in enumerate(lines):
        candidate = line.strip()
        if md5_hash(candidate) == target_hash:
            print(f"[+] CRACKED! MD5({target_hash}) = {candidate}")
            return candidate
        
        if show_progress and i % 10000 == 0:
            print(f"\r[{i}/{total}] Testados...", end='', flush=True)
    
    print(f"\n[-] Não encontrado na wordlist")
    return None

def crack_common_passwords(target_hash):
    """Passwords comuns hardcoded"""
    common = [
        "admin", "password", "123456", "12345678", "qwerty", "abc123",
        "Password123", "admin123", "letmein", "welcome", "monkey",
        "dragon", "master", "hello", "freedom", "whatever", "qazwsx",
        "trustno1", "prince", "shadow", "ginger", "photoshop", "azerty"
    ]
    
    print("[+] Testando senhas comuns...")
    for pwd in common:
        if md5_hash(pwd) == target_hash:
            print(f"[+] CRACKED! MD5({target_hash}) = {pwd}")
            return pwd
    return None

def rainbow_table_attack(target_hash, charset="abcdefghijklmnopqrstuvwxyz0123456789", max_len=6):
    """Rainbow table simples (brute force limitado)"""
    print(f"[+] Rainbow table attack (até {max_len} chars)...")
    
    from itertools import product
    import string
    
    chars = charset[:10]  # Limita charset para performance
    
    for length in range(1, max_len + 1):
        for combo in product(chars, repeat=length):
            candidate = ''.join(combo)
            if md5_hash(candidate) == target_hash:
                print(f"[+] CRACKED! MD5({target_hash}) = {candidate}")
                return candidate
    
    print("[-] Não encontrado no rainbow table")
    return None

def main():
    parser = argparse.ArgumentParser(description="MD5 Cracker para Pentest")
    parser.add_argument("hash_file", help="Arquivo com hash(es) MD5")
    parser.add_argument("wordlist", nargs="?", help="Wordlist (rockyou.txt)")
    parser.add_argument("--brute", action="store_true", help="Rainbow table attack")
    parser.add_argument("--maxlen", type=int, default=5, help="Max length brute force")
    
    args = parser.parse_args()
    
    if not Path(args.hash_file).exists():
        print(f"[-] Arquivo de hash não encontrado: {args.hash_file}")
        return
    
    with open(args.hash_file, 'r') as f:
        hashes = [line.strip() for line in f if line.strip()]
    
    print(f"[*] Carregando {len(hashes)} hash(es)...")
    
    for target_hash in hashes:
        if len(target_hash) != 32 or not all(c in '0123456789abcdef' for c in target_hash):
            print(f"[-] Hash inválido: {target_hash}")
            continue
            
        print(f"\n[*] Atacando: {target_hash}")
        start_time = time.time()
        
        # 1. Senhas comuns
        result = crack_common_passwords(target_hash)
        if result: continue
        
        # 2. Wordlist
        if args.wordlist:
            result = crack_from_wordlist(target_hash, args.wordlist)
            if result: continue
        
        # 3. Rainbow table
        if args.brute:
            result = rainbow_table_attack(target_hash, max_len=args.maxlen)
            if result: continue
        
        print(f"[-] Falha: {target_hash}")
        print(f"[*] Tempo: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()