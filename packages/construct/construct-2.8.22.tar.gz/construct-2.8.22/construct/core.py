# -*- coding: utf-8 -*-

import struct as packer
from struct import Struct as Packer
from struct import error as PackerError
from io import BytesIO, StringIO
from binascii import hexlify, unhexlify
import collections
import sys

from construct.lib import *
from construct.expr import *


#===============================================================================
# exceptions
#===============================================================================
class ConstructError(Exception):
    pass
class StreamError(ConstructError):
    pass
class FormatFieldError(ConstructError):
    pass
class SizeofError(ConstructError):
    pass
class AdaptationError(ConstructError):
    pass
class RangeError(ConstructError):
    pass
class SwitchError(ConstructError):
    pass
class SelectError(ConstructError):
    pass
class UnionError(ConstructError):
    pass
class TerminatedError(ConstructError):
    pass
class PaddingError(ConstructError):
    pass
class ConstError(ConstructError):
    pass
class StringError(ConstructError):
    pass
class ChecksumError(ConstructError):
    pass
class ValidationError(ConstructError):
    pass
class BitIntegerError(ConstructError):
    pass
class MappingError(ConstructError):
    pass
class ExplicitError(ConstructError):
    pass


#===============================================================================
# used internally
#===============================================================================
def singleton(arg):
    return arg()

def _read_stream(stream, length):
    if length < 0:
        raise StreamError("length must be >= 0", length)
    data = stream.read(length)
    if len(data) != length:
        raise StreamError("could not read enough bytes, expected %d, found %d" % (length, len(data)))
    return data

def _write_stream(stream, length, data):
    if length < 0:
        raise StreamError("length must be >= 0", length)
    if len(data) != length:
        raise StreamError("could not write bytes, expected %d, found %d" % (length, len(data)))
    written = stream.write(data)
    if written is not None and written != length:
        raise StreamError("could not write bytes, expected %d, written %d" % (length, written))


#===============================================================================
# abstract constructs
#===============================================================================
class Construct(object):
    r"""
    The mother of all constructs.

    This object is generally not directly instantiated, and it does not directly implement parsing and building, so it is largely only of interest to subclass implementors. There are also other abstract classes sitting on top of this one.

    The external user API:

     * ``parse()``
     * ``parse_stream()``
     * ``build()``
     * ``build_stream()``
     * ``sizeof()``

    Subclass authors should not override the external methods. Instead, another API is available:

     * ``_parse()``
     * ``_build()``
     * ``_sizeof()``

    And stateful copying:

     * ``__getstate__()``
     * ``__setstate__()``

    Attributes and Inheritance
    ==========================

    All constructs have a name and flags. The name is used for naming struct members and context dictionaries. Note that the name can be a string, or None by default. A single underscore "_" is a reserved name, used as up-level in nested containers. The name should be descriptive, short, and valid as a Python identifier, although these rules are not enforced. The flags specify additional behavioral information about this construct. Flags are used by enclosing constructs to determine a proper course of action. Flags are often inherited from inner subconstructs but that depends on each class behavior.
    """

    __slots__ = ["name", "flagbuildnone", "flagembedded"]
    def __init__(self):
        self.name = None
        self.flagbuildnone = False
        self.flagembedded = False

    def __repr__(self):
        return "<%s: %s%s%s>" % (self.__class__.__name__, self.name, " +nonbuild" if self.flagbuildnone else "", " +embedded" if self.flagembedded else "")

    def __getstate__(self):
        """Obtain a dictionary representing this construct's state."""
        attrs = {}
        if hasattr(self, "__dict__"):
            attrs.update(self.__dict__)
        slots = []
        c = self.__class__
        while c is not None:
            if hasattr(c, "__slots__"):
                slots.extend(c.__slots__)
            c = c.__base__
        for name in slots:
            if hasattr(self, name):
                attrs[name] = getattr(self, name)
        return attrs

    def __setstate__(self, attrs):
        """Set this construct's state to a given state."""
        for name, value in attrs.items():
            setattr(self, name, value)

    def __copy__(self):
        """Returns a copy of this construct."""
        self2 = object.__new__(self.__class__)
        self2.__setstate__(self, self.__getstate__())
        return self2

    def parse(self, data, context=None, **kw):
        """
        Parse an in-memory buffer (often bytes object).

        Strings, buffers, memoryviews, and other complete buffers can be parsed with this method.
        """
        return self.parse_stream(BytesIO(data), context, **kw)

    def parse_stream(self, stream, context=None, **kw):
        """
        Parse a stream.

        Files, pipes, sockets, and other streaming sources of data are handled by this method.
        """
        context2 = Container()
        if context is not None:
            context2.update(context)
        context2.update(kw)

        return self._parse(stream, context2, "(parsing)")

    def _parse(self, stream, context, path):
        """
        Override in your subclass.

        :returns: some value, usually based on bytes read from the stream but sometimes it is computed from nothing or from context
        """
        raise NotImplementedError

    def build(self, obj, context=None, **kw):
        """
        Build an object in memory.

        :returns: bytes
        """
        stream = BytesIO()
        self.build_stream(obj, stream, context, **kw)
        return stream.getvalue()

    def build_stream(self, obj, stream, context=None, **kw):
        """
        Build an object directly into a stream.

        :returns: None
        """
        context2 = Container()
        if context is not None:
            context2.update(context)
        context2.update(kw)

        self._build(obj, stream, context2, "(building)")

    def _build(self, obj, stream, context, path):
        """
        Override in your subclass.

        :returns: None or a new value to put into the context, few fields use this internal functionality
        """
        raise NotImplementedError

    def sizeof(self, context=None, **kw):
        """
        Calculate the size of this object, optionally using a context.

        Some constructs have no fixed size and can only know their size for a given hunk of data. These constructs will raise an error if they are not passed a context.

        :param context: a container

        :returns: an integer for a fixed size field
        :raises SizeofError: the size could not be determined, ever or just with actual context
        """
        if context is None:
            context = Container()
        context.update(kw)
        return self._sizeof(context, "(sizeof)")

    def _sizeof(self, context, path):
        """
        Override in your subclass.

        :returns: an integer for a fixed size field
        :raises SizeofError: the size could not be determined, ever or just with actual context
        """
        raise SizeofError

    def __rtruediv__(self, name):
        """
        Used for renaming subcons, usually part of a Struct, like "index" / Byte.
        """
        if name is not None:
            if not isinstance(name, stringtypes):
                raise TypeError("name must be b-string or u-string or None", name)
        return Renamed(name, self)

    __rdiv__ = __rtruediv__

    def __add__(self, other):
        """
        Used for making Struct like ("index"/Byte + "prefix"/Byte).
        """
        lhs = self.subcons  if isinstance(self,  Struct) else [self]
        rhs = other.subcons if isinstance(other, Struct) else [other]
        return Struct(*(lhs + rhs))

    def __rshift__(self, other):
        """
        Used for making Sequences like (Byte >> Short).
        """
        lhs = self.subcons  if isinstance(self,  Sequence) else [self]
        rhs = other.subcons if isinstance(other, Sequence) else [other]
        return Sequence(*(lhs + rhs))

    def __getitem__(self, count):
        """
        Used for making Ranges like Byte[5] or Byte[:].
        """
        if isinstance(count, slice):
            if count.step is not None:
                raise ValueError("slice must not contain a step: %r" % count)
            min = 0 if count.start is None else count.start
            max = 2**64 if count.stop is None else count.stop
            return Range(min, max, self)
        elif isinstance(count, int) or callable(count):
            return Range(count, count, self)
        else:
            raise TypeError("expected an int, a context lambda, or a slice thereof, but found %r" % count)


class Subconstruct(Construct):
    r"""
    Abstract subconstruct (wraps an inner construct, inheriting its name and flags). Parsing and building is by default deferred to subcon, same as sizeof.

    :param subcon: the construct to wrap
    """
    __slots__ = ["subcon"]
    def __init__(self, subcon):
        if not isinstance(subcon, Construct):
            raise TypeError("subcon should be a Construct field")
        super(Subconstruct, self).__init__()
        self.name = subcon.name
        self.subcon = subcon
        self.flagbuildnone = subcon.flagbuildnone
        self.flagembedded = subcon.flagembedded
    def _parse(self, stream, context, path):
        return self.subcon._parse(stream, context, path)
    def _build(self, obj, stream, context, path):
        return self.subcon._build(obj, stream, context, path)
    def _sizeof(self, context, path):
        return self.subcon._sizeof(context, path)


class Adapter(Subconstruct):
    r"""
    Abstract adapter parent class.

    Needs to implement ``_decode()`` for parsing and ``_encode()`` for building.

    :param subcon: the construct to wrap
    """
    def _parse(self, stream, context, path):
        return self._decode(self.subcon._parse(stream, context, path), context)
    def _build(self, obj, stream, context, path):
        return self.subcon._build(self._encode(obj, context), stream, context, path)
    def _decode(self, obj, context):
        raise NotImplementedError
    def _encode(self, obj, context):
        raise NotImplementedError


class SymmetricAdapter(Adapter):
    r"""
    Abstract adapter parent class.

    Needs to implement ``_decode()`` only, for both parsing and building.

    :param subcon: the construct to wrap
    """
    def _encode(self, obj, context):
        return self._decode(obj, context)


class Validator(SymmetricAdapter):
    r"""
    Abstract class that validates a condition on the encoded/decoded object.

    Needs to implement ``_validate()`` that returns a bool (or a truthy value)

    :param subcon: the subcon to validate
    """
    def _decode(self, obj, context):
        if not self._validate(obj, context):
            raise ValidationError("object failed validation: %s" % (obj,))
        return obj
    def _validate(self, obj, context):
        raise NotImplementedError


class Tunnel(Subconstruct):
    r"""
    Abstract class that reads entire stream when parsing, and writes all data when building, but serves as an adapter as well.

    Needs to implement ``_decode()`` for parsing and ``_encode()`` for building.
    """
    def _parse(self, stream, context, path):
        data = stream.read()  # reads entire stream
        data = self._decode(data, context)
        return self.subcon.parse(data, context)
    def _build(self, obj, stream, context, path):
        data = self.subcon.build(obj, context)
        data = self._encode(data, context)
        _write_stream(stream, len(data), data)
    def _sizeof(self, context, path):
        raise SizeofError
    def _decode(self, data, context):
        raise NotImplementedError
    def _encode(self, data, context):
        raise NotImplementedError


#===============================================================================
# bytes and bits
#===============================================================================
class Bytes(Construct):
    r"""
    Field consisting of a specified number of bytes. Builds from a bytes, or an integer (although deprecated and BytesInteger should be used instead).

    .. seealso:: Analog :func:`~construct.core.BytesInteger` that parses and builds from integers, as opposed to bytes.

    :param length: an integer or a context lambda that returns such an integer

    Example::

        >>> d = Bytes(4)
        >>> d.parse(b'beef')
        b'beef'
        >>> d.build(b'beef')
        b'beef'
        >>> d.build(0)
        b'\x00\x00\x00\x00'
        >>> d.sizeof()
        4
    """
    __slots__ = ["length"]
    def __init__(self, length):
        super(Bytes, self).__init__()
        self.length = length
    def _parse(self, stream, context, path):
        length = self.length(context) if callable(self.length) else self.length
        return _read_stream(stream, length)
    def _build(self, obj, stream, context, path):
        length = self.length(context) if callable(self.length) else self.length
        data = integer2bytes(obj, length) if isinstance(obj, int) else obj
        _write_stream(stream, length, data)
        return data
    def _sizeof(self, context, path):
        try:
            return self.length(context) if callable(self.length) else self.length
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


@singleton
class GreedyBytes(Construct):
    r"""
    Field that parses the stream to the end and builds into the stream as is.

    .. seealso:: Analog :func:`~construct.core.GreedyString` that parses and builds from strings using an encoding.

    Example::

        >>> GreedyBytes.parse(b"asislight")
        b'asislight'
        >>> GreedyBytes.build(b"asislight")
        b'asislight'
    """
    def _parse(self, stream, context, path):
        return stream.read()
    def _build(self, obj, stream, context, path):
        stream.write(obj)


