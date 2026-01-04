# Level 14

## 目的
ユーザー `flag14` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level14` ユーザーでログイン後、ホームディレクトリを確認しますが、何もありません。
システム内を検索しても、SetUIDバイナリは見当たりません。

そこで、`getflag` コマンド自体を解析することにします。
`getflag` は通常、実行ユーザーのUIDをチェックし、そのユーザーに対応するフラグを表示するプログラムです。

### 2. 解析 (Reverse Engineering)

`getflag` バイナリを解析するために、書き込み可能なディレクトリへコピーします。

```bash
cp /bin/getflag /tmp/getflag
```

`gdb` で `main` 関数を逆アセンブルしてロジックを確認します。

```bash
gdb -batch -ex "disas main" /tmp/getflag
```

解析の結果、以下のことが判明しました。

1.  **アンチデバッグ (Anti-Debugging)**:
    プログラムの冒頭で `ptrace(PTRACE_TRACEME, ...)` を呼び出しています。
    ```asm
    0x08048989 <+67>:    call   0x8048540 <ptrace@plt>
    0x0804898e <+72>:    test   %eax,%eax
    0x08048990 <+74>:    jns    0x80489a8 <main+98>
    ```
    GDB経由で実行すると `ptrace` はエラー（-1）を返すため、条件分岐 `jns`（負でないならジャンプ）が成立せず、プログラムは終了してしまいます。

2.  **UIDチェック**:
    プログラムの後半で `getuid` を呼び出し、その戻り値（UID）に応じて分岐しています。
    `flag14` のUIDである `3014` (`0xbc6`) と比較する箇所があります。
    ```asm
    0x08048afd <+439>:   call   0x80484b0 <getuid@plt>
    ...
    0x08048bb6 <+624>:   cmp    $0xbc6,%eax
    0x08048bbb <+629>:   je     0x8048de5 <main+1183>
    ```
    UIDが `3014` であれば、フラグ生成処理（`ft_des` 関数）へジャンプします。

### 3. GDBによるエクスプロイト

GDBを使用して実行中のメモリ（レジスタ）を書き換え、アンチデバッグ機構とUIDチェックの両方を回避します。

1.  `ptrace` 呼び出し後のチェックを回避するため、`eax` レジスタを `0`（成功）に書き換えます。
2.  `getuid` 呼び出し後のチェックを騙すため、`eax` レジスタを `3014` (`flag14` のUID) に書き換えます。

以下のGDBスクリプトを作成して実行します。

```bash
echo "break *0x0804898e
break *0x08048b02
run
set \$eax=0
continue
set \$eax=3014
continue
quit" > /tmp/gdb_script_14

gdb -batch -x /tmp/gdb_script_14 /tmp/getflag
```

### 4. 結果

すべてのチェックを通過し、`flag14` 用のトークンが表示されます。

```text
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```

## 結果

### トークン (Flag)
`7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ`
