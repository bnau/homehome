### Notes 

To get audio books
```bash
curl -s -X GET -H "Content-Type: application/json" -H "X-Emby-Client: test" -H "X-Emby-Client-Version: 1.0.0" -H "X-Emby-Device-Name: device" \
 -H "X-Emby-Device-Id: 1" \
 -H "X-Emby-Token: $(curl -s -X POST -H "Content-Type: application/json" -H "X-Emby-Client: test" -H "X-Emby-Client-Version: 1.0.0" \
 -H "X-Emby-Device-Name: device" -H "X-Emby-Device-Id: 1" -d '{"username":"bnau","pw":"XXXXXXX"}' \
 http://192.168.1.40:8096/Users/authenticatebyname | jq -r .AccessToken)" \
 http://192.168.1.40:8096/Users/60fb890c08fd418baf3a83d020986fb5/Items\?IncludeItemTypes\=MusicAlbum\&recursive\=true
```

To get albums
```bash
curl -g -X POST -d '{"id":1, "method":"slim.request", "params": ["-", ["albums", 0, 1425, "tags:aaly"]]}' http://192.168.1.40:9000/jsonrpc.js
```