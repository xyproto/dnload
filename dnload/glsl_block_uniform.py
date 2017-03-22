from dnload.glsl_block import GlslBlock
from dnload.glsl_block import extract_tokens
from dnload.glsl_block_layout import glsl_parse_layout

########################################
# GlslBlockUniform #####################
########################################
 
class GlslBlockUniform(GlslBlock):
  """Uniform declaration."""

  def __init__(self, layout, typeid, size, name):
    """Constructor."""
    GlslBlock.__init__(self)
    self.__layout = layout
    self.__typeid = typeid
    self.__size = size
    self.__name = name

  def format(self):
    """Return formatted output."""
    ret = ""
    if self.__layout:
      ret += self.__layout.format()
    ret += "uniform " + self.__typeid.format()
    if self.__size:
      ret += "[%s]" % (self.__size.format())
    return ret + " " + self.__name.format() + ";"

  def __str__(self):
    """String representation."""
    return "Uniform('%s')" % (self.__name.getName())

########################################
# Functions ############################
########################################

def glsl_parse_uniform(source):
  """Parse preprocessor block."""
  (layout, content) = glsl_parse_layout(source)
  if not layout:
    content = source
  # Extract actual uniform definition.
  (typeid, content) = extract_tokens(content, ("uniform", "?t"))
  if not typeid:
    return (None, source)
  # Try array types.
  (name, size, content) = extract_tokens(content, ("?n", "[", "?u", "]", ";"))
  if name and size:
    return (GlslBlockUniform(layout, typeid, size, name), content)
  (size, name, content) = extract_tokens(content, ("[", "?u", "]", "?n", ";"))
  if size and name:
    return (GlslBlockUniform(layout, typeid, size, name), content)
  # No array types, default to just name.
  (name, content) = extract_tokens(content, ("?n", ";"))
  if not name:
    return (None, source)
  return (GlslBlockUniform(layout, typeid, size, name), content)