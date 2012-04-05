## Madrona App Generator

### Purpose

This will run initially on a virtual machine allowing the user to specify application details to kickstart the launch of their initial app.
It is essentially a django-based GUI for constructing and running the ``create-madrona-project.py`` script distributed with madrona.

### Example command

```
create-madrona-project.py \
   --project testproject \
   --app testapp \
   --domain 192.168.1.111:8000 \
   --connection "dbname='example' user='madrona' password='<PASSWORD>'" \
   --studyregion "SRID=4326;POLYGON(((...)))" \
   --aoi "My Areas" \
   --aoi "My Other Areas" \
   --folder "Folder for Areas" \
   --kmls public.kml
```
### Notes

* appgen database and `madrona` dbuser will be pre-created on the VM
* connection string will be 'hardcoded'
* The appgen project will be created by a single django admin user with a known password
* The app will construct args to the create-madrona-project.py script
* appgen will run on port 80
* Newly created appconfigs will 1) create new db 2) generate code into /usr/local/apps/ 3) start gunicorn server on port xxxx
* Port will be auto-sequenced 

#### Full CRUD interface                                                               

* GET / on 80 will list table of all apps with [link to edit][link to view][link to delete]
* Single [Add App] button
* leverage admin as much as possible

### Feature types

Have some default show.html template (aka report) for each

Have icons ready

Will accept multiple opts

* AOI (--aoi "Area of Interest" ) report = area
* POI --poi , report = lat lon
* LOI --loi, report = length
* Folder --folder

### KML

``--kml`` URL or path to public KML

### Study region

``--studyregion`` shapefile or WKT or geojson

