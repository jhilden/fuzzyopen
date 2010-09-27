"""
    Class for suggestions
"""

import os
from util import debug

excluded_file_types = ["jpg", "jpeg", "gif", "png", "tif", "psd", "pyc"]

class FuzzySuggestion:
  def __init__( self, filepath, hidden=True ):
    self._fileset = []
    for dirname, dirnames, filenames in os.walk( filepath ):
      if hidden:
        for d in dirnames[:]:
          if d[0] == '.':
            dirnames.remove(d)
      path = os.path.relpath( dirname, filepath )
      for filename in filenames:
        if (not hidden or filename[0] != '.'):
          if os.path.splitext( filename )[-1][1:] not in excluded_file_types:
            self._fileset.append( os.path.join( path, filename ) )
    self._fileset = sorted( self._fileset )
    debug("Loaded files count = %d" % len(self._fileset))

  def suggest( self, sub ):
    suggestion = []
    for f in self._fileset:
      highlight, score = self._match_score( sub, f )
      if score >= len(sub):
        suggestion.append((highlight, f, score))
    suggestion = sorted(suggestion, key=lambda x: x[2], reverse=True)
    debug("Suggestion count = %d" % len(suggestion))
    return [ (s[0], s[1]) for s in suggestion ]

  def _match_score( self, sub, str ):
    result = 0
    score = 0
    pos = 0
    original_length = len(str)
    highlight = ''
    for c in sub:
      while str != '' and str[0] != c:
        score = 0
        highlight += str[0]
        str = str[1:]
      if str == '':
        return (highlight, 0)
      score += 1
      result += score
      pos += len(str)
      str = str[1:]
      highlight += "<b>" + c + "</b>"
    highlight += str
    if len(sub) != 0 and original_length > 1:
      pos = float(pos-1) / ((float(original_length)-1.0) * float(len(sub)))
    else:
      pos = 0.0
    return (highlight, float(result) + pos)

