# Telloドローン通信とプログラミング飛行の安定化手法

## 1. socket通信とポートに関する問題

TelloはUDPポート8889を使用して通信しますが、以下のような問題が考えられます:

- **ポートの競合**:
  - このポートに複数のデバイスがアクセスすると競合が発生し、通信が不安定になります。

- **UDP通信の特性**:
  - UDPは軽量ですが、パケットロスが発生しやすい特性があり、WiFi環境が不安定な場合や干渉が多い場合に通信が失敗することがあります。

---

## 2. WiFi干渉による影響

最近はWiFiの2.4GHz帯に多くの電波が飛び交っており、干渉が発生しやすい状況です。この干渉により以下の問題が起こる可能性があります:

- 通信の遅延や失敗
- 動作中に突然停止する、またはフリップ動作が実行されないなどの挙動の不安定さ

### 改善策

- **チャンネル設定を変更**:
  - 干渉の少ないWiFiチャンネルを選択します。
  
- **専用WiFi環境の用意**:
  - Tello専用のWiFiアクセスポイントやルーターを用意することで通信を安定させます。

---

## 3. djitellopyの利点とパケットロスについて

`djitellopy`はTelloの操作を簡素化するPythonライブラリで、内部で通信の処理が抽象化されています。このライブラリを使用すると以下の利点があります:

- **通信の安定性**:
  - パケットロスを検出し、自動的に再送信を行う仕組みを備えています。これによりUDP通信の弱点をある程度カバーできます。

- **簡単なインターフェース**:
  - シンプルな関数でTelloの動作を制御でき、コードの複雑さを軽減します。

> **注記**: djitellopyは純粋なsocketプログラミングよりも再送処理が効率的に行われますが、極端に干渉が多い環境では完全な解決には至りません。

---

## 4. まとめと提案

現在の通信問題はWiFi干渉やポート競合が原因である可能性が高いです。

### 提案

1. **専用WiFi環境の用意**:
   - 干渉を減らし、通信を安定させるための専用環境を整備します。

2. **プログラムの通信再試行ロジックの追加**:
   - UDP通信の弱点を補うため、失敗時に再送信を試みるロジックを組み込みます。

3. **次回の講義でのdjitellopy導入**:
   - 再送信やエラー処理を簡素化し、安定性を向上させるためにdjitellopyを活用します。

---

## サンプルコード: 再送信ロジックの実装

以下は、通信が失敗した場合に再送信を試みるPythonコードの例です。

```python
import socket
import time

# ソケットとTelloのアドレス設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.settimeout(5.0)  # タイムアウト設定

def send_command_with_retry(command, max_retries=3):
    retries = 0
    while retries < max_retries:
        sock.sendto(command.encode('utf-8'), tello_address)
        try:
            response, _ = sock.recvfrom(1024)
            print(f"Response: {response.decode('utf-8')}")
            return response.decode('utf-8')
        except socket.timeout:
            retries += 1
            print(f"Retry {retries}/{max_retries}: Command failed - {command}")
    raise Exception("Command failed after max retries")

# コマンドの送信
try:
    send_command_with_retry("command")
    send_command_with_retry("takeoff")
    time.sleep(5)
    send_command_with_retry("land")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
```

# Telloドローン通信とプログラミング飛行の安定化手法

## 1. 通信環境の最適化

### WiFiの専用化
- 専用ルーターやアクセスポイントを使用してTello専用のWiFi環境を作り、他のデバイスとの干渉を最小限に抑える。
- 電波干渉の少ないチャンネルを選択するために、2.4GHz帯のチャンネルを設定可能なWiFiルーターやチャンネルスキャナーを活用する。

### 環境の改善
- 通信の妨げとなる壁や家具を避け、見通しの良い場所で使用する。
- 複数台同時操作を避けるため、時間を分けて操作する。

---

## 2. プログラムの改善

### 再送信ロジックの追加
- コマンド失敗時に再送信を行うロジックを追加する。

### 命令間隔の調整
- 命令と命令の間に十分な間隔を設けることで、Telloの処理が混乱しないようにする（例: `time.sleep()`を使用）。

### サンプルコード: 再送信ロジック
```python
import socket
import time

def send_command_with_retry(command, max_retries=3):
    retries = 0
    while retries < max_retries:
        sock.sendto(command.encode('utf-8'), tello_address)
        try:
            response, _ = sock.recvfrom(1024)
            print(f"Response: {response.decode('utf-8')}")
            return response.decode('utf-8')
        except socket.timeout:
            retries += 1
            print(f"Retry {retries}/{max_retries}: Command failed - {command}")
    raise Exception("Command failed after max retries")
```

## 3. エラーハンドリングの強化

### エラー状態の検知
- 応答内容やエラーコードを確認し、状態に応じた適切な処理を行う。

### ログの記録
- 送信したコマンドと応答を記録し、トラブル発生時に原因を特定する。

#### サンプルコード: ログ記録
```python
def log_command(command, response):
    with open("tello_log.txt", "a") as log_file:
        log_file.write(f"Command: {command}, Response: {response}\n")
```

## 4. 通信プロトコルの工夫

### マルチスレッド化
- 通信の送受信を別々のスレッドで処理することで、通信の遅延を最小化する。

### UDP通信のタイムアウト設定
- `socket`オブジェクトにタイムアウトを設定し、不達時に適切な再送信を行う。

#### サンプルコード: タイムアウト設定
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5.0)  # タイムアウトを5秒に設定
```

## 5. 専用SDKの活用

- **Tello公式SDKを活用**することで、シンプルな構造で安定した通信が可能となります。
- SDKに沿ったカスタマイズを行うことで、通信の問題が発生しにくい設定を適用できます。

---

## 6. ハードウェア側の改善

### バッテリー状態の最適化
- 使用前に必ずフル充電を行い、長時間の使用後は十分な休息時間を確保します。

### ファームウェアの更新
- Telloのファームウェアを最新バージョンに保つことで、既知の問題が解決される可能性があります。

---

## 7. 次回以降の方針

次回の講義では、以下のアプローチを採用することでさらなる安定性が期待されます:

1. **djitellopyライブラリの導入**:
   - 再送信やエラー処理が内包されており、コード記述がシンプルになります。

2. **実践的な環境構築の指導**:
   - 専用WiFi環境の構築や干渉を避ける方法を指導します。

3. **事前テストの充実**:
   - 飛行環境や通信状態を事前に確認し、問題が発生しそうな要因を排除します。
