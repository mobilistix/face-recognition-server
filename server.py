import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from PIL import Image
import time
# 
# from http://stackoverflow.com/questions/11914472/stringio-in-python3
# in Python3 StringIO replaced with io (but not completely compatibile)
#import StringIO
from io import StringIO
from io import BytesIO
import uuid
import numpy
import json
from tornado.options import define, options
import opencv


#
# Python 3 changes
# http://stackoverflow.com/questions/826948/syntax-error-on-print-with-python-3
# http://stackoverflow.com/questions/2535760/python-try-except-comma-vs-as-in-except
# http://answers.opencv.org/question/56859/opencv-300-facerecognizer-and-python-bindings/
#

define("port", default=8888, help="run on the given poort", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
        #(r"/", MainHandler),
        #(r"/facedetector", FaceDetectHandler),
        (r"/", SetupHarvestHandler),
        (r"/harvesting", HarvestHandler),
        (r"/predict", PredictHandler),
        (r"/train", TrainHandler)
        ]

    settings = dict(
        cookie_secret="asdsafl.rleknknfkjqweonrkbknoijsdfckjnk 234jn",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        autoescape=None,
        debug=True
        )
    tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("facedetect.html")

# bi-directional websocket
# http://tornado.readthedocs.org/en/latest/websocket.html
#
class SocketHandler(tornado.websocket.WebSocketHandler):

  def open(self):
    logging.info('new connection')

  def on_message(self, message):
    # this is to open a file with a string name, but the message is a frame of video
    #  image = Image.open(StringIO.StringIO(message))
    #  in python 3, need to explicitly convert from bytes to String
    print("received: ",len(message))

    im = Image.open(BytesIO(message))
    print('format: ', im.format, ', mode: ', im.mode, ', size: ', im.size, ', width: ', im.width, ', height: ', im.height)
    ## file_ = open('/tmp/test.jpg','wb')
    ## file_.write(message)
    ## file_.close()
    ## decoder = "jpeg"
    ## mode = "RGB"
    ## im_size = 320, 240
    ## image = Image.frombytes(mode, im_size, message, decoder, None)
    # image = Image.open(StringIO(message.decode()))
    cv_image = numpy.array(im)
    self.process(cv_image)

  def on_close(self):
    logging.info('connection closed')

  def process(self, cv_image):
    pass

class FaceDetectHandler(SocketHandler):

  def process(self, cv_image):
    faces = opencv.detect_faces(cv_image)
    if len(faces) > 0:
      result = json.dumps(faces.tolist())
      self.write_message(result)

class SetupHarvestHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("harvest.html")

  def post(self):
    name = self.get_argument("label", None)
    if not name:
      logging.error("No label, bailing out")
      return
    logging.info("Got label %s" %  name)
    opencv.Label.get_or_create(name=name)[0].persist()
    logging.info("Setting secure cookie %s" % name)
    self.set_secure_cookie('label', name)
    self.redirect("/")

class HarvestHandler(SocketHandler):
  def process(self, cv_image):
    label = opencv.Label.get(opencv.Label.name == self.get_secure_cookie('label'))
    logging.info("Got label: %s" % label.name)
    if not label:
      logging.info("No cookie, bailing out")
      return
    logging.info("About to save image")
    result = opencv.Image(label=label).persist(cv_image)
    if result == 'Done':
      self.write_message(json.dumps(result))

class TrainHandler(tornado.web.RequestHandler):
  def post(self):
    opencv.train()

class PredictHandler(SocketHandler):
  def process(self, cv_image):
    result = opencv.predict(cv_image)
    if result: 
      self.write_message(json.dumps(result))

def main():
  tornado.options.parse_command_line()
  opencv.Image().delete()
  logging.info("Images deleted")
  opencv.Label().delete()
  logging.info("Labels deleted")
  opencv.load_images_to_db("data/images")
  logging.info("Labels and images loaded")
  opencv.train()
  logging.info("Model trained")
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
