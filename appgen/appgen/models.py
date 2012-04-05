from django.contrib.gis.db import models

class AppConfig(models.Model):
    app = models.CharField(verbose_name="App name", max_length=35)
    studyregion = models.PolygonField()
    features = models.ManyToManyField('UserFeature')
    kmls = models.ManyToManyField('BaseKml')
    ip = models.IPAddressField()
    objects = models.GeoManager()

    @property
    def project(self):
        return "exampleproject"

    @property
    def domain(self):
        """
        TODO determine IP dynamically?
        """
        return "%s:%d" % (self.ip, 8080)

    @property
    def connection(self):
        '''
        Assumes db has already been created, postgis installed, 
        user set up with local trust, etc
        '''
        return "dbname='example' user='madrona'"

    @property
    def public_kml(self):
        #TODO self.kmls
        return "<kml></kml>"
    
    def write_public_kml(self):
        """
        TODO write to filesystem (mediaroot?) and return path
        """
        kml = self.public_kml
        return "/tmp/public.kml"

    def command(self):
        cmd = """create-madrona-project.py \
            --project %(project) \
            --app %(app) \
            --domain %(domain) \
            --connection %(connection) \
            --studyregion %(wkt) \
            --kml %(public_kml_path) \
            %(features) 
        """  % {'project': self.project,
                'app': self.app,
                'domain': self.domain,
                'connection': self.connection,
                'wkt': self.studyregion.wkt,
                'public_kml_path': self.write_public_kml(),
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
