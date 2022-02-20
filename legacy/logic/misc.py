import re

identity = lambda s: s
remove_separators = lambda s: "".join(re.split("\.|\/|-", s))
