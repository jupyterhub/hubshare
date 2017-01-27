# hubshare planning

**This is a DRAFT document. All content is subject to change.**


[Storage](#storage) | [API](#api) | [UI](#ui) |
[Single user server interactions](#single-user-server-interactions) |
[nbgrader](#nbgrader) | [Interacting with HubShare](#interacting-with-hubshare)

## Storage

>Perhaps even before we get to the REST API (#6), we need to implement the storage itself. If we are importing a WebDAV server, we don't need to do much beyond mapping our ownership/permissions onto it, but if we are implementing our own API, we do.

>A simple approach would be to use content-addressable storage: keep each zipfile in /ab/cd/sha256-path.zip, since we already need the sha for the API, this makes finding files very simple. We shouldn't need to unpack the archives at any point in HubShare.


## API

The basic API has been described in the API [specification](../specification.md).


## UI

>Once we have the API (#6), we'll want a basic web UI for managing, browsing shares. I've added an empty package.json, assuming we'll be using the npm-style tooling we have elsewhere. I'd like to give react+es6 a try here, rather than the phosphor+typescript approach in JupyterLab. This won't be a desktop-style multi-pane application with menubar, commands, etc.

>We should draft what sort of features are needed in the UI, and what each page should look like.

>Basic pages:

>- user's home
- list user's shares
- single share
- owner actions: delete / rename / modify / upload
- non-owner actions: download (more?)
- list other users and their shares

>Related questions:

>what should a view of a single share look like? Does it need things like browsing files in the share, showing rendered notebooks, etc.? A simple file-listing and single-file view could be handled simply enough without needing to unpack the uploaded zipfiles.


## Single user server interactions

> How should a 'download' action on HubShare work? Should data be pushed to single-user servers via HubShare, or should data be pulled from HubShare by the single-user server?

> From the auth standpoint, actions initiated by the single-user server are probably going to be simplest.

> This will likely need a server extension implementing:

>- send data to HubShare
- get data from HubShare
- (possibly) maintain a record of local paths to shares, so that things like 'update' can be simple

>because there isn't currently a way to get data into or out of single-user servers in the form HubShare wants (zipped directories). Some basic functionality could be added to the single-user server to do this, though.


## nbgrader

>One of the main goals of this is to alleviate nbgrader's need to do assignment distribution and collection via the filesystem.

>we should sketch out each of nbgrader's assignment operations, to make sure that we can express them in terms of operations that can be accomplished cleanly with HubShare.


## Interacting with HubShare

- [Client library](#client-library)
- [JupyterLab extension](#jupyterlab-extension)

### Client library

>once this is up, we should probably have a simple Python client library (and possibly CLI) for interacting with HubShare.

>Since we've got a simple REST (and/or WebDAV) API, this should be pretty straightforward via requests.Session.

### JupyterLab extension

> once all of the working pieces are in order (#6, #8), we should have a JupyterLab extension for talking to HubShare.

>at least: uploading new/updated shares (a basic 'share' button would be), so users have a mechanism to start uploading things.
possibly (maybe too far): browsing, downloading existing shares. This might be nice, but would be redundant with UI already required to do the same on HubShare itself, so a lower priority. A link to HubShare would be enough to start.

[Storage](#storage) | [API](#api) | [UI](#ui) |
[Single user server interactions](#single-user-server-interactions) |
[nbgrader](#nbgrader) | [Interacting with HubShare](#interacting-with-hubshare)
