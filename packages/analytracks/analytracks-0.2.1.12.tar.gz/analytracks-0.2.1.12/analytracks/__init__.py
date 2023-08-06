__all__ = ['track', 'parsers','elevation','hr','processing']

from .track import Track
print('importing tracks')

def parse(filepath,platform='unknown',athlete='unknown',activityId='unknown'):
    return Track(filepath,platform,athlete,activityId)
    

import os
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "data", "googleElevationApi.key")
if os.path.isfile(DATA_PATH): 
    print(open(DATA_PATH).read())
else: 
    print('no file')
