import subprocess
import speedtest
import time


def set_network_config(interface, ip, subnet_mask, gateway):
    # Команды для настройки сети
    commands = [
        f'sudo ifconfig {interface} {ip} netmask {subnet_mask}',
        f'sudo route add default gw {gateway}',
    ]
    
    for cmd in commands:
        subprocess.run(cmd, shell=True)


def create_pptp_vpn(username, password, vpn_server):
    # Команда для создания PPTP VPN-подключения
    cmd = f'sudo pptpsetup --create my_vpn --server {vpn_server} --username {username} --password {password} --encrypt'
    subprocess.run(cmd, shell=True)


def change_wifi_settings(ssid, password):
    # Команда для изменения настроек Wi-Fi
    commands = [
        f'sudo nmcli device wifi connect {ssid} password {password}',
    ]
    
    for cmd in commands:
        subprocess.run(cmd, shell=True)


def measure_gprs_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    
    download_speed = st.download() / 1024 / 1024
    upload_speed = st.upload() / 1024 / 1024
    
    threshold_speed = 2.0  # Нижний порог скорости, ниже которого соединение считается медленным
    
    is_slow_gprs = download_speed < threshold_speed or upload_speed < threshold_speed
    
    return is_slow_gprs


def check_internet_connection():
    # Функция для проверки наличия интернет-соединения
    return subprocess.run("ping -c 1 google.com", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0


def disable_interface(interface):
    # Выключение интерфейса
    subprocess.run(f'sudo ifconfig {interface} down', shell=True)


def enable_interface(interface):
    # Включение интерфейса
    subprocess.run(f'sudo ifconfig {interface} up', shell=True)


interfaces = {
    'lan': 'eth0',
    'wifi': 'wlan0',
    'gprs': 'ppp0'
}

while True:
    active_interface = None
    
    if check_internet_connection():
        print("Интернет есть, ничего не меняем")
        time.sleep(60)
        continue
    
    print("Интернет отсутствует, переключаемся на другое подключение...")
    
    if not check_internet_connection():
        print("Переключаемся на Wi-Fi")
        active_interface = 'wifi'
    elif not check_internet_connection() and measure_gprs_speed():
        print("Переключаемся на GPRS")
        active_interface = 'gprs'
    else:
        print("Переключаемся на LAN")
        active_interface = 'lan'

    for interface_name in interfaces:
        if interface_name != active_interface:
            disable_interface(interface_name)
    
    # Включаем нужный интерфейс
    enable_interface(interfaces[active_interface])
    
    time.sleep(60)  # Пауза между проверками
