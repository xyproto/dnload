import re
from dnload.common import is_verbose

########################################
# GlslType #############################
########################################

class GlslName:
  """GLSL name identifier."""

  def __init__(self, source):
    """Constructor."""
    self.__name = source
    self.__rename = None
    # Reserved words are considered locked in all cases.
    if self.__name in get_list_locked():
      self.__rename = self.__name

  def format(self):
    """Return formatted output."""
    if not self.__rename:
      if is_verbose():
        print("WARNING: %s not locked" % (self))
      return self.__name
    return self.__rename

  def getName(self):
    """Gets the original, non-renamed name."""
    return self.__name

  def isLocked(self):
    """Tell if this is using a locked string."""
    if self.__rename:
      return True
    return False

  def __str__(self):
    """String representation."""
    return "GlslName('%s')" % (self.__name)

########################################
# Globals ##############################
########################################

g_locked = ("cross",
    "discard",
    "dot",
    "EmitVertex",
    "EndPrimitive",
    "gl_FragCoord",
    "gl_FragColor",
    "gl_PerVertex",
    "gl_Position",
    "layout",
    "length",
    "location",
    "main",
    "max_vertices",
    "mix",
    "normalize",
    "return",
    "uniform")

g_primitives = ("lines",
    "lines_adjacency",
    "points",
    "triangles",
    "triangle_strip")

########################################
# Functions ############################
########################################

def get_list_locked():
  """Get list of all locked words."""
  return g_locked + g_primitives

def get_list_primitives():
  """Get list of primitive words."""
  return g_primitives

def interpret_name(source):
  """Try to interpret name identifier."""
  # All reserved strings other than names here should have been interpreted before.
  # Names are interpreted last.
  if re.match(r'^([A-Za-z][A-Za-z0-9_]*)$', source, re.I):
    return GlslName(source)
  return None

def is_glsl_name(op):
  """Tell if token is type identifier."""
  return isinstance(op, GlslName)