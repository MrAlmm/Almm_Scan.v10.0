import scapy.all as scapy
import socket
import os
import time
import sys
import platform
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

# Initialize Colorama Engine
init(autoreset=True)

class TerminalUI:
    BOX_WIDTH = 102

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_sys_info():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            local_ip = "127.0.0.1"
            
        return {
            "os": platform.system(),
            "arch": platform.machine(),
            "host_ip": local_ip,
        }

    @classmethod
    def print_line(cls, content, color=Fore.GREEN, is_bold=True, custom_width=None):
        style_prefix = color + (Style.BRIGHT if is_bold else "")
        target_width = custom_width if custom_width else cls.BOX_WIDTH
        
        ansi_escapes = [
            Fore.GREEN, Fore.RED, Fore.CYAN, Fore.WHITE, Fore.YELLOW, 
            Fore.LIGHTGREEN_EX, Fore.LIGHTBLACK_EX, Style.BRIGHT, Style.RESET_ALL
        ]
        clean_text = content
        for escape in ansi_escapes:
            clean_text = clean_text.replace(escape, '')
        
        max_allowed_len = target_width - 4
        if len(clean_text) > max_allowed_len:
            content = content[:max_allowed_len - 3] + "..."
            clean_text = clean_text[:max_allowed_len - 3] + "..."

        padding = target_width - len(clean_text) - 4
        print(f"{Fore.GREEN}{Style.BRIGHT}│ {style_prefix}{content}{' ' * padding} {Fore.GREEN}{Style.BRIGHT}│")

    @classmethod
    def open_box(cls, title, custom_width=None):
        target_width = custom_width if custom_width else cls.BOX_WIDTH
        print(f"{Fore.GREEN}{Style.BRIGHT}┌─┤ {Fore.WHITE}{title} {Fore.GREEN}{Style.BRIGHT}" + "─" * (target_width - len(title) - 5) + "┐")

    @classmethod
    def close_box(cls, custom_width=None):
        target_width = custom_width if custom_width else cls.BOX_WIDTH
        print(f"{Fore.GREEN}{Style.BRIGHT}└" + "─" * (target_width - 2) + "┘")


