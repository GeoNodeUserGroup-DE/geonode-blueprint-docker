# Geonode Installation

This document will guide you through the installation of [GeoNode](https://geonode.org/), a spatial content management system.
The needed components are available as [Docker](https://www.docker.com/) images and will be set up and run via the [docker compose](https://docs.docker.com/compose/) tool.

## Component Overview

Here is a short overview of the installed components and how they are connected.

![GeoNode Architecture](./img/geonode_architecture_4x.png "Geonode Architecture")

The components are:

- **Django:** The actual GeoNode component.
It exposes a [pyCSW API](https://pycsw.org/) and the GeoNode API.
- **Celery:** [Celery](https://docs.celeryq.dev/en/stable/) forms the asynchronuous task queue of GeoNode.
- **GeoServer:** [GeoServer](https://geoserver.org/) is the backend server of GeoNode for sharing geospatial data.
It exposes OGC APIs such as WMS, WFS, etc. 
- **Nginx:** [Nginx](https://nginx.com) serves as advanced load balancer, web server and reverse proxy to all GeoNode components.
- **PostgreSQL:** GeoNode and GeoServer are using [PostgreSQL](https://www.postgresql.org)  with the geospatial extension [PostGIS](https://postgis.net) as the database.

## Setup Project

Make sure you have installed `git`, `Docker` and `docker compose`.

Clone the [istg_geonode repository]( https://github.com/52North/istg_geonode) and change directory your local working copy:

```
git clone https://github.com/52North/istg_geonode geonode
cd geonode
```

## Configuration

> :bulb: **Note**
>
> Settings (e.g. geodatabase parameters) are mainly configured in the `.env` file. 
> To review in-built default settings of an image, run the `env` command on an image.
> For example `docker run 52north/istg_geoserver env | sort`.
>
> For a complete set of available options take the [GeoNode Settings](https://docs.geonode.org/en/master/basic/settings/index.html#settings) documentation as a reference.

The containers get configured during creation via environment variables. 
The `geonode/settings.py` settings module takes further configuration of the GeoNode containers (`django` and `celery`) and aligns some names with those documented.


Copy the `sample.env` to `.env` and make your changes (`.env` is not versioned).
For a quick start taking default values you can run `docker compose up -d --env-file=sample.env`.


Have a look at the [Ways to set environment variables in Compose](https://docs.docker.com/compose/environment-variables/set-environment-variables/) documentation.



## Start and Run

### Docker-Compose Basics

Run `docker compose up -d` to start all geonode components.
Review all started components by executing `docker compose ps`. 
You can follow logs via `docker compose logs -f` and optionally pass a service to only follow a service's log.

Stop all components via `docker compose down`, and pass a `-v` flag to clean up all volumes (CAUTION: removes all persisted data).

For more features and available commands, `docker compose --help`, or read [the docker compose CLI documentation](https://docs.docker.com/compose/reference/).

### Add a Service Unit

When running GeoNode on a systemd-based Linux, you may want to add a service unit:

/etc/systemd/system/geonode.service
```sh
[Unit]
Description=IStG GeoNode Instance

[Service]
Type=oneshot
ExecStart=docker compose up -d /path/to/workingcopy

[Install]
WantedBy=multi-user.target
```

Then reload the systemd daemon:

```sh
systemctl daemon-reload
```

And enable GeoNode start on each boot:

```sh
systemctl enable geonode.service
```

Check the service status:

```sh
systemctl status geonode.service
```
