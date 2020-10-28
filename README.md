# hubshare

[![TravisCI build status](https://img.shields.io/travis/com/jupyterhub/hubshare?logo=travis)](https://travis-ci.com/jupyterhub/hubshare)
[![Google Group](https://img.shields.io/badge/google-group-blue.svg)](https://groups.google.com/forum/#!forum/jupyter)

A **directory sharing service** for JupyterHub.

*Important: This repo is in early development (it doesn't work).*

## Project goals

This project's primary goal is enabling **simple**, coarse sharing of notebooks within a JupyterHub instance.

The release of JupyterHub v0.7 added support for [**Services**](https://jupyterhub.readthedocs.io/en/latest/services.html). The availability of Services provides the base foundation for a directory sharing service.

General goals:

- The **sharing unit** is directories.
- **publish** and **download** are explicit actions (no sharing in-place).

These are explicitly **not** goals and are out of this project's scope:

- In-place or real-time sharing (these are tasks for the single-user server)


## Specification

See [specification.md](specification.md) for the planned spec.
