import requests

url = "https://www.virustotal.com/api/v3/files"
apk_file = 'D://apktool//Drebin//02-Adrd//addApi.apk'

files = { "file": ("D://apktool//Drebin//02-Adrd//addApi.apk",
                   open("D://apktool//Drebin//02-Adrd//addApi.apk", "rb"), "application/vnd.android.package-archive") }
headers = {
    "accept": "application/json",
    "x-apikey": "169d3b77091cf49775f723ca99feabdbbb336650ae2d912889f3dd0cf3119588"
}

response = requests.post(url, files=files, headers=headers)

print(response.text)

"""
    输出内容：
{
  "data": {
    "type": "analysis",
    "id": "MGYyYzY5MjQ3OTUzNDBkYzE1MWYyZmY3YzJiZGYyOTA6MTcxNTY1Njc4NA==",
    "links": {
      "self": "https://www.virustotal.com/api/v3/analyses/MGYyYzY5MjQ3OTUzNDBkYzE1MWYyZmY3YzJiZGYyOTA6MTcxNTY1Njc4NA=="
    }
  }
}
"""
