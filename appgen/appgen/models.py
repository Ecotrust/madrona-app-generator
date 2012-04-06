from django.contrib.gis.db import models

class AppConfig(models.Model):
    app = models.CharField(verbose_name="App name", max_length=35)
    desc = models.TextField(verbose_name="Description")
    studyregion = models.PolygonField()
    features = models.ManyToManyField('UserFeature')
    kmls = models.ManyToManyField('BaseKml')
    ip = models.IPAddressField()
    objects = models.GeoManager()

    class Meta:
        verbose_name = "Madrona App"
        verbose_name_plural = "Madrona Apps"

    def __unicode__(self):
        return self.app

    @property
    def project(self):
        return "exampleproject"

    @property
    def features_list(self):
        inner = ' '.join(['<li>'+f.fname+'</li>' for f in self.features.all()])
        return '<ul>'+inner+'</ul>'

    @property
    def extent(self):
        return self.studyregion.extent

    @property
    def links(self):
        # TODO Probably should put this in the templatetags or a template of some sort?
        return """
        <style>
        .golink {
            padding-left: 12px;
            background: url(/static/admin/img/icon-yes.gif) 0 .2em no-repeat;
        }
        </style>
        <div style="width:100px !important;">
            <p><a href="/admin/appgen/appconfig/%d/delete/" class="deletelink"> Delete </a></p>
            <p><a href="http://%s" class="golink"> Go to App </a></p>
            <p><a href="#" class="changelink"> Customize </a></p>
        </div>
        """ % (self.pk, self.domain)

        """
         WE DONT PROVIDE AND EDIT LINK !
         because the code is generated once, its a one shot deal
            <li><a href="/admin/appgen/appconfig/%d/" class="changelink"> Edit </a></li>
        """


    @property
    def status(self):
        # TODO
        return """
        <div>
        <p>Status: <br/> Not Running <br/> (<em>12:03pm</em>)</p>
        </div>
        <br/><br/>
        <ul class="object-tools">
            <li><a href="/reload/%d/" class="tablelink"> Stop/Reload/Restart </a></li>
        </ul>
        """ % self.pk

    @property
    def wms(self): 
        area = self.studyregion.area
        w = area ** 0.5
        w = w/2
        g = self.studyregion.buffer(w)
        extent = g.extent
        return '<img src="http://vmap0.tiles.osgeo.org/wms/vmap0?LAYERS=basic&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image/jpeg&SRS=EPSG:4326&BBOX=%s,%s,%s,%s&WIDTH=160&HEIGHT=160" width="160" height="160"/>' % extent

    @property
    def domain(self):
        """
        TODO determine IP dynamically?
        """
        return "%s:%d" % (self.ip, 8080)

    @property
    def port(self):
        # TODO
        return 8080

    @property
    def connection(self):
        '''
        Assumes db has already been created, postgis installed, user set up with local trust, etc
        '''
        return "dbname='example' user='madrona'"

    @property
    def public_kml(self):
        #TODO self.kmls
        return "<kml></kml>"
    
    def command_html(self):
        create = '<pre>'+self.create_command()+'</pre>'
        db = '<pre>'+self.db_command()+'</pre>'
        serv = '<pre>'+self.serv_command()+'</pre>'
        return db + create + serv

    def db_command(self):
        return "createdb %s -U madrona" % self.app  # TODO slug

    def serv_command(self):
        return "python /usr/local/apps/%s/%s/manage.py runserver 0.0.0.0:%s" % (self.app, self.app, self.port)  # TODO slug

    def create_command(self):
        feature_cmds = ["--%s '%s' " % (f.ftype, f.fname) for f in self.features.all()]
        feature_cmd = ' '.join(feature_cmds)
        kml_cmds = ["--kml '%s|%s' " % (k.fname, k.furl) for k in self.kmls.all()]
        kml_cmd = ' '.join(kml_cmds)
        cmd = """create-madrona-project.py 
            --project '%(project)s' 
            --app '%(app)s' 
            --domain '%(domain)s' 
            --connection "%(connection)s" 
            --studyregion '%(wkt)s' 
            %(kmls)s 
            %(features)s
        """  % {'project': self.project,
                'app': self.app,
                'domain': self.domain,
                'connection': self.connection,
                'wkt': self.studyregion.ewkt,
                'kmls': kml_cmd,
                'features': feature_cmd}

        return cmd


class UserFeature(models.Model):
    def __unicode__(self):
        return u'%s' % self.fname 

    TYPES = (
        ('aoi', 'Polygon/Area'),
        ('loi', 'Line'),
        ('poi', 'Point'),
        ('fld', 'Folder/Collection'),
    )
    fname = models.CharField(verbose_name="Feature Name", max_length=35)
    ftype = models.CharField(max_length=3, verbose_name="Feature Type", choices=TYPES)

class BaseKml(models.Model):
    "TODO Need fixture"
    def __unicode__(self):
        return u'%s' % self.fname 

    fname = models.CharField(verbose_name="KML Name", max_length=65)
    fdesc = models.TextField(verbose_name="Description")
    furl = models.URLField(verbose_name="URL")
