##
# This file is used for zappa runner as zappa does not handle
# flask app factories well.
# See more about this issue: https://github.com/Miserlou/Zappa/issues/1771
#

from app import create_app

app = create_app()
