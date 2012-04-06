from django.contrib.gis.db import models

class AppConfig(models.Model):
    app = models.CharField(verbose_name="App name", max_length=35)
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
        return ', '.join([f.fname for f in self.features.all()])

    @property
    def extent(self):
        return self.studyregion.extent

    @property
    def wms(self): 
        area = self.studyregion.area
        w = area ** 0.5
        w = w/2
        g = self.studyregion.buffer(w)
        extent = g.extent
        return 'http://vmap0.tiles.osgeo.org/wms/vmap0?LAYERS=basic&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image/jpeg&SRS=EPSG:4326&BBOX=%s,%s,%s,%s&WIDTH=256&HEIGHT=256' % extent

    @property
    def domain(self):
        """
        TODO determine IP dynamically?
        """
        return "%s:%d" % (self.ip, 8080)

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
    
    def get_command(self):
        feature_cmds = ["--%s '%s' " % (f.ftype, f.fname) for f in self.features.all()]
        feature_cmd = ' '.join(feature_cmds)
        kml_cmds = ["--kml '%s|%s' " % (k.fname, k.furl) for k in self.kmls.all()]
        kml_cmd = ' '.join(kml_cmds)
        cmd = """create-madrona-project.py \
            --project '%(project)s' \
            --app '%(app)s' \
            --domain '%(domain)s' \
            --connection "%(connection)s" \
            --studyregion '%(wkt)s' \
            --kml '%(kmls)s' \
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
