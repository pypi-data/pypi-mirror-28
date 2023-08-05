# frida-push
Wrapper tool to identify the remote device and push device specific frida-server binary.

## Installing

```bash
sudo pip install frida-push
```

## Running

```bash
$ frida-push -h

usage: frida-push [-h] [-d DEVICE_NAME] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE_NAME, --device-name DEVICE_NAME
  --version             show program's version number and exit
```

```bash
$ adb devices -l

List of devices attached
emulator-5554          device product:sdk_google_phone_x86 model:Android_SDK_built_for_x86 device:generic_x86 transport_id:5
emulator-5553          device product:sdk_google_phone_x86 model:Android_SDK_built_for_x86 device:generic_x86 transport_id:4
emulator-5552          device product:sdk_google_phone_x86 model:Android_SDK_built_for_x86 device:generic_x86 transport_id:3

$ frida-push -d emulator-5553

[i] Devices: 
	 emulator-5554
	 emulator-5553
	 emulator-5552
[i] Current installed Frida version: 10.6.32
	[+] Found arch: x86
	[+] Downloading: https://github.com/frida/frida/releases/download/10.6.32/frida-server-10.6.32-android-x86.xz
	[+] Writing file as: frida-server-10.6.32-android-x86.
	[+] File pushed to device successfully.
	[+] Executing frida-server on device.
```
