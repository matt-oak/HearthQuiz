from  tornado.escape import json_decode
from sqlalchemy import create_engine
import pandas as pd
import tornado.ioloop
import tornado.web
import psycopg2
import unirest
import random

#Handler for homepage
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./html/homepage.html")

#Handler for Classic-game page
class ClassicHandler(tornado.web.RequestHandler):
  def get(self):
        self.render("./html/classic.html")

class PlayClassicHandler(tornado.web.RequestHandler):
    def get(self):
        engine = create_engine("postgresql://test:pass@localhost:5432/hearthquiz")
        query = "SELECT * FROM classic"
        dataframe = pd.read_sql_query(query, con = engine)
        rand_entry = random.randint(0, len(dataframe.index))
        answer = dataframe.loc[rand_entry]
        dic = answer.to_dict()
        dic.pop("index")
        dic.pop("id")
        print dic
        self.write(dic)

def make_app():
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/classic", ClassicHandler),
        (r"/play-classic", PlayClassicHandler),
        (r"/js/(.*)",tornado.web.StaticFileHandler, {"path": "./static/js"},),
        (r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "./static/css"},),
        (r"/img/(.*)",tornado.web.StaticFileHandler, {"path": "./static/img"},),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
