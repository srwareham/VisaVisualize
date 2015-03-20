# VisaVisualizer

### Server
Do all these commands within the server folder.

- [Server Installation](#server installation)
- [Server Deployment](#server_deployment)
- [Server API](#server_api)

## Server Installation
    pip install -r requirements.txt

## Server Deployment
	python application.py

## Server API
### POST: /hello_world/name
You can issue a `POST` request with the following fields to get a reply of 'Hello' + name you sent

The request must be a valid JSON object with the `Content-Type` set to
`application/json.` The following fields are required:

| Field     | Description                                                   |
| --------- | ------------------------------------------------------------- |
| name      | A string                                                      |