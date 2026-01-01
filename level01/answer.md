# Level 01

## 目的
ユーザー `flag01` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 情報収集

`level01` ユーザーでログイン後、システム内のユーザーアカウント情報が格納されている `/etc/passwd` を確認します。

```bash
cat /etc/passwd
```

出力結果の中に、以下の興味深い行が見つかりました：
```text
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

通常、パスワードフィールド（2番目のフィールド）は `x` となっており、実際のハッシュは `/etc/shadow` に格納されますが、ここでは `flag01` のハッシュ `42hDRfypTqqnw` が直接公開されています。

### 2. John the Ripper によるパスワード解析

このハッシュを解読するために、パスワードクラックツール **John the Ripper** を使用します。

1.  **解析対象の準備**:
    問題の行をローカルのファイル（例: `shadow_copy`）に保存します。
    ```bash
    echo "flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash" > passwd
    ```

2.  **john の実行**:
    john にファイルを読み込ませて解析を開始します。
    ```bash
    john passwd
    ```

3.  **解析結果の確認**:
    解析が完了すると、以下のようにパスワードが表示されます。
    ```bash
    john --show passwd
    ```
    出力結果:
    ```text
    flag01:abcdefg:3001:3001::/home/flag/flag01:/bin/bash
    ```
    これにより、パスワードが `abcdefg` であることが判明しました。

### 3. フラグの取得

判明したパスワードを使って `flag01` ユーザーとしてログインし、フラグを取得します。

```bash
su flag01
# Password: abcdefg
getflag
```

## 結果

### flag01 のパスワード
`abcdefg`

### トークン (Flag)
`f2av5il02puano7naaf6adaaf`
