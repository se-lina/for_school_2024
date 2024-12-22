Telloドローン通信改善手法

作成日　2024年12月22日

Telloドローンをプログラミングで動作させる場合の通信改善を行ったドキュメントとプログラミング例です。  
下記の内容で原因と説明及び改善を含めてお伝えします。  
高校生向けの資料に極力配慮していますが、  
通信関係の箇所があるため、難しい部分もあり、予めご了承ください。
  
* [Telloドローン通信とプログラミング飛行の安定化手法①(このページ)](https://github.com/se-lina/for_school_2024/blob/main/document3.md)  
* [Telloドローン通信とプログラミング飛行の安定化手法②](https://github.com/se-lina/for_school_2024/blob/main/document3_1.md)  
* [改善後Telloドローンのプログラム説明資料](https://github.com/se-lina/for_school_2024/blob/main/basic_act_improvement.py)  

  
# Telloドローン通信とプログラミング飛行の安定化手法①
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
こちらに関しては、プログラミング言語の考え方など、少し難しい手法があり、  
初見での導入は難しいですが、参考程度に見ていただけると幸いです。
