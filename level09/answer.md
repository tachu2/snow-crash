# Level 09

## 目的
ユーザー `flag09` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level09` ユーザーでログイン後、ホームディレクトリを確認します。

```bash
ls -l
```
出力:
```text
-rwsr-sr-x 1 flag09  level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09  level09   26 Mar  5  2016 token
```
`level09` というSetUIDバイナリと、中身が読めない（バイナリ形式の）`token` ファイルがあります。

`level09` コマンドを実行してみると、引数として渡した文字列を単純に変化させて出力することがわかります。

```bash
./level09 aaaaa
# output: abcde
```

この変化の法則は、文字のASCIIコードにインデックス（0から始まる位置番号）を加算するというものです。
*   'a' (97) + 0 = 'a' (97)
*   'a' (97) + 1 = 'b' (98)
*   ...

`token` ファイルには、この法則で暗号化されたパスワードが保存されていると推測されます。

### 2. 復号

`token` ファイルの中身を読み出し、逆の計算（文字コード - インデックス）を行って元のパスワードを復元するスクリプトを作成します。

```python
# tokenファイルの内容（バイナリとして読み込む）
encrypted = b'f4kmm6p|=\x82\x7fp\x82n\x83\x82DB\x83Du{\x7f\x8c\x89\n'
decrypted = ""

for i, byte in enumerate(encrypted):
    # 最後の改行文字などは計算結果が負になる場合があるため無視する
    val = byte - i
    if val >= 0:
        decrypted += chr(val)

print(decrypted)
```

このスクリプトを実行すると、以下の文字列が得られました。
`f3iji1ju5yuevaus41q1afiuq`

### 3. 結果

復元したパスワードを使って `flag09` としてログインし、フラグを取得します。

```bash
su flag09
# Password: f3iji1ju5yuevaus41q1afiuq
getflag
```

## 結果

### flag09 のパスワード
`f3iji1ju5yuevaus41q1afiuq`

### トークン (Flag)
`s5cAJpM8ev6XHw998pRWG728z`
