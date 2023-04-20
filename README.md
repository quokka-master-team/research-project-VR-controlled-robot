# research-project-VR-controlled-robot

## Remote Raspberry Pi Access
In Raspberry Pi network ports 22,80 have been forwarded and exposed to Internet via router port forwarding and also by using ngrok service. In order to connect remotely to Raspberry Pi please connect via ssh command:

```ssh devuser@153.19.214.20 -p 2222```

If not available please connect via: 

```ssh devuser@0.tcp.eu.ngrok.io -p 19408```

Web service that listens internally on port 80 is available on: 

```http://153.19.214.20:8080/```

```https://e1f8-153-19-214-20.ngrok-free.app```

If you want to upload your ssh key to Raspberry or gain password for remote access please contact your administrator :)

## Notes
- Please refrain from unecessary rebooting or shutting down the Raspberry Pi!
