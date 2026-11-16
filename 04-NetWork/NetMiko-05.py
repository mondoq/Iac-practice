from netmiko import ConnectHandler
import json
from netmiko.exceptions import NetmikoTimeoutException,NetmikoAuthenticationException



#1.接続情報の定義(村長 R!と広場　SW1)

rt1={
"type": "cisco_ios",
"host":"192.168.1.1",
"username": "admin",
"password":"password123",
"secret":"enable123",
}

sw1={
 "type": "cisco_ios",
"host":"192.168.1.2",
"username": "admin",
"password":"password123",
"secret":"enable123",
}
#2.入力するコンフィグコマンド投入リスト
# 村長（R1）：ゲートウェイ設定 ＋ DHCPサーバー（住所の自動配布）設定
r1_config_commands=[
   "hostname R1",
   "interface GigabitEthernet0/0",
   "ip address 192.168.1.1 255.255.255.0",
   "no shutdown",
   "exit",
   # 固定IP用（192.168.1.1 〜 192.168.1.9）を自動配布から除外
   "ip dhcp excluded-adress 192.168.1.1 192.168.1.9",
   # 住民用のDHCPプール作成
   "ip dhcp pool VILLAGE_LAN",
   "network 192.168.1.0 255.255.255.0",
   "default-router 192.168.1.1",
   "dns-server 8.8.8.8",
   "exit"
]


sw1_configlist=[
 "hostname SW1",
 "interface range GigabitEternet0/1-2"
 "switchport mode access",
 "switchport access vlan 1",
 "spanning-tree portfast",
 "no shutdown",
 "exit",

#村長(R1)へつなぐポート
"interface GigabitEternet0/24",
"switchport mode access",
"switchport access vlan 1",
"no shutdown",
"exit",
]

#構築＆確認を実行するメイン関数
def build_village():
    print("1.R1ゲートウェイとDHCPサーバーを構築")
    try:
        with ConnectHandler(**rt1) as connect:
            connect.enable()


            output=connect.send_cofig_set(r1_config_commands)
            connect.save_config()
            print("RT1の設定が完了、保存いたしました")

            if_brief=connect.send_command("show ip interface brief | exclude unassigned")

            dhcp=conect.send_command("show ip dhcp binding",use_textfsm=True)

            print("\n---[R1]インターフェイス状態---")

            print(if_brief)
            print("\nDHCP住所配布リスト")

            print(json.dumps(dhcp,indent=2,ensure_ascii=False))

    except (NetmikoTimeoutException,NetmikoAuthenticationEception) as e:
          print(f"[R1 エラー]接続に失敗しました：｛e｝")
    print("\n"+"="*50+"\n")

    print("アクセスポートとportFastの構築") 
    try:
        with ConnectHandler(**sw1) as sw_conn:
             sw_conn.enable()
             sw_output=sw_conn.send_config_set(sw1_configlist)
             sw_conn.save_config()
             print("設定保存が完了") 

             mac_table=sw_conn.send_command("show mac address table",use_textfsm=True)   

             print("macアドレステーブル)(json)")
             print(json.jump(mac_table, indent=2, ensure_ascii=False))
    except(NetmikoTimeoutException,NetmikoAuthenticationException) as e :
          print(f"[SW1 エラー] 接続に失敗しました: {e}")           
       

if __name__ == "__main__":
     build_village()