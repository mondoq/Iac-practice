from netmiko import ConnectHandler

device={
   "device_type": "cisco_ios",  # 機器に応じたタイプを指定
    "host": "192.168.1.1",
    "username": "admin",
    "password": "password123",
    "secret": "enable_secret",   # 特権モード(enable)パスワード（必要な場合）
}


config_commands=[
  "interface GigabitEthernet0/1",
   "description  Connected_to_CoreSwitch",
   "ip address 10.0.0.1 255.255.255.0",
   "no shutdown",
]
with ConnectHandler(**device) as connect:

    connect.enable()

    #コンフィグ投入
    cfg_output =connect.send_config_set(config_commands)
    print(cfg_output)
    
    #設定の保存（write memory/copy run start）
    save_output=connect.save_config()
    print(save_output)


