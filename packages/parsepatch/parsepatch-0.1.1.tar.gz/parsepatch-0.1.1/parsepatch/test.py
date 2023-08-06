from .patch import Patch as patch
from pprint import pprint


r = patch.parse_file('/tmp/patch.diff', skip_comments=False)
pprint(r)
