# 川崎総合科学高等学校プログラミング講義
## 実施日と講義資料
7月29日  
https://drive.google.com/file/d/13NcvVI1JnNOOxINp_omOwzv4NEavg5f9/view?usp=sharing

8月28日  
このGitHubの資料を使います。

## 講義の目的
この講義では、Pythonを使ったプログラミングの基礎と、Telloドローンの操作を通じて、プログラミングの実践的な応用を学びます。

## 1. PCのセットアップ確認
### WindowsにPythonをインストールする手順
1. Pythonの公式ウェブサイト（https://www.python.org）からインストーラーをダウンロードします。
2. ダウンロードしたインストーラーを実行し、「Add Python to PATH」にチェックを入れてからインストールを進めます。

### GitHubアカウントの作成と基本的な使い方
- GitHubにアクセス（https://github.com）して、「Sign up」からアカウントを作成します。
- 基本的なリポジトリ操作（クローン、プル、プッシュ）については、GitHubのヘルプセクションを参照してください。

## 2. Pythonプログラミングの基礎
Pythonの基本的な構文として、変数、データ型、条件分岐、ループについて説明します。具体的なコード例は以下のリンクから参照できます。  
本講義では、Telloを動かす基礎的なところだけを学びます。  
- [Pythonの基礎](https://pycamp.pycon.jp/textbook/index.html)
- [Python Boot Camp 教科書](https://pycamp.pycon.jp/textbook/index.html)

## 3. PCとTelloの接続方法とバックグラウンド技術
### ネットワーク設定とUDP通信
- TelloドローンとのWi-Fi接続設定方法とUDP通信の基本を解説します。

## 4. 接続してデモフライトの実施
Pythonを使用してTelloドローンを操作する基本的なコマンドを実行します。以下に基本的なフライトコマンドの例を示します。

```python
# Telloドローンを離陸させる
drone.takeoff()

# 前進させる
drone.move_forward(30)

# 旋回させる
drone.rotate_clockwise(90)

# 着陸させる
drone.land()
