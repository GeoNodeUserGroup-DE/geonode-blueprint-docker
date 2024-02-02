# Customizing Config App

Holds configuration assets like templates, snippets, etc. for your GeoNode docker setup.

> :bulb: **Why this module?**
>
> `geonode_mapstore_client` runs as contrib and ships Django assets like templates, snippets, etc.
> That module adds itself at the beginning of `TEMPLATES.DIRS` so all assets are found there at first.
> Use `customization` pushes forward, so you can put your custom config here which take precedence over those defined in `geonode_mapstore_client`.
