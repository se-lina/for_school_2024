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
            print(f"Response: {response.decode('utf-8')}")
            return response.decode('utf-8')
        except socket.timeout:
            retries += 1
            print(f"Retry {retries}/{max_retries}: No response for command - {command}")
    raise Exception(f"Command '{command}' failed after {max_retries} retries")

def main():
    try:
        # Telloをコマンドモードにする
        send_command_with_retry("command")

        # 離陸
        send_command_with_retry("takeoff")
        time.sleep(5)

        # 前進100cm
        send_command_with_retry("forward 100")
        time.sleep(2)

        # 左回転90度
        send_command_with_retry("ccw 90")
        time.sleep(2)

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
