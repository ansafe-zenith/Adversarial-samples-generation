import requests

url = "https://www.virustotal.com/api/v3/files/0f2c6924795340dc151f2ff7c2bdf290"

headers = {
    "accept": "application/json",
    "x-apikey": "169d3b77091cf49775f723ca99feabdbbb336650ae2d912889f3dd0cf3119588"
}

response = requests.get(url, headers=headers)

print(response.text)

"""
    输出内容：
{
  "data": {
    "id": "fffd0720fd0647668119e41475dfeda27d418d139dca5bc236fe970e85b9edde",
    "type": "file",
    "links": {
      "self": "https://www.virustotal.com/api/v3/files/fffd0720fd0647668119e41475dfeda27d418d139dca5bc236fe970e85b9edde"
    },
    "attributes": {
      "crowdsourced_ids_results": [
        {
          "rule_category": "misc-activity",
          "alert_severity": "low",
          "rule_msg": "(eth) truncated ethernet header",
          "rule_raw": "alert ( gid:116; sid:424; rev:2; msg:\"(eth) truncated ethernet header\"; metadata: policy max-detect-ips drop, rule-type decode; classtype:misc-activity;)",
          "rule_url": "https://www.snort.org/downloads/#rule-downloads",
          "rule_source": "Snort registered user ruleset",
          "rule_id": "116:424"
        },
        {
          "rule_category": "Misc activity",
          "alert_severity": "low",
          "rule_msg": "ET INFO Android Device Connectivity Check",
          "rule_raw": "alert http $HOME_NET any -> $EXTERNAL_NET any (msg:\"ET INFO Android Device Connectivity Check\"; flow:established,to_server; urilen:13; http.method; content:\"GET\"; http.uri; content:\"/generate_204\"; fast_pattern; endswith; http.host; content:\"connectivitycheck.gstatic.com\"; http.accept_enc; content:\"gzip\"; depth:4; endswith; http.header_names; content:!\"Cache\"; content:!\"Referer\"; classtype:misc-activity; sid:2036220; rev:4; metadata:affected_product Android, attack_target Mobile_Client, created_at 2018_09_14, deployment Perimeter, deployment Internal, former_category INFO, performance_impact Low, signature_severity Informational, tag Connectivity_Check, updated_at 2020_09_16;)",
          "alert_context": [
            {
              "url": "http://connectivitycheck.gstatic.com/generate_204",
              "hostname": "connectivitycheck.gstatic.com",
              "dest_port": 80,
              "dest_ip": "142.251.143.131"
            }
          ],
          "rule_url": "https://rules.emergingthreats.net/",
          "rule_source": "Proofpoint Emerging Threats Open",
          "rule_id": "1:2036220"
        },
        {
          "rule_category": "Generic Protocol Command Decode",
          "alert_severity": "low",
          "rule_msg": "SURICATA STREAM Packet with invalid ack",
          "rule_raw": "alert tcp any any -> any any (msg:\"SURICATA STREAM Packet with invalid ack\"; stream-event:pkt_invalid_ack; classtype:protocol-command-decode; sid:2210045; rev:2;)",
          "alert_context": [
            {
              "dest_ip": "142.251.168.188",
              "dest_port": 443
            }
          ],
          "rule_url": "https://www.openinfosecfoundation.org/",
          "rule_source": "Suricata",
          "rule_id": "1:2210045"
        },
        {
          "rule_category": "Generic Protocol Command Decode",
          "alert_severity": "low",
          "rule_msg": "SURICATA STREAM SHUTDOWN RST invalid ack",
          "rule_raw": "alert tcp any any -> any any (msg:\"SURICATA STREAM SHUTDOWN RST invalid ack\"; stream-event:rst_invalid_ack; classtype:protocol-command-decode; sid:2210046; rev:2;)",
          "alert_context": [
            {
              "dest_ip": "142.251.168.188",
              "dest_port": 5228
            }
          ],
          "rule_url": "https://www.openinfosecfoundation.org/",
          "rule_source": "Suricata",
          "rule_id": "1:2210046"
        }
      ],
      "sandbox_verdicts": {
        "Zenbox": {
          "category": "harmless",
          "confidence": 88,
          "sandbox_name": "Zenbox",
          "malware_classification": [
            "CLEAN"
          ]
        }
      },
      "sha256": "fffd0720fd0647668119e41475dfeda27d418d139dca5bc236fe970e85b9edde",
      "size": 1361198,
      "type_extension": "apk",
      "ssdeep": "24576:gnbEUYdgPO4JHPkwlFAdL/Xy3GU9aRUk1J/MzoscG2DGniokesXt5tTYXOB8t5:QpBFAx/XyCHMzoq2DFresXtm3t5",
      "md5": "0f2c6924795340dc151f2ff7c2bdf290",
      "times_submitted": 5,
      "popular_threat_classification": {
        "popular_threat_name": [
          {
            "count": 19,
            "value": "adrd"
          }
        ],
        "suggested_threat_label": "trojan.adrd",
        "popular_threat_category": [
          {
            "count": 13,
            "value": "trojan"
          },
          {
            "count": 2,
            "value": "spyware"
          }
        ]
      },
      "last_analysis_stats": {
        "malicious": 30,
        "suspicious": 0,
        "undetected": 39,
        "harmless": 0,
        "timeout": 0,
        "confirmed-timeout": 0,
        "failure": 0,
        "type-unsupported": 8
      },
      "total_votes": {
        "harmless": 0,
        "malicious": 0
      },
      "first_submission_date": 1700293881,
      "type_tag": "android",
      "androguard": {
        "VTAndroidInfo": 2,
        "AndroidApplicationError": false,
        "AndroguardVersion": "4.0",
        "Activities": [
          "doris.ad.rename.FileList",
          "doris.ad.rename.MPMain",
          "doris.ad.rename.UMPlayList",
          "doris.ad.rename.UMZone",
          "doris.ad.rename.UMWeb",
          "doris.ad.rename.UMApp",
          "doris.ad.rename.UMPHelp"
        ],
        "certificate": {
          "Subject": {
            "DN": "C:CN, CN:android, L:xian, O:apk, ST:shannxi, OU:signer",
            "C": "CN",
            "CN": "android",
            "L": "xian",
            "O": "apk",
            "ST": "shannxi",
            "OU": "signer"
          },
          "validto": "2033-07-24 05:37:44",
          "serialnumber": "fdc67bca60eb2291",
          "thumbprint": "cfaedd069a747d9804841953922b3099e3fe7f46",
          "validfrom": "2023-09-15 05:37:44",
          "Issuer": {
            "DN": "C:CN, CN:android, L:xian, O:apk, ST:shannxi, OU:signer",
            "C": "CN",
            "CN": "android",
            "L": "xian",
            "O": "apk",
            "ST": "shannxi",
            "OU": "signer"
          }
        },
        "AndroidApplication": 1,
        "RiskIndicator": {
          "APK": {
            "DEX": 1,
            "SHARED LIBRARIES": 4
          },
          "PERM": {
            "PRIVACY": 2,
            "NORMAL": 2,
            "DANGEROUS": 5,
            "INTERNET": 1,
            "SYSTEM": 2,
            "SIGNATURE": 2
          }
        },
        "Services": [
          "doris.xxx.yyy.MyService"
        ],
        "AndroidVersionCode": "1",
        "Package": "doris.ad.rename",
        "AndroidVersionName": "1.0",
        "AndroidApplicationInfo": "APK",
        "Receivers": [
          "doris.xxx.yyy.MyBoolService",
          "doris.xxx.yyy.MyAlarmReceiver",
          "doris.xxx.yyy.NetWorkReceiver",
          "doris.xxx.yyy.CustomBroadcastReceiver",
          "doris.ad.rename.ShutdownReceiver"
        ],
        "StringsInformation": [
          "http://adrd.taxuan.net/index.aspx?im=",
          "http://adrd.xiaxiab.com/pic.aspx?im=",
          "http://jump.gjm123.cn/umplayer.aspx",
          "http://list.mno6.cn/downvc.aspx?for=",
          "http://sxmobi002.gicp.net:8800/SmartPhoneApp/?PlatForm=android&Model=all&Resolution=all&AppId=02",
          "http://wap.baidu.com/"
        ],
        "main_activity": "doris.ad.rename.FileList",
        "intent_filters": {
          "Activities": {
            "doris.ad.rename.FileList": {
              "action": [
                "android.intent.action.MAIN"
              ],
              "category": [
                "android.intent.category.LAUNCHER"
              ]
            },
            "doris.ad.rename.MPMain": {
              "action": [
                "android.intent.action.VIEW"
              ],
              "category": [
                "android.intent.category.DEFAULT"
              ]
            }
          },
          "Receivers": {
            "doris.xxx.yyy.NetWorkReceiver": {
              "action": [
                "android.net.conn.CONNECTIVITY_CHANGE"
              ]
            },
            "doris.xxx.yyy.MyBoolService": {
              "action": [
                "android.intent.action.BOOT_COMPLETED"
              ]
            },
            "doris.xxx.yyy.MyAlarmReceiver": {
              "action": [
                "com.lz.myservicestart"
              ]
            },
            "doris.xxx.yyy.CustomBroadcastReceiver": {
              "action": [
                "android.intent.action.PHONE_STATE"
              ]
            },
            "doris.ad.rename.ShutdownReceiver": {
              "action": [
                "android.intent.action.ACTION_SHUTDOWN"
              ]
            }
          }
        },
        "permission_details": {
          "android.permission.WRITE_APN_SETTINGS": {
            "permission_type": "signature|system",
            "short_description": "change/intercept network settings and traffic",
            "full_description": "Allows the app to change network settings and to intercept and inspect all network traffic,\n      for example to change the proxy and port of any APN. Malicious apps may monitor, redirect, or modify network\n      packets without your knowledge."
          },
          "android.permission.RECEIVE_BOOT_COMPLETED": {
            "permission_type": "normal",
            "short_description": "run at startup",
            "full_description": "Allows the app to\n        have itself started as soon as the system has finished booting.\n        This can make it take longer to start the phone and allow the\n        app to slow down the overall phone by always running."
          },
          "android.permission.WRITE_SETTINGS": {
            "permission_type": "dangerous",
            "short_description": "modify system settings",
            "full_description": "Allows the app to modify the\n        system's settings data. Malicious apps may corrupt your system's\n        configuration."
          },
          "android.permission.READ_PHONE_STATE": {
            "permission_type": "dangerous",
            "short_description": "read phone status and identity",
            "full_description": "Allows the app to access the phone\n      features of the device.  This permission allows the app to determine the\n      phone number and device IDs, whether a call is active, and the remote number\n      connected by a call."
          },
          "android.permission.ACCESS_NETWORK_STATE": {
            "permission_type": "normal",
            "short_description": "view network connections",
            "full_description": "Allows the app to view\n      information about network connections such as which networks exist and are\n      connected."
          },
          "android.permission.WAKE_LOCK": {
            "permission_type": "dangerous",
            "short_description": "prevent phone from sleeping",
            "full_description": "Allows the app to prevent the phone from going to sleep."
          },
          "android.permission.BLUETOOTH": {
            "permission_type": "dangerous",
            "short_description": "pair with Bluetooth devices",
            "full_description": "Allows the app to view the\n      configuration of the Bluetooth on the phone, and to make and accept\n      connections with paired devices."
          },
          "android.permission.RECORD_AUDIO": {
            "permission_type": "dangerous",
            "short_description": "record audio",
            "full_description": "Allows the app to record audio with the\n      microphone.  This permission allows the app to record audio at any time\n      without your confirmation."
          },
          "android.permission.MODIFY_PHONE_STATE": {
            "permission_type": "signature|system",
            "short_description": "modify phone state",
            "full_description": "Allows the app to control the\n        phone features of the device. An app with this permission can switch\n        networks, turn the phone radio on and off and the like without ever notifying\n        you."
          },
          "android.permission.MODIFY_AUDIO_SETTINGS": {
            "permission_type": "dangerous",
            "short_description": "change your audio settings",
            "full_description": "Allows the app to modify global audio settings such as volume and which speaker is used for output."
          },
          "android.permission.INTERNET": {
            "permission_type": "dangerous",
            "short_description": "full network access",
            "full_description": "Allows the app to create\n     network sockets and use custom network protocols. The browser and other\n     applications provide means to send data to the internet, so this\n     permission is not required to send data to the internet."
          },
          "android.permission.WRITE_EXTERNAL_STORAGE": {
            "permission_type": "dangerous",
            "short_description": "modify or delete the contents of your SD card",
            "full_description": "Allows the app to write to the SD card."
          }
        }
      },
      "type_tags": [
        "executable",
        "mobile",
        "android",
        "apk"
      ],
      "last_analysis_results": {
        "Bkav": {
          "method": "blacklist",
          "engine_name": "Bkav",
          "engine_version": "2.0.0.1",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Lionic": {
          "method": "blacklist",
          "engine_name": "Lionic",
          "engine_version": "7.5",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Trojan.AndroidOS.Adrd.l!c"
        },
        "Elastic": {
          "method": "blacklist",
          "engine_name": "Elastic",
          "engine_version": "4.0.144",
          "engine_update": "20240509",
          "category": "undetected",
          "result": null
        },
        "Cynet": {
          "method": "blacklist",
          "engine_name": "Cynet",
          "engine_version": "4.0.1.1",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Malicious (score: 99)"
        },
        "FireEye": {
          "method": "blacklist",
          "engine_name": "FireEye",
          "engine_version": "35.47.0.0",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "CAT-QuickHeal": {
          "method": "blacklist",
          "engine_name": "CAT-QuickHeal",
          "engine_version": "22.00",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Android.Adrd.A"
        },
        "Skyhigh": {
          "method": "blacklist",
          "engine_name": "Skyhigh",
          "engine_version": "v2021.2.0+4045",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "McAfee": {
          "method": "blacklist",
          "engine_name": "McAfee",
          "engine_version": "6.0.6.653",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Malwarebytes": {
          "method": "blacklist",
          "engine_name": "Malwarebytes",
          "engine_version": "4.5.5.54",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Zillya": {
          "method": "blacklist",
          "engine_name": "Zillya",
          "engine_version": "2.0.0.5111",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Sangfor": {
          "method": "blacklist",
          "engine_name": "Sangfor",
          "engine_version": "2.23.0.0",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Trustlook": {
          "method": "blacklist",
          "engine_name": "Trustlook",
          "engine_version": "1.0",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Android.Malware.Spyware"
        },
        "Alibaba": {
          "method": "blacklist",
          "engine_name": "Alibaba",
          "engine_version": "0.3.0.5",
          "engine_update": "20190527",
          "category": "malicious",
          "result": "TrojanSpy:Android/Generic.54ade841"
        },
        "K7GW": {
          "method": "blacklist",
          "engine_name": "K7GW",
          "engine_version": "12.158.51967",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Trojan ( 00550b5f1 )"
        },
        "K7AntiVirus": {
          "method": "blacklist",
          "engine_name": "K7AntiVirus",
          "engine_version": "12.158.51957",
          "engine_update": "20240510",
          "category": "undetected",
          "result": null
        },
        "Arcabit": {
          "method": "blacklist",
          "engine_name": "Arcabit",
          "engine_version": "2022.0.0.18",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Baidu": {
          "method": "blacklist",
          "engine_name": "Baidu",
          "engine_version": "1.0.0.2",
          "engine_update": "20190318",
          "category": "undetected",
          "result": null
        },
        "VirIT": {
          "method": "blacklist",
          "engine_name": "VirIT",
          "engine_version": "9.5.700",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "SymantecMobileInsight": {
          "method": "blacklist",
          "engine_name": "SymantecMobileInsight",
          "engine_version": "2.0",
          "engine_update": "20240103",
          "category": "malicious",
          "result": "Trojan:Adrd"
        },
        "Symantec": {
          "method": "blacklist",
          "engine_name": "Symantec",
          "engine_version": "1.21.0.0",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Trojan.Gen.MBT"
        },
        "tehtris": {
          "method": "blacklist",
          "engine_name": "tehtris",
          "engine_version": "v0.1.4",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "ESET-NOD32": {
          "method": "blacklist",
          "engine_name": "ESET-NOD32",
          "engine_version": "29221",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "a variant of Android/Adrd.E"
        },
        "TrendMicro-HouseCall": {
          "method": "blacklist",
          "engine_name": "TrendMicro-HouseCall",
          "engine_version": "10.0.0.1040",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Avast": {
          "method": "blacklist",
          "engine_name": "Avast",
          "engine_version": "23.9.8494.0",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Android:Adrd-X [Trj]"
        },
        "ClamAV": {
          "method": "blacklist",
          "engine_name": "ClamAV",
          "engine_version": "1.3.1.0",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Andr.Trojan.Adrd-1"
        },
        "Kaspersky": {
          "method": "blacklist",
          "engine_name": "Kaspersky",
          "engine_version": "22.0.1.28",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "HEUR:Trojan-Spy.AndroidOS.Adrd.a"
        },
        "BitDefender": {
          "method": "blacklist",
          "engine_name": "BitDefender",
          "engine_version": "7.2",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "NANO-Antivirus": {
          "method": "blacklist",
          "engine_name": "NANO-Antivirus",
          "engine_version": "1.0.146.25796",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Trojan.Android.ADRD.dmhnnl"
        },
        "SUPERAntiSpyware": {
          "method": "blacklist",
          "engine_name": "SUPERAntiSpyware",
          "engine_version": "5.6.0.1032",
          "engine_update": "20240511",
          "category": "undetected",
          "result": null
        },
        "MicroWorld-eScan": {
          "method": "blacklist",
          "engine_name": "MicroWorld-eScan",
          "engine_version": "14.0.409.0",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "Tencent": {
          "method": "blacklist",
          "engine_name": "Tencent",
          "engine_version": "1.0.0.1",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "TrojanSpy.Android.Adrd.b"
        },
        "Emsisoft": {
          "method": "blacklist",
          "engine_name": "Emsisoft",
          "engine_version": "2024.1.0.53752",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "F-Secure": {
          "method": "blacklist",
          "engine_name": "F-Secure",
          "engine_version": "18.10.1547.307",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Malware.ANDROID/Spy.Adrd.H.Gen"
        },
        "DrWeb": {
          "method": "blacklist",
          "engine_name": "DrWeb",
          "engine_version": "7.0.62.1180",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Android.ADRD.1.origin"
        },
        "VIPRE": {
          "method": "blacklist",
          "engine_name": "VIPRE",
          "engine_version": "6.0.0.35",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "TrendMicro": {
          "method": "blacklist",
          "engine_name": "TrendMicro",
          "engine_version": "11.0.0.1006",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "CMC": {
          "method": "blacklist",
          "engine_name": "CMC",
          "engine_version": "2.4.2022.1",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Sophos": {
          "method": "blacklist",
          "engine_name": "Sophos",
          "engine_version": "2.5.5.0",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "GData": {
          "method": "blacklist",
          "engine_name": "GData",
          "engine_version": "A:25.37983B:27.35988",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "Jiangmin": {
          "method": "blacklist",
          "engine_name": "Jiangmin",
          "engine_version": "16.0.100",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Varist": {
          "method": "blacklist",
          "engine_name": "Varist",
          "engine_version": "6.5.1.2",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "AndroidOS/Adrd.B"
        },
        "Avira": {
          "method": "blacklist",
          "engine_name": "Avira",
          "engine_version": "8.3.3.18",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "ANDROID/Spy.Adrd.H.Gen"
        },
        "MAX": {
          "method": "blacklist",
          "engine_name": "MAX",
          "engine_version": "2023.1.4.1",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "malware (ai score=99)"
        },
        "Antiy-AVL": {
          "method": "blacklist",
          "engine_name": "Antiy-AVL",
          "engine_version": "3.0",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Trojan/Generic.ASMalwAD.1AC"
        },
        "Kingsoft": {
          "method": "blacklist",
          "engine_name": "Kingsoft",
          "engine_version": "None",
          "engine_update": "20230906",
          "category": "undetected",
          "result": null
        },
        "Gridinsoft": {
          "method": "blacklist",
          "engine_name": "Gridinsoft",
          "engine_version": "1.0.175.174",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "Xcitium": {
          "method": "blacklist",
          "engine_name": "Xcitium",
          "engine_version": "36699",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Microsoft": {
          "method": "blacklist",
          "engine_name": "Microsoft",
          "engine_version": "1.1.24040.1",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "TrojanSpy:AndroidOS/Adrd.A"
        },
        "ViRobot": {
          "method": "blacklist",
          "engine_name": "ViRobot",
          "engine_version": "2014.3.20.0",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "ZoneAlarm": {
          "method": "blacklist",
          "engine_name": "ZoneAlarm",
          "engine_version": "1.0",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "HEUR:Trojan-Spy.AndroidOS.Adrd.a"
        },
        "Avast-Mobile": {
          "method": "blacklist",
          "engine_name": "Avast-Mobile",
          "engine_version": "240513-00",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Android:Evo-gen [Trj]"
        },
        "Google": {
          "method": "blacklist",
          "engine_name": "Google",
          "engine_version": "1715650237",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Detected"
        },
        "BitDefenderFalx": {
          "method": "blacklist",
          "engine_name": "BitDefenderFalx",
          "engine_version": "2.0.936",
          "engine_update": "20240128",
          "category": "malicious",
          "result": "Android.Riskware.Agent.KQI"
        },
        "AhnLab-V3": {
          "method": "blacklist",
          "engine_name": "AhnLab-V3",
          "engine_version": "3.25.1.10473",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Spyware/Android.Adrd.1208727"
        },
        "Acronis": {
          "method": "blacklist",
          "engine_name": "Acronis",
          "engine_version": "1.2.0.121",
          "engine_update": "20240328",
          "category": "undetected",
          "result": null
        },
        "VBA32": {
          "method": "blacklist",
          "engine_name": "VBA32",
          "engine_version": "5.0.0",
          "engine_update": "20240510",
          "category": "undetected",
          "result": null
        },
        "ALYac": {
          "method": "blacklist",
          "engine_name": "ALYac",
          "engine_version": "2.0.0.10",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "TACHYON": {
          "method": "blacklist",
          "engine_name": "TACHYON",
          "engine_version": "2024-05-14.01",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "Zoner": {
          "method": "blacklist",
          "engine_name": "Zoner",
          "engine_version": "2.2.2.0",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "Rising": {
          "method": "blacklist",
          "engine_name": "Rising",
          "engine_version": "25.0.0.27",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "Yandex": {
          "method": "blacklist",
          "engine_name": "Yandex",
          "engine_version": "5.5.2.24",
          "engine_update": "20240514",
          "category": "undetected",
          "result": null
        },
        "Ikarus": {
          "method": "blacklist",
          "engine_name": "Ikarus",
          "engine_version": "6.3.12.0",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Trojan.AndroidOS.Adrd"
        },
        "MaxSecure": {
          "method": "blacklist",
          "engine_name": "MaxSecure",
          "engine_version": "1.0.0.1",
          "engine_update": "20240510",
          "category": "malicious",
          "result": "Android.adrd.a"
        },
        "Fortinet": {
          "method": "blacklist",
          "engine_name": "Fortinet",
          "engine_version": "None",
          "engine_update": "20240514",
          "category": "malicious",
          "result": "Android/Hongtoutou.W!tr"
        },
        "BitDefenderTheta": {
          "method": "blacklist",
          "engine_name": "BitDefenderTheta",
          "engine_version": "7.2.37796.0",
          "engine_update": "20240422",
          "category": "undetected",
          "result": null
        },
        "AVG": {
          "method": "blacklist",
          "engine_name": "AVG",
          "engine_version": "23.9.8494.0",
          "engine_update": "20240513",
          "category": "malicious",
          "result": "Android:Adrd-X [Trj]"
        },
        "Cybereason": {
          "method": "blacklist",
          "engine_name": "Cybereason",
          "engine_version": "1.2.449",
          "engine_update": "20240502",
          "category": "undetected",
          "result": null
        },
        "Panda": {
          "method": "blacklist",
          "engine_name": "Panda",
          "engine_version": "4.6.4.2",
          "engine_update": "20240513",
          "category": "undetected",
          "result": null
        },
        "CrowdStrike": {
          "method": "blacklist",
          "engine_name": "CrowdStrike",
          "engine_version": "1.0",
          "engine_update": "20231026",
          "category": "undetected",
          "result": null
        },
        "DeepInstinct": {
          "method": "blacklist",
          "engine_name": "DeepInstinct",
          "engine_version": "5.0.0.8",
          "engine_update": "20240509",
          "category": "type-unsupported",
          "result": null
        },
        "APEX": {
          "method": "blacklist",
          "engine_name": "APEX",
          "engine_version": "6.531",
          "engine_update": "20240513",
          "category": "type-unsupported",
          "result": null
        },
        "Paloalto": {
          "method": "blacklist",
          "engine_name": "Paloalto",
          "engine_version": "0.9.0.1003",
          "engine_update": "20240514",
          "category": "type-unsupported",
          "result": null
        },
        "Trapmine": {
          "method": "blacklist",
          "engine_name": "Trapmine",
          "engine_version": "4.0.16.96",
          "engine_update": "20240223",
          "category": "type-unsupported",
          "result": null
        },
        "Webroot": {
          "method": "blacklist",
          "engine_name": "Webroot",
          "engine_version": "1.0.0.403",
          "engine_update": "20240514",
          "category": "type-unsupported",
          "result": null
        },
        "Cylance": {
          "method": "blacklist",
          "engine_name": "Cylance",
          "engine_version": "2.0.0.0",
          "engine_update": "20240502",
          "category": "type-unsupported",
          "result": null
        },
        "SentinelOne": {
          "method": "blacklist",
          "engine_name": "SentinelOne",
          "engine_version": "24.2.1.1",
          "engine_update": "20240417",
          "category": "type-unsupported",
          "result": null
        },
        "alibabacloud": {
          "method": "blacklist",
          "engine_name": "alibabacloud",
          "engine_version": "2.1.0",
          "engine_update": "20240513",
          "category": "type-unsupported",
          "result": null
        }
      },
      "magic": "Zip archive data, at least v2.0 to extract, compression method=deflate",
      "tags": [
        "telephony",
        "android",
        "reflection",
        "crypto",
        "contains-elf",
        "apk"
      ],
      "tlsh": "T10155234AF3DFF8E2DC93B03657B04B13B92842549285E2F61561D46C4EDAFC9878AE4C",
      "sha1": "afb6da70edef60958f250f41431dc1c9483f8393",
      "last_modification_date": 1715655447,
      "last_analysis_date": 1715654771,
      "trid": [
        {
          "file_type": "Android Package",
          "probability": 63.7
        },
        {
          "file_type": "Java Archive",
          "probability": 26.4
        },
        {
          "file_type": "ZIP compressed archive",
          "probability": 7.8
        },
        {
          "file_type": "PrintFox/Pagefox bitmap (640x800)",
          "probability": 1.9
        }
      ],
      "last_submission_date": 1715655447,
      "bundle_info": {
        "highest_datetime": "2023-11-18 15:50:48",
        "lowest_datetime": "2023-11-18 15:50:48",
        "num_children": 220,
        "extensions": {
          "xml": 90,
          "dex": 1,
          "MF": 1,
          "RSA": 1,
          "so": 5,
          "SF": 1,
          "png": 120
        },
        "file_types": {
          "XML": 90,
          "DEX": 1,
          "ELF": 4,
          "PNG": 120,
          "unknown": 5
        },
        "type": "APK",
        "uncompressed_size": 2169546
      },
      "vhash": "1b6c18df04baf20574af9c1ebe6fea37",
      "crowdsourced_ids_stats": {
        "high": 0,
        "info": 0,
        "medium": 0,
        "low": 4
      },
      "meaningful_name": "addApi.apk",
      "type_description": "Android",
      "unique_sources": 4,
      "reputation": 0,
      "names": [
        "addApi.apk"
      ],
      "permhash": "a4253c6989e01023e3c9ade12c8fec01e9c4fa7331d38695a357e2b07a16fa26"
    }
  }
}
"""
