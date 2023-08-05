# -*- encoding: utf8 -*-
# © Toons
__version__ = "1.3"

import os
import imp
import sys
import logging
import requests

__PY3__ = True if sys.version_info[0] >= 3 else False
__FROZEN__ = hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")

# ROOT is the folder containing the __inti__.py file or the frozen executable
ROOT = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if __FROZEN__ else __file__)))
if __FROZEN__:
	# if frozen code, HOME adn ROOT pathes are same
	HOME = ROOT
else:
	try:
		HOME = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])
	except:
		HOME = os.environ.get("HOME", ROOT)

# configure logging
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.basicConfig(
	filename  = os.path.normpath(
		os.path.join(ROOT, __name__+".log")) if __FROZEN__ else \
		os.path.normpath(os.path.join(HOME, "."+__name__)
	),
	format = '[None][%(asctime)s] %(message)s',
	level = logging.INFO,
)
