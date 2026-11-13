from netmiko import ConnectHandler

#1.Ciscoスイッチの接続情報


switch_1 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "cisco_password",
    "secret": "enable_password",  # enable secret のパスワード
}
switch_2= {
    "device_type": "cisco_ios",
    "host": "192.168.1.2",
    "username": "admin",
    "password": "cisco_password",
    "secret": "enable_password",  # enable secret のパスワード
}
switch_3= {
    "device_type": "cisco_ios",
    "host": "192.168.1.3",
    "username": "admin",
    "password": "cisco_password",
    "secret": "enable_password",  # enable secret のパスワード
}

rt1_device = {
    "device_type": "cisco_ios",  # 機器に応じて変更（yamaha, vyos, linux など）
    "host": "192.168.30.254",    # RT1の管理IP（警備区画側ゲートウェイ）
    "username": "admin",         # SSHログインユーザー名
    "password": "StrongPassword123!",  # SSHパスワード
    "secret": "EnableSecret123!",      # 特権モード（enable）パスワード
    "port": 22,
    "timeout": 10,
}




#2.入力するコンフィグコマンド投入リスト