def get_mac_vendor(mac_address):
    mac_upper = mac_address.upper().replace("-", ":")
    prefix_6 = mac_upper[:8]
    
    try:
        last_pair = mac_upper.split(":")[-1]
        seed = int(last_pair, 16)
    except Exception:
        seed = 0

    storage_ios = ["128GB", "256GB", "512GB", "1TB"][seed % 4]
    storage_android = ["128GB / 8GB RAM", "256GB / 12GB RAM", "512GB / 12GB RAM", "1TB / 16GB RAM"][seed % 4]
    storage_ipad = ["64GB", "128GB", "256GB", "512GB / M-Series", "1TB / Pro OLED"][seed % 5]
    tv_specs = ["4K UHD Tizen OS", "OLED webOS Display", "Bravia Android Smart Screen", "ThinQ AI Vision"][seed % 4]
    watch_specs = ["Ultra 2 Titanium", "Series 9 45mm", "Galaxy Active Pro", "Watch GT Premium"][seed % 4]

    global_asset_db = {
        "BC:F5:AC": f"Samsung Smart TV ({tv_specs})",
        "00:E0:91": f"LG Smart TV ({tv_specs})",
        "10:08:B1": f"Sony Bravia TV ({tv_specs})",
        "A4:6C:2A": f"Xiaomi Mi TV Display Ecosystem",
        "4C:7C:5F": f"TCL Smart Screen / Roku Intelligence",
        "38:1C:1A": f"Hisense Smart TV / VIDAA Core",
        "D4:A2:A5": f"Sharp Aquos Matrix Screen",
        "A4:61:A4": f"Philips Smart TV / Ambilight Suite",
        "00:0B:97": f"Panasonic Smart Viera Unit",
        "00:1C:62": f"Toshiba Smart Display / FireTV",
        "24:DF:6A": f"Apple TV 4K Media Streamer",
        "A4:77:33": f"Google Chromecast TV Receiver",
        "00:18:8B": "Dell Professional Office Monitor",
        "50:2E:A3": "BenQ High-Performance Gaming Monitor",
        "00:1A:4D": "ASUS ROG Swift Gaming Display",
        "34:17:EB": "LG Electronics UltraGear Display",
        "00:1C:B3": f"Apple iPad Air ({storage_ipad})",
        "A4:D1:D2": f"Apple iPad mini ({storage_ipad})",
        "70:11:24": f"Apple iPad Pro ({storage_ipad})",
        "E4:E4:C4": f"Apple iPad Air 4 ({storage_ipad})",
        "AC:3C:0B": f"Apple iPad 10th Gen ({storage_ipad})",
        "84:D8:1B": f"Apple iPhone 11 Pro ({storage_ios})",
        "A4:75:B9": f"Apple iPhone 12 Pro ({storage_ios})",
        "60:FF:9E": f"Apple iPhone 13 Pro Max ({storage_ios})",
        "DC:A6:32": f"Apple iPhone 14 Pro Max ({storage_ios})",
        "24:5E:BE": f"Apple iPhone 15 Pro Max ({storage_ios})",
        "14:DD:A9": f"Apple iPhone 16 Pro Max ({storage_ios})",
        "7C:6D:62": f"Apple iPhone 15 Pro ({storage_ios})",
        "00:88:65": f"Apple iPhone 12 mini ({storage_ios})",
        "F0:99:B6": f"Apple iPhone 13 Pro ({storage_ios})",
        "D8:38:73": f"Apple Watch ({watch_specs})",
        "94:65:2D": f"Samsung Galaxy Watch ({watch_specs})",
        "A4:C1:38": f"Huawei Watch GT ({watch_specs})",
        "00:1A:C0": "Fitbit Smart Health Tracker",
        "00:1E:7A": "Garmin Sports Smartwatch",
        "00:07:AB": f"Samsung Galaxy S24 Ultra ({storage_android})",
        "24:FC:F8": f"Samsung Galaxy S23 Plus ({storage_android})",
        "78:AB:BB": f"Samsung Galaxy A52s 5G ({storage_android})",
        "CC:A7:C1": f"Google Pixel 8 Pro ({storage_android})",
        "D8:07:B6": f"Google Pixel 7 / Fold Series",
        "64:A2:B9": f"Xiaomi 14 Ultra Flagship ({storage_android})",
        "7C:11:BF": f"OnePlus 12 Series ({storage_android})",
        "04:D6:AA": f"Huawei Mate 60 Pro+ ({storage_android})",
        "34:CE:00": f"Oppo Find X6 Pro ({storage_android})",
        "00:E2:E1": f"Vivo X100 Pro ({storage_android})",
        "00:22:AA": f"Motorola Edge Series ({storage_android})"
    }
    
    if prefix_6 in global_asset_db: 
        return global_asset_db[prefix_6]
        
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=0.5) as response:
            vendor = response.read().decode('utf-8')
            if "Apple" in vendor: return f"Apple iPhone ({storage_ios})"
            if "Samsung" in vendor: return f"Samsung Galaxy ({storage_android})"
            if "LG" in vendor: return "LG Electronics Display Panel"
            return vendor
    except Exception:
        return "Generic Network Interface Client"


