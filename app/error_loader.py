from flask import (
    Flask,
    request,
    jsonify,
    current_app,
    render_template
)
from flask_wtf.csrf import CSRFError

def load_error(app: Flask) -> None:
    @app.errorhandler(CSRFError)
    def csrf_error(e):
        current_app.logger.error(msg="Request Header does not contain CSRF Token or has invalid CSRF Token", exc_info=1)
        if request.path.startswith("/api/"):
            return jsonify({"status": e.name, "code": e.code, "msg":"Refresh the page and try again."}), e.code
        return render_template("error/csrf_error.html"), 400
    
    @app.errorhandler(400)
    def bad_request(e):
        current_app.logger.error(msg=e.description[1], exc_info=1)
        if request.path.startswith("/api/"):
            return jsonify({"status": e.name, "code": e.code, "msg":e.description[0]}), e.code
        return render_template("error/bad_request.html"), 400
    
    @app.errorhandler(404)
    def not_found(e):
        current_app.logger.error(msg=e.description[1], exc_info=1)
        if request.path.startswith("/api/"):
            return jsonify({"status": e.name, "code": e.code, "msg":e.description[0]}), e.code
        return render_template("error/not_found.html"), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        current_app.logger.error(msg=e.description[1], exc_info=1)
        if request.path.startswith("/api/"):
            return jsonify({"status": e.name, "code": e.code, "msg":e.description[0]}), e.code
        return render_template("error/method_not_allowed.html"), 405
    

    @app.errorhandler(429)
    def too_many_requests(e):
        current_app.logger.error(msg=e.description[1], exc_info=1)
        if request.path.startswith("/api/"):
            return jsonify({"status": e.name, "code": e.code, "msg":e.description[0]}), e.code
        return render_template("error/too_many_requests.html"), 405
    
    @app.errorhandler(500)
    def server_error(e):
        current_app.logger.error(msg=e.description[1], exc_info=1)
        if request.path.startswith("/api/"):
            return jsonify({"status": e.name, "code": e.code, "msg":e.description[0]}), e.code
        return render_template("error/server_error.html"), 500