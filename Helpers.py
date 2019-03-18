def route(func):
    def wrapper(*args):
        args[0].app.route(func, args[1], methods=[args[2]])

    return wrapper

# def errorhandler(func):
#     def wrapper(app, path, method):
#         app.route(func, path, methods=[method])
#     return wrapper
#
#     @flaskApp.errorhandler(404)
#     def page_not_found(self, e):
#         return "<h1>404</h1><p>The resource could not be found.</p>", 404
