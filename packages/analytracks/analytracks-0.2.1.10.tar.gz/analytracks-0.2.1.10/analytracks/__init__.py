__all__ = ['track', 'parsers','elevation','hr','processing']

from .track import Track
print('importing tracks')

def parse(filepath,platform='unknown',athlete='unknown',activityId='unknown'):
    return Track(filepath,platform,athlete,activityId)
    
  