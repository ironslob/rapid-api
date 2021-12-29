# -*- coding: utf-8 -*-

from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime


def init(app):
    @app.after_request
    def nocache(response):
        if (
            "Last-Modified" not in response.headers
            and "Cache-Control" not in response.headers
        ):
            response.headers["Last-Modified"] = format_date_time(
                mktime(datetime.utcnow().timetuple())
            )
            response.headers[
                "Cache-Control"
            ] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "-1"

        return response
