from netmiko import ConnectHandler

#1.Ciscoスイッチの接続情報

cisco_switch = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "cisco_password",
    "secret": "enable_password",  # enable secret のパスワード
}


#2.入力するコンフィグコマンド投入リスト

vlan_commands=[
 #---VLAN作成---
 "vlan 10",
 "name SALES",
 "exit",
#---アクセスポートへの割り当て--

"interface GigabitEthernet0/1",
"swithport mode acess",
"switchport access vlan 10",
"exit",

#---トランクポートの設定---
"interface GigabitEthernet0/24",
"swirchport mode trunk",
"switchport trunk allowed vlan 10,20",
]

#3.SSh接続してコマンドを流し込む
with ConnectHandler(**cisco_switch)as connect:
    
    #特権EVECモード(Switch)へ移行
    connect.enable()

    #グローバルコンフィグモードに入り、リストのコマンドを一括投入してエンドで終える

    config_output = connect.send_command("show vlan brief")
    print("\n===確認コマンド(show vlan brief)===")
    print(show_output)

    connect.save_config()
    








