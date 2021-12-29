# -*- coding: utf-8 -*-

import logging
import re

logger = logging.getLogger(__name__)


assert "internal/constants.py" in __file__

instance_path = re.sub(r"internal/constants.py$", "", __file__)

logger.debug("instance path is %s" % instance_path)
