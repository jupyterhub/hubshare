# Specification of hubshare REST API

## Directories

This part of the REST API contains calls for working with directories.
Conceptually, a directory has the following properties:

* Is a zipped directory of contents.
* Has an owner.
* Can be copied by other users, which creates a new directory entry
  with a `parent` field.
* Has a `SHA` that labels the version of the directory.
* Has a list of other user that can upload (`writers`) and downloads
  (`readers`) the directory.
* Has list of users than are administrators (`admins`) of the directory.
  These users can add/remove readers, writers and admins.

### List your directories

List directories that are accessible to the authenticated users.

```
GET /users/dirs
```

#### Response

```
Status: 200 OK
```

```json
[
  {
    "id": 123,
    "owner": {"name": "person1", "type": "user"}
    "sha": "asdf",
    "name": "data301-assignment01",
    "parent": {
      "id": 456,
      "name": "data301-assignment01",
      "owner": {"name": "person2", "type": "user"},
      "sha": "adsf"
    }
    "readers": [
      {"name": "person2", "type": "user"},
      {"name": "group1", "type": "group"}
    ],
    "writers": [
      {"name": "person2", "type": "user"},
      {"name": "group1", "type": "group"}
    ],
    "admins": [],
    "content_url": "/api/url_to_get_contents",
    "created_at": "2011-01-26T19:06:43Z",
    "permissions": {
      "admin": false,
      "upload": true,
      "download": true
    }
  }
]
```

### List user directories

List public directories for the specified users.

```
GET /users/:username/dirs
```

The response is the same as the previous call.

### List all public directories

List all public directories.

```
GET /dirs
```

The response is the same as the previous call.


### Create a directory

Create a new directory for the authenticated user.

```
POST /users/dirs
```

#### Input

```json
{
  "name": "data301-assignment01",
  "private": true,
  "readers": [
    {"name": "person2", "type": "user"},
    {"name": "group1", "type": "group"}
  ],
  "writers": []
  ],
  "admins": []
}
```

#### Response


```
Status: 201 Created
```

```json
{
  "name": "data301-assignment01",
  "private": true,
  "sha": "asdf",
  "readers": [
    {"name": "person2", "type": "user"},
    {"name": "group1", "type": "group"}
  ],
  "writers": []
  ],
  "admins": []
  "content_url": "/api/url_to_get_contents",
  "created_at": "2011-01-26T19:06:43Z",
  "permissions": {
    "admin": true,
    "upload": true,
    "download": true
  }
}

```

### Get a directory

Get the model for a individual directory, without the contents.

```
GET /dirs/:owner/:dir
```

#### Response

```
Status: 200 OK
```

```json
{
  "id": 123,
  "owner": {"name": "person1", "type": "user"}
  "sha": "asdf",
  "name": "data301-assignment01",
  "parent": {
    "name": "data301-assignment01",
    "owner": {"name": "person2", "type": "user"},
    "sha": "adsf"
  },
  "readers": [
    {"name": "person2", "type": "user"},
    {"name": "group1", "type": "group"}
  ],
  "writers": [
    {"name": "person2", "type": "user"},
    {"name": "group1", "type": "group"}
  ],
  "admins": [],
  "content_url": "/api/url_to_get_contents",
  "created_at": "2011-01-26T19:06:43Z",
  "permissions": {
    "admin": false,
    "upload": true,
    "download": true
  }
}
```

### Update a directory

Update the model for an existing directory, with the contents.

```
PATCH /dirs/:owner/:dir
```

#### Input

```json
{
  "name": "data301-assignment01",
  "readers": [
    {"name": "person2", "type": "user"},
  ],
  "writers": [],
  "admins": [],
}
```

#### Response

```
Status: 200 OK
```

```json
{
  "id": 123,
  "owner": {"name": "person1", "type": "user"}
  "sha": "asdf",
  "name": "data301-assignment01",
  "parent": {
    "name": "data301-assignment01",
    "owner": {"name": "person2", "type": "user"},
    "sha": "adsf"
  },
  "readers": [
    {"name": "person2", "type": "user"},
  ],
  "writers": [],
  "admins": [],
  "content_url": "/api/url_to_get_contents",
  "created_at": "2011-01-26T19:06:43Z",
  "permissions": {
    "admin": false,
    "upload": true,
    "download": true
  }
}
```

### Delete a directory

Delete the model for a directory, not its contents.

```
DELETE /dirs/:owner/:dir
```

#### Response

```
Status: 204 No Content
```

## Collaborators

A directory can have a set of collaborators associated with it. These
collaborators can have different permissions:

* Download
* Upload
* Admin

### List collaborators

List the collaborators (readers, writers) for the directory.

```
GET /dirs/:owner/:dir/collaborators
```

#### Response

```
Status: 200 OK
```

```json
[
  {
    "name": person1,
    "type": "user",
    "permissions": {
      "admin": false,
      "upload": true,
      "download": true
    }
  }
]
```

### Add user as a collaborator

Add a user as a collaborator on a directory.

```
PUT /dirs/:owner/:dir/collaborators/:username
```

#### Input

```json
{
    "permissions": {
      "admin": false,
      "upload": true,
      "download": true
    }
    "type": "group"
}
```

#### Response

```
Status: 204 No Content
```

```json
{
  "directory": {directory model},
  "invitee": {
    "name": "group1",
    "type": "group"
  }
  "inviter": {
    "name": "person2",
    "type": "user"
  }
}
```

### Remove user as a collaborator

Remove a user as a collaborator on a directory.

```
DELETE /dirs/:owner/:dir/collaborators/:username
```

#### Response

```
Status: 204 No Content
```

## Contents

The contents API is for uploading and downloading the actual zipped
directory contents.

### Get contents

Download the actual zipped directory contents.

```
GET /dirs/:owner/:dir/contents
```

#### Response

```
Status: 200 OK
```

The body of the response will contain the zipped directory contents.

### Create contents

Create a new zipped directory contents.

```
PUT /dirs/:owner/:dir/contents
```

#### Response

```
Status: 201 Created
```

### Update contents

Update a previously uploaded contents.

```
PUT /dirs/:owner/:dir/contents
```

#### Reaponse

```
Status: 204 No Content
```


### Delete contents

Delete a previously uploaded directory contents.

```
DELETE /dirs/:owner/:dir/contents
```

#### Rasponse

```
Status: 204 No Content
```

## Copies

### List copies

List all of the copies of a directory

```
GET /dirs/:owner/:dir/copies
```

#### Response

```
Status: 200 OK
```

```json
[
    {directory model 1},
    {directory model 2},
    {directory model 3}
]
```

### Create a copy

Create a copy of a directory.

```
POST /dirs/:owner/:dir/copies
```

#### Input

```json
{
  "name": "data301-assignment01",
  "owner": {owner model},
  "readers": [],
  "writers": [],
  "admins": [] 
}
```

#### Response

```
Status: 200 OK
```

```json
{directory model}
```











