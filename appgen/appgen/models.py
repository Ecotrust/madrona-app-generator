from django.contrib.gis.db import models
import os
from madrona.common.utils import cachemethod
from django.conf import settings

def get_ip():
    # from http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('ecotrust.org', 0))
    return s.getsockname()[0]

class AppConfig(models.Model):
    app = models.CharField(verbose_name="App name", max_length=35, unique=True)
    desc = models.TextField(verbose_name="Description")
    studyregion = models.PolygonField()
    features = models.ManyToManyField('UserFeature')
    kmls = models.ManyToManyField('BaseKml')
    objects = models.GeoManager()

    class Meta:
        verbose_name = "Madrona App"
        verbose_name_plural = "Madrona Apps"

    def __unicode__(self):
        return self.app

    @property
    def project(self):
        return "%s_project" % self.appslug

    @property
    def data_list(self):
        kmls = ' '.join(['<li>'+k.fname+'</li>' for k in self.kmls.all()])
        features = ' '.join(['<li>'+f.fname+'</li>' for f in self.features.all()])
        return '<strong>Features</strong><ul>%s</ul><strong>KMLs</strong><ul>%s</ul>' % (features, kmls)

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
            <p><a href="/delete/%d/" class="deletelink"> Delete </a></p>
            <p><a href="http://ecotrust.github.com/madrona/docs/tutorial.html" target="_blank" class="changelink"> Customize </a></p>
        </div>
        """ % (self.pk)

        """
         WE DONT PROVIDE AN EDIT LINK !
         because the code is generated once, its a one shot deal
            <li><a href="/admin/appgen/appconfig/%d/" class="changelink"> Edit </a></li>
        """

    @property
    def running(self):
        dest_dir = os.path.join(settings.USERAPP_DIR, self.project)
        # check that dest_dir is symlinked to ACTIVEAPP_DIR
        if os.path.realpath(dest_dir) == os.path.realpath(settings.ACTIVEAPP_DIR): 
            return True

        return False

    @property
    def initialized(self):
        # Test for dir
        dest_dir = os.path.join(settings.USERAPP_DIR, self.project)
        if not os.path.exists(dest_dir):
            print dest_dir + " does not exist!"
            return False

        # Test for DB
        import psycopg2
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            cursor.execute("SELECT PostGIS_Version();")
            records = cursor.fetchone()
        except:
            print "Database does not exist: ", self.connection
            return False

        # All good
        return True

    def cleanup(self):
        # drop db, remove code dir
        from appgen.views import _call
        cmd = self.db_command()
        cmd = cmd.replace('createdb','dropdb')
        out, code = _call(cmd)

        # rm code dir
        dest_dir = os.path.join(settings.USERAPP_DIR, self.project)
        import shutil
        shutil.rmtree(dest_dir)
        return False

    @property
    def status(self):
        init = self.initialized
        running = self.running

        msg = "Unknown status"

        if running and init:
            msg = """
            <div>
            <p>Status: <br/> <strong>Active</strong> </p>
            </div>
            <br/><br/>
            <p><a href="http://%s" class="golink" target="_blank"> Go to App </a></p>
            """ % self.domain
        elif init and not running:
            msg = """
            <div>
            <p>Status: <br/> Initialized but not active </p>
            </div>
            <br/><br/>
            <ul class="object-tools">
                <li><a href="/activate/%d/" class="tablelink"> Activate </a></li>
            </ul>
            """ % self.pk
        elif not init and not running:
            msg = """
            <div>
            <p>Status: <br/> Not initialized </p>
            </div>
            <br/><br/>
            <ul class="object-tools">
                <li><a href="/initialize/%d/" class="tablelink"> Initialize </a></li>
            </ul>
            """ % self.pk

        return msg

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
        port = settings.ACTIVEAPP_PORT
        if port == 80:
            return "%s" % (settings.ACTIVEAPP_DOMAIN)
        else:
            return "%s:%d" % (settings.ACTIVEAPP_DOMAIN, port)

    @property
    def connection(self):
        '''
        Assumes db has already been created, postgis installed, user set up with local trust, etc
        '''
        return "dbname='%s' user='%s'" % (self.appslug, self.dbuser)

    @property
    def public_kml(self):
        #TODO self.kmls
        return "<kml></kml>"
    
    def command_html(self):
        create = '<pre>'+self.create_command()+'</pre>'
        db = '<pre>'+self.db_command()+'</pre>'
        return db + create

    @property
    def appslug(self):
        from django.template.defaultfilters import slugify
        s = slugify(self.app)
        return s.replace('-','_')

    @property
    def dbuser(self):
        return 'madrona'

    def db_command(self):
        return "createdb %s -U %s" % (self.appslug, self.dbuser)

    def create_command(self):
        feature_cmds = ["--%s '%s' " % (f.ftype, f.fname) for f in self.features.all()]
        feature_cmd = ' '.join(feature_cmds)
        kml_cmds = ["--kml '%s|%s' " % (k.fname, k.furl) for k in self.kmls.all()]
        kml_cmd = ' '.join(kml_cmds)
        cmd = """create-madrona-project.py \
            --outdir '%(outdir)s' \
            --project '%(project)s' \
            --app '%(app)s' \
            --domain '%(domain)s' \
            --connection "%(connection)s"  \
            --studyregion '%(wkt)s' \
            %(kmls)s \
            %(features)s \
            --superuser
        """  % {'outdir': os.path.join(settings.USERAPP_DIR, self.project),
                'project': self.project,
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

