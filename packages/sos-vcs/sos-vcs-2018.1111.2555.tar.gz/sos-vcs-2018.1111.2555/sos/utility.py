#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xbae409f

# Compiled with Coconut version 1.3.1 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Utiliy functions
import bz2  # line 6
import codecs  # line 6
import difflib  # line 6
import hashlib  # line 6
import logging  # line 6
import os  # line 6
import re  # line 6
sys = _coconut_sys  # line 6
import time  # line 6
START_TIME = time.time()  # line 6
try:  # line 7
    from typing import Any  # only required for mypy  # line 8
    from typing import Callable  # only required for mypy  # line 8
    from typing import Dict  # only required for mypy  # line 8
    from typing import FrozenSet  # only required for mypy  # line 8
    from typing import IO  # only required for mypy  # line 8
    from typing import List  # only required for mypy  # line 8
    from typing import Sequence  # only required for mypy  # line 8
    from typing import Tuple  # only required for mypy  # line 8
    from typing import Type  # only required for mypy  # line 8
    from typing import TypeVar  # only required for mypy  # line 8
    from typing import Union  # only required for mypy  # line 8
    Number = Union[int, float]  # line 9
except:  # typing not available (e.g. Python 2)  # line 10
    pass  # typing not available (e.g. Python 2)  # line 10
try:  # line 11
    import wcwidth  # line 11
except:  # optional dependency  # line 12
    pass  # optional dependency  # line 12
longint = eval("long") if sys.version_info.major < 3 else int  # type: Type  # for Python 2 compatibility  # line 13


verbose = os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv  # imported from utility, and only modified here  # line 16

# Classes
class Accessor(dict):  # line 19
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 20
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # line 21
        dict.__init__(_, mapping)  # line 21
    @_coconut_tco  # line 22
    def __getattribute__(_, name: 'str') -> 'Any':  # line 22
        try:  # line 23
            return _[name]  # line 23
        except:  # line 24
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 24

class Counter:  # line 26
    ''' A simple counter. Can be augmented to return the last value instead. '''  # line 27
    def __init__(_, initial: 'Number'=0) -> 'None':  # line 28
        _.value = initial  # type: Number  # line 28
    def inc(_, by=1) -> 'Number':  # line 29
        _.value += by  # line 29
        return _.value  # line 29

class EnumValue:  # line 31
    def __init__(_, tipe, name, value) -> 'None':  # line 32
        _.tipe, _.name, _.value = tipe, name, value  # line 32
    def __str__(_) -> 'str':  # line 33
        return "%s.%s" % (_.tipe, _.name)  # line 33
    def __repr__(_) -> 'str':  # line 34
        return "<enum '%s.%s'>" % (_.tipe, _.name)  # line 34

