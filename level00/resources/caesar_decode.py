import sys

def caesar_cipher(text, shift):
    """
    指定されたシフト数で文字列を回転（シーザー暗号）させます。
    """
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <encrypted_string>")
        sys.exit(1)
    
    s = sys.argv[1]
    print(f"Brute-forcing rotations for: {s}\n")
    
    # 全26パターンの回転を出力して、意味の通る単語を探す
    for i in range(26):
         print(f"Rot {i:2}: {caesar_cipher(s, i)}")
