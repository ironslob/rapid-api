# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level = logging.DEBUG)

from {{ config.backend.package }}.app.instance import app

if __name__ == "__main__":
    app.run(debug=True)
