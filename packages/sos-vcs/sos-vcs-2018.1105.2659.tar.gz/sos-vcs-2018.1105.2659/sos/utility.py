#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xdec38068

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

class Logger:  # line 31
    ''' Logger that supports many items. '''  # line 32
    def __init__(_, log):  # line 33
        _._log = log  # line 33
    def debug(_, *s):  # line 34
        _._log.debug(sjoin(*s))  # line 34
    def info(_, *s):  # line 35
        _._log.info(sjoin(*s))  # line 35
    def warn(_, *s):  # line 36
        _._log.warning(sjoin(*s))  # line 36
    def error(_, *s):  # line 37
        _._log.error(sjoin(*s))  # line 37


# Constants
_log = Logger(logging.getLogger(__name__))  # line 41
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 41
UTF8 = "utf_8"  # early used constant, not defined in standard library  # line 42
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress"]  # line 43
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # line 44
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # all lower-case normalized  # line 45
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # line 46
PROGRESS_MARKER = ["|", "/", "-", "\\"]  # line 47
metaFolder = ".sos"  # type: str  # line 48
metaFile = ".meta"  # type: str  # line 49
bufSize = 1 << 20  # type: int  # 1 MiB  # line 50
SVN = "svn"  # line 51
SLASH = "/"  # line 52
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs"}  # type: Dict[str, str]  # line 53
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 54
lateBinding = Accessor({"verbose": False, "start": 0})  # type: Accessor  # line 55


# Value types
class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]')])):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 59
    __slots__ = ()  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 59
    __ne__ = _coconut.object.__ne__  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 59
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[]):  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 59
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked))  # tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place  # line 59
# tracked is a list on purpose, as serialization to JSON needs effort and frequent access is not taking place
class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 60
    __slots__ = ()  # line 60
    __ne__ = _coconut.object.__ne__  # line 60
    def __new__(_cls, number, ctime, message=None):  # line 60
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 60