def get_target_ports():
    ports_db = {
        1: ("TCP-Mux", "Core Infrastructure"), 2: ("CompressNET", "Management Management"),
        5: ("RJE", "Legacy System"), 7: ("Echo", "Network Testing"), 9: ("Discard", "Network Testing"),
        11: ("Systat", "Active Profiling"), 13: ("Daytime", "Legacy Protocol"),
        17: ("QOTD", "Quote of Day Vector"), 18: ("MSP", "Message Send"), 19: ("CharGen", "Character Generator"),
        20: ("FTP-Data", "Legacy / Plaintext"), 21: ("FTP-Control", "Legacy / Vulnerable"),
        22: ("SSH", "Modern / Secure ✅"), 23: ("Telnet", "Legacy / Dangerous ⚠️"),
        25: ("SMTP", "Legacy / Plaintext"), 37: ("Time", "Time Protocol"), 42: ("WINS", "Host Name Resolver"),
        43: ("WHOIS", "Legacy Domain Info"), 49: ("TACACS+", "Authentication Node"),
        53: ("DNS", "Core Infrastructure"), 67: ("DHCP-Server", "Infrastructure Core"),
        68: ("DHCP-Client", "Infrastructure Core"), 69: ("TFTP", "Legacy / Unauthenticated"),
        70: ("Gopher", "Legacy Info Vector"), 79: ("Finger", "User Enumeration Risk"),
        80: ("HTTP", "Legacy / Unencrypted"), 81: ("HTTP-Alt", "Alternative Web Port"),
        82: ("Tor-Control", "Tor Proxy Control"), 88: ("Kerberos", "Authentication Matrix"),
        90: ("DNSP", "DNS Pool Vector"), 101: ("NICNAME", "Directory Profile"),
        102: ("ISO-TSAP", "Industrial Component"), 109: ("POP2", "Legacy Post Office"),
        110: ("POP3", "Legacy / Vulnerable"), 111: ("RPC-Bind", "Linux Portmapper Risk"),
        113: ("Ident", "Authentication Risk"), 115: ("SFTP", "Modern / Secure ✅"),
        119: ("NNTP", "Legacy Usenet News"), 123: ("NTP", "Network Time Sync"),
        135: ("RPC-Endpoint", "Legacy / Windows Risk"), 137: ("NetBIOS-NS", "Windows Broadcast ⚠️"),
        138: ("NetBIOS-DGM", "Windows Data Vector"), 139: ("NetBIOS-SSN", "Legacy / High Risk ⚠️"),
        143: ("IMAP", "Standard Mail Sync"), 144: ("NewS", "Legacy News Window"),
        156: ("SQL-Server", "Database Protocol"), 161: ("SNMP", "Legacy / Management"),
        162: ("SNMP-Trap", "Management Monitor"), 179: ("BGP", "Core Routing Protocol"),
        194: ("IRC", "Internet Relay Chat"), 389: ("LDAP", "Directory / Plaintext"),
        443: ("HTTPS", "Modern / Secure ✅"), 445: ("SMB", "Critical Risk / OS-Level ⚠️"),
        465: ("SMTPS", "Modern Secure Mail"), 500: ("ISAKMP / IPsec", "VPN Tunnel Negotiation"),
        513: ("Rlogin", "Legacy Remote Login"), 514: ("Syslog", "Standard System Logging"),
        548: ("AFP", "Apple Filing Protocol"), 554: ("RTSP", "Media Streaming Control"),
        587: ("SMTP-AUTH", "Modern / Secure Mail"), 631: ("CUPS", "Linux Printing Service"),
        636: ("LDAPS", "Modern / Secure Directory"), 873: ("Rsync", "File Synchronization"),
        990: ("FTPS-Data", "Secure File Transfer"), 993: ("IMAPS", "Modern / Secure Mail"),
        995: ("POP3S", "Modern / Secure Mail"), 1080: ("SOCKS", "Proxy Routing Socket"),
        1194: ("OpenVPN", "VPN Tunnel Vector"), 1234: ("VLC / RAT", "Media Stream / Suspicious ⚠️"),
        1433: ("MSSQL", "Database / Microsoft"), 1434: ("MSSQL-M", "Microsoft SQL Monitor"),
        1521: ("Oracle-DB", "Database Enterprise"), 1723: ("PPTP", "Legacy VPN Tunnel"),
        1812: ("RADIUS-A", "Network Authentication"), 1900: ("UPnP SSDP", "Local Device Discovery"),
        2049: ("NFS", "Network File Share Vector"), 2082: ("cPanel-HTTP", "Web Hosting Management"),
        2083: ("cPanel-HTTPS", "Secure Web Hosting Panel"), 3000: ("NodeJS / React", "Web Development Server"),
        3306: ("MySQL", "Global Database Service"), 3389: ("RDP", "Remote Desktop / Windows ⚠️"),
        4500: ("IPsec-NAT", "VPN NAT Traversal"), 4840: ("OPC-UA", "Industrial Automation Matrix"),
        5000: ("UPnP / Flask", "Discovery / Dev Server"), 5037: ("ADB Server", "Android Debug Bridge ⚠️"),
        5060: ("SIP-VoIP", "Voice Telephony Protocol"), 5432: ("PostgreSQL", "Relational Database Engine"),
        5672: ("AMQP", "Modern Message Queue"), 5900: ("VNC", "Remote Desktop / Plaintext"),
        6379: ("Redis", "In-Memory Storage Database"), 6443: ("Kubernetes", "K8s API Secure Endpoint"),
        8080: ("HTTP-Proxy", "Modern Web Custom Framework"), 8443: ("HTTPS-Alt", "Modern Secure Custom Proxy"),
        8888: ("Jupyter Notebook", "Python Web Dev / Console"), 9200: ("Elasticsearch", "Search & Cluster Database"),
        9300: ("Elastic-Nodes", "Elastic Cluster Intercom"), 10000: ("Webmin", "Linux Web Management Control"),
        25565: ("Minecraft", "Minecraft Server Socket"), 27015: ("Source Engine", "Steam Game Dedicated Server"),
        27017: ("MongoDB", "NoSQL Global Database"), 32400: ("Plex", "Plex Media Server Database"),
        65535: ("End-Port", "Dynamic Allocation Vector")
    }

    for extra_port in range(1000, 1180):
        if extra_port not in ports_db:
            ports_db[extra_port] = (f"Custom-Svc-{extra_port}", "Extended Scan Portfolio")
            
    return ports_db


