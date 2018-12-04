# CleverTap
An OMG service to access the CleverTap event and profile APIs.

## Usage
```coffeescript
clevertap push event: "Logged In" identity: "john"
clevertap push event: "Logged In" properties: {"Source": "Website"} identity: "john"
clevertap push profile: {"Fruit": "Mango"} identity: "john"
```