class Enum(dict):  # line 36
    def __init__(_, name: 'str', values: 'Union[List[Union[str, Tuple[str, Number]]], Dict[str, Number]]', first: 'int'=0, step: 'int'=1):  # line 37
        assert name  # line 38
        assert values  # line 39
        _.name = name  # type: str  # line 40
        _.values = {}  # type: Dict[Number, EnumValue]  # line 41
        if isinstance(values, list):  # line 42
            count = first  # type: int  # line 43
            for item in values:  # type: List[Union[str,Tuple[str,Number]]]  # line 44
                if isinstance(item, tuple):  # line 45
                    _.values[item[1]] = EnumValue(name, item[0], item[1])  # line 46
                    count = item[1] + step  # line 47
                else:  # str  # line 48
                    _.values[count] = EnumValue(name, item, count)  # line 49
                    count += step  # line 50
        elif isinstance(values, dict):  # line 51
            _.values.update({k: EnumValue(name, v, k) for v, k in values.items()})  # line 52
        else:  # line 53
            raise ValueError("Illegal values provided: expecting list(str), list of (str,num) or dict(str,num)")  # line 53
    def __str__(_) -> 'str':  # line 54
        return _.name  # line 54
    def __repr__(_) -> 'str':  # line 55
        return "<enum '%s'>" % _.name  # line 55
    @_coconut_tco  # line 56
    def entries(_) -> '_coconut.typing.Sequence[EnumValue]':  # line 56
        return _coconut_tail_call(list, sorted(_.values.values(), key=lambda v: v.value))  # line 56
    @_coconut_tco  # line 57
    def names(_) -> '_coconut.typing.Sequence[str]':  # line 57
        return _coconut_tail_call(list, sorted([v.name for v in _.values.values()]))  # line 57
    @_coconut_tco  # line 58
    def numbers(_) -> '_coconut.typing.Sequence[Number]':  # line 58
        return _coconut_tail_call(list, sorted(_.values.keys()))  # line 58
    @_coconut_tco  # line 59
    def __getattribute__(_, name: 'str') -> 'EnumValue':  # line 59
        try:  # line 60
            return [v for v in _.values.values() if v.name == name][0]  # line 60
        except:  # line 61
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 61
    def __getitem__(_, key: 'Number') -> 'str':  # line 62
        assert isinstance(key, (int, float))  # or decimal  # line 63
        return _.values[key]  # line 64
# TODO implement equal / is_ comparison

class Logger:  # line 67
    ''' Logger that supports many items. '''  # line 68
    def __init__(_, log):  # line 69
        _._log = log  # line 69
    def debug(_, *s):  # line 70
        _._log.debug(sjoin(*s))  # line 70
    def info(_, *s):  # line 71
        _._log.info(sjoin(*s))  # line 71
    def warn(_, *s):  # line 72
        _._log.warning(sjoin(*s))  # line 72
    def error(_, *s):  # line 73
        _._log.error(sjoin(*s))  # line 73


# Constants
_log = Logger(logging.getLogger(__name__))  # line 77
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 77
UTF8 = "utf_8"  # early used constant, not defined in standard library  # line 78
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress"]  # line 79
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # line 80
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # all lower-case normalized  # line 81
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # line 82
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 83
metaFolder = ".sos"  # type: str  # line 84
metaFile = ".meta"  # type: str  # line 85
bufSize = 1 << 20  # type: int  # 1 MiB  # line 86
SVN = "svn"  # line 87
SLASH = "/"  # line 88
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 89
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 90
lateBinding = Accessor({"verbose": False, "start": 0})  # type: Accessor  # line 91


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 95
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 95
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 95
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 95
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 95
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 96
    __slots__ = ()  # line 96
    __ne__ = _coconut.object.__ne__  # line 96
    def __new__(_cls, number, ctime, message=None):  # line 96
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 96

