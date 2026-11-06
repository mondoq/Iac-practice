from netmiko import ConnectHandler

# 使い方の大枠イメージ
from netmiko import ConnectHandler

# 接続したいルーターの情報をセットする
cisco_router = {
    'device_type': 'cisco_ios',  # 機器の種類（Cisco）
    'host': '192.168.1.1',       # ルーターのIP
    'username': 'admin',         # ユーザー名
    'password': 'password123',   # パスワード
}

# ConnectHandlerを使って実際に接続する（裏で自動ログインされる）
with  ConnectHandler(**cisco_router) as connect:
     #接続後の処理を記載をする
     output=connect.send_command("show ip interface brief")
    