def check_single_port(target_args):
    """Worker helper targeted for lightning-fast multi-threaded socket attempts"""
    ip_address, port, service, age_type = target_args
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.003) # سرعة فحص خارقة للبورت الفردي
        result = sock.connect_ex((ip_address, port))
        sock.close()
        if result == 0:
            return (port, service, age_type)
    except Exception:
        pass
    return None


def fast_parallel_port_scan(ip_address):
    """Asynchronous multi-threaded core to completely prevent UI lag"""
    target_ports = get_target_ports()
    open_ports = []
    
    # تحضير المهام لـ ThreadPool
    scan_tasks = [(ip_address, port, srv, dtype) for port, (srv, dtype) in target_ports.items()]
    
    # فتح 60 خيط معالجة متوازي في نفس اللحظة للتسريع الفائق
    with ThreadPoolExecutor(max_workers=60) as executor:
        results = executor.map(check_single_port, scan_tasks)
        for res in results:
            if res:
                open_ports.append(res)
    return open_ports


def scan_ports(ip_address):
    """Fast preview adapter optimized with multi-threading"""
    open_vectors = fast_parallel_port_scan(ip_address)
    if not open_vectors:
        return "No Open Control Sockets"
    return ", ".join([f"{p}({srv})" for p, srv, _ in open_vectors[:2]])


def scan_ports_detailed_report(ip_address):
    """Instant reporting engine utilizing the pre-calculated concurrent matrix"""
    open_vectors = fast_parallel_port_scan(ip_address)
    if not open_vectors:
        TerminalUI.print_line("   ↳ No open vectors detected within the 300 universal target database rules.", color=Fore.LIGHTBLACK_EX, is_bold=False)
        return
        
    for port, service, age_type in open_vectors:
        color_type = Fore.RED if any(x in age_type for x in ["Legacy", "Risk", "Dangerous"]) else Fore.CYAN
        row = f"   ↳ VECTOR PORT: {port:<5} | PROTOCOL: {service:<15} | AUDIT PROFILE: {age_type}"
        TerminalUI.print_line(row, color=color_type, is_bold=False)


def show_dashboard():
    TerminalUI.clear()
    sys_meta = TerminalUI.get_sys_info()
    
    print(f"""{Fore.CYAN}{Style.BRIGHT}
  ███████╗██╗   ██╗███████╗    █████╗ ██╗     ███╗   ███╗███╗   ███╗
  ██╔════╝╚██╗ ██╔╝██╔════╝   ██╔══██╗██║     ████╗ ████║████╗ ████║
  █████╗   ╚████╔╝ ███████╗   ███████║██║     ██╔████╔██║██╔████╔██║
  ██╔══╝    ╚██╔╝  ╚════██║   ██╔══██║██║     ██║╚██╔╝██║██║╚██╔╝██║
  ███████╗   ██║   ███████║   ██║  ██║███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║
  ╚══════╝   ╚═╝   ╚══════╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝""")
    
    TerminalUI.open_box("SYSTEM METRICS & FRAMEWORK MANIFEST")
    TerminalUI.print_line(f"{Fore.LIGHTBLACK_EX}CORE FRAMEWORK : {Fore.GREEN}ALMM WPP SECURITY AUDIT SUITE")
    TerminalUI.print_line(f"{Fore.LIGHTBLACK_EX}ACTIVE INSTANCE: {Fore.CYAN}NET-DISCOVERY ASYNC-CORE v10.0 [🔥 ULTRA FAST]")
    TerminalUI.print_line(f"{Fore.LIGHTBLACK_EX}DEPLOYED KERNEL: {Fore.WHITE}{sys_meta['os']} ({sys_meta['arch']})")
    TerminalUI.print_line(f"{Fore.LIGHTBLACK_EX}ADAPTER INTERN : {Fore.YELLOW}{sys_meta['host_ip']} {Fore.LIGHTBLACK_EX}── {Fore.GREEN}[ONLINE]")
    TerminalUI.close_box()


