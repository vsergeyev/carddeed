import sys
import os
import cherrypy

from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler

os.environ["DJANGO_SETTINGS_MODULE"] = "carddeed.settings"

class DjangoApp(object):
    django_conf = { 
        '/carddeed/appmedia' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.root' : os.path.abspath(os.path.join(os.path.dirname(__file__),'carddeed','deed')),
            'tools.staticdir.dir' : 'appmedia',
        }
    }


if __name__ == '__main__':
    sys.path.insert(0,"..")
    conf = os.path.join(os.path.dirname(__file__), 'pieserver.conf')
    cherrypy.config.update(conf)
    cherrypy.tree.graft(AdminMediaHandler(WSGIHandler()), '/')
    cherrypy.server.quickstart()
    cherrypy.engine.start()