class PathInfo(_coconut_NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 97
    __slots__ = ()  # size == None means deleted in this revision  # line 97
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 97
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 98
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 98
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 98
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 99
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 99
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 99
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 100
    __slots__ = ()  # line 100
    __ne__ = _coconut.object.__ne__  # line 100
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 100
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 100

class GlobBlock(_coconut_NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 101
    __slots__ = ()  # for file pattern rename/move matching  # line 101
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 101
class GlobBlock2(_coconut_NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 102
    __slots__ = ()  # matching file pattern and input filename for translation  # line 102
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 102


# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 106
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 106
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 107
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 107
class MergeBlockType:  # modify = intra-line changes  # line 108
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 108


# Functions
try:  # line 112
    import chardet  # https://github.com/chardet/chardet  # line 113
    def detectEncoding(binary: 'bytes') -> 'str':  # line 114
        return chardet.detect(binary)["encoding"]  # line 114
except:  # line 115
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 116
        ''' Fallback if chardet library missing. '''  # line 117
        try:  # line 118
            binary.decode(UTF8)  # line 118
            return UTF8  # line 118
        except UnicodeError:  # line 119
            pass  # line 119
        try:  # line 120
            binary.decode("utf_16")  # line 120
            return "utf_16"  # line 120
        except UnicodeError:  # line 121
            pass  # line 121
        try:  # line 122
            binary.decode("cp1252")  # line 122
            return "cp1252"  # line 122
        except UnicodeError:  # line 123
            pass  # line 123
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 124

@_coconut_tco  # line 126
def wcswidth(string: 'str') -> 'int':  # line 126
    l = None  # type: int  # line 127
    try:  # line 128
        l = wcwidth.wcswitdh(string)  # line 129
        if l < 0:  # line 130
            return len(string)  # line 130
    except:  # line 131
        return _coconut_tail_call(len, string)  # line 131
    return l  # line 132

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # line 134
    return a & b if a else b  # line 134

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 136
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 136

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 138
    ''' Determine EOL style from a binary string. '''  # line 139
    lf = file.count(b"\n")  # type: int  # line 140
    cr = file.count(b"\r")  # type: int  # line 141
    crlf = file.count(b"\r\n")  # type: int  # line 142
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 143
        if lf != crlf or cr != crlf:  # line 144
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 144
        return b"\r\n"  # line 145
    if lf != 0 and cr != 0:  # line 146
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 146
    if lf > cr:  # Linux/Unix  # line 147
        return b"\n"  # Linux/Unix  # line 147
    if cr > lf:  # older 8-bit machines  # line 148
        return b"\r"  # older 8-bit machines  # line 148
    return None  # no new line contained, cannot determine  # line 149

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 151
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 151
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 151

try:  # line 153
    Splittable = TypeVar("Splittable", str, bytes)  # line 153
except:  # Python 2  # line 154
    pass  # Python 2  # line 154
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 155
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 155

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 157
    return (sep + (nl + sep).join(seq)) if seq else ""  # line 157

@_coconut_tco  # line 159
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 159
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 159

@_coconut_tco  # line 161
def hashStr(datas: 'str') -> 'str':  # line 161
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 161

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 163
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 163

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 165
    return lizt[index:].index(what) + index  # line 165

def getTermWidth() -> 'int':  # line 167
    try:  # line 167
        import termwidth  # line 168
    except:  # line 169
        return 80  # line 169
    return termwidth.getTermWidth()[0]  # line 170

def branchFolder(branch: 'int', revision: 'int', base=".", file=None) -> 'str':  # line 172
    return os.path.join(base, metaFolder, "b%d" % branch, "r%d" % revision) + ((os.sep + file) if file else "")  # line 172

def Exit(message: 'str'="", code=1) -> 'None':  # line 174
    print("[EXIT%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "") + (" " + message + "." if message != "" else ""), file=sys.stderr)  # line 174
    sys.exit(code)  # line 174

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 176
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 177
    _hash = hashlib.sha256()  # line 178
    wsize = 0  # type: longint  # line 179
    if saveTo and os.path.exists(saveTo):  # line 180
        Exit("Hash conflict. Leaving revision in inconsistent state. This should happen only once in a lifetime.")  # line 180
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 181
    with open(path, "rb") as fd:  # line 182
        while True:  # line 183
            buffer = fd.read(bufSize)  # line 184
            _hash.update(buffer)  # line 185
            if to:  # line 186
                to.write(buffer)  # line 186
            if len(buffer) < bufSize:  # line 187
                break  # line 187
        if to:  # line 188
            to.close()  # line 189
            wsize = os.stat(saveTo).st_size  # line 190
    return (_hash.hexdigest(), wsize)  # line 191

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 193
    ''' Utility. '''  # line 194
    for k, v in map.items():  # line 195
        if k in params:  # line 196
            return v  # line 196
    return default  # line 197

@_coconut_tco  # line 199
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 199
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 199

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 201
    encoding = None  # type: str  # line 201
    eol = None  # type: bytes  # line 201
    lines = []  # type: _coconut.typing.Sequence[str]  # line 202
    if filename is not None:  # line 203
        with open(filename, "rb") as fd:  # line 204
            content = fd.read()  # line 204
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 205
    eol = eoldet(content)  # line 206
    if filename is not None:  # line 207
        with codecs.open(filename, encoding=encoding) as fd:  # line 208
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 208
    elif content is not None:  # line 209
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 210
    else:  # line 211
        return (sys.getdefaultencoding(), b"\n", [])  # line 211
    return (encoding, eol, lines)  # line 212

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 214
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 219
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 220
    for path, pinfo in last.items():  # line 221
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 222
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 222
        vs = diff[path]  # reference to potentially changed path set  # line 223
        if vs.size is None:  # marked for deletion  # line 224
            changes.deletions[path] = pinfo  # marked for deletion  # line 224
            continue  # marked for deletion  # line 224
        if pinfo.size == None:  # re-added  # line 225
            changes.additions[path] = pinfo  # re-added  # line 225
            continue  # re-added  # line 225
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 226
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 226
    for path, pinfo in diff.items():  # added loop  # line 227
        if path not in last:  # line 228
            changes.additions[path] = pinfo  # line 228
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 229
    assert not any([path in changes.additions for path in changes.deletions])  # line 230
    return changes  # line 231

try:  # line 233
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 233
except:  # Python 2  # line 234
    pass  # Python 2  # line 234

@_coconut_tco  # line 236
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 236
    r = _old._asdict()  # line 236
    r.update(**_kwargs)  # line 236
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 236
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 239
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 239
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 240
    encoding = None  # type: str  # line 241
    othr = None  # type: _coconut.typing.Sequence[str]  # line 241
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 241
    curr = None  # type: _coconut.typing.Sequence[str]  # line 241
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 241
    differ = difflib.Differ()  # line 242
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 243
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 244
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 245
    except Exception as E:  # line 246
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 246
    if None not in [othreol, curreol] and othreol != curreol:  # line 247
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 247
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 248
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 249
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 250
    tmp = []  # type: List[str]  # block lines  # line 251
    last = " "  # line 252
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 253
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 254
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 254
            continue  # continue filling consecutive block, no matter what type of block  # line 254
        if line == "X":  # EOF marker - perform action for remaining block  # line 255
            if len(tmp) == 0:  # nothing left to do  # line 256
                break  # nothing left to do  # line 256
        if last == " ":  # block is same in both files TODO sometimes adds empty keep block at beginning of file?  # line 257
            if len(tmp) > 0:  # line 258
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 258
        elif last == "-":  # may be a deletion or replacement, store for later  # line 259
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 260
        elif last == "+":  # may be insertion or replacement  # line 261
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 262
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 263
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 264
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 265
                else:  # may have intra-line modifications  # line 266
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 267
                blocks.pop()  # remove TOS  # line 268
        elif last == "?":  # intra-line change comment  # line 269
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 270
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 271
        last = line[0]  # line 272
        tmp[:] = [line[2:]]  # line 273
    debug("Diff blocks: " + repr(blocks))  # line 274
    if diffOnly:  # line 275
        return blocks  # line 275
    output = []  # line 276
    for block in blocks:  # line 277
        if block.tipe == MergeBlockType.KEEP:  # line 278
            output.extend(block.lines)  # line 279
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 280
            output.extend(block.lines)  # line 281
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 282
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 283
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 283
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 284
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 284
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 285
            output.extend(block.lines)  # line 286
        elif block.tipe == MergeBlockType.MODIFY:  # changes.tipe marks intra-line changes  # line 287
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  character insert  # line 288
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 289
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 290
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 291
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 292
                if conflictResolution == ConflictResolution.THEIRS:  # line 293
                    output.extend(block.replaces.lines)  # line 294
                elif conflictResolution == ConflictResolution.MINE:  # line 295
                    output.extend(block.lines)  # line 296
                elif conflictResolution == ConflictResolution.ASK:  # line 297
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 298
                    print(ajoin("MIN ", block.lines, "\n"))  # line 299
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 300
                    debug("User selected %d" % reso)  # TODO enum output  # line 301
                    _coconut_match_check = False  # line 302
                    _coconut_match_to = reso  # line 302
                    if _coconut_match_to is None:  # line 302
                        _coconut_match_check = True  # line 302
                    if _coconut_match_check:  # line 302
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 303
                    _coconut_match_check = False  # line 304
                    _coconut_match_to = reso  # line 304
                    if _coconut_match_to == ConflictResolution.MINE:  # line 304
                        _coconut_match_check = True  # line 304
                    if _coconut_match_check:  # line 304
                        debug("Using mine")  # line 305
                        output.extend(block.lines)  # line 306
                    _coconut_match_check = False  # line 307
                    _coconut_match_to = reso  # line 307
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 307
                        _coconut_match_check = True  # line 307
                    if _coconut_match_check:  # line 307
                        debug("Using theirs")  # line 308
                        output.extend(block.replaces.lines)  # line 309
                    _coconut_match_check = False  # line 310
                    _coconut_match_to = reso  # line 310
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 310
                        _coconut_match_check = True  # line 310
                    if _coconut_match_check:  # line 310
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 311
                        output.extend(block.lines)  # line 312
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 313
                warn("Investigate this case")  # line 314
                output.extend(block.lines)  # default or not .replaces?  # line 315
    debug("Merge output: " + "; ".join(output))  # line 316
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 317
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 318
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 321
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 321
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 322
    if "^" in line:  # line 323
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 323
    if "+" in line:  # line 324
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 324
    if "-" in line:  # line 325
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 325
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # TODO detect and mark replacement from -/+  # line 326

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 328
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 329
    debug("Detecting root folders...")  # line 330
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 331
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 332
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 333
        contents = set(os.listdir(path))  # line 334
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 335
        choice = None  # type: _coconut.typing.Optional[str]  # line 336
        if len(vcss) > 1:  # line 337
            choice = SVN if SVN in vcss else vcss[0]  # line 338
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 339
        elif len(vcss) > 0:  # line 340
            choice = vcss[0]  # line 340
        if not vcs[0] and choice:  # memorize current repo root  # line 341
            vcs = (path, choice)  # memorize current repo root  # line 341
        new = os.path.dirname(path)  # get parent path  # line 342
        if new == path:  # avoid infinite loop  # line 343
            break  # avoid infinite loop  # line 343
        path = new  # line 344
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 345
        if vcs[0]:  # already detected vcs base and command  # line 346
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 346
        sos = path  # line 347
        while True:  # continue search for VCS base  # line 348
            new = os.path.dirname(path)  # get parent path  # line 349
            if new == path:  # no VCS folder found  # line 350
                return (sos, None, None)  # no VCS folder found  # line 350
            path = new  # line 351
            contents = set(os.listdir(path))  # line 352
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 353
            choice = None  # line 354
            if len(vcss) > 1:  # line 355
                choice = SVN if SVN in vcss else vcss[0]  # line 356
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 357
            elif len(vcss) > 0:  # line 358
                choice = vcss[0]  # line 358
            if choice:  # line 359
                return (sos, path, choice)  # line 359
    return (None, vcs[0], vcs[1])  # line 360

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 362
    index = 0  # type: int  # line 363
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 364
    while index < len(pattern):  # line 365
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 366
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 366
            continue  # line 366
        if pattern[index] in "*?":  # line 367
            count = 1  # type: int  # line 368
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 369
                count += 1  # line 369
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 370
            index += count  # line 370
            continue  # line 370
        if pattern[index:index + 2] == "[!":  # line 371
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 371
            index += len(out[-1][1])  # line 371
            continue  # line 371
        count = 1  # line 372
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 373
            count += 1  # line 373
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 374
        index += count  # line 374
    return out  # line 375

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 377
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 378
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 379
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 381
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 381
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 382
        Exit("Source and target file patterns differ in semantics")  # line 382
    return (ot, nt)  # line 383

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 385
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 386
    pairs = []  # type: List[Tuple[str, str]]  # line 387
    for filename in filenames:  # line 388
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 389
        nextliteral = 0  # type: int  # line 390
        parsedOld = []  # type: List[GlobBlock2]  # line 391
        index = 0  # type: int  # line 392
        for part in oldPattern:  # match everything in the old filename  # line 393
            if part.isLiteral:  # line 394
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 394
                index += len(part.content)  # line 394
                nextliteral += 1  # line 394
            elif part.content.startswith("?"):  # line 395
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 395
                index += len(part.content)  # line 395
            elif part.content.startswith("["):  # line 396
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 396
                index += 1  # line 396
            elif part.content == "*":  # line 397
                if nextliteral >= len(literals):  # line 398
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 398
                    break  # line 398
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 399
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 400
                index = nxt  # line 400
            else:  # line 401
                Exit("Invalid file pattern specified for move/rename")  # line 401
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 402
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 403
        nextliteral = 0  # line 404
        nextglob = 0  # type: int  # line 404
        outname = []  # type: List[str]  # line 405
        for part in newPattern:  # generate new filename  # line 406
            if part.isLiteral:  # line 407
                outname.append(literals[nextliteral].content)  # line 407
                nextliteral += 1  # line 407
            else:  # line 408
                outname.append(globs[nextglob].matches)  # line 408
                nextglob += 1  # line 408
        pairs.append((filename, "".join(outname)))  # line 409
    return pairs  # line 410

@_coconut_tco  # line 412
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 412
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 416
    if not actions:  # line 417
        return []  # line 417
    sources = None  # type: List[str]  # line 418
    targets = None  # type: List[str]  # line 418
    sources, targets = [list(l) for l in zip(*actions)]  # line 419
    last = len(actions)  # type: int  # line 420
    while last > 1:  # line 421
        clean = True  # type: bool  # line 422
        for i in range(1, last):  # line 423
            try:  # line 424
                index = targets[:i].index(sources[i])  # type: int  # line 425
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 426
                targets.insert(index, targets.pop(i))  # line 427
                clean = False  # line 428
            except:  # target not found in sources: good!  # line 429
                continue  # target not found in sources: good!  # line 429
        if clean:  # line 430
            break  # line 430
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 431
    if exitOnConflict:  # line 432
        for i in range(1, len(actions)):  # line 433
            if sources[i] in targets[:i]:  # line 434
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 434
    return _coconut_tail_call(list, zip(sources, targets))  # line 435

def relativize(root: 'str', path: 'str') -> 'Tuple[str, str]':  # line 437
    ''' Determine OS-independent relative folder path, and relative pattern path. '''  # line 438
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(path)), root).replace(os.sep, SLASH)  # line 439
    return relpath, os.path.join(relpath, os.path.basename(path)).replace(os.sep, SLASH)  # line 440

def parseOnlyOptions(root: 'str', options: '_coconut.typing.Sequence[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 442
    ''' Returns set of --only arguments, and set or --except arguments. '''  # line 443
    cwd = os.getcwd()  # type: str  # line 444
    onlys = []  # type: List[str]  # line 445
    excps = []  # type: List[str]  # line 445
    index = 0  # type: int  # line 445
    while True:  # line 446
        try:  # line 447
            index = 1 + listindex(options, "--only", index)  # line 448
            onlys.append(options[index])  # line 449
        except:  # line 450
            break  # line 450
    index = 0  # line 451
    while True:  # line 452
        try:  # line 453
            index = 1 + listindex(options, "--except", index)  # line 454
            excps.append(options[index])  # line 455
        except:  # line 456
            break  # line 456
    return (frozenset((relativize(root, o)[1] for o in onlys)) if onlys else None, frozenset((relativize(root, e)[1] for e in excps)) if excps else None)  # line 457
