# Specification of hubshare REST API

## Directories

### List your directories

List directories that are accessible to the authenticated users.

```
GET /users/dirs
```

### List user directories

List public directories for the specified users.

```
GET /users/:username/dirs
```

### List all public directories

```
GET /directories
```

### Create a directory

```
POST /users/dirs
```

### Get a directory

```
GET /dirs/:owner/:dir
```

### Update a directory

```
PATCH /dirs/:owner/:dir
```

### List readers

```
GET /dirs/:owner/:dir/readers
```

### List writers

```
GET /dirs/:owner/:dir/writers
```

### Delete a directory

```
DELETE /dirs/:owner/:dir
```

## Collaborators

### List collaborators

```
GET /dirs/:owner/:dir/collaborators
```

### Check if a user is a collaborator

```
GET /dirs/:owner/:dir/collaborators/:username
```

### Add user as a collaborator

```
PUT /dirs/:owner/:dir/collaborator
```

### Remove user as a collaborator

```
DELETE /dirs/:owner/:dir/collaborators/:username
```

## Contents

### Get contents

```
GET /dirs/:owner/:dir/contents
```

### Create contents

```
PUT /dirs/:owner/:dir/contents
```

### Update contents

```
PUT /dirs/:owner/:dir/contents
```

### Delete contents

```
DELETE /dirs/:owner/:dir/contents
```

## Copies

### List copies

```
GET /dirs/:owner/:dir/copies
```

### Create a copy

```
POST /dirs/:owner/:dir/copies
```












