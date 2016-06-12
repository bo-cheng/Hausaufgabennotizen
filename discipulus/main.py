import cherrypy
import os
import json

from jinja2 import Environment, FileSystemLoader

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'js'))

#env = Environment(loader = PackageLoader('discipulus', 'templates'))
env = Environment(loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class Hausaufgaben(object):
    def __init__(self):
        self.index_template = env.get_template('index.html')
        self.jquery_template = env.get_template('jquery-1.12.0.min.js')
    def jquery(self):
        return self.jquery_template.render()
    jquery.exposed = True
    def index(self):
        db_json = dict()
        with open('datenbank.json', 'r') as db:
            db_string = db.read()
            if db_string != "":
                db_json = json.loads(db_string)
        return self.index_template.render(db_json = db_json)
    index.exposed = True
    def add(self,hausaufgabe):
        with open('datenbank.json', 'r+') as db:
            db_string = db.read()
            print(db_string)
            if db_string == "":
                db_json = dict()
            else:
                db_json = json.loads(db_string)
            print(db_json)
            db_json[hausaufgabe] = False
            print(db_json)
            db.seek(0)
            db.truncate()
            db.write(json.dumps(db_json))
        raise cherrypy.HTTPRedirect("/")
    add.exposed = True
    def delete(self,hausaufgabe):
        with open('datenbank.json', 'r+') as db:
            db_string = db.read()
            print(db_string)
            if db_string == "":
                db_json = dict()
            else:
                db_json = json.loads(db_string)
            print(db_json)
            db_json.pop(hausaufgabe, None)
            print(db_json)
            db.seek(0)
            db.truncate()
            db.write(json.dumps(db_json))
    delete.exposed = True

cherrypy.config.update({'server.socket_port': 4594})
##conf = {
##    "/": {
##        'tools.staticdir.on': True,
##        'tools.staticdir.dir': '.',
##        'tools.staticdir.root': PATH
##    }
##}
cherrypy.quickstart(Hausaufgaben())