def Bitwise(subcon):
    r"""
    Converts the stream from bytes to bits, and passes the bitstream to underlying subcon.

    .. seealso:: Analog :func:`~construct.core.Bytewise` that transforms bits back to bytes.

    .. warning:: Do not use pointers inside this or other restreamed contexts.

    :param subcon: any field that works with bits like BitStruct or Bit/Nibble/Octet or BitsInteger

    Example::

        >>> d = Bitwise(Octet)
        >>> d.parse(b"\xff")
        255
        >>> d.build(1)
        b'\x01'
        >>> d.sizeof()
        1
    """
    return Restreamed(subcon, bits2bytes, 8, bytes2bits, 1, lambda n: n//8)


def Bytewise(subcon):
    r"""
    Converts the stream from bits back to bytes. Must be used within Bitwise.

    :param subcon: any field that works with bytes

    Example::

        >>> d = Bitwise(Bytewise(Byte))
        >>> d.parse(b"\xff")
        255
        >>> d.build(255)
        b'\xff'
        >>> d.sizeof()
        1
    """
    return Restreamed(subcon, bytes2bits, 1, bits2bytes, 8, lambda n: n*8)


#===============================================================================
# integers and floats
#===============================================================================
class FormatField(Bytes):
    r"""
    Field that uses ``struct`` module to pack and unpack data. This is used to implement basic Int* and Float* fields, but cannot pack 24-bit integers for example, which is left to BytesInteger.

    See ``struct`` documentation for instructions on crafting format strings.

    :param endianity: endianness character like < > =
    :param format: format character like f d B H L Q b h l q

    Example::

        >>> d = FormatField(">", "H")
        >>> d.parse(b"\x01\x00")
        256
        >>> d.build(256)
        b"\x01\x00"
        >>> d.sizeof()
        2
    """
    __slots__ = ["fmtstr"]
    def __init__(self, endianity, format):
        if endianity not in list("=<>"):
            raise ValueError("endianity must be like: = < >", endianity)
        if format not in list("fdBHLQbhlq"):
            raise ValueError("format must be like: f d B H L Q b h l q", format)
        super(FormatField, self).__init__(packer.calcsize(endianity+format))
        self.fmtstr = endianity+format
    def _parse(self, stream, context, path):
        try:
            data = _read_stream(stream, self.sizeof())
            return packer.unpack(self.fmtstr, data)[0]
        except Exception:
            raise FormatFieldError("packer %r error during parsing" % self.fmtstr)
    def _build(self, obj, stream, context, path):
        try:
            data = packer.pack(self.fmtstr, obj)
            _write_stream(stream, self.sizeof(), data)
        except Exception:
            raise FormatFieldError("packer %r error during building, given value %r" % (self.fmtstr, obj))


class BytesInteger(Construct):
    r"""
    Field that builds from integers as opposed to bytes. Similar to Int* fields but can have arbitrary size.

    .. seealso:: Analog :func:`~construct.core.BitsInteger` that operates on bits.

    :param length: number of bytes in the field, and integer or a context function that returns such an integer
    :param signed: whether the value is signed (two's complement), default is False (unsigned)
    :param swapped: whether to swap byte order (little endian), default is False (big endian)

    Example::

        >>> d = BytesInteger(4) or Int32ub
        >>> d.parse(b"abcd")
        1633837924
        >>> d.build(1)
        b'\x00\x00\x00\x01'
        >>> d.sizeof()
        4
    """
    __slots__ = ["length", "signed", "swapped"]
    def __init__(self, length, signed=False, swapped=False):
        super(BytesInteger, self).__init__()
        self.length = length
        self.signed = signed
        self.swapped = swapped
    def _parse(self, stream, context, path):
        length = self.length(context) if callable(self.length) else self.length
        data = _read_stream(stream, length)
        if self.swapped:
            data = swapbytes(data, 1)
        return bytes2integer(data, self.signed)
    def _build(self, obj, stream, context, path):
        if obj < 0 and not self.signed:
            raise BitIntegerError("object is negative, but field is not signed", obj)
        length = self.length(context) if callable(self.length) else self.length
        data = integer2bytes(obj, length)
        if self.swapped:
            data = swapbytes(data, 1)
        _write_stream(stream, len(data), data)
    def _sizeof(self, context, path):
        try:
            return self.length(context) if callable(self.length) else self.length
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


class BitsInteger(Construct):
    r"""
    Field that builds from integers as opposed to bytes. Similar to Bit/Nibble/Octet fields but can have arbitrary sizes. Must be enclosed in Bitwise.

    :param length: number of bits in the field, an integer or a context function that returns such an integer
    :param signed: whether the value is signed (two's complement), default is False (unsigned)
    :param swapped: whether to swap byte order (little endian), default is False (big endian)

    Example::

        >>> d = Bitwise(BitsInteger(8))
        >>> d.parse(b"\x10")
        16
        >>> d.build(255)
        b'\xff'
        >>> d.sizeof()
        1
    """
    __slots__ = ["length", "signed", "swapped"]
    def __init__(self, length, signed=False, swapped=False):
        super(BitsInteger, self).__init__()
        self.length = length
        self.signed = signed
        self.swapped = swapped
    def _parse(self, stream, context, path):
        length = self.length(context) if callable(self.length) else self.length
        data = _read_stream(stream, length)
        if self.swapped:
            data = swapbytes(data, 8)
        return bits2integer(data, self.signed)
    def _build(self, obj, stream, context, path):
        if obj < 0 and not self.signed:
            raise BitIntegerError("object is negative, but field is not signed", obj)
        length = self.length(context) if callable(self.length) else self.length
        data = integer2bits(obj, length)
        if self.swapped:
            data = swapbytes(data, 8)
        _write_stream(stream, len(data), data)
    def _sizeof(self, context, path):
        try:
            return self.length(context) if callable(self.length) else self.length
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


@singleton
def Bit():
    """A 1-bit integer, must be enclosed in a Bitwise (eg. BitStruct)"""
    return BitsInteger(1)
@singleton
def Nibble():
    """A 4-bit integer, must be enclosed in a Bitwise (eg. BitStruct)"""
    return BitsInteger(4)
@singleton
def Octet():
    """A 8-bit integer, must be enclosed in a Bitwise (eg. BitStruct)"""
    return BitsInteger(8)

@singleton
def Int8ub():
    """Unsigned, big endian 8-bit integer"""
    return FormatField(">", "B")
@singleton
def Int16ub():
    """Unsigned, big endian 16-bit integer"""
    return FormatField(">", "H")
@singleton
def Int32ub():
    """Unsigned, big endian 32-bit integer"""
    return FormatField(">", "L")
@singleton
def Int64ub():
    """Unsigned, big endian 64-bit integer"""
    return FormatField(">", "Q")

@singleton
def Int8sb():
    """Signed, big endian 8-bit integer"""
    return FormatField(">", "b")
@singleton
def Int16sb():
    """Signed, big endian 16-bit integer"""
    return FormatField(">", "h")
@singleton
def Int32sb():
    """Signed, big endian 32-bit integer"""
    return FormatField(">", "l")
@singleton
def Int64sb():
    """Signed, big endian 64-bit integer"""
    return FormatField(">", "q")

@singleton
def Int8ul():
    """Unsigned, little endian 8-bit integer"""
    return FormatField("<", "B")
@singleton
def Int16ul():
    """Unsigned, little endian 16-bit integer"""
    return FormatField("<", "H")
@singleton
def Int32ul():
    """Unsigned, little endian 32-bit integer"""
    return FormatField("<", "L")
@singleton
def Int64ul():
    """Unsigned, little endian 64-bit integer"""
    return FormatField("<", "Q")

@singleton
def Int8sl():
    """Signed, little endian 8-bit integer"""
    return FormatField("<", "b")
@singleton
def Int16sl():
    """Signed, little endian 16-bit integer"""
    return FormatField("<", "h")
@singleton
def Int32sl():
    """Signed, little endian 32-bit integer"""
    return FormatField("<", "l")
@singleton
def Int64sl():
    """Signed, little endian 64-bit integer"""
    return FormatField("<", "q")

@singleton
def Int8un():
    """Unsigned, native endianity 8-bit integer"""
    return FormatField("=", "B")
@singleton
def Int16un():
    """Unsigned, native endianity 16-bit integer"""
    return FormatField("=", "H")
@singleton
def Int32un():
    """Unsigned, native endianity 32-bit integer"""
    return FormatField("=", "L")
@singleton
def Int64un():
    """Unsigned, native endianity 64-bit integer"""
    return FormatField("=", "Q")

@singleton
def Int8sn():
    """Signed, native endianity 8-bit integer"""
    return FormatField("=", "b")
@singleton
def Int16sn():
    """Signed, native endianity 16-bit integer"""
    return FormatField("=", "h")
@singleton
def Int32sn():
    """Signed, native endianity 32-bit integer"""
    return FormatField("=", "l")
@singleton
def Int64sn():
    """Signed, native endianity 64-bit integer"""
    return FormatField("=", "q")

Byte  = Int8ub
Short = Int16ub
Int   = Int32ub
Long  = Int64ub

@singleton
def Float32b():
    """Big endian, 32-bit IEEE floating point number"""
    return FormatField(">", "f")
@singleton
def Float32l():
    """Little endian, 32-bit IEEE floating point number"""
    return FormatField("<", "f")
@singleton
def Float32n():
    """Native endianity, 32-bit IEEE floating point number"""
    return FormatField("=", "f")

@singleton
def Float64b():
    """Big endian, 64-bit IEEE floating point number"""
    return FormatField(">", "d")
@singleton
def Float64l():
    """Little endian, 64-bit IEEE floating point number"""
    return FormatField("<", "d")
@singleton
def Float64n():
    """Native endianity, 64-bit IEEE floating point number"""
    return FormatField("=", "d")

Single = Float32b
Double = Float64b

native = (sys.byteorder == "little")

@singleton
def Int24ub():
    """A 3-byte big-endian unsigned integer, as used in ancient file formats."""
    return BytesInteger(3, signed=False, swapped=False)
@singleton
def Int24ul():
    """A 3-byte little-endian unsigned integer, as used in ancient file formats."""
    return BytesInteger(3, signed=False, swapped=True)
@singleton
def Int24un():
    """A 3-byte native-endian unsigned integer, as used in ancient file formats."""
    return BytesInteger(3, signed=False, swapped=native)
@singleton
def Int24sb():
    """A 3-byte big-endian signed integer, as used in ancient file formats."""
    return BytesInteger(3, signed=True, swapped=False)
@singleton
def Int24sl():
    """A 3-byte little-endian signed integer, as used in ancient file formats."""
    return BytesInteger(3, signed=True, swapped=True)
@singleton
def Int24sn():
    """A 3-byte native-endian signed integer, as used in ancient file formats."""
    return BytesInteger(3, signed=True, swapped=native)


@singleton
class VarInt(Construct):
    r"""
    Varint encoded integer. Each 7 bits of the number are encoded in one byte of the stream, where leftmost (MSB) bit is unset when byte is terminal.

    Can only encode non-negative numbers.

    Scheme defined at Google's site:
    https://developers.google.com/protocol-buffers/docs/encoding
    https://techoverflow.net/blog/2013/01/25/efficiently-encoding-variable-length-integers-in-cc/

    Example::

        >>> VarInt.build(16)
        b'\x10'
        >>> VarInt.build(2**100)
        b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x04'
    """
    def _parse(self, stream, context, path):
        acc = []
        while True:
            b = byte2int(_read_stream(stream, 1))
            acc.append(b & 0b01111111)
            if not b & 0b10000000:
                break
        num = 0
        for b in reversed(acc):
            num = (num << 7) | b
        return num
    def _build(self, obj, stream, context, path):
        if obj < 0:
            raise ValueError("varint cannot build from negative number: %r" % (obj,))
        while obj > 0b01111111:
            _write_stream(stream, 1, int2byte(0b10000000 | (obj & 0b01111111)))
            obj >>= 7
        _write_stream(stream, 1, int2byte(obj))


#===============================================================================
# structures and sequences
#===============================================================================
class Struct(Construct):
    r"""
    Sequence of usually named constructs, similar to structs in C. The elements are parsed and built in the order they are defined. If a member is anonymous (its name is None) then it gets parsed and its value discarded, or it gets build from nothing (from None).

    Some fields do not need to be named, since they are built without value anyway. See Const Padding Pass Terminated for examples of such fields.

    Size is the sum of all subcon sizes, unless any subcon raises SizeofError.

    Operator + can also be used to make Structs.

    .. seealso:: Can be nested easily, and embedded using :func:`~construct.core.Embedded` wrapper that merges members with parent's members.

    :param subcons: subcons that make up this structure, some can be anonymous

    Example::

        >>> d = Struct("a"/Int8ul, "data"/Bytes(2), "data2"/Bytes(this.a))
        >>> d.parse(b"\x01abc")
        Container(a=1)(data=b'ab')(data2=b'c')
        >>> d.build(_)
        b'\x01abc'
        >>> d.build(dict(a=5, data=b"??", data2=b"hello"))
        b'\x05??hello'

        >>> d = Struct(Const(b"MZ"), Padding(2), Pass, Terminated)
        >>> d.build({})
        b'MZ\x00\x00'
        >>> d.parse(_)
        Container()
        >>> d.sizeof()
        4

        Alternative syntax (not recommended):
        >>> ("a"/Byte + "b"/Byte + "c"/Byte + "d"/Byte)

        Alternative syntax, note this works ONLY on python 3.6+:
        >>> Struct(a=Byte, b=Byte, c=Byte, d=Byte)
    """
    __slots__ = ["subcons"]
    def __init__(self, *subcons, **kw):
        super(Struct, self).__init__()
        self.subcons = list(subcons) + list(k/v for k,v in kw.items()) 
    def _parse(self, stream, context, path):
        obj = Container()
        context = Container(_ = context)
        for sc in self.subcons:
            try:
                subobj = sc._parse(stream, context, path)
                if sc.flagembedded:
                    if subobj is not None:
                        obj.update(subobj)
                        context.update(subobj)
                else:
                    if sc.name is not None:
                        obj[sc.name] = subobj
                        context[sc.name] = subobj
            except StopIteration:
                break
        return obj
    def _build(self, obj, stream, context, path):
        context = Container(_ = context)
        context.update(obj)
        for sc in self.subcons:
            try:
                if sc.flagembedded:
                    subobj = obj
                elif sc.flagbuildnone:
                    subobj = obj.get(sc.name, None)
                else:
                    subobj = obj[sc.name]

                if sc.flagembedded:
                    context.update(subobj)
                if sc.name is not None:
                    context[sc.name] = subobj

                buildret = sc._build(subobj, stream, context, path)
                if buildret is not None:
                    if sc.flagembedded:
                        context.update(buildret)
                    if sc.name is not None:
                        context[sc.name] = buildret
            except StopIteration:
                break
        return context
    def _sizeof(self, context, path):
        try:
            def isStruct(sc):
                return isStruct(sc.subcon) if isinstance(sc, Renamed) else isinstance(sc, Struct)
            def nest(context, sc):
                if isStruct(sc) and not sc.flagembedded and sc.name in context:
                    context2 = context[sc.name]
                    context2["_"] = context
                    return context2
                else:
                    return context
            return sum(sc._sizeof(nest(context, sc), path) for sc in self.subcons)
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


class Sequence(Struct):
    r"""
    Sequence of unnamed constructs. The elements are parsed and built in the order they are defined. If a member is named, its parsed value gets inserted into the context. This allows using members that refer to previous members values.

    Size is the sum of all subcon sizes, unless any subcon raises SizeofError.

    Operator >> can also be used to make Sequences.

    .. seealso:: Can be nested easily, and embedded using :func:`~construct.core.Embedded` wrapper that merges entries with parent's entries.

    :param subcons: subcons that make up this sequence, some can be named

    Example::

        >>> d = (Byte >> Byte)
        >>> d.parse(b'\x01\x02')
        [1, 2]
        >>> d.build([1, 2])
        b'\x01\x02'
        >>> d.sizeof()
        2

        >>> d = Sequence(Byte, CString(), Float32b)
        >>> d.build([255, b"hello", 123.0])
        b'\xffhello\x00B\xf6\x00\x00'
        >>> d.parse(_)
        [255, b'hello', 123.0]

        Alternative syntax (not recommended):
        >>> (Byte >> "Byte >> "c"/Byte >> "d"/Byte)

        Alternative syntax, note this works ONLY on python 3.6+:
        >>> Sequence(a=Byte, b=Byte, c=Byte, d=Byte)
    """
    def _parse(self, stream, context, path):
        obj = ListContainer()
        context = Container(_ = context)
        for i,sc in enumerate(self.subcons):
            try:
                subobj = sc._parse(stream, context, path)
                if sc.flagembedded:
                    obj.extend(subobj)
                    context[i] = subobj
                else:
                    obj.append(subobj)
                    if sc.name is not None:
                        context[sc.name] = subobj
                    context[i] = subobj
            except StopIteration:
                break
        return obj
    def _build(self, obj, stream, context, path):
        context = Container(_ = context)
        objiter = iter(obj)
        for i,sc in enumerate(self.subcons):
            try:
                if sc.flagembedded:
                    subobj = objiter
                else:
                    subobj = next(objiter)
                    if sc.name is not None:
                        context[sc.name] = subobj
                context[i] = subobj
                buildret = sc._build(subobj, stream, context, path)
                if buildret is not None:
                    if sc.flagembedded:
                        context.update(buildret)
                    if sc.name is not None:
                        context[sc.name] = buildret
                    context[i] = buildret
            except StopIteration:
                break


#===============================================================================
# arrays and repeaters
#===============================================================================
class Range(Subconstruct):
    r"""
    Homogenous array of elements. The array will iterate through between ``min`` to ``max`` times. If an exception occurs (EOF, validation error) then repeater exits cleanly. If less than ``min`` elements were parsed or more than ``max`` elements were provided for building, error is raised. 

    Operator [] can be used to make instances.

    .. seealso:: Analog to :func:`~construct.core.GreedyRange` that parses until end of stream.

    :param min: the minimal count, an integer or a context lambda
    :param max: the maximal count, an integer or a context lambda
    :param subcon: the subcon to process individual elements

    :raises RangeError: when consumed or produced too little or too many elements

    Example::

        >>> d = Range(3,5,Byte) or Byte[3:5]
        >>> d.parse(b'\x01\x02\x03\x04')
        [1,2,3,4]
        >>> d.build([1,2,3,4])
        b'\x01\x02\x03\x04'
        >>> d.build([1,2])
        construct.core.RangeError: expected from 3 to 5 elements, found 2
        >>> d.build([1,2,3,4,5,6])
        construct.core.RangeError: expected from 3 to 5 elements, found 6

        Alternative syntax (recommended):
        >>> Byte[3:5], Byte[3:], Byte[:5], Byte[:]
    """
    __slots__ = ["min", "max"]
    def __init__(self, min, max, subcon):
        super(Range, self).__init__(subcon)
        self.min = min
        self.max = max
    def _parse(self, stream, context, path):
        min = self.min(context) if callable(self.min) else self.min
        max = self.max(context) if callable(self.max) else self.max
        if not 0 <= min <= max:
            raise RangeError("unsane min %s and max %s" % (min, max))
        obj = ListContainer()
        context = Container(_ = context)
        try:
            while len(obj) < max:
                fallback = stream.tell()
                obj.append(self.subcon._parse(stream, context._, path))
                context[len(obj)-1] = obj[-1]
        except StopIteration:
            pass
        except ExplicitError:
            raise
        except Exception:
            if len(obj) < min:
                raise RangeError("expected %d to %d elements, found %d" % (min, max, len(obj)))
            stream.seek(fallback)
        return obj
    def _build(self, obj, stream, context, path):
        min = self.min(context) if callable(self.min) else self.min
        max = self.max(context) if callable(self.max) else self.max
        if not 0 <= min <= max:
            raise RangeError("unsane min %s and max %s" % (min, max))
        if not isinstance(obj, collections.Sequence):
            raise RangeError("expected sequence type, found %s" % type(obj))
        if not min <= len(obj) <= max:
            raise RangeError("expected %d to %d elements, found %d" % (min, max, len(obj)))
        context = Container(_ = context)
        try:
            for i,subobj in enumerate(obj):
                context[i] = subobj
                self.subcon._build(subobj, stream, context._, path)
        except StopIteration:
            pass
        except ExplicitError:
            raise
        except Exception:
            if len(obj) < min:
                raise RangeError("expected %d to %d, found %d" % (min, max, len(obj)))
            else:
                raise
    def _sizeof(self, context, path):
        try:
            min = self.min(context) if callable(self.min) else self.min
            max = self.max(context) if callable(self.max) else self.max
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")
        if min == max:
            return min * self.subcon._sizeof(context, path)
        raise SizeofError("cannot calculate size, unless element count and size is fixed")


def GreedyRange(subcon):
    r"""
    Homogenous array of elements that parses until end of stream and builds from all elements. 

    Operator [] can be used to make instances.

    :param subcon: the subcon to process individual elements

    Example::

        >>> d = GreedyRange(Byte) or Byte[:]
        >>> d.build(range(8))
        b'\x00\x01\x02\x03\x04\x05\x06\x07'
        >>> d.parse(_)
        [0, 1, 2, 3, 4, 5, 6, 7]

        Alternative syntax (recommended):
        >>> Byte[3:5], Byte[3:], Byte[:5], Byte[:]
    """
    return Range(0, 2**64, subcon)


def Array(count, subcon):
    r"""
    Homogenous array of elements. The array will iterate through exactly ``count`` elements. This is just a macro around `Range`. 

    Operator [] can be used to make instances.

    :param count: an integer or a context function that returns such an integer
    :param subcon: the subcon to process individual elements

    Example::

        >>> d = Array(5,5,Byte) or Byte[5]
        >>> d.build(range(5))
        b'\x00\x01\x02\x03\x04'
        >>> d.parse(_)
        [0, 1, 2, 3, 4]

        Alternative syntax (recommended):
        >>> Byte[3:5], Byte[3:], Byte[:5], Byte[:]
    """
    return Range(count, count, subcon)


class RepeatUntil(Subconstruct):
    r"""
    Homogenous array that repeats until the predicate indicates it to stop. Note that the last element (that predicate indicated as True) is included in the return list.

    :param predicate: a predicate function that takes (obj, list, context) and returns True to break or False to continue (or a truthy value)
    :param subcon: the subcon used to parse and build each element

    Example::

        >>> d = RepeatUntil(lambda x,lst,ctx: x>7, Byte)
        >>> d.build(range(20))
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08'
        >>> d.parse(b"\x01\xff\x02")
        [1, 255]

        >>> d = RepeatUntil(lambda x,lst,ctx: lst[-2:]==[0,0], Byte)
        >>> d.parse(b"\x01\x00\x00\xff")
        [1, 0, 0]
    """
    __slots__ = ["predicate"]
    def __init__(self, predicate, subcon):
        super(RepeatUntil, self).__init__(subcon)
        self.predicate = predicate
    def _parse(self, stream, context, path):
        obj = []
        while True:
            subobj = self.subcon._parse(stream, context, path)
            obj.append(subobj)
            if self.predicate(subobj, obj, context):
                return ListContainer(obj)
    def _build(self, obj, stream, context, path):
        for i, subobj in enumerate(obj):
            self.subcon._build(subobj, stream, context, path)
            if self.predicate(subobj, obj[:i+1], context):
                break
        else:
            raise RangeError("expected any item to match predicate, when building")
    def _sizeof(self, context, path):
        raise SizeofError("cannot calculate size, amount depends on actual data")


#===============================================================================
# specials
#===============================================================================
class Embedded(Subconstruct):
    r"""
    Embeds a struct into the enclosing struct, merging fields. Can also embed sequences into sequences, merging items. Name is inherited from subcon.

    .. warning:: You can use Embedded(Switch(...)) but not Switch(Embedded(...)). Sames applies to If and IfThenElse macros.

    :param subcon: the inner struct to embed inside outer struct or sequence

    Example::

        >>> d = Struct("a"/Byte, Embedded(Struct("b"/Byte)), "c"/Byte)
        >>> d.parse(b"abc")
        Container(a=97)(b=98)(c=99)
    """
    def __init__(self, subcon):
        super(Embedded, self).__init__(subcon)
        self.flagembedded = True


class Renamed(Subconstruct):
    r"""
    Renames an existing construct. This creates a wrapper so underlying subcon retains it's original name, which by default is just None. Can be used to give same construct few different names. Used internally by / operator.

    Also this wrapper is responsible for building a path (a chain of names) that gets attached to error message when parsing, building, or sizeof fails. Fields that are not named do not appear in the path string.

    :param newname: the new name, as string
    :param subcon: the subcon to rename

    Example::

        >>> "name" / Int32ul
        <Renamed: name>
    """
    def __init__(self, newname, subcon):
        super(Renamed, self).__init__(subcon)
        self.name = newname
    def _parse(self, stream, context, path):
        try:
            path += " -> %s" % (self.name)
            return self.subcon._parse(stream, context, path)
        except ConstructError as e:
            if "\n" in str(e):
                raise
            raise e.__class__("%s\n    %s" % (e, path))
    def _build(self, obj, stream, context, path):
        try:
            path += " -> %s" % (self.name)
            return self.subcon._build(obj, stream, context, path)
        except ConstructError as e:
            if "\n" in str(e):
                raise
            raise e.__class__("%s\n    %s" % (e, path))
    def _sizeof(self, context, path):
        try:
            path += " -> %s" % (self.name)
            return self.subcon._sizeof(context, path)
        except ConstructError as e:
            if "\n" in str(e):
                raise
            raise e.__class__("%s\n    %s" % (e, path))


#===============================================================================
# miscellaneous
#===============================================================================
class Const(Subconstruct):
    r"""
    Field enforcing a constant value. It is used for file signatures, to validate that the given pattern exists. When parsed, the value must strictly match.

    Usually a member of a Struct, where it can be anonymous (so it does not appear in parsed dictionary for simplicity).

    Note that a variable length subcon may still provide positive verification. Const does not consume a precomputed amount of bytes (and hence does NOT require a fixed sized lenghtfield), but depends on the subcon to read the appropriate amount (eg. VarInt is acceptable).

    :param value: the expected value, or a bytes literal
    :param subcon: optional, the subcon used to build value from, Bytes if value was a bytes literal

    :raises ConstError: when parsed data does not match specified value, or building from wrong value

    Example::

        >>> d = Const(b"IHDR")
        >>> d.build(None)
        b'IHDR'
        >>> d.parse(b"JPEG")
        construct.core.ConstError: expected b'IHDR' but parsed b'JPEG'

        >>> d = Const(16, Int32ul)
        >>> d.build(None)
        b'\x10\x00\x00\x00'
    """
    __slots__ = ["value"]
    def __init__(self, value, subcon=None):
        if subcon is None:
            subcon = Bytes(len(value))
        super(Const, self).__init__(subcon)
        self.value = value
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        obj = self.subcon._parse(stream, context, path)
        if obj != self.value:
            raise ConstError("parsing expected %r but parsed %r" % (self.value, obj))
        return obj
    def _build(self, obj, stream, context, path):
        if obj not in (None, self.value):
            raise ConstError("building expected None or %r but got %r" % (self.value, obj))
        return self.subcon._build(self.value, stream, context, path)
    def _sizeof(self, context, path):
        return self.subcon._sizeof(context, path)


class Computed(Construct):
    r"""
    Field computing a value. Underlying byte stream is unaffected. When parsing, the context function provides the value. Constant literal value can also be provided.

    Building does not require a value, the value gets computed from context, the same as during parsing.

    Size is defined as 0 because parsing and building does not consume or produce bytes.

    :param func: a context function or a constant value

    Example::
        >>> d = Struct(
        ...     "width" / Byte,
        ...     "height" / Byte,
        ...     "total" / Computed(this.width * this.height),
        ... )
        >>> d.build(dict(width=4,height=5))
        b'\x04\x05'
        >>> d.parse(b"12")
        Container(width=49)(height=50)(total=2450)

        >>> d = Computed(lambda ctx: 7)
        >>> d.parse(b"")
        7

        >>> import os
        >>> d = Computed(lambda ctx: os.urandom(10))
        >>> d.parse(b"")
        b'\x98\xc2\xec\x10\x07\xf5\x8e\x98\xc2\xec'
    """
    __slots__ = ["func"]
    def __init__(self, func):
        super(Computed, self).__init__()
        self.func = func
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        return self.func(context) if callable(self.func) else self.func
    def _build(self, obj, stream, context, path):
        return self.func(context) if callable(self.func) else self.func
    def _sizeof(self, context, path):
        return 0


class Rebuild(Subconstruct):
    r"""
    Parses the field like normal, but computes the value used for building from a context function. Constant value can also be used instead.

    Building does not require a value, because the value gets recomputed anyway.

    Size is the same as subcon size.

    .. seealso:: Useful for length and count fields when :class:`~construct.core.Prefixed` and :class:`~construct.core.PrefixedArray` cannot be used.

    Example::

        >>> d = Struct(
        ...     "count" / Rebuild(Byte, len_(this.items)),
        ...     "items" / Byte[this.count],
        ... )
        >>> d.build(dict(items=[1,2,3]))
        b'\x03\x01\x02\x03'
    """
    __slots__ = ["func"]
    def __init__(self, subcon, func):
        super(Rebuild, self).__init__(subcon)
        self.func = func
        self.flagbuildnone = True
    def _build(self, obj, stream, context, path):
        obj = self.func(context) if callable(self.func) else self.func
        self.subcon._build(obj, stream, context, path)
        return obj


class Default(Subconstruct):
    r"""
    Allows to make a field have a default value, which comes handly when building a Struct from a dict with missing keys.

    Building does not require a value, but can accept one.

    Size is the same as subcon size.

    Example::

        >>> d = Struct(
        ...     "a" / Default(Byte, 0),
        ... )
        >>> d.build(dict(a=1))
        b'\x01'
        >>> d.build(dict())
        b'\x00'
    """
    __slots__ = ["value"]
    def __init__(self, subcon, value):
        super(Default, self).__init__(subcon)
        self.value = value
        self.flagbuildnone = True
    def _build(self, obj, stream, context, path):
        obj = (self.value(context) if callable(self.value) else self.value) if obj is None else obj
        self.subcon._build(obj, stream, context, path)
        return obj


class Check(Construct):
    r"""
    Checks for a condition, and raises ValidationError if the check fails.

    :param func: a context function returning a bool (or truthy value)

    :raises ValidationError: when condition fails

    Example::

        Check(lambda ctx: len(ctx.payload.data) == ctx.payload_len)
        Check(len_(this.payload.data) == this.payload_len)
    """
    def __init__(self, func):
        super(Check, self).__init__()
        self.func = func
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        passed = self.func(context) if callable(self.func) else self.func
        if not passed:
            raise ValidationError("check failed during parsing")
    def _build(self, obj, stream, context, path):
        passed = self.func(context) if callable(self.func) else self.func
        if not passed:
            raise ValidationError("check failed during building")
    def _sizeof(self, context, path):
        return 0


@singleton
class Error(Construct):
    r"""
    Raises an exception when triggered by parse or build. Can be used as a sentinel that blows a whistle when a conditional branch goes the wrong way, or to raise an error explicitly the declarative way.

    :raises ExplicitError: when parsed or build

    Example::

        >>> d = ("x"/Byte >> IfThenElse(this.x > 0, Byte, Error))
        >>> d.parse(b"\xff\x05")
        construct.core.ExplicitError: Error field was activated during parsing
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        raise ExplicitError("Error field was activated during parsing")
    def _build(self, obj, stream, context, path):
        raise ExplicitError("Error field was activated during building")


class FocusedSeq(Construct):
    r"""
    Parses and builds a sequence where only one subcon value is returned from parsing or taken into building, other fields are parsed and discarded or built from nothing.

    :param parsebuildfrom: which subcon to use, an integer index or string name, or a context lambda returning either
    :param \*subcons: a list of members
    :param \*\*kw: a list of members (works ONLY on python 3.6)

    Excample::

        >>> d = FocusedSeq(1 or "num", Const(b"MZ"), "num"/Byte, Terminated)
        >>> d.parse(b"MZ\xff")
        255
        >>> d.build(255)
        b'MZ\xff'
    """
    def __init__(self, parsebuildfrom, *subcons, **kw):
        subcons = list(subcons) + list(k/v for k,v in kw.items()) 
        super(FocusedSeq, self).__init__()
        self.parsebuildfrom = parsebuildfrom
        self.subcons = subcons
    def _parse(self, stream, context, path):
        if callable(self.parsebuildfrom):
            self.parsebuildfrom = self.parsebuildfrom(context)
        if isinstance(self.parsebuildfrom, int):
            index = self.parsebuildfrom
            self.subcons[index]  #IndexError check
        if isinstance(self.parsebuildfrom, str):
            index = [i for i,sc in enumerate(self.subcons) if sc.name == self.parsebuildfrom][0]
        for i,sc in enumerate(self.subcons):
            parseret = sc._parse(stream, context, path)
            context[i] = parseret
            if sc.name is not None:
                context[sc.name] = parseret
            if i == index:
                finalobj = parseret
        return finalobj
    def _build(self, obj, stream, context, path):
        if callable(self.parsebuildfrom):
            self.parsebuildfrom = self.parsebuildfrom(context)
        if isinstance(self.parsebuildfrom, int):
            index = self.parsebuildfrom
            self.subcons[index]  #IndexError check
        if isinstance(self.parsebuildfrom, str):
            index = [i for i,sc in enumerate(self.subcons) if sc.name == self.parsebuildfrom][0]
        for i,sc in enumerate(self.subcons):
            if i == index:
                context[i] = obj
                if sc.name is not None:
                    context[sc.name] = obj
        for i,sc in enumerate(self.subcons):
            buildret = sc._build(obj if i==index else None, stream, context, path)
            if buildret is not None:
                if sc.name is not None:
                    context[sc.name] = buildret
                context[i] = buildret
            if i == index:
                finalobj = buildret
        return finalobj
    def _sizeof(self, context, path):
        try:
            if callable(self.parsebuildfrom):
                self.parsebuildfrom = self.parsebuildfrom(context)
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")
        if isinstance(self.parsebuildfrom, int):
            index = self.parsebuildfrom
            self.subcons[index]  #IndexError check
        if isinstance(self.parsebuildfrom, str):
            index = [i for i,sc in enumerate(self.subcons) if sc.name == self.parsebuildfrom][0]
        return self.subcons[index]._sizeof(context, path)


@singleton
class Numpy(Construct):
    r"""
    Preserves numpy arrays (both shape, dtype and values).

    :raises ImportError: when numpy cannot be imported during init

    Example::

        >>> import numpy
        >>> a = numpy.asarray([1,2,3])
        >>> Numpy.build(a)
        b"\x93NUMPY\x01\x00F\x00"...
        >>> Numpy.parse(_)
        array([1, 2, 3])
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        try:
            import numpy
            self.lib = numpy
        except ImportError:
            pass # in case import fails on Travis during singleton making
    def _parse(self, stream, context, path):
        return self.lib.load(stream)
    def _build(self, obj, stream, context, path):
        self.lib.save(stream, obj)


class NamedTuple(Adapter):
    r"""
    Both arrays, structs, and sequences can be mapped to a namedtuple from collections module. To create a named tuple, you need to provide a name and a sequence of fields, either a string with space-separated names or a list of string names. Just like the standard namedtuple.

    :raises AdaptationError: when subcon is not either Struct Sequence Range

    Example::

        >>> d = NamedTuple("coord", "x y z", Byte[3])
        >>> d = NamedTuple("coord", "x y z", Byte >> Byte >> Byte)
        >>> d = NamedTuple("coord", "x y z", "x"/Byte + "y"/Byte + "z"/Byte)
        >>> d.parse(b"123")
        coord(x=49, y=50, z=51)
    """
    def __init__(self, tuplename, tuplefields, subcon):
        super(NamedTuple, self).__init__(subcon)
        self.factory = collections.namedtuple(tuplename, tuplefields)
    def _decode(self, obj, context):
        if isinstance(obj, list):
            return self.factory(*obj)
        if isinstance(obj, dict):
            return self.factory(**obj)
        raise AdaptationError("can only decode and encode from lists and dicts")
    def _encode(self, obj, context):
        if isinstance(self.subcon, (Sequence,Range)):
            return list(obj)
        if isinstance(self.subcon, Struct):
            return {sc.name:getattr(obj,sc.name) for sc in self.subcon.subcons if sc.name is not None}
        raise AdaptationError("can only decode and encode from lists and dicts")


#===============================================================================
# alignment and padding
#===============================================================================
def Padding(length, pattern=b"\x00"):
    r"""
    Padding field that adds bytes when building, discards bytes when parsing.

    :param length: length of the padding, an integer or a context function returning such an integer
    :param pattern: padding pattern as b-character, default is \\x00

    :raises PaddingError: when strict is set and actual parsed pattern differs from specified

    Example::

        >>> d = Padding(4)
        >>> d.build(None)
        b'\x00\x00\x00\x00'
        >>> d.parse(b"****")
        None
        >>> d.sizeof()
        4
    """
    return Padded(length, Pass, pattern=pattern)


class Padded(Subconstruct):
    r"""
    Appends additional null bytes to achieve a fixed length. Fails if actual data is longer than specified length. Note that subcon can actually be variable size, it is the eventual size during building that determines actual padding.

    :raises PaddingError: when parsed or build data is longer than the length

    Example::

        >>> d = Padded(4, Byte)
        >>> d.build(255)
        b'\xff\x00\x00\x00'
        >>> d.parse(_)
        255
        >>> d.sizeof()
        4

        >>> d = Padded(4, VarInt)
        >>> d.build(1)
        b'\x01\x00\x00\x00'
        >>> d.build(70000)
        b'\xf0\xa2\x04\x00'
    """
    __slots__ = ["length", "pattern"]
    def __init__(self, length, subcon, pattern=b"\x00"):
        if not isinstance(pattern, bytes) or len(pattern) != 1:
            raise PaddingError("pattern expected to be bytes of length 1")
        super(Padded, self).__init__(subcon)
        self.length = length
        self.pattern = pattern
    def _parse(self, stream, context, path):
        length = self.length(context) if callable(self.length) else self.length
        position1 = stream.tell()
        obj = self.subcon._parse(stream, context, path)
        position2 = stream.tell()
        padlen = length - (position2 - position1)
        if padlen < 0:
            raise PaddingError("subcon parsed %d bytes but was allowed only %d" % (position2-position1, length))
        _read_stream(stream, padlen)
        return obj
    def _build(self, obj, stream, context, path):
        length = self.length(context) if callable(self.length) else self.length
        position1 = stream.tell()
        subobj = self.subcon._build(obj, stream, context, path)
        position2 = stream.tell()
        padlen = length - (position2 - position1)
        if padlen < 0:
            raise PaddingError("subcon build %d bytes but was allowed only %d" % (position2-position1, length))
        _write_stream(stream, padlen, self.pattern * padlen)
        return subobj
    def _sizeof(self, context, path):
        try:
            return self.length(context) if callable(self.length) else self.length
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


class Aligned(Subconstruct):
    r"""
    Appends additional null bytes to achieve a length that is shortest multiple of a modulus.

    :param modulus: the modulus to final length, an integer or a context function returning such an integer
    :param subcon: the subcon to align
    :param pattern: optional, the padding pattern, a b-character (default is \x00)

    Example::

        >>> d = Aligned(4, Int16ub)
        >>> d.parse(b'\x00\x01\x00\x00')
        1
        >>> d.sizeof()
        4
    """
    __slots__ = ["subcon", "modulus", "pattern"]
    def __init__(self, modulus, subcon, pattern=b"\x00"):
        if not isinstance(pattern, bytes) or len(pattern) != 1:
            raise PaddingError("pattern expected to be bytes character")
        super(Aligned, self).__init__(subcon)
        self.modulus = modulus
        self.pattern = pattern
    def _parse(self, stream, context, path):
        modulus = self.modulus(context) if callable(self.modulus) else self.modulus
        position1 = stream.tell()
        obj = self.subcon._parse(stream, context, path)
        position2 = stream.tell()
        pad = -(position2 - position1) % modulus
        _read_stream(stream, pad)
        return obj
    def _build(self, obj, stream, context, path):
        modulus = self.modulus(context) if callable(self.modulus) else self.modulus
        position1 = stream.tell()
        subobj = self.subcon._build(obj, stream, context, path)
        position2 = stream.tell()
        pad = -(position2 - position1) % modulus
        _write_stream(stream, pad, self.pattern * pad)
        return subobj
    def _sizeof(self, context, path):
        try:
            modulus = self.modulus(context) if callable(self.modulus) else self.modulus
            subconlen = self.subcon._sizeof(context, path)
            return subconlen + (-subconlen % modulus)
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


def AlignedStruct(modulus, *subcons, **kw):
    r"""
    Makes a structure where each field is aligned to the same modulus (it is a struct of aligned fields, not an aligned struct).

    .. seealso:: Uses :func:`~construct.core.Aligned` and :func:`~construct.core.Struct`.

    :param modulus: passed to each member
    :param \*subcons: subcons that make up the Struct
    :param \*\*kw: named subcons, extend the Struct

    Example::

        >>> d = AlignedStruct(4, "a"/Int8ub, "b"/Int16ub)
        >>> d.build(dict(a=1,b=5))
        b'\x01\x00\x00\x00\x00\x05\x00\x00'
        >>> d.parse(_)
        Container(a=1)(b=5)
        >>> d.sizeof()
        8
    """
    subcons = list(subcons) + list(k/v for k,v in kw.items())
    return Struct(*[Aligned(modulus, sc) for sc in subcons])


def BitStruct(*subcons):
    r"""
    Makes a structure inside a Bitwise.

    .. seealso:: Uses :func:`~construct.core.Bitwise` and :func:`~construct.core.Struct`.

    :param \*subcons: the subcons that make up this structure

    Example::

        >>> d = BitStruct(
        ...     "a" / Flag,
        ...     "b" / Nibble,
        ...     "c" / BitsInteger(10),
        ...     "d" / Padding(1),
        ... )
        >>> d.parse(b"\xbe\xef")
        Container(a=True)(b=7)(c=887)(d=None)
        >>> d.sizeof()
        2
    """
    return Bitwise(Struct(*subcons))


def EmbeddedBitStruct(*subcons):
    r"""
    Makes an embedded BitStruct.

    .. seealso:: Uses :func:`~construct.core.Bitwise` and :func:`~construct.core.Embedded` and :func:`~construct.core.Struct`.

    :param \*subcons: the subcons that make up this structure

    Example::

        EmbeddedBitStruct  <-->  Bitwise(Embedded(Struct(...)))
    """
    return Bitwise(Embedded(Struct(*subcons)))


#===============================================================================
# conditional
#===============================================================================
class Union(Construct):
    r"""
    Treats the same data as multiple constructs (similar to C union statement) so you can look at the data in multiple views.

    When parsing, all fields read the same data bytes, but stream ultimately gets reverted to initial offset, unless parsefrom selects a subcon by index or name. 
    When building, the first subcon that can find an entry in the dict (or builds from None, so it does not require an entry) is automatically selected.

    .. warning:: If you skip the `parsefrom` parameter then stream will be left back at the starting offset, not seeked to any common denominator between subcons.

    :param parsefrom: how to leave stream after parsing, can be integer index or string name selecting a subcon, None (leaves stream at initial offset, the default), a context lambda returning either of previously mentioned
    :param subcons: subconstructs (order and name sensitive)

    Example::

        >>> d = Union(0, "raw"/Bytes(8), "ints"/Int32ub[2], "shorts"/Int16ub[4], "chars"/Byte[8])
        >>> d.parse(b"12345678")
        Container(raw=b'12345678')(ints=[825373492, 892745528])(shorts=[12594, 13108, 13622, 14136])(chars=[49, 50, 51, 52, 53, 54, 55, 56])
        >>> d.build(dict(chars=range(8)))
        b'\x00\x01\x02\x03\x04\x05\x06\x07'

        Alternative syntax, note this works ONLY on python 3.6+:
        >>> Union(0, raw=Bytes(8), ints=Int32ub[2], shorts=Int16ub[4], chars=Byte[8])
    """
    __slots__ = ["subcons","parsefrom"]
    def __init__(self, parsefrom, *subcons, **kw):
        if isinstance(parsefrom, Construct):
            raise UnionError("parsefrom should be either: None int str context-function")
        subcons = list(subcons) + list(k/v for k,v in kw.items()) 
        super(Union, self).__init__()
        self.subcons = subcons
        self.parsefrom = parsefrom
    def _parse(self, stream, context, path):
        obj = Container()
        context = Container(_ = context)
        fallback = stream.tell()
        forwards = {}
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = list(sc._parse(stream, context, path).items())
                obj.update(subobj)
                context.update(subobj)
            else:
                subobj = sc._parse(stream, context, path)
                if sc.name is not None:
                    obj[sc.name] = subobj
                    context[sc.name] = subobj
            forwards[i] = stream.tell()
            if sc.name is not None:
                forwards[sc.name] = stream.tell()
            stream.seek(fallback)
        parsefrom = self.parsefrom
        if callable(parsefrom):
            parsefrom = parsefrom(context)
        if isinstance(parsefrom, (int,str)):
            stream.seek(forwards[parsefrom])
        return obj
    def _build(self, obj, stream, context, path):
        context = Container(_ = context)
        context.update(obj)
        for sc in self.subcons:
            if sc.flagbuildnone:
                subobj = obj.get(sc.name, None)
                buildret = sc._build(subobj, stream, context, path)
                if buildret is not None:
                    if sc.flagembedded:
                        context.update(buildret)
                    if sc.name is not None:
                        context[sc.name] = buildret
                return buildret
            elif sc.name in obj:
                context[sc.name] = obj[sc.name]
                buildret = sc._build(obj[sc.name], stream, context, path)
                if buildret is not None:
                    if sc.flagembedded:
                        context.update(buildret)
                    if sc.name is not None:
                        context[sc.name] = buildret
                return buildret
        else:
            raise UnionError("cannot build, none of subcons %s were found in the dictionary %s" % ([sc.name for sc in self.subcons], obj))
    def _sizeof(self, context, path):
        parsefrom = self.parsefrom
        try:
            if callable(parsefrom):
                parsefrom = parsefrom(context)
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")
        if parsefrom is None:
            raise SizeofError("cannot calculate size")
        if isinstance(parsefrom, int):
            sc = self.subcons[parsefrom]
            return sc._sizeof(context, path)
        if isinstance(parsefrom, str):
            sc = {sc.name:sc for sc in self.subcons if sc.name is not None}[parsefrom]
            return sc._sizeof(context, path)
        raise UnionError("parsefrom should be either: None, an int, a str, or context function")


class Select(Construct):
    r"""
    Selects the first matching subconstruct. It will literally try each of the subconstructs, until one matches.

    :param subcons: the subcons to try (order sensitive)
    :param includename: indicates whether to include the name of the selected subcon in the return value of parsing, default is False

    Example::

        >>> d = Select(Int32ub, CString(encoding="utf8"))
        >>> d.build(1)
        b'\x00\x00\x00\x01'
        >>> d.build(u"Афон")
        b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00'

        Alternative syntax, note this works ONLY on python 3.6+:
        >>> Select(num=Int32ub, text=CString(encoding="utf8"))
    """
    __slots__ = ["subcons", "includename"]
    def __init__(self, *subcons, **kw):
        subcons = list(subcons) + list(k/v for k,v in kw.items() if k != "includename") 
        super(Select, self).__init__()
        self.subcons = subcons
        self.flagbuildnone = all(sc.flagbuildnone for sc in subcons)
        self.flagembedded = all(sc.flagembedded for sc in subcons)
        self.includename = kw.pop("includename", False)
    def _parse(self, stream, context, path):
        for sc in self.subcons:
            fallback = stream.tell()
            try:
                obj = sc._parse(stream, context, path)
            except ExplicitError:
                raise
            except ConstructError:
                stream.seek(fallback)
            else:
                return (sc.name,obj) if self.includename else obj
        raise SelectError("no subconstruct matched")
    def _build(self, obj, stream, context, path):
        if self.includename:
            name, obj = obj
            for sc in self.subcons:
                if sc.name == name:
                    return sc._build(obj, stream, context, path)
        else:
            for sc in self.subcons:
                try:
                    data = sc.build(obj, context)
                except ExplicitError:
                    raise
                except Exception:
                    pass
                else:
                    _write_stream(stream, len(data), data)
                    return
        raise SelectError("no subconstruct matched: %s" % (obj,))


def Optional(subcon):
    r"""
    Makes an optional construct, that tries to parse the subcon. If parsing fails, returns None. If building fails, writes nothing.

    Size cannot be computed, because whether bytes are consumed or produced depends on actual data and context.

    :param subcon: the subcon to optionally parse or build

    Example::

        >>> d = Optional(Int64ul)
        >>> d.parse(b"12345678")
        4050765991979987505
        >>> d.parse(b"")
        None
        >>> d.build(1)
        b'\x01\x00\x00\x00\x00\x00\x00\x00'
        >>> d.build(None)
        b''
    """
    return Select(subcon, Pass)


def If(predicate, subcon):
    r"""
    An if-then conditional construct. If the context predicate indicates True, the `subcon` will be used for parsing and building, otherwise parsing returns None and building is no-op. Note that the predicate has no access to parsed value, it computes only on context.

    :param predicate: a function taking context and returning a bool
    :param subcon: the subcon that will be used if the predicate returns True

    Example::

        >>> d = If(this.x > 0, Byte)
        >>> d.build(255, dict(x=1))
        b'\xff'
        >>> d.build(255, dict(x=0))
        b''
    """
    return IfThenElse(predicate, subcon, Pass)


def IfThenElse(predicate, thensubcon, elsesubcon):
    r"""
    An if-then-else conditional construct. One of the two subcons is used for parsing or building, depending whether the predicate returns a truthy or falsey value for given context. Constant truthy value can also be used.

    :param predicate: a context function that returns a bool (or truthy value)
    :param thensubcon: the subcon that will be used if the predicate indicates True
    :param elsesubcon: the subcon that will be used if the predicate indicates False

    Example::

        >>> d = IfThenElse(this.x > 0, VarInt, Byte)
        >>> d.build(255, dict(x=1))
        b'\xff\x01'
        >>> d.build(255, dict(x=0))
        b'\xff'
    """
    return Switch(
        lambda ctx: bool(predicate(ctx)) if callable(predicate) else bool(predicate),
        {True:thensubcon, False:elsesubcon},
    )


class Switch(Construct):
    r"""
    A conditional branch. Switch will choose the case to follow based on the return value of keyfunc. If no case is matched and no default value is given, SwitchError will be raised.

    .. warning:: You can use Embedded(Switch(...)) but not Switch(Embedded(...)). Same applies to If and IfThenElse macros.

    :param keyfunc: a context function that returns a key which will choose a case, or a constant
    :param cases: a dictionary mapping keys to subcons
    :param default: a default field to use when the key is not found in the cases. if not supplied, an exception will be raised when the key is not found. Pass can be used for do-nothing
    :param includekey: whether to include the key in the return value of parsing, default is False

    :raises SwitchError: when actual value is not in the dict nor a default is given

    Example::

        >>> d = Switch(this.n, { 1:Int8ub, 2:Int16ub, 4:Int32ub })
        >>> d.build(5, dict(n=1))
        b'\x05'
        >>> d.build(5, dict(n=4))
        b'\x00\x00\x00\x05'
    """

    @singleton
    class NoDefault(Construct):
        def _parse(self, stream, context, path):
            raise SwitchError("no default case defined")
        def _build(self, obj, stream, context, path):
            raise SwitchError("no default case defined")
        def _sizeof(self, context, path):
            raise SwitchError("no default case defined")

    __slots__ = ["subcons", "keyfunc", "cases", "default", "includekey"]
    def __init__(self, keyfunc, cases, default=NoDefault, includekey=False):
        super(Switch, self).__init__()
        self.keyfunc = keyfunc
        self.cases = cases
        self.default = default
        self.includekey = includekey
        allcases = list(cases.values())
        if default is not self.NoDefault:
            allcases.append(default)
        self.flagbuildnone = all(sc.flagbuildnone for sc in allcases)
        self.flagembedded = all(sc.flagembedded for sc in allcases)
    def _parse(self, stream, context, path):
        key = self.keyfunc(context) if callable(self.keyfunc) else self.keyfunc
        obj = self.cases.get(key, self.default)._parse(stream, context, path)
        return (key,obj) if self.includekey else obj
    def _build(self, obj, stream, context, path):
        if self.includekey:
            key,obj = obj
        else:
            key = self.keyfunc(context) if callable(self.keyfunc) else self.keyfunc
        case = self.cases.get(key, self.default)
        return case._build(obj, stream, context, path)
    def _sizeof(self, context, path):
        try:
            key = self.keyfunc(context) if callable(self.keyfunc) else self.keyfunc
            sc = self.cases.get(key, self.default)
            return sc._sizeof(context, path)
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


class StopIf(Construct):
    r"""
    Checks for a condition, and stops a Struct/Sequence/Range from parsing or building further.

    :param condfunc: a context function returning a bool (or truthy value)

    Example::

        >>> Struct('x'/Byte, StopIf(this.x == 0), 'y'/Byte)
        >>> Sequence('x'/Byte, StopIf(this.x == 0), 'y'/Byte)
        >>> GreedyRange(FocusedSeq(0, 'x'/Byte, StopIf(this.x == 0)))
    """
    def __init__(self, condfunc):
        super(StopIf, self).__init__()
        self.condfunc = condfunc
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        if self.condfunc(context):
            raise StopIteration
    def _build(self, obj, stream, context, path):
        if self.condfunc(context):
            raise StopIteration
    def _sizeof(self, context, path):
        return SizeofError("Struct/Sequence/Range cannot compute size because StopIf is runtime-dependant")


#===============================================================================
# stream manipulation
#===============================================================================
class Pointer(Subconstruct):
    r"""
    Changes the stream position to a given offset, where the construction should take place, and restores the stream position when finished.

    Offset can also be negative, indicating a position from EOF backwards.

    Size is defined as unknown, instead of previous 0.

    :param offset: an integer or a context function that returns a stream position, where the construction would take place
    :param subcon: the subcon to use at the offset

    Example::

        >>> d = Pointer(8, Bytes(1))
        >>> d.parse(b"abcdefghijkl")
        b'i'
        >>> d.build(b"Z")
        b'\x00\x00\x00\x00\x00\x00\x00\x00Z'
    """
    __slots__ = ["offset"]
    def __init__(self, offset, subcon):
        super(Pointer, self).__init__(subcon)
        self.offset = offset
    def _parse(self, stream, context, path):
        offset = self.offset(context) if callable(self.offset) else self.offset
        fallback = stream.tell()
        stream.seek(offset, 2 if offset < 0 else 0)
        obj = self.subcon._parse(stream, context, path)
        stream.seek(fallback)
        return obj
    def _build(self, obj, stream, context, path):
        offset = self.offset(context) if callable(self.offset) else self.offset
        fallback = stream.tell()
        stream.seek(offset, 2 if offset < 0 else 0)
        buildret = self.subcon._build(obj, stream, context, path)
        stream.seek(fallback)
        return buildret
    def _sizeof(self, context, path):
        raise SizeofError


class Peek(Subconstruct):
    r"""
    Peeks at the stream. Parses without changing the stream position, or rather measures stream position before parsing and seeks back to that position afterwards. If the end of the stream is reached when reading, returns None. Building is no-op.

    Size is defined as 0 because build does not put anything into the stream. 

    .. seealso:: The :func:`~construct.core.Union` class uses Peek to parse each member.

    :param subcon: the subcon to peek at

    Example::

        >>> d = Sequence(Peek(Int8ub), Peek(Int16ub))
        >>> d.parse(b"\x01\x02")
        [1, 258]
        >>> d.sizeof()
        0
    """
    def __init__(self, subcon):
        super(Peek, self).__init__(subcon)
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        fallback = stream.tell()
        try:
            return self.subcon._parse(stream, context, path)
        except ExplicitError:
            raise
        except ConstructError:
            pass
        finally:
            stream.seek(fallback)
    def _build(self, obj, stream, context, path):
        pass
    def _sizeof(self, context, path):
        return 0


class Seek(Construct):
    r"""
    Sets a new stream position when parsing or building. Seeks are useful when many other fields follow the jump. Pointer works when there is only one field to look at, but when there is more to be done, Seek may come useful.

    .. seealso:: Analog :func:`~construct.core.Pointer` wrapper that has same side effect but also processes a subcon.

    :param at: where to jump to, can be an integer or a context lambda returning such an integer
    :param whence: is the offset from beginning (0) or from current position (1) or from ending (2), can be an integer or a context lambda returning such an integer, default is 0

    Example::

        >>> d = (Seek(5) >> Byte)
        >>> d.parse(b"01234x")
        [5, 120]

        >>> d = (Bytes(10) >> Seek(5) >> Byte)
        >>> d.build([b"0123456789", None, 255])
        b'01234\xff6789'
    """
    __slots__ = ["at", "whence"]
    def __init__(self, at, whence=0):
        super(Seek, self).__init__()
        self.at = at
        self.whence = whence
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        at = self.at(context) if callable(self.at) else self.at
        whence = self.whence(context) if callable(self.whence) else self.whence
        return stream.seek(at, whence)
    def _build(self, obj, stream, context, path):
        at = self.at(context) if callable(self.at) else self.at
        whence = self.whence(context) if callable(self.whence) else self.whence
        return stream.seek(at, whence)
    def _sizeof(self, context, path):
        raise SizeofError("Seek seeks the stream, sizeof is not meaningful")


@singleton
class Tell(Construct):
    r"""
    Gets the stream position when parsing or building.

    Tell is useful for adjusting relative offsets to absolute positions, or to measure sizes of Constructs. To get an absolute pointer, use a Tell plus a relative offset. To get a size, place two Tells and measure their difference using a Compute field.

    Size is defined as 0 because parsing and building does not consume or add into the stream.

    .. seealso:: Its better to use :func:`~construct.core.RawCopy` instead of manually extracting two positions and computing difference.

    Example::

        >>> d = Struct("num"/VarInt, "offset"/Tell)
        >>> d.build(dict(num=88))
        b'X'
        >>> d.parse(_)
        Container(num=88)(offset=1)
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        return stream.tell()
    def _build(self, obj, stream, context, path):
        return stream.tell()
    def _sizeof(self, context, path):
        return 0


@singleton
class Pass(Construct):
    r"""
    No-op construct, useful as default cases for Switch and Enum. 

    Returns None on parsing, puts nothing on building, size is 0 by definition. Building does not require a value, and any provided value gets discarded.

    Example::

        >>> Pass.parse(b"")
        None
        >>> Pass.build(None)
        b''
        >>> Pass.sizeof()
        0
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        return None
    def _build(self, obj, stream, context, path):
        pass
    def _sizeof(self, context, path):
        return 0


@singleton
class Terminated(Construct):
    r"""
    Asserts that end of stream has been reached at the point it was placed. You can use this to ensure no more unparsed data follows in the stream.

    This construct is only meaningful for parsing. Building does nothing. Size is 0.

    Example::

        >>> Terminated.parse(b"")
        None
        >>> Terminated.parse(b"remaining")
        construct.core.TerminatedError: expected end of stream
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        try:
            if stream.read(1):
                raise TerminatedError("expected end of stream")
        except IOError:
            # Restreamed.read(1) does not return empty string like BytesIO
            pass
    def _build(self, obj, stream, context, path):
        pass
    def _sizeof(self, context, path):
        return 0


class Restreamed(Subconstruct):
    r"""
    Transforms bytes between the underlying stream and the subcon.

    When the parsing or building is done, the wrapper stream is closed. If read buffer or write buffer is not empty, error is raised.

    .. seealso:: Both :func:`~construct.core.Bitwise` and :func:`~construct.core.Bytewise` are implemented using Restreamed.

    .. warning:: Remember that subcon must consume or produce an amount of bytes that is a multiple of encoding or decoding units. For example, in a Bitwise context you should process a multiple of 8 bits or the stream will fail after parsing/building. Also do NOT use pointers inside.

    :param subcon: the subcon which will operate on the buffer
    :param encoder: a function that takes bytes and returns bytes (used when building)
    :param encoderunit: ratio as integer, encoder takes that many bytes at once
    :param decoder: a function that takes bytes and returns bytes (used when parsing)
    :param decoderunit: ratio as integer, decoder takes that many bytes at once
    :param sizecomputer: a function that computes amount of bytes outputed by some bytes

    Example::

        Bitwise  <--> Restreamed(subcon, bits2bytes, 8, bytes2bits, 1, lambda n: n//8)
        Bytewise <--> Restreamed(subcon, bytes2bits, 1, bits2bytes, 8, lambda n: n*8)
    """

    __slots__ = ["sizecomputer", "encoder", "encoderunit", "decoder", "decoderunit"]
    def __init__(self, subcon, encoder, encoderunit, decoder, decoderunit, sizecomputer):
        super(Restreamed, self).__init__(subcon)
        self.encoder = encoder
        self.encoderunit = encoderunit
        self.decoder = decoder
        self.decoderunit = decoderunit
        self.sizecomputer = sizecomputer
    def _parse(self, stream, context, path):
        stream2 = RestreamedBytesIO(stream, self.encoder, self.encoderunit, self.decoder, self.decoderunit)
        obj = self.subcon._parse(stream2, context, path)
        stream2.close()
        return obj
    def _build(self, obj, stream, context, path):
        stream2 = RestreamedBytesIO(stream, self.encoder, self.encoderunit, self.decoder, self.decoderunit)
        buildret = self.subcon._build(obj, stream2, context, path)
        stream2.close()
        return buildret
    def _sizeof(self, context, path):
        if self.sizecomputer is None:
            raise SizeofError("cannot calculate size")
        else:
            return self.sizecomputer(self.subcon._sizeof(context, path))


class Rebuffered(Subconstruct):
    r"""
    Caches bytes from the underlying stream, so it becomes seekable and tellable. Also makes the stream blocking, in case it came from a socket or a pipe. Optionally, stream can forget bytes that went a certain amount of bytes beyond the current offset, allowing only a limited seeking capability while allowing to process an endless stream.

    .. warning:: Experimental implementation. May not be mature enough.

    :param subcon: the subcon which will operate on the buffered stream
    :param tailcutoff: optional, amount of bytes kept in buffer, by default buffers everything

    Example::

        Rebuffered(..., tailcutoff=1024).parse_stream(nonseekable_stream)
    """
    __slots__ = ["stream2", "tailcutoff"]
    def __init__(self, subcon, tailcutoff=None):
        super(Rebuffered, self).__init__(subcon)
        self.stream2 = RebufferedBytesIO(None, tailcutoff=tailcutoff)
    def _parse(self, stream, context, path):
        self.stream2.substream = stream
        return self.subcon._parse(self.stream2, context, path)
    def _build(self, obj, stream, context, path):
        self.stream2.substream = stream
        return self.subcon._build(obj, self.stream2, context, path)


#===============================================================================
# tunneling and swapping
#===============================================================================
class RawCopy(Subconstruct):
    r"""
    Returns a dict containing both parsed subcon, the raw bytes that were consumed by it, starting and ending offset in the stream, and the amount of bytes. Builds either from raw bytes or a value used by subcon.

    Context does contain a dict with data (if built from raw bytes) or with both (if built from value or parsed).

    :raises ConstructError: when building and neither data or value is given

    Example::

        >>> d = RawCopy(Byte)
        >>> d.parse(b"\xff")
        Container(data=b'\xff')(value=255)(offset1=0)(offset2=1)(length=1)
        >>> d.build(dict(data=b"\xff"))
        '\xff'
        >>> d.build(dict(value=255))
        '\xff'
    """
    def _parse(self, stream, context, path):
        offset1 = stream.tell()
        obj = self.subcon._parse(stream, context, path)
        offset2 = stream.tell()
        stream.seek(offset1)
        data = _read_stream(stream, offset2-offset1)
        return Container(data=data, value=obj, offset1=offset1, offset2=offset2, length=(offset2-offset1))
    def _build(self, obj, stream, context, path):
        if 'data' in obj:
            data = obj['data']
            offset1 = stream.tell()
            _write_stream(stream, len(data), data)
            offset2 = stream.tell()
            return Container(obj, data=data, offset1=offset1, offset2=offset2, length=len(data))
        if 'value' in obj:
            value = obj['value']
            offset1 = stream.tell()
            ret = self.subcon._build(value, stream, context, path)
            value = value if ret is None else ret
            offset2 = stream.tell()
            stream.seek(offset1)
            data = _read_stream(stream, offset2-offset1)
            return Container(obj, data=data, value=value, offset1=offset1, offset2=offset2, length=(offset2-offset1))
        raise ConstructError('both data and value keys are missing, cannot build')


def ByteSwapped(subcon):
    r"""
    Swap the byte order within boundaries of the given subcon. Requires a fixed sized subcon.

    :param subcon: the subcon on top of byte swapped bytes

    Example::

        Int24ul <--> ByteSwapped(Int24ub) <--> BytesInteger(3, swapped=True)
    """
    return Restreamed(subcon,
        lambda s: s[::-1], subcon.sizeof(),
        lambda s: s[::-1], subcon.sizeof(),
        lambda n: n)


def BitsSwapped(subcon):
    r"""
    Swap the bit order within each byte within boundaries of the given subcon. Does NOT require a fixed sized subcon.

    :param subcon: the subcon on top of bit swapped bytes

    Example::

        >>> d = Bitwise(Bytes(8))
        >>> d.parse(b"\x01")
        '\x00\x00\x00\x00\x00\x00\x00\x01'
        >>>> BitsSwapped(d).parse(b"\x01")
        '\x01\x00\x00\x00\x00\x00\x00\x00'
    """
    return Restreamed(subcon,
        lambda s: bits2bytes(bytes2bits(s)[::-1]), 1,
        lambda s: bits2bytes(bytes2bits(s)[::-1]), 1,
        lambda n: n)


class Prefixed(Subconstruct):
    r"""
    Parses the length field. Then reads that amount of bytes and parses the subcon using only those bytes. Constructs that consume entire remaining stream are constrained to consuming only the specified amount of bytes. When building, data is prefixed by its length. Optionally, length field can include its own size.

    .. seealso:: The :class:`~construct.core.VarInt` encoding should be preferred over `Int*` fixed sized fields. VarInt is more compact and never overflows.

    :param lengthfield: a subcon used for storing the length
    :param subcon: the subcon used for storing the value
    :param includelength: optional, whether length field should include own size

    Example::

        >>> Prefixed(VarInt, GreedyRange(Int32ul)).parse(b"\x08abcdefgh")
        [1684234849, 1751606885]

        >>> PrefixedArray(VarInt, Int32ul).parse(b"\x02abcdefgh")
        [1684234849, 1751606885]
    """
    __slots__ = ["name", "lengthfield", "subcon", "includelength"]
    def __init__(self, lengthfield, subcon, includelength=False):
        super(Prefixed, self).__init__(subcon)
        self.lengthfield = lengthfield
        self.includelength = includelength
    def _parse(self, stream, context, path):
        length = self.lengthfield._parse(stream, context, path)
        if self.includelength:
            length -= self.lengthfield._sizeof(context, path)
        stream2 = BytesIO(_read_stream(stream, length))
        return self.subcon._parse(stream2, context, path)
    def _build(self, obj, stream, context, path):
        stream2 = BytesIO()
        obj = self.subcon._build(obj, stream2, context, path)
        data = stream2.getvalue()
        length = len(data)
        if self.includelength:
            length += self.lengthfield._sizeof(context, path)
        self.lengthfield._build(length, stream, context, path)
        _write_stream(stream, len(data), data)
        return obj
    def _sizeof(self, context, path):
        return self.lengthfield._sizeof(context, path) + self.subcon._sizeof(context, path)


def PrefixedArray(lengthfield, subcon):
    r"""
    Homogenous array prefixed by item count (as opposed to prefixed by byte count, see :func:`~construct.core.Prefixed`).

    :param lengthfield: field parsing and building an integer
    :param subcon: subcon to process individual elements

    Example::

        >>> Prefixed(VarInt, GreedyRange(Int32ul)).parse(b"\x08abcdefgh")
        [1684234849, 1751606885]

        >>> PrefixedArray(VarInt, Int32ul).parse(b"\x02abcdefgh")
        [1684234849, 1751606885]
    """
    return FocusedSeq(1,
        "count"/Rebuild(lengthfield, len_(this.items)),
        "items"/subcon[this.count],
    )


class Checksum(Construct):
    r"""
    Field that is build or validated by a hash of a given byte range.

    :param checksumfield: a subcon field that reads the checksum, usually Bytes(int)
    :param hashfunc: a function taking bytes and returning whatever checksumfield takes when building
    :param bytesfunc: a function taking context and returning the bytes or object to be hashed, usually like this.rawcopy1.data

    Example::

        import hashlib
        d = Struct(
            "fields" / RawCopy(Struct(
                "a" / Byte,
                "b" / Byte,
            )),
            "checksum" / Checksum(Bytes(64), lambda data: hashlib.sha512(data).digest(), this.fields.data),
        )
        d.build(dict(fields=dict(value=dict(a=1,b=2))))
        -> b'\x01\x02\xbd\xd8\x1a\xb23\xbc\xebj\xd23\xcd'...
    """
    __slots__ = ["checksumfield", "hashfunc", "bytesfunc"]
    def __init__(self, checksumfield, hashfunc, bytesfunc):
        super(Checksum, self).__init__()
        self.checksumfield = checksumfield
        self.hashfunc = hashfunc
        self.bytesfunc = bytesfunc
        self.flagbuildnone = True
    def _parse(self, stream, context, path):
        hash1 = self.checksumfield._parse(stream, context, path)
        hash2 = self.hashfunc(self.bytesfunc(context))
        if hash1 != hash2:
            raise ChecksumError("wrong checksum, read %r, computed %r" % (
                hash1 if not isinstance(hash1,bytes) else hexlify(hash1),
                hash2 if not isinstance(hash2,bytes) else hexlify(hash2), ))
        return hash1
    def _build(self, obj, stream, context, path):
        hash2 = self.hashfunc(self.bytesfunc(context))
        self.checksumfield._build(hash2, stream, context, path)
        return hash2
    def _sizeof(self, context, path):
        return self.checksumfield._sizeof(context, path)


class Compressed(Tunnel):
    r"""
    Compresses and decompresses underlying stream when processing the subcon. When parsing, entire stream is consumed. When building, puts compressed bytes without marking the end. This construct should be used with :func:`~construct.core.Prefixed` or entire stream.

    :param subcon: the subcon used for storing the value
    :param encoding: any of the module names like zlib/gzip/bzip2/lzma, otherwise any of codecs module bytes<->bytes encodings, usually requires some Python version
    :param level: optional, an integer between 0..9, lzma discards it

    Example::

        Prefixed(VarInt, Compressed(GreedyBytes, "zlib"))
   """
    __slots__ = ["encoding", "level", "lib"]
    def __init__(self, subcon, encoding, level=None):
        super(Compressed, self).__init__(subcon)
        self.encoding = encoding
        self.level = level
        if self.encoding == "zlib":
            import zlib
            self.lib = zlib
        elif self.encoding == "gzip":
            import gzip
            self.lib = gzip
        elif self.encoding == "bzip2":
            import bz2
            self.lib = bz2
        elif self.encoding == "lzma":
            import lzma
            self.lib = lzma
        else:
            import codecs
            self.lib = codecs
    def _decode(self, data, context):
        if self.encoding in ("zlib", "gzip", "bzip2", "lzma"):
            return self.lib.decompress(data)
        return self.lib.decode(data, self.encoding)
    def _encode(self, data, context):
        if self.encoding in ("zlib", "gzip", "bzip2", "lzma"):
            if self.level is None or self.encoding == "lzma":
                return self.lib.compress(data)
            else:
                return self.lib.compress(data, self.level)
        return self.lib.encode(data, self.encoding)


#===============================================================================
# lazy equivalents
#===============================================================================
class LazyStruct(Construct):
    r"""
    Equivalent to Struct construct, however fixed size members are parsed on demand, others are parsed immediately. If entire struct is fixed size then entire parse is essentially one stream seek.

    .. seealso:: Equivalent to :func:`~construct.core.Struct`.

    .. warning:: Struct members that depend on earlier context entries do not work properly, because since Struct is lazy, there is no guarantee that previous members were parsed and put into context dictionary.

    """
    __slots__ = ["subcons", "offsetmap", "totalsize", "subsizes", "keys"]
    def __init__(self, *subcons, **kw):
        super(LazyStruct, self).__init__()
        self.subcons = list(subcons) + list(k/v for k,v in kw.items()) 

        try:
            keys = Container()
            self.offsetmap = {}
            at = 0
            for sc in self.subcons:
                if sc.flagembedded:
                    raise SizeofError
                if sc.name is not None:
                    keys[sc.name] = None
                    self.offsetmap[sc.name] = (at, sc)
                at += sc.sizeof()
            self.totalsize = at
            self.keys = list(keys.keys())
        except SizeofError:
            self.offsetmap = None
            self.totalsize = None

        self.subsizes = []
        for sc in self.subcons:
            try:
                self.subsizes.append(sc.sizeof())
            except SizeofError:
                self.subsizes.append(None)

    def _parse(self, stream, context, path):
        if self.offsetmap is not None:
            position = stream.tell()
            stream.seek(self.totalsize, 1)
            return LazyContainer(self.keys, self.offsetmap, {}, stream, position, context)
        context = Container(_ = context)
        offsetmap = {}
        keys = Container()
        values = {}
        position = stream.tell()
        for (sc,size) in zip(self.subcons, self.subsizes):
            if sc.flagembedded:
                subobj = list(sc._parse(stream, context, path).items())
                keys.update(subobj)
                values.update(subobj)
                context.update(subobj)
            elif size is None:
                subobj = sc._parse(stream, context, path)
                if sc.name is not None:
                    keys[sc.name] = None
                    values[sc.name] = subobj
                    context[sc.name] = subobj
            else:
                if sc.name is not None:
                    keys[sc.name] = None
                    offsetmap[sc.name] = (stream.tell(), sc)
                stream.seek(size, 1)
        return LazyContainer(list(keys.keys()), offsetmap, values, stream, 0, context)

    def _build(self, obj, stream, context, path):
        context = Container(_ = context)
        context.update(obj)
        for sc in self.subcons:
            if sc.flagembedded:
                subobj = obj
            elif sc.flagbuildnone:
                subobj = obj.get(sc.name, None)
            else:
                subobj = obj[sc.name]
            buildret = sc._build(subobj, stream, context, path)
            if buildret is not None:
                if sc.flagembedded:
                    context.update(buildret)
                if sc.name is not None:
                    context[sc.name] = buildret
        return context

    def _sizeof(self, context, path):
        if self.totalsize is not None:
            return self.totalsize
        else:
            raise SizeofError("cannot calculate size, not all members are fixed size")


class LazyRange(Construct):
    r"""
    Equivalent to Range construct, but members are parsed on demand. Works only with fixed size subcon. Entire parse is essentially one stream seek.

    .. seealso:: Equivalent to :func:`~construct.core.Range`.

    """
    __slots__ = ["subcon", "min", "max", "subsize"]
    def __init__(self, min, max, subcon):
        super(LazyRange, self).__init__()
        self.subcon = subcon
        self.min = min
        self.max = max
        self.subsize = subcon.sizeof()

    def _parse(self, stream, context, path):
        currentmin = self.min(context) if callable(self.min) else self.min
        currentmax = self.max(context) if callable(self.max) else self.max
        if not 0 <= currentmin <= currentmax:
            raise RangeError("unsane min %s and max %s" % (currentmin, currentmax))
        starts = stream.tell()
        ends = stream.seek(0,2)
        remaining = ends - starts
        objcount = min(remaining//self.subsize, currentmax)
        if objcount < currentmin:
            raise RangeError("not enough bytes %d to read the min %d of %d bytes each" % (remaining, currentmin, self.subsize))
        stream.seek(starts + objcount*self.subsize, 0)
        return LazyRangeContainer(self.subcon, self.subsize, objcount, stream, starts, context)

    def _build(self, obj, stream, context, path):
        currentmin = self.min(context) if callable(self.min) else self.min
        currentmax = self.max(context) if callable(self.max) else self.max
        if not 0 <= currentmin <= currentmax:
            raise RangeError("unsane min %s and max %s" % (currentmin, currentmax))
        if not isinstance(obj, collections.Sequence):
            raise RangeError("expected sequence type, found %s" % type(obj))
        if not currentmin <= len(obj) <= currentmax:
            raise RangeError("expected from %d to %d elements, found %d" % (currentmin, currentmax, len(obj)))
        try:
            for i,subobj in enumerate(obj):
                context[i] = subobj
                self.subcon._build(subobj, stream, context, path)
        except ConstructError:
            if len(obj) < currentmin:
                raise RangeError("expected %d to %d, found %d" % (currentmin, currentmax, len(obj)))

    def _sizeof(self, context, path):
        try:
            currentmin = self.min(context) if callable(self.min) else self.min
            currentmax = self.max(context) if callable(self.max) else self.max
            if not 0 <= currentmin <= currentmax:
                raise RangeError("unsane min %s and max %s" % (currentmin, currentmax))
            if currentmin == currentmax:
                return self.min * self.subsize
            else:
                raise SizeofError("cannot calculate size, min not equal to max")
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


class LazySequence(Construct):
    r"""
    Equivalent to Sequence construct, however fixed size members are parsed on demand, others are parsed immediately. If entire sequence is fixed size then entire parse is essentially one seek.

    .. seealso:: Equivalent to :func:`~construct.core.Sequence`.

    """
    __slots__ = ["subcons", "offsetmap", "totalsize", "subsizes"]
    def __init__(self, *subcons, **kw):
        super(LazySequence, self).__init__()
        self.subcons = list(subcons) + list(k/v for k,v in kw.items())

        try:
            self.offsetmap = {}
            at = 0
            for i,sc in enumerate(self.subcons):
                if sc.flagembedded:
                    raise SizeofError
                self.offsetmap[i] = (at, sc)
                at += sc.sizeof()
            self.totalsize = at
        except SizeofError:
            self.offsetmap = None
            self.totalsize = None

        self.subsizes = []
        for sc in self.subcons:
            try:
                self.subsizes.append(sc.sizeof())
            except SizeofError:
                self.subsizes.append(None)

    def _parse(self, stream, context, path):
        context = Container(_ = context)
        if self.totalsize is not None:
            position = stream.tell()
            stream.seek(self.totalsize, 1)
            return LazySequenceContainer(len(self.subcons), self.offsetmap, {}, stream, position, context)
        offsetmap = {}
        values = {}
        i = 0
        for sc,size in zip(self.subcons, self.subsizes):
            if sc.flagembedded:
                subobj = list(sc._parse(stream, context, path))
                for e in subobj:
                    values[i] = e
                    context[i] = e
                    i += 1
            elif size is None:
                obj = sc._parse(stream, context, path)
                values[i] = obj
                context[i] = obj
                i += 1
            else:
                offsetmap[i] = (stream.tell(), sc)
                stream.seek(size, 1)
                i += 1
        return LazySequenceContainer(i, offsetmap, values, stream, 0, context)

    def _build(self, obj, stream, context, path):
        context = Container(_ = context)
        objiter = iter(obj)
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = objiter
            else:
                subobj = next(objiter)
                if sc.name is not None:
                    context[sc.name] = subobj
            context[i] = subobj
            buildret = sc._build(subobj, stream, context, path)
            if buildret is not None:
                if sc.flagembedded:
                    context.update(buildret)
                if sc.name is not None:
                    context[sc.name] = buildret
                context[i] = buildret

    def _sizeof(self, context, path):
        if self.totalsize is not None:
            return self.totalsize
        else:
            raise SizeofError("cannot calculate size, not all members are fixed size")


class OnDemand(Subconstruct):
    r"""
    Allows for lazy parsing of one field. When parsing, it will return a parameterless function that when called, will return the parsed value. Object is cached after first parsing, so non-deterministic subcons will be affected. Works only with fixed size subcon.

    :param subcon: the subcon to read/write on demand, must be fixed size

    Example::

        >>> d = OnDemand(Byte)
        >>> d.parse(b"\xff")
        <function OnDemand._parse.<locals>.<lambda> at 0x7fdc241cfc80>
        >>> _()
        255
        >>> d.build(255)
        b'\xff'

        Can also re-build from the lambda returned at parsing.

        >>> d.parse(b"\xff")
        <function OnDemand._parse.<locals>.<lambda> at 0x7fcbd9855f28>
        >>> d.build(_)
        b'\xff'
    """
    def _parse(self, stream, context, path):
        offset = stream.tell()
        stream.seek(self.subcon._sizeof(context, path), 1)
        cache = {}
        def effectuate():
            if not cache:
                fallback = stream.tell()
                stream.seek(offset)
                obj = self.subcon._parse(stream, context, path)
                stream.seek(fallback)
                cache["value"] = obj
            return cache["value"]
        return effectuate
    def _build(self, obj, stream, context, path):
        obj = obj() if callable(obj) else obj
        return self.subcon._build(obj, stream, context, path)


class LazyBound(Construct):
    r"""
    Lazy-bound construct that binds to the construct only at runtime. Useful for recursive data structures (like linked lists or trees), where a construct needs to refer to itself (while it does not exist yet).

    :param subconfunc: a context function returning a Construct (derived) instance, can also return Pass or itself

    Example::

        >>> d = Struct(
        ...     "value"/Byte,
        ...     "next"/If(this.value > 0, LazyBound(lambda ctx: d)),
        ... )
        ...
        >>> d.parse(b"\x05\x09\x00")
        Container(value=5)(next=Container(value=9)(next=Container(value=0)(next=None)))
        ...
        >>> print(d.parse(b"\x05\x09\x00"))
        Container:
            value = 5
            next = Container:
                value = 9
                next = Container:
                    value = 0
                    next = None
    """
    __slots__ = ["subconfunc"]
    def __init__(self, subconfunc):
        super(LazyBound, self).__init__()
        self.subconfunc = subconfunc
    def _parse(self, stream, context, path):
        return self.subconfunc(context)._parse(stream, context, path)
    def _build(self, obj, stream, context, path):
        return self.subconfunc(context)._build(obj, stream, context, path)
    def _sizeof(self, context, path):
        try:
            return self.subconfunc(context)._sizeof(context, path)
        except (KeyError, AttributeError):
            raise SizeofError("cannot calculate size, key not found in context")


#===============================================================================
# mappings
#===============================================================================
class Mapping(Adapter):
    r"""
    Adapter that maps objects to other objects. Translates objects before parsing and before building.

    :param subcon: the subcon to map
    :param decoding: the decoding (parsing) mapping as a dict
    :param encoding: the encoding (building) mapping as a dict
    :param decdefault: the default return value when object is not found in the mapping, if no object is given an exception is raised, if ``Pass`` is used, the unmapped object will be passed as-is
    :param encdefault: the default return value when object is not found in the mapping, if no object is given an exception is raised, if ``Pass`` is used, the unmapped object will be passed as-is

    Example::

        ???
    """
    __slots__ = ["encoding", "decoding", "encdefault", "decdefault"]
    def __init__(self, subcon, decoding, encoding, decdefault=NotImplemented, encdefault=NotImplemented):
        super(Mapping, self).__init__(subcon)
        self.decoding = decoding
        self.encoding = encoding
        self.decdefault = decdefault
        self.encdefault = encdefault
    def _encode(self, obj, context):
        try:
            return self.encoding[obj]
        except (KeyError, TypeError):
            if self.encdefault is NotImplemented:
                raise MappingError("no encoding mapping for %r" % (obj,))
            if self.encdefault is Pass:
                return obj
            return self.encdefault
    def _decode(self, obj, context):
        try:
            return self.decoding[obj]
        except (KeyError, TypeError):
            if self.decdefault is NotImplemented:
                raise MappingError("no decoding mapping for %r" % (obj,))
            if self.decdefault is Pass:
                return obj
            return self.decdefault


def SymmetricMapping(subcon, mapping, default=NotImplemented):
    r"""
    Defines a symmetric mapping, same mapping is used on parsing and building.

    .. seealso:: Based on :func:`~construct.core.Mapping`.

    :param subcon: the subcon to map
    :param encoding: the mapping as a dict
    :param decdefault: the default return value when object is not found in the mapping, if no object is given an exception is raised, if ``Pass`` is used, the unmapped object will be passed as-is

    Example::

        ???
    """
    return Mapping(subcon,
        encoding = mapping,
        decoding = dict((v,k) for k,v in mapping.items()),
        encdefault = default,
        decdefault = default,
    )


@singleton
def Flag():
    r"""
    One byte (or one bit) field that maps to True or False. Other non-zero bytes are also considered True.

    Example::

        >>> Flag.parse(b"\x01")
        True
        >>> Flag.build(True)
        b'\x01'
    """
    return SymmetricMapping(Byte, {True : 1, False : 0}, default=True)


class Enum(Subconstruct):
    r"""
    Translates unicode label names to subcon values, and vice versa. 

    :param subcon: the subcon to map
    :param \*\*mapping: keyword arguments which serve as the mapping
    :param default: an optional, keyword-only argument that specifies the default value to use when an unknown labels gets build, can overlap with some existing label, if Pass then parsing returns "default" label and building skips stream

    :raises MappingError: when label (during building) or value (during parsing) cannot be translated, and no default was provided

    Example::

        >>> d = Enum(Byte, zero=0, one=1)
        >>> d.parse(b"\x01")
        'one'
        >>> d.parse(b"\xff")
        construct.core.MappingError: no decoding mapping for 255
        >>> d.build("one")
        b'\x01'
        >>> d.build(1)
        b'\x01'
    """
    __slots__ = ["default", "encmapping", "decmapping"]
    def __init__(self, subcon, default=NotImplemented, **mapping):
        super(Enum, self).__init__(subcon)
        self.default = default
        self.encmapping =      {k:v for k,v in mapping.items()}
        self.encmapping.update({v:v for k,v in mapping.items()})
        self.decmapping =      {v:k for k,v in mapping.items()}
        self.decmapping.update({k:k for k,v in mapping.items()})
        if self.default is not NotImplemented and self.default is not Pass:
            if True:
                self.decmapping.update({"default":default})
            if default not in self.decmapping:
                self.decmapping.update({default:"default"})
    def _parse(self, stream, context, path):
        obj2 = self.subcon._parse(stream, context, path)
        try:
            obj = self.decmapping[obj2]
        except KeyError:
            if self.default is NotImplemented:
                raise MappingError("no mapping for %r, no default either" % (obj2,))
            if self.default is Pass:
                return "default"
            return "default"
        return obj
    def _build(self, obj, stream, context, path):
        try:
            obj2 = self.encmapping[obj]
        except KeyError:
            if self.default is NotImplemented:
                raise MappingError("no mapping for %r, no default either" % (obj,))
            if self.default is Pass:
                return
            obj = "default"
            obj2 = self.default
        self.subcon._build(obj2, stream, context, path)
        return obj


class FlagsEnum(Adapter):
    r"""
    Set of flag values mapping. Each flag is extracted from the number, resulting in a FlagsContainer dict that has each key assigned True or False.

    :param subcon: the subcon to extract
    :param \*\*flags: a dictionary mapping flag-names to their value

    Example::

        >>> d = FlagsEnum(Byte, a=1, b=2, c=4, d=8)
        >>> d.parse(b"\x03")
        Container(c=False)(b=True)(a=True)(d=False)
    """
    __slots__ = ["flags"]
    def __init__(self, subcon, **flags):
        super(FlagsEnum, self).__init__(subcon)
        self.flags = flags
    def _encode(self, obj, context):
        try:
            flags = 0
            for name,value in obj.items():
                if value:
                    flags |= self.flags[name]
            return flags
        except AttributeError:
            raise MappingError("not a mapping type: %r" % (obj,))
        except KeyError:
            raise MappingError("unknown flag: %s" % (name,))
    def _decode(self, obj, context):
        obj2 = FlagsContainer()
        for name,value in self.flags.items():
            obj2[name] = bool(obj & value)
        return obj2


#===============================================================================
# adapters and validators
#===============================================================================
class ExprAdapter(Adapter):
    r"""
    A generic adapter that takes ``encoder`` and ``decoder`` as parameters. You can use ExprAdapter instead of writing a full-blown class when only a simple lambda is needed.

    :param subcon: the subcon to adapt
    :param encoder: a function that takes (obj, context) and returns an encoded version of obj, or None for identity
    :param decoder: a function that takes (obj, context) and returns an decoded version of obj, or None for identity

    Example::

        Ident = ExprAdapter(Byte,
            encoder = lambda obj,ctx: obj+1,
            decoder = lambda obj,ctx: obj-1, )
    """
    __slots__ = ["_encode", "_decode"]
    def __init__(self, subcon, encoder, decoder):
        super(ExprAdapter, self).__init__(subcon)
        ident = lambda obj,ctx: obj
        self._encode = encoder if callable(encoder) else ident
        self._decode = decoder if callable(decoder) else ident


class ExprSymmetricAdapter(ExprAdapter):
    def __init__(self, subcon, encoder):
        super(ExprAdapter, self).__init__(subcon)
        ident = lambda obj,ctx: obj
        self._encode = encoder if callable(encoder) else ident
        self._decode = self._encode


class ExprValidator(Validator):
    r"""
    A generic adapter that takes ``validator`` as parameter. You can use ExprValidator instead of writing a full-blown class when only a simple expression is needed.

    :param subcon: the subcon to adapt
    :param encoder: a function that takes (obj, context) and returns a bool

    Example::

        OneOf = ExprValidator(Byte,
            validator = lambda obj,ctx: obj in [1,3,5])
    """
    def __init__(self, subcon, validator):
        super(ExprValidator, self).__init__(subcon)
        self._validate = validator


def OneOf(subcon, valids):
    r"""
    Validates that the object is one of the listed values, both during parsing and building. Note that providing a set instead of a list may increase performance.

    Notice that `OneOf(dtype, [value])` is essentially equivalent to `Const(dtype, value)`.

    :param subcon: a construct to validate
    :param valids: a collection implementing __contains__

    :raises ValidationError: when actual value is not among valids

    Example::

        >>> d = OneOf(Byte, [1,2,3])
        >>> d.parse(b"\x01")
        1
        >>> d.parse(b"\xff")
        construct.core.ValidationError: ('object failed validation', 255)

        >>> d = OneOf(Bytes(2), b"1234567890")
        >>> d.parse(b"78")
        b'78'
        >>> d.parse(b"19")
        construct.core.ValidationError: ('invalid object', b'19')
    """
    return ExprValidator(subcon, lambda obj,ctx: obj in valids)


def NoneOf(subcon, invalids):
    r"""
    Validates that the object is none of the listed values, both during parsing and building.

    :param subcon: a construct to validate
    :param valids: a collection implementing __contains__

    :raises ValidationError: when actual value is among invalids

    """
    return ExprValidator(subcon, lambda obj,ctx: obj not in invalids)


def Filter(predicate, subcon):
    r"""
    Filters a list leaving only the elements that passed through the validator.

    :param subcon: a construct to validate, usually a Range Array Sequence
    :param predicate: a function taking (obj, context) and returning a bool

    Example::

        >>> d = Filter(obj_ != 0, Byte[:])
        >>> d.parse(b"\x00\x02\x00")
        [2]
        >>> d.build([0,1,0,2,0])
        b'\x01\x02'
    """
    return ExprSymmetricAdapter(subcon, lambda obj,ctx: [x for x in obj if predicate(x,ctx)])


class Slicing(Adapter):
    r"""
    Adapter for slicing a list (getting a slice from that list). Works with Range and Sequence and their lazy equivalents.

    :param subcon: the subcon to slice
    :param count: expected number of elements, needed during building
    :param start: start index (or None for entire list)
    :param stop: stop index (or None for up-to-end)
    :param step: step (or 1 for every element)
    :param empty: value to fill the list with during building

    Example::

        ???
    """
    __slots__ = ["count", "start", "stop", "step", "empty"]
    def __init__(self, subcon, count, start, stop, step=1, empty=None):
        super(Slicing, self).__init__(subcon)
        self.count = count
        self.start = start
        self.stop = stop
        self.step = step
        self.empty = empty
    def _encode(self, obj, context):
        if self.start is None:
            return obj
        elif self.stop is None:
            output = [self.empty] * self.count
            output[self.start::self.step] = obj
        else:
            output = [self.empty] * self.count
            output[self.start:self.stop:self.step] = obj
        return output
    def _decode(self, obj, context):
        return obj[self.start:self.stop:self.step]


class Indexing(Adapter):
    r"""
    Adapter for indexing a list (getting a single item from that list). Works with Range and Sequence and their lazy equivalents.

    :param subcon: the subcon to index
    :param count: expected number of elements, needed during building
    :param index: the index of the list to get
    :param empty: value to fill the list with during building

    Example::

        ???
    """
    __slots__ = ["count", "index", "empty"]
    def __init__(self, subcon, count, index, empty=None):
        super(Indexing, self).__init__(subcon)
        self.count = count
        self.index = index
        self.empty = empty
    def _encode(self, obj, context):
        output = [self.empty] * self.count
        output[self.index] = obj
        return output
    def _decode(self, obj, context):
        return obj[self.index]


def Hex(subcon):
    r"""
    Adapter for hex-dumping bytes. It returns a hex dump when parsing, and un-dumps when building.

    Example::

        >>> d = Hex(GreedyBytes)
        >>> d.parse(b"abcd")
        b'61626364'
        >>> d.build("01020304")
        b'\x01\x02\x03\x04'
    """
    return ExprAdapter(subcon,
        encoder = lambda obj,ctx: None if subcon.flagbuildnone else unhexlify(obj),
        decoder = lambda obj,ctx: hexlify(obj),
    )


def HexDump(subcon, linesize=16):
    r"""
    Adapter for hex-dumping bytes. It returns a hex dump when parsing, and un-dumps when building.

    :param linesize: default 16 bytes per line
    :param buildraw: by default build takes the same format that parse returns, set to build from a bytes directly

    Example::

        >>> d = HexDump(Bytes(10))
        >>> d.parse(b"12345abc;/")
        '0000   31 32 33 34 35 61 62 63 3b 2f                     12345abc;/       \n'
    """
    return ExprAdapter(subcon,
        encoder = lambda obj,ctx: None if subcon.flagbuildnone else hexundump(obj, linesize=linesize),
        decoder = lambda obj,ctx: hexdump(obj, linesize=linesize),
    )


#===============================================================================
# strings
#===============================================================================
globalstringencoding = None


def setglobalstringencoding(encoding):
    r"""
    Sets the encoding globally for all String/PascalString/CString/GreedyString instances.

    :param encoding: a string like "utf8", or None which means working with bytes (not unicode)
    """
    global globalstringencoding
    globalstringencoding = encoding


class StringEncoded(Adapter):
    """Used internally."""
    __slots__ = ["encoding"]
    def __init__(self, subcon, encoding):
        super(StringEncoded, self).__init__(subcon)
        self.encoding = encoding
    def _decode(self, obj, context):
        encoding = self.encoding or globalstringencoding
        if encoding:
            if isinstance(encoding, str):
                obj = obj.decode(encoding)
            else:
                obj = encoding.decode(obj)
        return obj
    def _encode(self, obj, context):
        encoding = self.encoding or globalstringencoding
        if not isinstance(obj, bytes):
            if not encoding:
                raise StringError("no encoding provided when processing a unicode obj")
            if isinstance(encoding, str):
                obj = obj.encode(encoding)
            else:
                obj = encoding.encode(obj)
        return obj


class StringPaddedTrimmed(Adapter):
    """Used internally."""
    __slots__ = ["length", "padchar", "paddir", "trimdir"]
    def __init__(self, length, subcon, padchar=b"\x00", paddir="right", trimdir="right"):
        if not isinstance(padchar, bytes):
            raise StringError("padchar must be b-string character")
        super(StringPaddedTrimmed, self).__init__(subcon)
        self.length = length
        self.padchar = padchar
        self.paddir = paddir
        self.trimdir = trimdir
    def _decode(self, obj, context):
        if self.paddir == "right":
            obj = obj.rstrip(self.padchar)
        elif self.paddir == "left":
            obj = obj.lstrip(self.padchar)
        elif self.paddir == "center":
            obj = obj.strip(self.padchar)
        else:
            raise StringError("paddir must be one of: right left center")
        return obj
    def _encode(self, obj, context):
        length = self.length(context) if callable(self.length) else self.length
        if self.paddir == "right":
            obj = obj.ljust(length, self.padchar[0:1])
        elif self.paddir == "left":
            obj = obj.rjust(length, self.padchar[0:1])
        elif self.paddir == "center":
            obj = obj.center(length, self.padchar[0:1])
        else:
            raise StringError("paddir must be one of: right left center")
        if len(obj) > length:
            if self.trimdir == "right":
                obj = obj[:length]
            elif self.trimdir == "left":
                obj = obj[-length:]
            else:
                raise StringError("expected a string of length %s given %s (%r)" % (length,len(obj),obj))
        return obj


def String(length, encoding=None, padchar=b"\x00", paddir="right", trimdir="right"):
    r"""
    Configurable, fixed-length or variable-length string field.

    When parsing, the byte string is stripped of pad character (as specified) from the direction (as specified) then decoded (as specified). Length is a constant integer or a context function.
    When building, the string is encoded (as specified) then padded (as specified) from the direction (as specified) or trimmed (as specified).

    The padding character and direction must be specified for padding to work. The trim direction must be specified for trimming to work.

    If encoding is not specified, it works with bytes (not unicode strings).

    :param length: length in bytes (not unicode characters), as integer or context function
    :param encoding: encoding (eg. "utf8") or None for bytes
    :param padchar: bytes character to pad out strings (by default b"\x00")
    :param paddir: direction to pad out strings (one of: right left both)
    :param trimdir: direction to trim strings (one of: right left)

    Example::

        >>> d = String(10)
        >>> d.build(b"hello")
        b'hello\x00\x00\x00\x00\x00'
        >>> d.parse(_)
        b'hello'
        >>> d.sizeof()
        10

        >>> d = String(10, encoding="utf8")
        >>> d.build(u"Афон")
        b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00\x00'
        >>> d.parse(_)
        u'Афон'

        >>> d = String(10, padchar=b"XYZ", paddir="center")
        >>> d.build(b"abc")
        b'XXXabcXXXX'
        >>> d.parse(b"XYZabcXYZY")
        b'abc'

        >>> d = String(10, trimdir="right")
        >>> d.build(b"12345678901234567890")
        b'1234567890'
    """
    return StringEncoded(
        StringPaddedTrimmed(length, Bytes(length), padchar, paddir, trimdir),
        encoding)


def PascalString(lengthfield, encoding=None):
    r"""
    Length-prefixed string. The length field can be variable length (such as VarInt) or fixed length (such as Int64ul). VarInt is recommended for new designs. Stored length is in bytes, not characters.

    :param lengthfield: a field used to parse and build the length (eg. VarInt Int64ul)
    :param encoding: encoding (eg. "utf8"), or None for bytes

    Example::

        >>> d = PascalString(VarInt, encoding="utf8")
        >>> d.build(u"Афон")
        b'\x08\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd'
        >>> d.parse(_)
        u'Афон'
    """
    return StringEncoded(Prefixed(lengthfield, GreedyBytes), encoding)


def CString(terminators=b"\x00", encoding=None):
    r"""
    String ending in a terminator byte.

    By default, the terminator is the \x00 byte character. Terminators field can be a longer bytes, and any one of the characters breaks parsing. First terminator byte is used when building.

    :param terminators: sequence of valid terminators, first is used when building, all are used when parsing
    :param encoding: encoding (eg. "utf8"), or None for bytes

    .. warning:: Do not use >1 byte encodings like UTF16 or UTF32 with string classes. This a known bug that has something to do with the fact that library inherently works with bytes (not codepoints) and codepoint-to-byte conversions are too tricky.

    Example::

        >>> d = CString(encoding="utf8")
        >>> d.build(u"Афон")
        b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00'
        >>> d.parse(_)
        u'Афон'
    """
    return StringEncoded(
        ExprAdapter(
            RepeatUntil(lambda obj,lst,ctx: int2byte(obj) in terminators, Byte),
            encoder = lambda obj,ctx: iterateints(obj+terminators),
            decoder = lambda obj,ctx: b''.join(int2byte(c) for c in obj[:-1])),
        encoding)


def GreedyString(encoding=None):
    r"""
    String that reads the rest of the stream until EOF, and writes a given string as is. If no encoding is specified, this is essentially GreedyBytes.

    :param encoding: encoding (eg. "utf8"), or None for bytes

    .. seealso:: Analog to :class:`~construct.core.GreedyBytes` and the same when no enoding is used.

    Example::

        >>> d = GreedyString(encoding="utf8")
        >>> d.build(u"Афон")
        b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd'
        >>> d.parse(_)
        u'Афон'
    """
    return StringEncoded(GreedyBytes, encoding)


#===============================================================================
# end of file
#===============================================================================
