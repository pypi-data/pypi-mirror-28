"""
fn-aware functions from the builtin operator module.
"""
import operator as _
from .fn import fn

abs = fn(_.abs)
add = fn(_.add)
and_ = fn(_.and_)
attrgetter = fn(_.attrgetter)
concat = fn(_.concat)
contains = fn(_.contains)
countOf = fn(_.countOf)
delitem = fn(_.delitem)
eq = fn(_.eq)
floordiv = fn(_.floordiv)
ge = fn(_.ge)
getitem = fn(_.getitem)
gt = fn(_.gt)
iadd = fn(_.iadd)
iand = fn(_.iand)
iconcat = fn(_.iconcat)
ifloordiv = fn(_.ifloordiv)
ilshift = fn(_.ilshift)
imod = fn(_.imod)
imul = fn(_.imul)
index = fn(_.index)
indexOf = fn(_.indexOf)
inv = fn(_.inv)
invert = fn(_.invert)
ior = fn(_.ior)
ipow = fn(_.ipow)
irshift = fn(_.irshift)
is_ = fn(_.is_)
is_not = fn(_.is_not)
isub = fn(_.isub)
itemgetter = fn(_.itemgetter)
itruediv = fn(_.itruediv)
ixor = fn(_.ixor)
le = fn(_.le)
lshift = fn(_.lshift)
lt = fn(_.lt)
methodcaller = fn(_.methodcaller)
mod = fn(_.mod)
mul = fn(_.mul)
ne = fn(_.ne)
neg = fn(_.neg)
not_ = fn(_.not_)
or_ = fn(_.or_)
pos = fn(_.pos)
pow = fn(_.pow)
rshift = fn(_.rshift)
setitem = fn(_.setitem)
sub = fn(_.sub)
truediv = fn(_.truediv)
truth = fn(_.truth)
xor = fn(_.xor)

# Methods for Python 3.5+
if hasattr(_, 'matmul'):
    matmul = fn(_.matmul)
    imatmul = fn(_.imatmul)

if hasattr(_, 'length_hint'):
    length_hint = fn(_.length_hint)

del fn
