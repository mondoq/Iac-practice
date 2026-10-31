from netmiko import ConnectHandler

# 1.接続先ルータの定義
R1={
  'device_type':'cisco_ios',
  'host':'192.168.1.1',
  'username':'admin',
  'password':'password123',
  'secret'  :'enable_password',
}

R2={
  'device_type':'cisco_ios',
  'host':'192.168.1.2',
  'username':'admin',
  'password':'password123',
  'secret'  :'enable_password',
}


with ConnectHandler(**R1) as net_connect:
    print(net_connect.send_command('show ip interface brief'))





