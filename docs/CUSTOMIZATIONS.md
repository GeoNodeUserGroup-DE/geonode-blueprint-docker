# Possible Customizations

This blueprint is designed to give you the flexibility you may need to apply settings and customizations necessary to your project.
It does so with the intent to put the complex parts to the back without hiding them. 
You can separate needed upstream adjustments to avoid versioning conflicts while keeping the possibility to compare changes over time to keep your project maintainable and close to upstream. 


## Settings / Configuration

GeoNode can be configured via `.env` file.
The variables therein will become environment variables in the Docker containers.
However, spinning up configuration is quite complex and there's some logic here and there doing some magic.

Some hot places are

- `settings.py`
- `entrypoint.sh`
- `tasks.py`  

The docker blueprint tries to provide reasonable defaults for lesser used variables.
Those variables which would are updated commonly for a deployment, are listed in `sample.env` (for simple key-value properties) and `override_settings.json` (for more complex configuration).

If in doubt or you are missing a particular setting, prepare to have available the [settings documentation](https://docs.geonode.org/en/master/basic/settings/index.html#settings) and [the settings.py source](https://github.com/GeoNode/geonode/blob/master/geonode/settings.py) as a reference.


## Custom Apps

Django apps lets you extend GeoNode (as with any other Django based application).
Under `geonode/apps` you can put your apps under version control.
Use git submodules to track modules which are versioned in different repositories.
Modules are added to the project via Docker volumes and have to be configured via Django's `INSTALLED_APPS`.

The project's `geonode/apps/customizations` app is some kind of special as it includes general changes to UI parts via templates and styling.


## Initial Data

Django gives you the possibility to add data from an fixture exported from the database.
This is handy in some cases where you want to have initial data available.
Some exmple data is provided in the `fixtures` folder, e.g. `additionallicenses.json` includes [creative-commons licenses](https://creativecommons.org/).

However, fixtures are a bit brittle to maintain over time.
So use with care.

## GeoNode MapStore Client (`geonode-mapstore-client`)

Since GeoNode `v4` the UI has switched (mainly) to a react client.
The client now is based on the `MapStore2` framework and uses GeoNode REST API to communicate with the backend.

> :info: 
>
> There are UI parts which are still Django templates.
> The client is embedded into the actual main template where all the GeoNode based styling is applied upon.

Currently, UI adjustments are limited to `Mapstore2` extensions as there is no API to customize components within `geonode-mapstore-client`.
However, you can configure (to some extend) avaiable components via `geonode-mapstore-client/_geonode_config.html`

If you make UI changes which requires a `geonode-mapstore-client` fork building the GeoNode image can be cumborsome.
To improve performance, add the project as git submodule and add it in `Dockerfile` via `COPY`.


## Layout and Styling (GeoNode)

Styling and theming are two-fold: Django based templates and MapStore2 based configuration.


### GeoNode Templates

The Django admin gives you control over simple styling of your GeoNode application.
There is a `Themes` section where you can adjust multiple parts of the UI:

- logo
- jumbotron
- slideshow
- background

To get more control over your layout you can use template snippets:

- `brand_navbar.html`
- `custom_theme.html`
- `footer.html`
- `header.html`
- `hero.html`
- `language_selector.html`
- `loader_style.html`
- `loader.html`
- `menu_item.html`
- `search_bar.html`
- `topbar.html`

By default, this setup provides a `custom_theme.html` snippet which includes some styling variables.
You can create your own theme via [GeoNode styling tool](https://geonode.org/geonode-mapstore-client/master/tutorial-theme.html).

Django's admin interface lets you create multiple themes and switch between them.
Customizing template snippets are more flexible, though, as these gives you more control over HTML structure and look.
It even can be combined with code (e.g. URL routes, template tags, ...) which gives you full control and the possibility to leverage other tooling like database or libraries of your choice.


### Styling via MapStore2

The MapStore2 framework provides different arrangement configuration of your Website dependent on the display context.
For example, you can provide configuration modes for `mobile`, `desktop`, `embedded`, and other.

> :warning: `localConfig.json`
>
> The whole configuration is located in the `/static/mapstore/configs/localConfig.json` file which is quite big.
> In addition, the `geonode-mapstore-client` follows its own magic on applying `MapStore2` routing, i.e. its documentation does not apply to GeoNode UI necessarily.
> 
> Double check before making changes.

While Django templates can be used to apply general styling, some `MapStore2` components provide config properties to apply adjustments.
These can be applied by overriding `overrideLocalConfig` function within the `geonode-mapstore-client/_geonode_config.html` templates.


### References

- https://geonode.org/geonode-mapstore-client/master/tutorial-theme.html
- https://geonode.org/geonode-mapstore-client/master/tutorial-02-theme-variables.html
- https://geonode.org/geonode-mapstore-client/master/tutorial-03-override-local-config.html


## Adding Subsites

Makes available a subset of resources under a particular URL.
You are able restrict user permissions and apply individual themes.

Include the `Subsites` app (`INSTALLED_APPS`) and configure a subsite which displays a filtered set of resources.
Follow the documentation on the [SUBSITES documentation](./SUBSITES.md).


### References

- https://github.com/geosolutions-it/geonode-subsites/blob/main/README.md
- https://docs.geonode.org/en/4.2.5/advanced/contrib/subsites/index.html#geonode-subsites


## Advanced Configuration and Patching

Provide more extensive patching which completely overlays a upstream files.
Changes are tracked within the container as changes are compared to the included working copy.

> :info: Uncommon Practice
>
> It is uncommon a container image includes a whole git working directory.
> GeoNode is currently doing this so we are (mis?)using that, so file overlays can be tracked conflict free while still being able to compare upstream changes within the container.
> 
> This possibility might change in case upstream removes working copy from the image.

We take the `thuenen_atlas` as an example:

As a federeal research institute, metadata has to comply with the GDI-DE metadata schema which is a profile of ISO 19135.
To match certain requirements, the `full_metadata.xml` had to be adjusted to some extend.
The `thuenen_atlas` tracks its local customized `full_metadata.xml` template, while GeoNode upstream follows more common requirements.
Two versioning strategies have to be considered.

However, we have different repositories and cannot do a simple git diff, so how to track changes?
The GeoNode Docker image contains the project's git working directory. 
To keep track on the upstream changes, just start and `exec` into the container.
Alternatively, you can use IDE tooling by starting the devcontainer environment to compare your changes with upstream.

To be frank, this is not the nicest solution but works in this integrated development setup.
No need to pick for diff'ing individual files from different repositories.

### References

- https://github.com/Thuenen-GeoNode-Development/thuenen_atlas
- https://testsuite.gdi-de.org/
