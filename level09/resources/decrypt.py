import os

# スクリプトと同じディレクトリにあるtokenファイルを参照するように修正
file_path = os.path.join(os.path.dirname(__file__), "token")

try:
    with open(file_path, "rb") as f:
        data = f.read()
except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    exit(1)

decrypted = ""
for i, byte in enumerate(data):
    # 各バイト値からインデックス番号を引く
    val = byte - i
    # 表示可能な文字（ASCII 32-126）の範囲内であれば追加
    if 32 <= val <= 126:
        decrypted += chr(val)

# 復号されたパスワードのみを表示
print(decrypted)