class PathInfo(_coconut_NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 61
    __slots__ = ()  # size == None means deleted in this revision  # line 61
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 61
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 62
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 62
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 62
class Range(_coconut_NamedTuple("Range", [("tipe", 'int'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # line 63
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # line 63
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # line 63
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'int'), ("lines", '_coconut.typing.Sequence[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 64
    __slots__ = ()  # line 64
    __ne__ = _coconut.object.__ne__  # line 64
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 64
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 64

class GlobBlock(_coconut_NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 65
    __slots__ = ()  # for file pattern rename/move matching  # line 65
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 65
class GlobBlock2(_coconut_NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 66
    __slots__ = ()  # matching file pattern and input filename for translation  # line 66
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 66


# Enums
class ConflictResolution:  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 70
    THEIRS, MINE, ASK, NEXT = range(4)  # prefer their changes, prefer my changes, ask user for each change, go to next deeper level (e.g. from files to lines, characters)  # line 70
class MergeOperation:  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 71
    INSERT, REMOVE, BOTH = 1, 2, 3  # insert remote changes into current, remove remote deletions from current, do both (replicate remote state) TODO handle inline-operations separate?  # line 71
class MergeBlockType:  # modify = intra-line changes  # line 72
    KEEP, INSERT, REMOVE, REPLACE, MODIFY, MOVE = range(6)  # modify = intra-line changes  # line 72


# Functions
try:  # line 76
    import chardet  # https://github.com/chardet/chardet  # line 77
    def detectEncoding(binary: 'bytes') -> 'str':  # line 78
        return chardet.detect(binary)["encoding"]  # line 78
except:  # line 79
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 80
        ''' Fallback if chardet library missing. '''  # line 81
        try:  # line 82
            binary.decode(UTF8)  # line 82
            return UTF8  # line 82
        except UnicodeError:  # line 83
            pass  # line 83
        try:  # line 84
            binary.decode("utf_16")  # line 84
            return "utf_16"  # line 84
        except UnicodeError:  # line 85
            pass  # line 85
        try:  # line 86
            binary.decode("cp1252")  # line 86
            return "cp1252"  # line 86
        except UnicodeError:  # line 87
            pass  # line 87
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 88

@_coconut_tco  # line 90
def wcswidth(string: 'str') -> 'int':  # line 90
    l = None  # type: int  # line 91
    try:  # line 92
        l = wcwidth.wcswitdh(string)  # line 93
        if l < 0:  # line 94
            return len(string)  # line 94
    except:  # line 95
        return _coconut_tail_call(len, string)  # line 95
    return l  # line 96

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # line 98
    return a & b if a else b  # line 98

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO':  # Abstraction for opening both compressed and plain files  # line 100
    return bz2.BZ2File(file, mode) if compress else open(file, mode + "b")  # Abstraction for opening both compressed and plain files  # line 100

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 102
    ''' Determine EOL style from a binary string. '''  # line 103
    lf = file.count(b"\n")  # type: int  # line 104
    cr = file.count(b"\r")  # type: int  # line 105
    crlf = file.count(b"\r\n")  # type: int  # line 106
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 107
        if lf != crlf or cr != crlf:  # line 108
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 108
        return b"\r\n"  # line 109
    if lf != 0 and cr != 0:  # line 110
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 110
    if lf > cr:  # Linux/Unix  # line 111
        return b"\n"  # Linux/Unix  # line 111
    if cr > lf:  # older 8-bit machines  # line 112
        return b"\r"  # older 8-bit machines  # line 112
    return None  # no new line contained, cannot determine  # line 113

@_coconut_tco  # referenceso __builtin__.raw_input on Python 2  # line 115
def user_input(msg: 'str') -> 'str':  # referenceso __builtin__.raw_input on Python 2  # line 115
    return _coconut_tail_call(input, msg)  # referenceso __builtin__.raw_input on Python 2  # line 115

try:  # line 117
    Splittable = TypeVar("Splittable", str, bytes)  # line 117
except:  # Python 2  # line 118
    pass  # Python 2  # line 118
def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> '_coconut.typing.Sequence[Splittable]':  # line 119
    return s.split(("\n" if isinstance(s, str) else b"\n") if d is None else d) if len(s) > 0 else []  # line 119

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl="") -> 'str':  # line 121
    return (sep + (nl + sep).join(seq)) if seq else ""  # line 121

@_coconut_tco  # line 123
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 123
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 123

@_coconut_tco  # line 125
def hashStr(datas: 'str') -> 'str':  # line 125
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 125

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 127
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0  # line 127

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 129
    return lizt[index:].index(what) + index  # line 129

def getTermWidth() -> 'int':  # line 131
    try:  # line 131
        import termwidth  # line 132
    except:  # line 133
        return 80  # line 133
    return termwidth.getTermWidth()[0]  # line 134

def branchFolder(branch: 'int', revision: 'int', base=".", file=None) -> 'str':  # line 136
    return os.path.join(base, metaFolder, "b%d" % branch, "r%d" % revision) + ((os.sep + file) if file else "")  # line 136

def Exit(message: 'str'="", code=1) -> 'None':  # line 138
    print("[EXIT%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "") + (" " + message + "." if message != "" else ""), file=sys.stderr)  # line 138
    sys.exit(1)  # line 138

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None) -> 'Tuple[str, longint]':  # line 140
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 141
    _hash = hashlib.sha256()  # line 142
    wsize = 0  # type: longint  # line 143
    if saveTo and os.path.exists(saveTo):  # line 144
        Exit("Hash conflict. Leaving revision in inconsistent state. This should happen only once in a lifetime.")  # line 144
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 145
    with open(path, "rb") as fd:  # line 146
        while True:  # line 147
            buffer = fd.read(bufSize)  # line 148
            _hash.update(buffer)  # line 149
            if to:  # line 150
                to.write(buffer)  # line 150
            if len(buffer) < bufSize:  # line 151
                break  # line 151
        if to:  # line 152
            to.close()  # line 153
            wsize = os.stat(saveTo).st_size  # line 154
    return (_hash.hexdigest(), wsize)  # line 155

def firstOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 157
    ''' Utility. '''  # line 158
    for k, v in map.items():  # line 159
        if k in params:  # line 160
            return v  # line 160
    return default  # line 161

@_coconut_tco  # line 163
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 163
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 163

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 165
    encoding = None  # type: str  # line 165
    eol = None  # type: bytes  # line 165
    lines = []  # type: _coconut.typing.Sequence[str]  # line 166
    if filename is not None:  # line 167
        with open(filename, "rb") as fd:  # line 168
            content = fd.read()  # line 168
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # line 169
    eol = eoldet(content)  # line 170
    if filename is not None:  # line 171
        with codecs.open(filename, encoding=encoding) as fd:  # line 172
            lines = safeSplit(fd.read(), (b"\n" if eol is None else eol).decode(encoding))  # line 172
    elif content is not None:  # line 173
        lines = safeSplit(content.decode(encoding), (b"\n" if eol is None else eol).decode(encoding))  # line 174
    else:  # line 175
        return (sys.getdefaultencoding(), b"\n", [])  # line 175
    return (encoding, eol, lines)  # line 176

def diffPathSets(last: 'Dict[str, PathInfo]', diff: 'Dict[str, PathInfo]') -> 'ChangeSet':  # line 178
    ''' Computes a changeset between in-memory and on-disk file lists.
      Additions contains PathInfo for entries in diff
      Deletions contains PathInfo for entries not anymore in diff
      Modifications contains PathInfo for entries changed from last to diff (new state)
  '''  # line 183
    changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 184
    for path, pinfo in last.items():  # line 185
        if path not in diff:  # now change  changes.deletions[path] = pinfo; continue  # line 186
            continue  # now change  changes.deletions[path] = pinfo; continue  # line 186
        vs = diff[path]  # reference to potentially changed path set  # line 187
        if vs.size is None:  # marked for deletion  # line 188
            changes.deletions[path] = pinfo  # marked for deletion  # line 188
            continue  # marked for deletion  # line 188
        if pinfo.size == None:  # re-added  # line 189
            changes.additions[path] = pinfo  # re-added  # line 189
            continue  # re-added  # line 189
        if pinfo.size != vs.size or pinfo.mtime != vs.mtime or pinfo.hash != vs.hash:  # not need to make hash comparison optional here  # line 190
            changes.modifications[path] = vs  # not need to make hash comparison optional here  # line 190
    for path, pinfo in diff.items():  # added loop  # line 191
        if path not in last:  # line 192
            changes.additions[path] = pinfo  # line 192
    assert not any([path in changes.deletions for path in changes.additions])  # invariant checks  # line 193
    assert not any([path in changes.additions for path in changes.deletions])  # line 194
    return changes  # line 195

try:  # line 197
    DataType = TypeVar("DataType", ChangeSet, MergeBlock, BranchInfo)  # line 197
except:  # Python 2  # line 198
    pass  # Python 2  # line 198

@_coconut_tco  # line 200
def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, **_kwargs) -> 'DataType':  # line 200
    r = _old._asdict()  # line 200
    r.update(**_kwargs)  # line 200
    return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # line 200
# TODO test namedtuple instead of instantiated tuple types in "datatype"?

@_coconut_tco  # line 203
def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation=MergeOperation.BOTH, conflictResolution=ConflictResolution.ASK, diffOnly: 'bool'=False) -> 'Union[bytes, List[MergeBlock]]':  # line 203
    ''' Merges binary text contents 'file' into file 'into', returning merged result. '''  # line 204
    encoding = None  # type: str  # line 205
    othr = None  # type: _coconut.typing.Sequence[str]  # line 205
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 205
    curr = None  # type: _coconut.typing.Sequence[str]  # line 205
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 205
    differ = difflib.Differ()  # line 206
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 207
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file)  # line 208
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into)  # line 209
    except Exception as E:  # line 210
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 210
    if None not in [othreol, curreol] and othreol != curreol:  # line 211
        warn("Differing EOL-styles detected during merge. Using current file's style for merge output")  # line 211
    output = list(differ.compare(othr, curr))  # type: List[str]  # from generator expression  # line 212
    debug("Diff output: " + "".join([o.replace("\n", "\\n") for o in output]))  # line 213
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 214
    tmp = []  # type: List[str]  # block lines  # line 215
    last = " "  # line 216
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 217
        if line[0] == last:  # continue filling consecutive block, no matter what type of block  # line 218
            tmp.append(line[2:])  # continue filling consecutive block, no matter what type of block  # line 218
            continue  # continue filling consecutive block, no matter what type of block  # line 218
        if line == "X":  # EOF marker - perform action for remaining block  # line 219
            if len(tmp) == 0:  # nothing left to do  # line 220
                break  # nothing left to do  # line 220
        if last == " ":  # block is same in both files  # line 221
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - len(tmp)))  # line 222
        elif last == "-":  # may be a deletion or replacement, store for later  # line 223
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - len(tmp)))  # line 224
        elif last == "+":  # may be insertion or replacement  # line 225
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - len(tmp)))  # line 226
            if len(blocks) >= 2 and len(blocks[-1].lines) == len(blocks[-2].lines):  # replaces previously removed section entirely if any  # line 227
                if len(blocks[-1].lines) >= 2 or (blocks[-1].changes is None and blocks[-2].changes is None):  # full block or no intra-line comment  # line 228
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-1].lines, line=no - len(tmp) - 1, replaces=blocks[-2])  # remember replaced stuff TODO why -1 necessary?  # line 229
                else:  # may have intra-line modifications  # line 230
                    blocks[-2] = MergeBlock(MergeBlockType.MODIFY, blocks[-1].lines, line=no - len(tmp), replaces=blocks[-2], changes=blocks[-1].changes)  # line 231
                blocks.pop()  # remove TOS  # line 232
        elif last == "?":  # intra-line change comment  # line 233
            ilm = getIntraLineMarkers(tmp[0])  # tipe is one of MergeBlockType 1, 2, 4. # "? " line includes a trailing \n for some reason  # line 234
            blocks[-1] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.MODIFY, changes=ilm)  # update to MODIFY, otherwise may be REPLACE instead  # line 235
        last = line[0]  # line 236
        tmp[:] = [line[2:]]  # line 237
    debug("Diff blocks: " + repr(blocks))  # line 238
    if diffOnly:  # line 239
        return blocks  # line 239
    output = []  # line 240
    for block in blocks:  # line 241
        if block.tipe == MergeBlockType.KEEP:  # line 242
            output.extend(block.lines)  # line 243
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation & MergeOperation.REMOVE):  # line 244
            output.extend(block.lines)  # line 245
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 246
            if mergeOperation & MergeOperation.INSERT:  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 247
                output.extend(block.replaces.lines)  # replaced stuff TODO allow insertion BEFORE and alternatively AFTER?  # line 247
            if not (mergeOperation & MergeBlockType.REMOVE):  # if remove, don't add replaced lines, otherwise do  # line 248
                output.extend(block.lines)  # if remove, don't add replaced lines, otherwise do  # line 248
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation & MergeOperation.INSERT:  # line 249
            output.extend(block.lines)  # line 250
        elif block.tipe == MergeBlockType.MODIFY:  # line 251
            if block.changes is not None and block.changes.tipe == MergeBlockType.INSERT:  # cannot be REMOVE, because it's always "-" then "+"  # line 252
                output.extend(block.lines if mergeOperation & MergeOperation.INSERT else block.replaces.lines)  # TODO logic?  # line 253
            elif block.replaces.changes is not None and block.replaces.changes.tipe == MergeBlockType.REMOVE:  # line 254
                output.extend(block.lines if mergeOperation & MergeOperation.REMOVE else block.replaces.lines)  # line 255
            elif block.changes is not None and block.changes.tipe == MergeBlockType.MODIFY:  # always both sides modified, but may differ in markers  # line 256
                if conflictResolution == ConflictResolution.THEIRS:  # line 257
                    output.extend(block.replaces.lines)  # line 258
                elif conflictResolution == ConflictResolution.MINE:  # line 259
                    output.extend(block.lines)  # line 260
                elif conflictResolution == ConflictResolution.ASK:  # line 261
                    print(ajoin("THR ", block.replaces.lines, "\n"))  # line 262
                    print(ajoin("MIN ", block.lines, "\n"))  # line 263
                    reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT, "u": None}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge, [U]ser defined: ").strip().lower(), ConflictResolution.MINE)  # type: _coconut.typing.Optional[int]  # line 264
                    debug("User selected %d" % reso)  # line 265
                    _coconut_match_check = False  # line 266
                    _coconut_match_to = reso  # line 266
                    if _coconut_match_to is None:  # line 266
                        _coconut_match_check = True  # line 266
                    if _coconut_match_check:  # line 266
                        warn("Manual input not implemented yet")  # TODO allow multi-line input (CTRL+D?)  # line 267
                    _coconut_match_check = False  # line 268
                    _coconut_match_to = reso  # line 268
                    if _coconut_match_to == ConflictResolution.MINE:  # line 268
                        _coconut_match_check = True  # line 268
                    if _coconut_match_check:  # line 268
                        debug("Using mine")  # line 269
                        output.extend(block.lines)  # line 270
                    _coconut_match_check = False  # line 271
                    _coconut_match_to = reso  # line 271
                    if _coconut_match_to == ConflictResolution.THEIRS:  # line 271
                        _coconut_match_check = True  # line 271
                    if _coconut_match_check:  # line 271
                        debug("Using theirs")  # line 272
                        output.extend(block.replaces.lines)  # line 273
                    _coconut_match_check = False  # line 274
                    _coconut_match_to = reso  # line 274
                    if _coconut_match_to == ConflictResolution.NEXT:  # line 274
                        _coconut_match_check = True  # line 274
                    if _coconut_match_check:  # line 274
                        warn("Intra-line merge not implemented yet, skipping line(s)")  # line 275
                        output.extend(block.replaces.lines)  # line 276
            else:  # e.g. contains a deletion, but user was asking for insert only??  # line 277
                warn("Investigate this case")  # line 278
                output.extend(block.lines)  # default or not .replaces?  # line 279
    debug("Merge output: " + "; ".join(output))  # line 280
    nl = b"\n" if othreol is None else othreol if curreol is None else curreol  # type: bytes  # line 281
    return _coconut_tail_call(nl.join, [line.encode(encoding) for line in output])  # returning bytes  # line 282
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 285
def getIntraLineMarkers(line: 'str') -> 'Range':  # line 285
    ''' Return (type, [affected indices]) of "? "-line diff markers ("? " suffix must be removed). '''  # line 286
    if "^" in line:  # line 287
        return _coconut_tail_call(Range, MergeBlockType.MODIFY, [i for i, c in enumerate(line) if c == "^"])  # line 287
    if "+" in line:  # line 288
        return _coconut_tail_call(Range, MergeBlockType.INSERT, [i for i, c in enumerate(line) if c == "+"])  # line 288
    if "-" in line:  # line 289
        return _coconut_tail_call(Range, MergeBlockType.REMOVE, [i for i, c in enumerate(line) if c == "-"])  # line 289
    return _coconut_tail_call(Range, MergeBlockType.KEEP, [])  # line 290

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 292
    ''' Attempts to find sos and legacy VCS base folders. '''  # line 293
    debug("Detecting root folders...")  # line 294
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 295
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 296
    while not os.path.exists(os.path.join(path, metaFolder)):  # line 297
        contents = set(os.listdir(path))  # line 298
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # type: _coconut.typing.Sequence[str]  # determine VCS type from dot folder  # line 299
        choice = None  # type: _coconut.typing.Optional[str]  # line 300
        if len(vcss) > 1:  # line 301
            choice = SVN if SVN in vcss else vcss[0]  # line 302
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 303
        elif len(vcss) > 0:  # line 304
            choice = vcss[0]  # line 304
        if not vcs[0] and choice:  # memorize current repo root  # line 305
            vcs = (path, choice)  # memorize current repo root  # line 305
        new = os.path.dirname(path)  # get parent path  # line 306
        if new == path:  # avoid infinite loop  # line 307
            break  # avoid infinite loop  # line 307
        path = new  # line 308
    if os.path.exists(os.path.join(path, metaFolder)):  # found something  # line 309
        if vcs[0]:  # already detected vcs base and command  # line 310
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 310
        sos = path  # line 311
        while True:  # continue search for VCS base  # line 312
            new = os.path.dirname(path)  # get parent path  # line 313
            if new == path:  # no VCS folder found  # line 314
                return (sos, None, None)  # no VCS folder found  # line 314
            path = new  # line 315
            contents = set(os.listdir(path))  # line 316
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 317
            choice = None  # line 318
            if len(vcss) > 1:  # line 319
                choice = SVN if SVN in vcss else vcss[0]  # line 320
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 321
            elif len(vcss) > 0:  # line 322
                choice = vcss[0]  # line 322
            if choice:  # line 323
                return (sos, path, choice)  # line 323
    return (None, vcs[0], vcs[1])  # line 324

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 326
    index = 0  # type: int  # line 327
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 328
    while index < len(pattern):  # line 329
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 330
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 330
            continue  # line 330
        if pattern[index] in "*?":  # line 331
            count = 1  # type: int  # line 332
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 333
                count += 1  # line 333
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 334
            index += count  # line 334
            continue  # line 334
        if pattern[index:index + 2] == "[!":  # line 335
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 335
            index += len(out[-1][1])  # line 335
            continue  # line 335
        count = 1  # line 336
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 337
            count += 1  # line 337
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 338
        index += count  # line 338
    return out  # line 339

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 341
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 342
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 343
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 345
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 345
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 346
        Exit("Source and target file patterns differ in semantics")  # line 346
    return (ot, nt)  # line 347

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 349
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 350
    pairs = []  # type: List[Tuple[str, str]]  # line 351
    for filename in filenames:  # line 352
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 353
        nextliteral = 0  # type: int  # line 354
        parsedOld = []  # type: List[GlobBlock2]  # line 355
        index = 0  # type: int  # line 356
        for part in oldPattern:  # match everything in the old filename  # line 357
            if part.isLiteral:  # line 358
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 358
                index += len(part.content)  # line 358
                nextliteral += 1  # line 358
            elif part.content.startswith("?"):  # line 359
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 359
                index += len(part.content)  # line 359
            elif part.content.startswith("["):  # line 360
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 360
                index += 1  # line 360
            elif part.content == "*":  # line 361
                if nextliteral >= len(literals):  # line 362
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 362
                    break  # line 362
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 363
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 364
                index = nxt  # line 364
            else:  # line 365
                Exit("Invalid file pattern specified for move/rename")  # line 365
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 366
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 367
        nextliteral = 0  # line 368
        nextglob = 0  # type: int  # line 368
        outname = []  # type: List[str]  # line 369
        for part in newPattern:  # generate new filename  # line 370
            if part.isLiteral:  # line 371
                outname.append(literals[nextliteral].content)  # line 371
                nextliteral += 1  # line 371
            else:  # line 372
                outname.append(globs[nextglob].matches)  # line 372
                nextglob += 1  # line 372
        pairs.append((filename, "".join(outname)))  # line 373
    return pairs  # line 374

