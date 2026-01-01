# Level 00

## 目的
ユーザー `flag00` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 手がかりの検索

まず、権限を持っている可能性が高い `flag00` ユーザーが所有するファイルをシステム全体から検索します。

```bash
find / -user flag00 2>/dev/null
```

*   **コマンド説明**:
    *   `find /`: ルートディレクトリ `/` から検索を開始します。
    *   `-user flag00`: 所有者が `flag00` であるファイルを指定します。
    *   `2>/dev/null`: 「許可がありません（Permission denied）」などのエラーメッセージを画面に表示しないように破棄します。

**実行結果**:
```text
/usr/sbin/john
/rofs/usr/sbin/john
```
`/usr/sbin/john` というファイルが見つかりました。

### 2. ファイル内容の確認

見つかったファイルの内容とファイル形式を確認します。

```bash
cat /usr/sbin/john
```

*   **コマンド説明**:
    *   `cat`: ファイルの内容を表示します。

**実行結果**:
```text
cdiiddwpgswtgt
```
意味不明な文字列が表示されました。これは暗号化されたパスワードである可能性が高いです。

### 3. 暗号の解読

文字列が単純なアルファベットのみで構成されているため、シーザー暗号（回転暗号）を疑います。
解読用のスクリプトを作成して実行します。

**実行コマンド**:
```bash
python3 level00/resources/caesar_decode.py cdiiddwpgswtgt
```

*   **コマンド説明**:
    *   作成した `caesar_decode.py` スクリプトに、見つかった文字列 `cdiiddwpgswtgt` を引数として渡します。
    *   スクリプトは0から25までの全パターンの回転を行い、結果を出力します。

**スクリプトの出力結果（一部抜粋）**:
```text
...
Rot 11: nottoohardhere
...
```
`Rot 11` の結果が `nottoohardhere` （Not too hard here = ここまでは難しくない）という英語の文章になりました。これがパスワードです。

### 4. フラグの取得

判明したパスワードを使って `flag00` ユーザーに切り替え、フラグを取得します。

```bash
su flag00
```

*   **コマンド説明**:
    *   `su flag00`: ユーザーを `flag00` に切り替えます（Switch User）。
    *   パスワードを求められるので、先ほど解読した `nottoohardhere` を入力します。

ログインに成功したら、`getflag` コマンドを実行します。

```bash
getflag
```

*   **コマンド説明**:
    *   `getflag`: この課題専用のコマンドで、条件を満たしていればフラグを表示します。

## 結果

### flag00 のパスワード
`nottoohardhere`

### トークン (Flag)
`x24ti5gi3x0ol2eh4esiuxias`
