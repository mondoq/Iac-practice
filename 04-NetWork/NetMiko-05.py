from netmiko import ConnectHandler
import json
from netmiko.exceptions import NetmikoTimeoutException,NetmikoAuthenticationException

sw={
 "type":"cisco_ios",
 "host":"192.168.10.1",
 "username":"admin",
 "password":"password123",
 "secrets":"enable123",
 }
#スイッチ単体で村を構築するためのコンフィグコマンド
commands=[
   "hostname LAN1",
  
  #村人としての頭脳を有効化---
   "ip routing",
   "servixce dhcp",

   #  村の区画(vlan 10)
   "vlan 10",
   "name LAN1",
   "exit",

   #---C.住民を接続するポート
   "interface range GigabitEthernet0/1-2",
   "switchport mode access ",
   "switchport access vlan 10",
   "spanning-tree portfast",
   "no shutdown",
   "exit",
   #ルーター自身に設定をしてゲートウェイIPを付与
   "interface vlan 10",
   "description gateway",
   "ip adress 192.168.10.1 255.255.255.0",
   "no shutdown",
   "exit",

   "ip dhcp excluded-address 192.168.10.1 192.168.10.9",
   "ip dhcp pool vpool",
   "network 192.168.10.1",
   "dns-server 8.8.8.8",
   "exit",
]


def build_single_village():
    print("ネットワークの自動構築開始")
    try:
        with ConnectHandler(**sw) as connect:

            connect.enable()

            output=connect.send_cofig_set(commands)
            print("コンフィグ投入ログ")

            print(output)

            connect.save_config()

            print("設定を保存しました")

#構築後の状態確認
            print("vlan 10の確認")

            status_vlan=connect.send_command("show ip interface brief |include vlan 10")
            print(status_vlan)

            print("DHCPのステータス確認")

            dhcp=connect.send_command("show ip dhcp binding",use_textfsm=True)
            print(json.dump(dhcp,index=2,ensure_ascii=False))

            print("マックテーブル確認")

            mac_table=connect.send_config("show mac address-table vlan 10",use_textfsm=True)
            print(json.dump(mac_table,index=2,ensure_ascii=False))
    except(NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"スイッチへの接続に失敗しました",{e})


if __name__=="__main__":
    print (build_single_village())