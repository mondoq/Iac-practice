from netmiko import ConnectHander
import pprint

sw1={
  "device_type":"cisco_ios",
  "host":"192.168.10.254",
  "username":"admin",
  "password":"cisco_password",
  "secret":"class",
}


pc_assignments=[
{"port":"FastEthernet0/1","pc_name":"PC1","ip":"192.168.10.11","vlan":1}
{"port":"FastEthernet0/2","pc_name":"PC2","ip":"192.168.10.12","vlan":2},
{"port":"FastEthernet0/3","pc_name":"PC3","ip":"192.168.10.13","vlan":3},
{"port":"FastEthernet0/4","pc_name":"PC4","ip":"192.168.10.14","vlan":4},
{"port":"FastEthernet0/5","pc_name":"PC5","ip":"192.168.10.15","vlan":5}
]

def build_port_commands(assignments:list[dict])->list[str]:
    #設計テーブルからスイッチのポート設定コマンド群を生成する
    commands=[]
    for item in assignments:
        commands.extend([
            f"interface {item['port']}",
             "switchport mode access",
            f"description{item['pc_name']}{item['ip']}"
            f"switchport access {item['vlan']}",
             "spanning-tree portfast",
             "no shutdown",
        ])
    return commands
def main()->None:
   commands=build_port_commands(pc_assignments)

   with ConnectHander(**sw1) as connect:
       connect.enable

       print("コンフィグ投入開始")

       output=connect.send_config_set(commands)
       print(output)

       save_out=connect.save_config
       print("出力結果")
       print(save_out)

       print("インナーフェイス状態")
       intf=connect.send_command("show ip interface brief",use_textfsm=True)
       pprint.pprint(intf)

       print("MACtable表示")

       mac=connect.send_command("show mac address-table",use_textfsm=True)
       pprint.pprint(mac)

if __name__ =="__main__":
    main()
    