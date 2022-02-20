import re

identity = lambda _, s: s
remove_separators = lambda _, s: "".join(re.split("\.|\/|-", s))
