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

* DB will already be created (blank) and dbuser existing
* connection string will be 'hardcoded'
* No authentication
* construct args to the create-madrona-project.py script
* run on port 8080? Or run on desktop if gui?
* inital app on 80 will just be a wsgi script in /usr/local/apps/example/deploy which serves a page with link to 8080
* GET / on 8080 will check for creation of project (look at db tables and filesystem) and direct users to app (port 80)... maybe brief note about how they can restart from scratch
* if not existing, will show a form which can be POSTed to the same URL
* Successful POST will construct a create-madrona-project.py command, mv /usr/local/apps/example, run cmd, touch deploy/wsgi.py (the host will already be configured to look for it) and return a redirect to 80. 
* provide some docs on how to wipe DB and filesystem to restart the process
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

