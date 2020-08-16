# API

Base URL: https://sc-backend-v0.herokuapp.com

### Note about error responses
All endpoints except for the email confirmation and confirming a password reset will return a JSON object of the following form:
```json
{
    "status": "error",
    "reason": "Sample error message"
}
```

## User API
We use JWTs to manage authentication, mainly for allowing the user to edit their club's information.

### Does email exist? (before sign up)
* Description: Given an email for a potential sign up, check if it exists within to list of scrapped CalLink emails?
* Path: `GET /api/user/email-exists`
* Sample body input:
```json
{
    "email": "lol@gmail.com",
}
```
* Sample body output:
```json
{
    "exists": true
}
```

### Register a new user
* Description: Registers a new user and club pair
* Path: `POST /api/user/register`
* Sample body input:
```json
{
    "name": "Test Club",
    "email": "testclub@gmail.com",
    "password": "thisistotallyasecurepasswordlol",
    "tags": [3, 1, 4],
    "app-required": true,
    "new-members": true,
}
```
* Sample body output:
```json
{
    "status": "success"
}
```

### Confirm new user
* Description: Confirms the new user and club pair (this endpoint is normally within an email)
* Path: `GET /api/user/confirm/<confirm_token>`
* Result: Redirects you to the club edit profile page (ideally)

### Login user
* Description: Logs in a user
* Path: `POST /api/user/login`
* Sample body input:
```json
{
    "email": "testclub@gmail.com",
    "password": "thisistotallyasecurepasswordlol"
}
```
* Sample body output:
```json
{
    "access": "somereallylongaccesstokenthatdoesnotlooklikethis",
    "refresh": "somereallylongrefreshtokenthatdoesnotlooklikethis"
}
```

### Refresh access token
* Description: Fetches a new access token given a valid refresh token
* Path: `POST /api/user/refresh`
* Headers:
    - `Authorization: Bearer <refresh_token>`
* Sample body output:
```json
{
    "access": "somereallylongaccesstokenthatdoesnotlooklikethis"
}
```

### Revoke access token
* Description: Revokes an issued access token, preventing further use of it
* Path: `POST /api/user/revoke-access`
* Headers:
    - `Authorization: Bearer <access_token>`
* Sample body output:
```json
{
    "status": "success",
    "message": "Access token revoked!"
}
```

### Revoke refresh token
* Description: Revokes an issued refresh token, preventing further use of it
* Path: `POST /api/user/revoke-refresh`
* Headers:
    - `Authorization: Bearer <refresh_token>`
* Sample body output:
```json
{
    "status": "success",
    "message": "Refresh token revoked!"
}
```

### Reset Password
* TODO

### Confirm Reset Password
* TODO


## Catalog API

### Fetch set of tags
* Description: Fetches the set of category tags
* Path: `GET /api/catalog/tags`
* Sample body output:
```json
[
    {
        "id": 42,
        "name": "Example tag"
    },
    {
        "id": 84,
        "name": "Another Example Tag"
    }
]
```

### Fetch organizations (unfiltered)
* Description: Fetches the list of organizations without filters, sorted alphabetically.
* Path: `GET /api/catalog/organizations`
* Sample body input:
```json
{
    "limit": 50,
    "skip": 0
}
```
* Sample body output:
```json
[
    {
        "id": "bfx",
        "name": "BFX",
        "logo": "<base64-encoded-image>",
        "banner": "<base64-encoded-image>",
        "tags": [1, 3, 4],
        "app_required": true,
        "new_members": false,
    }
]
```

### Fetch organizations (filtered)
* Description: Fetches the list of organizations with filters, sorted by match relevency
* Path: `GET /api/catalog/organizations`
* Sample body input:
```json
{
    "search": "BFX",
    "tags": [],
    "app-required": true,
    "accepting-members": false,
    "limit": 50,
    "skip": 0
}
```
* Sample body output:
```json
[
    {
        "id": "bfx",
        "name": "BFX",
        "tags": [1, 3, 4],
        "logo": "<base64-encoded-image>",
        "banner": "<base64-encoded-image>",
        "app_required": true,
        "new_members": false,
    }
]
```

### Fetch single organization
* Description: Fetches all the information of a single organization by ID
* Path: `GET /api/catalog/organizations/<org-id>`
* Sample output:
```json
{
    "id": "bfx",
    "name": "BFX",
    "owner": "tejashah88@gmail.com",
    "tags": [1, 3, 4],
    "logo": "<base64-encoded-image>",
    "banner": "<base64-encoded-image>",
    "app_required": true,
    "new_members": false,
    "about_us": "This is something about the club.",
    "get_involved": "This is something about getting involved.",
    "resources": [
        {
            "name": "Example resource",
            "link": "https://www.resource.com"
        }
    ],
    "events": [
        {
            "name": "Example event",
            "link": "https://www.event.com",
            "start_datetime": "<seconds-since-epoch>",
            "end_datetime": "<seconds-since-epoch>",
            "description": "This is a description about example event.",
        }
    ]
}
```

