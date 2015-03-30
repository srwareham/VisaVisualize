# Campaign Advisor

### Server
Do all these commands within the server folder.

- [Server Installation](#server installation)
- [Server Deployment](#server_deployment)
- [Server API](#server_api)

## <a name="server_installation"></a>Server Installation
    pip install -r requirements.txt

## <a name="server_deployment"></a>Server Deployment
	python application.py

## <a name="server_api"></a>Server API
### POST: /hello_world/name
You can issue a `POST` request with the following fields to get a reply of 'Hello' + name you sent

The request must be a valid JSON object with the `Content-Type` set to
`application/json.` The following fields are required:

| Field     | Description                                                   |
| --------- | ------------------------------------------------------------- |
| name      | A string                                                      |
