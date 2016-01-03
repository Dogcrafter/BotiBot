Please create a configuration.json file in this folder
and register all service files

{
  "modules": [
	"test/testService"
  ]
}

Please create a auth.json file in this folder
with the following entries

{
  "token": "TELEGRAM-TOKEN",
  "allowedChatIds": [
    1,
    2,
    3
  ]
}

- Change TELEGRAM-Token to your token
- Enter the allowed Chat Ids in the allowedChatIds array
 