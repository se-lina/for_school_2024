import socket
import time

# ソケットとTelloアドレスの設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(('', 9000))  # ローカルポート9000で受信待機
sock.settimeout(5.0)  # タイムアウトを5秒に設定

def send_command_with_retry(command, max_retries=3):
    """
    Telloにコマンドを送信し、応答が得られない場合に再送信を試みる
    """
    retries = 0
    while retries < max_retries:
        try:
            print(f"Sending command: {command}")
            sock.sendto(command.encode('utf-8'), tello_address)
            response, _ = sock.recvfrom(1024)  # 応答待ち
            response_decoded = response.decode('utf-8', errors='ignore')
            print(f"Response: {response_decoded}")
            return response_decoded
        except socket.timeout:
            retries += 1
            print(f"Retry {retries}/{max_retries}: No response for command - {command}")
    raise Exception(f"Command '{command}' failed after {max_retries} retries")

def get_battery_level():
    """
    Telloのバッテリー残量を取得
    """
    try:
        response = send_command_with_retry("battery?")
        print(f"Battery level: {response}%")
        return int(response)
    except Exception as e:
        print(f"Failed to get battery level: {e}")
        return -1  # エラー時は-1を返す

def main():
    try:
        # Telloをコマンドモードにする
        send_command_with_retry("command")

        # バッテリー残量を表示
        battery_level = get_battery_level()
        if battery_level < 20:
            print("Warning: Low battery level. Please charge before flight.")
            return  # バッテリーが低い場合、処理を終了

        # 離陸
        send_command_with_retry("takeoff")
        time.sleep(5)

        # 前進100cm
        print("Moving forward 100cm")
        send_command_with_retry("forward 100")
        time.sleep(3)

        # 左100cm移動
        print("Moving left 100cm")
        send_command_with_retry("left 100")
        time.sleep(3)

        # 後進100cm
        print("Moving backward 100cm")
        send_command_with_retry("back 100")
        time.sleep(3)

        # 右100cm移動
        print("Moving right 100cm")
        send_command_with_retry("right 100")
        time.sleep(3)

        # 着陸
        send_command_with_retry("land")
        print("Landing completed")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # ソケットを閉じる
        sock.close()

if __name__ == "__main__":
    main()
