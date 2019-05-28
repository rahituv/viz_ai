from best_most_common_finder import BestImageOfMostCommonFaceFinder
from azure_api_utils import my_keys

import tornado.ioloop
import tornado.web
import tornado.gen
import json
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

APP_PORT = 8080

settings = {}


class BestMostCommonFaceHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=24)
    image_name_list_key = "image_name_list"
    _best_most_common_face_finder = BestImageOfMostCommonFaceFinder(image_folder="images", azure_key=my_keys[0])

    @tornado.gen.coroutine
    def post(self):
        body_json = json.loads(self.request.body)
        if self.image_name_list_key not in body_json:
            self.set_status(400, "BadArgument")
            return
        yield self._respond_in_background(body_json[self.image_name_list_key])
        return

    @run_on_executor
    def _respond_in_background(self, image_name_list):

        try:
            self.write(self._best_most_common_face_finder.get_best_image_of_most_common_face(
                image_name_list=image_name_list))
        except:
            pass

def make_app():
    return tornado.web.Application([
        (r"/best_most_common_face", BestMostCommonFaceHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(APP_PORT)
    print "Starting server on: ", APP_PORT
    tornado.ioloop.IOLoop.current().start()
