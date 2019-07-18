# _CleverTap_ OMG Microservice

[![Open Microservice Guide](https://img.shields.io/badge/OMG%20Enabled-👍-green.svg?)](https://microservice.guide)

An OMG service to access the CleverTap event and profile APIs.

## Direct usage in [Storyscript](https://storyscript.io/):

##### Upload Event
```coffee
clevertap push event: "Logged In" identity: "john" properties: {"Source": "Website"}
```
##### Get Event
```coffee
clevertap getEvent event: "Logged In" from:20190715 to:20190716
```
##### Get Event Count
```coffee
clevertap getEventCount event: "Logged In" properties: {"Source": "Website"} from:20190715 to:20190716
```
##### Upload Profile
```coffee 
clevertap push identity: "Demo User" profile: {"Name": "Jack Montana","Email": "jack@gmail.com","Phone": "+14155551234","Gender": "M"}
```
##### Get User Profile
```coffee
clevertap getUserProfile event: "Logged In" from: 20181203 to: 20190716
```
##### Get Profile Count
```coffee
clevertap getProfileCount event: "Logged In" properties: {"Source": "Website"} from: 20181203 to: 20190716
```
##### Delete User Profile
```coffee
clevertap deleteUserProfile identity :"Demo User"
```

Curious to [learn more](https://docs.storyscript.io/)?

✨🍰✨

## Usage with [OMG CLI](https://www.npmjs.com/package/omg)

##### Upload Event
```shell
$ omg run push -a event=<EVENT_NAME> -a identity=<EVENT_IDENTITY> -a properties=<PROPERTIES_IN_MAP_TYPE> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```
##### Get Event
```shell
$ omg run getEvent -a event=<EVENT_NAME> -a from=<FROM_DATE> -a to=<TO_DATE> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```
**Note**: FROM_DATE and TO_DATE should be in YYYYMMDD format.
##### Get Event Count
```shell
$ omg run getEventCount -a event=<EVENT_NAME> -a properties=<PROPERTIES_IN_MAP_TYPE> -a from=<FROM_DATE> -a to=<TO_DATE> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```

##### Upload Profile
```shell
$ omg run push -a identity=<PROFILE_IDENTITY> -a profile=<PROFILE_IN_MAP_TYPE> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```
##### Get Profile
```shell
$ omg run getUserProfile -a event=<EVENT_NAME> -a from=<FROM_DATE> -a to=<TO_DATE> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```
##### Get Profile Count
```shell
$ omg run getProfileCount -a event=<EVENT_NAME> -a properties=<PROPERTIES_IN_MAP_TYPE> -a from=<FROM_DATE> -a to=<TO_DATE> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```
##### Delete User Profile
```shell
$ omg run deleteUserProfile -a identity=<PROFILE_IDENTITY> -e ACCOUNT_ID=<ACCOUNT_ID> -e ACCOUNT_PASSCODE=<ACCOUNT_PASSCODE>
```

**Note**: The OMG CLI requires [Docker](https://docs.docker.com/install/) to be installed.

## License
[MIT License](https://github.com/omg-services/clevertap/blob/master/LICENSE).
