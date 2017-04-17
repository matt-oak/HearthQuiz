import tornado.ioloop
import tornado.web
from  tornado.escape import json_decode

#Handler for main (index) page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #URL to main (index) page
        self.render("./html/homepage.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/js/(.*)",tornado.web.StaticFileHandler, {"path": "./static/js"},),
        (r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "./static/css"},),
        (r"/img/(.*)",tornado.web.StaticFileHandler, {"path": "./static/img"},),
        #(r"/dropdown-fill/(.*)", DropdownFillHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
