import sys
sys.path.append("..")
from jardb.errors import *


try:
    raise DbBaseException
except Exception as e:
    pass

try:
    raise DbFilePathError
except Exception as e:
    pass

try:
    raise DbBuildError
except Exception as e:
    pass

try:
    raise DbIOException
except Exception as e:
    pass

try:
    raise DbDecodeException
except Exception as e:
    pass

try:
    raise DbEncodeException
except Exception as e:
    pass

try:
    raise DbFilterException
except Exception as e:
    pass

try:
    raise DbInsertException
except Exception as e:
    pass

try:
    raise DbInsertNotNullExcption
except Exception as e:
    pass

try:
    raise DbInsertUniqueExcption
except Exception as e:
    pass