@_coconut_tco  # line 376
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 376
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 380
    if not actions:  # line 381
        return []  # line 381
    sources = None  # type: List[str]  # line 382
    targets = None  # type: List[str]  # line 382
    sources, targets = [list(l) for l in zip(*actions)]  # line 383
    last = len(actions)  # type: int  # line 384
    while last > 1:  # line 385
        clean = True  # type: bool  # line 386
        for i in range(1, last):  # line 387
            try:  # line 388
                index = targets[:i].index(sources[i])  # type: int  # line 389
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 390
                targets.insert(index, targets.pop(i))  # line 391
                clean = False  # line 392
            except:  # target not found in sources: good!  # line 393
                continue  # target not found in sources: good!  # line 393
        if clean:  # line 394
            break  # line 394
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 395
    if exitOnConflict:  # line 396
        for i in range(1, len(actions)):  # line 397
            if sources[i] in targets[:i]:  # line 398
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 398
    return _coconut_tail_call(list, zip(sources, targets))  # line 399

def relativize(root: 'str', path: 'str') -> 'Tuple[str, str]':  # line 401
    ''' Determine OS-independent relative folder path, and relative pattern path. '''  # line 402
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(path)), root).replace(os.sep, SLASH)  # line 403
    return relpath, os.path.join(relpath, os.path.basename(path)).replace(os.sep, SLASH)  # line 404

def parseOnlyOptions(root: 'str', options: '_coconut.typing.Sequence[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 406
    ''' Returns set of --only arguments, and set or --except arguments. '''  # line 407
    cwd = os.getcwd()  # type: str  # line 408
    onlys = []  # type: List[str]  # line 409
    excps = []  # type: List[str]  # line 409
    index = 0  # type: int  # line 409
    while True:  # line 410
        try:  # line 411
            index = 1 + listindex(options, "--only", index)  # line 412
            onlys.append(options[index])  # line 413
        except:  # line 414
            break  # line 414
    index = 0  # line 415
    while True:  # line 416
        try:  # line 417
            index = 1 + listindex(options, "--except", index)  # line 418
            excps.append(options[index])  # line 419
        except:  # line 420
            break  # line 420
    return (frozenset((relativize(root, o)[1] for o in onlys)) if onlys else None, frozenset((relativize(root, e)[1] for e in excps)) if excps else None)  # line 421