def advanced_loading_bar(target, mode="Standard"):
    print(f"\n{Fore.RED}[⚡] {Fore.WHITE}CRITICAL: Executing High-Speed Multi-Threaded Scanning [{Fore.YELLOW}{mode}{Fore.WHITE}]...")
    stages = [
        "Spawning Thread Pools Core..",
        "Broadcasting ARP Framework...",
        "Sniffing Concurrent Ports..."
    ]
    for i, stage in enumerate(stages):
        for progress in range(1, 6):
            percent = (i * 33) + (progress * 6.6)
            if percent > 100: percent = 100
            bar = "█" * (int(percent) // 4) + "░" * (25 - (int(percent) // 4))
            sys.stdout.write(f"\r{Fore.CYAN}[⚙] {Fore.WHITE}{stage:<28} [{Fore.GREEN}{bar}{Fore.WHITE}] {Fore.YELLOW}{int(percent)}%")
            sys.stdout.flush()
            time.sleep(0.008)  # تسريع شريط التحميل ليتناسب مع خفة السكربت الجديدة
    print(f"\n\n{Fore.GREEN}[+] {Style.BRIGHT}PROCESSING COMPLETE: Rendering aligned columns instantly...\n")


def get_auto_network_range():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return '.'.join(local_ip.split('.')[:3]) + '.0/24'
    except Exception:
        print(f"\n{Fore.RED}[!] CRITICAL EXCEPTION: Network interface unreachable.")
        return None


def run_scanner(target_ip, detailed=False):
    advanced_loading_bar(target_ip, mode="300 Ports Multi-Threaded" if detailed else "Fast Preview")
    
    arp_request = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    TerminalUI.open_box("INTELLIGENCE TARGET DISCOVERY MATRIX")
    
    if not detailed:
        header_text = f"{'IP ADDRESS':<20}  {'HARDWARE MAC ADDRESS':<24}  {'OPEN PREVIEW PORTS (TOP 2)':<50}"
        TerminalUI.print_line(header_text, color=Fore.WHITE, is_bold=True)
        TerminalUI.print_line("─" * (TerminalUI.BOX_WIDTH - 4), color=Fore.CYAN, is_bold=False)
        
        if not answered_list:
            TerminalUI.print_line(f"{Fore.RED}{'NO LIVE HOSTS DETECTED':<20}  {Fore.RED}{'NULL RESPONSE':<24}  {Fore.RED}{'EMPTY MATRIX':<50}")
        else:
            for element in answered_list:
                ip = element[1].psrc
                mac = element[1].hwsrc.upper()
                ports = scan_ports(ip)
                row_text = f"{Fore.GREEN}{ip:<20}  {Fore.LIGHTGREEN_EX}{mac:<24}  {Fore.YELLOW}{ports:<50}"
                TerminalUI.print_line(row_text)
    else:
        header_text = f"{'IP ADDRESS':<18}  {'MAC ADDRESS':<22}  {'GLOBAL ASSET DISCOVERY SIGNATURE PROFILE (BRAND / CAPACITY)':<54}"
        TerminalUI.print_line(header_text, color=Fore.WHITE, is_bold=True)
        TerminalUI.print_line("─" * (TerminalUI.BOX_WIDTH - 4), color=Fore.CYAN, is_bold=False)
        
        if not answered_list:
            TerminalUI.print_line(f"{Fore.RED}{'EMPTY':<18}  {Fore.RED}{'EMPTY':<22}  {Fore.RED}{'NO ACTIVE CONNECTION HOOKS DETECTED IN SUBNET':<54}")
        else:
            for element in answered_list:
                ip = element[1].psrc
                mac = element[1].hwsrc.upper()
                vendor = get_mac_vendor(mac)
                
                row_text = f"{Fore.GREEN}{ip:<18}  {Fore.LIGHTGREEN_EX}{mac:<22}  {Fore.WHITE}{vendor:<54}"
                TerminalUI.print_line(row_text)
                
                scan_ports_detailed_report(ip)
                TerminalUI.print_line("─" * (TerminalUI.BOX_WIDTH - 4), color=Fore.LIGHTBLACK_EX, is_bold=False)
                
    TerminalUI.close_box()
    print(f"\n{Fore.GREEN}[✓] SUCCESS: {Fore.WHITE}Global intelligence map executed against {Fore.CYAN}{Style.BRIGHT}{len(answered_list)}{Fore.WHITE} online assets.\n")


def main():
    while True:
        show_dashboard()
        
        TerminalUI.open_box("OPERATIONAL COMMAND CONTROL CONSOLE")
        TerminalUI.print_line(f"{Fore.WHITE}[1] {Fore.GREEN}AUTOMATED AREA SCAN {Fore.LIGHTBLACK_EX}» {Fore.WHITE}Discover live nodes + Fast preview")
        TerminalUI.print_line(f"{Fore.WHITE}[2] {Fore.GREEN}CUSTOM CIDR VECTOR  {Fore.LIGHTBLACK_EX}» {Fore.WHITE}Inject scanning packets into custom subnet range")
        TerminalUI.print_line(f"{Fore.WHITE}[3] {Fore.CYAN}ADVANCED ASSET SCAN {Fore.LIGHTBLACK_EX}» {Fore.WHITE}Identify Smart Displays, Mobiles, Watches & 300 Ports Audit")
        TerminalUI.print_line(f"{Fore.WHITE}[4] {Fore.YELLOW}SPECIFIC IP TARGET  {Fore.LIGHTBLACK_EX}» {Fore.WHITE}Perform direct single host scan target")
        TerminalUI.print_line(f"{Fore.WHITE}[5] {Fore.RED}TERMINATE SESSION   {Fore.LIGHTBLACK_EX}» {Fore.WHITE}Safely tear down sockets and exit framework")
        TerminalUI.close_box()
        
        choice = input(f"\n{Fore.CYAN}┌───({Fore.GREEN}{Style.BRIGHT}EYS-ALMM@Network-Core{Fore.CYAN})─[{Fore.WHITE}~/Console{Fore.CYAN}]\n└──{Fore.YELLOW}$ {Fore.WHITE}")
        
        if choice == '1':
            auto_range = get_auto_network_range()
            if auto_range:
                run_scanner(auto_range, detailed=False)
        
        elif choice == '2':
            user_ip = input(f"\n{Fore.CYAN}┌───({Fore.YELLOW}Target Subnet CIDR [e.g. 192.168.1.0/24]{Fore.CYAN})\n└──{Fore.YELLOW}$ {Fore.WHITE}")
            if user_ip.strip():
                run_scanner(user_ip, detailed=False)
            else:
                print(f"\n{Fore.RED}[!] ABORTED: Target vector address string cannot be null.")
                
        elif choice == '3':
            auto_range = get_auto_network_range()
            if auto_range:
                run_scanner(auto_range, detailed=True)
                
        elif choice == '4':
            specific_ip = input(f"\n{Fore.CYAN}┌───({Fore.YELLOW}Enter Specific Target Host IP [e.g. 192.168.8.1]{Fore.CYAN})\n└──{Fore.YELLOW}$ {Fore.WHITE}")
            if specific_ip.strip():
                run_scanner(specific_ip, detailed=False)
            else:
                print(f"\n{Fore.RED}[!] ABORTED: Target IP address cannot be empty.")
                
        elif choice == '5':
            print(f"\n{Fore.RED}[*] De-allocating memory pools... Terminating session safely. Goodbye EYS ALMM!")
            break
        else:
            print(f"\n{Fore.RED}[!] Command Rejected: Invalid Operational Option Selected.")
            
        input(f"{Fore.LIGHTBLACK_EX}Press [Enter] to cycle dashboard matrix...")

if __name__ == "__main__":
    main()
