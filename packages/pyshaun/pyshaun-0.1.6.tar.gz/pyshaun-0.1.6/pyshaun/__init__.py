__version__ = '0.1.6'
__all__ = [ 'load', 'load_file', 'dump', 'Numeric' ]

from .decoder import SHAUNDecoder
from .prettyprinter import SHAUNPP
from .numeric import Numeric

def load_file(fp, **kwargs):
    try:
        if isinstance(fp, str):
            return load(open(fp, 'r').read(), **kwargs)
        else:
            return load(fp.read(), **kwargs)
    except:
        return {}

def load(s, **kwargs):
    dec = SHAUNDecoder(s, **kwargs)
    return dec.decode()

def dump(sn):
    return SHAUNPP(sn).dump()
