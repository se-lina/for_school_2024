# Telloドローン通信とプログラミング飛行の安定化手法②

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

### 上記を加味した新しいプログラミングをお伝えします。
#### 追加された機能のポイント
再送信ロジック (send_command_with_retry):

コマンドを送信し、応答がない場合に最大3回まで再送信を試みます。
応答が得られない場合、例外をスローします。
タイムアウトの設定:

ソケットのタイムアウトを5秒に設定し、長時間応答がない場合に次の処理に進めるようにしています。
リトライ処理の実装:

コマンド送信に失敗した場合の処理を強化し、通信の信頼性を向上させています。

https://github.com/se-lina/for_school_2024/blob/main/basic_act_improvement.py


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
