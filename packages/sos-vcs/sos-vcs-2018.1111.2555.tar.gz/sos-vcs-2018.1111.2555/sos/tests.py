#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xd6d3f6ba

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

import builtins  # line 5
import json  # line 5
import logging  # line 5
import os  # line 5
import shutil  # line 5
sys = _coconut_sys  # line 5
import time  # line 5
import traceback  # line 5
import unittest  # line 5
import uuid  # line 5
StringIO = (__import__("StringIO" if sys.version_info.major < 3 else "io")).StringIO  # enables import via ternary expression  # line 6
try:  # Py3  # line 7
    from unittest import mock  # Py3  # line 7
except:  # installed via pip  # line 8
    import mock  # installed via pip  # line 8
try:  # only required for mypy  # line 9
    from typing import Any  # only required for mypy  # line 9
    from typing import List  # only required for mypy  # line 9
    from typing import Union  # only required for mypy  # line 9
except:  # line 10
    pass  # line 10

testFolder = os.path.abspath(os.path.join(os.getcwd(), "test"))  # line 12
try:  # line 13
    import configr  # optional dependency  # line 14
    os.environ["TEST"] = testFolder  # needed to mock configr library calls in sos  # line 15
except:  # declare as undefined  # line 16
    configr = None  # declare as undefined  # line 16
import sos  # line 17
sos.defaults["defaultbranch"] = "trunk"  # because sos.main() is never called  # line 18

def sync() -> 'None':  # line 20
    if (sys.version_info.major, sys.version_info.minor) >= (3, 3):  # line 21
        os.sync()  # line 21


def determineFilesystemTimeResolution() -> 'float':  # line 24
    name = str(uuid.uuid4())  # type: str  # line 25
    with open(name, "w") as fd:  # create temporary file  # line 26
        fd.write("x")  # create temporary file  # line 26
    mt = os.stat(name).st_mtime  # type: float  # get current timestamp  # line 27
    while os.stat(name).st_mtime == mt:  # wait until timestamp modified  # line 28
        time.sleep(0.05)  # to avoid 0.00s bugs (came up some time for unknown reasons)  # line 29
        with open(name, "w") as fd:  # line 30
            fd.write("x")  # line 30
    mt, start, _count = os.stat(name).st_mtime, time.time(), 0  # line 31
    while os.stat(name).st_mtime == mt:  # now cound and measure time until modified again  # line 32
        time.sleep(0.05)  # line 33
        _count += 1  # line 34
        with open(name, "w") as fd:  # line 35
            fd.write("x")  # line 35
    os.unlink(name)  # line 36
    fsprecision = round(time.time() - start, 2)  # type: float  # line 37
    print("File system timestamp precision is %.2fs; wrote to the file %d times during that time" % (fsprecision, _count))  # line 38
    return fsprecision  # line 39


FS_PRECISION = determineFilesystemTimeResolution() * 1.05  # line 42


@_coconut_tco  # line 45
def debugTestRunner(post_mortem=None):  # line 45
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 46
    import pdb  # line 47
    if post_mortem is None:  # line 48
        post_mortem = pdb.post_mortem  # line 48
    class DebugTestResult(unittest.TextTestResult):  # line 49
        def addError(self, test, err):  # called before tearDown()  # line 50
            traceback.print_exception(*err)  # line 51
            post_mortem(err[2])  # line 52
            super(DebugTestResult, self).addError(test, err)  # line 53
        def addFailure(self, test, err):  # line 54
            traceback.print_exception(*err)  # line 55
            post_mortem(err[2])  # line 56
            super(DebugTestResult, self).addFailure(test, err)  # line 57
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 58

@_coconut_tco  # line 60
def wrapChannels(func: '_coconut.typing.Callable[..., Any]'):  # line 60
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 61
    oldv, oldo, olde = sys.argv, sys.stdout, sys.stderr  # line 62
    buf = StringIO()  # line 63
    sys.stdout = sys.stderr = buf  # line 64
    handler = logging.StreamHandler(buf)  # line 65
    logging.getLogger().addHandler(handler)  # line 66
    try:  # capture output into buf  # line 67
        func()  # capture output into buf  # line 67
    except Exception as E:  # line 68
        buf.write(str(E) + "\n")  # line 68
        traceback.print_exc(file=buf)  # line 68
    except SystemExit as F:  # line 69
        buf.write("EXIT CODE %s" % F.code + "\n")  # line 69
        traceback.print_exc(file=buf)  # line 69
    logging.getLogger().removeHandler(handler)  # line 70
    sys.argv, sys.stdout, sys.stderr = oldv, oldo, olde  # line 71
    return _coconut_tail_call(buf.getvalue)  # line 72

def mockInput(datas: '_coconut.typing.Sequence[str]', func) -> 'Any':  # line 74
    with mock.patch("builtins.input" if sys.version_info.major >= 3 else "utility._coconut_raw_input", side_effect=datas):  # line 75
        return func()  # line 75

def setRepoFlag(name: 'str', value: 'bool') -> 'None':  # line 77
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 78
        flags, branches = json.loads(fd.read())  # line 78
    flags[name] = value  # line 79
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 80
        fd.write(json.dumps((flags, branches)))  # line 80

def checkRepoFlag(name: 'str', flag: 'bool') -> 'bool':  # line 82
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 82
        flags, branches = json.loads(fd.read())  # line 83
    return name in flags and flags[name] == flag  # line 84


class Tests(unittest.TestCase):  # line 87
    ''' Entire test suite. '''  # line 88

    def setUp(_):  # line 90
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 91
            resource = os.path.join(testFolder, entry)  # line 92
            shutil.rmtree(resource) if os.path.isdir(resource) else os.unlink(resource)  # line 93
        os.chdir(testFolder)  # line 94

    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 96
        [_.assertIn(w, where) for w in what]  # line 96

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]') -> 'None':  # line 98
        [_.assertNotIn(w, where) for w in what]  # line 98

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 100
        [_.assertIn(what, w) for w in where]  # line 100

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 102
        _.assertTrue(any((what in w for w in where)))  # line 102

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]') -> 'None':  # line 104
        _.assertFalse(any((what in w for w in where)))  # line 104

    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None) -> 'None':  # line 106
        if prefix and not os.path.exists(prefix):  # line 107
            os.makedirs(prefix)  # line 107
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 108
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 108

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 110
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 111
            return False  # line 111
        if expectedContents is None:  # line 112
            return True  # line 112
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 113
            return fd.read() == expectedContents  # line 113

    def testAccessor(_):  # line 115
        a = sos.Accessor({"a": 1})  # line 116
        _.assertEqual((1, 1), (a["a"], a.a))  # line 117

    def testEnum(_):  # line 119
        e = sos.Enum("Abc", ["A", "B"])  # type: sos.Enum  # line 120
        _.assertEqual("Abc", str(e))  # line 121
        _.assertEqual("<enum 'Abc'>", repr(e))  # line 122
        _.assertEqual(["A", "B"], e.names())  # line 123
        _.assertEqual([0, 1], e.numbers())  # line 124
        _.assertTrue(sos.EnumValue, type(e.entries()[0]))  # line 125
        e = sos.Enum("Abc", [("A", 2), "B"], step=2)  # line 126
        _.assertEqual([2, 4], e.numbers())  # line 127
        _.assertEqual(4, e.B.value)  # line 128
        _.assertEqual("B", e[4].name)  # line 129
        _.assertEqual("<enum 'Abc.A'>", repr(e.A))  # line 130
        _.assertEqual("Abc.A", str(e[2]))  # line 131

    def testGetAnyOfmap(_):  # line 133
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 134
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 135

    def testAjoin(_):  # line 137
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 138
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 139

    def testFindChanges(_):  # line 141
        m = sos.Metadata(os.getcwd())  # line 142
        try:  # line 143
            sos.config("set", ["texttype", "*"])  # line 143
        except SystemExit as E:  # line 144
            _.assertEqual(0, E.code)  # line 144
        try:  # line 145
            sos.config("set", ["ignores", "*.cfg;*.cfg.bak"])  # line 145
        except SystemExit as E:  # line 146
            _.assertEqual(0, E.code)  # line 146
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 147
        m.loadBranches()  # line 148
        _.createFile(1, "1")  # line 149
        m.createBranch(0)  # line 150
        _.assertEqual(1, len(m.paths))  # line 151
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 152
        _.createFile(1, "2")  # modify existing file  # line 153
        _.createFile(2, "2")  # add another file  # line 154
        m.loadCommit(0, 0)  # line 155
        changes = m.findChanges()  # detect time skew  # line 156
        _.assertEqual(1, len(changes.additions))  # line 157
        _.assertEqual(0, len(changes.deletions))  # line 158
        _.assertEqual(1, len(changes.modifications))  # line 159
        m.integrateChangeset(changes)  # line 160
        _.createFile(2, "12")  # modify file again  # line 161
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 162
        _.assertEqual(0, len(changes.additions))  # line 163
        _.assertEqual(0, len(changes.deletions))  # line 164
        _.assertEqual(1, len(changes.modifications))  # line 165
        _.assertTrue(os.path.exists(sos.branchFolder(0, 1)))  # line 166
        _.assertTrue(os.path.exists(sos.branchFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 167

    def testDiffFunc(_):  # line 169
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 170
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 171
        changes = sos.diffPathSets(a, b)  # line 172
        _.assertEqual(0, len(changes.additions))  # line 173
        _.assertEqual(0, len(changes.deletions))  # line 174
        _.assertEqual(0, len(changes.modifications))  # line 175
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 176
        changes = sos.diffPathSets(a, b)  # line 177
        _.assertEqual(0, len(changes.additions))  # line 178
        _.assertEqual(0, len(changes.deletions))  # line 179
        _.assertEqual(1, len(changes.modifications))  # line 180
        b = {}  # diff contains no entries -> no change  # line 181
        changes = sos.diffPathSets(a, b)  # line 182
        _.assertEqual(0, len(changes.additions))  # line 183
        _.assertEqual(0, len(changes.deletions))  # line 184
        _.assertEqual(0, len(changes.modifications))  # line 185
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 186
        changes = sos.diffPathSets(a, b)  # line 187
        _.assertEqual(0, len(changes.additions))  # line 188
        _.assertEqual(1, len(changes.deletions))  # line 189
        _.assertEqual(0, len(changes.modifications))  # line 190
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 191
        changes = sos.diffPathSets(a, b)  # line 192
        _.assertEqual(1, len(changes.additions))  # line 193
        _.assertEqual(0, len(changes.deletions))  # line 194
        _.assertEqual(0, len(changes.modifications))  # line 195
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 196
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 197
        changes = sos.diffPathSets(a, b)  # line 198
        _.assertEqual(1, len(changes.additions))  # line 199
        _.assertEqual(0, len(changes.deletions))  # line 200
        _.assertEqual(0, len(changes.modifications))  # line 201
        changes = sos.diffPathSets(b, a)  # line 202
        _.assertEqual(0, len(changes.additions))  # line 203
        _.assertEqual(1, len(changes.deletions))  # line 204
        _.assertEqual(0, len(changes.modifications))  # line 205

    def testPatternPaths(_):  # line 207
        sos.offline(options=["--track"])  # line 208
        os.mkdir("sub")  # line 209
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 210
        sos.add("sub", "sub/file?")  # line 211
        sos.commit("test")  # should pick up sub/file1 pattern  # line 212
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 213
        _.createFile(1)  # line 214
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 215
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 215
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 215
        except:  # line 216
            pass  # line 216

    def testTokenizeGlobPattern(_):  # line 218
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 219
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 220
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 221
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 222
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 223
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 224

    def testTokenizeGlobPatterns(_):  # line 226
        try:  # because number of literal strings differs  # line 227
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 227
            _.fail()  # because number of literal strings differs  # line 227
        except:  # line 228
            pass  # line 228
        try:  # because glob patterns differ  # line 229
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 229
            _.fail()  # because glob patterns differ  # line 229
        except:  # line 230
            pass  # line 230
        try:  # glob patterns differ, regardless of position  # line 231
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 231
            _.fail()  # glob patterns differ, regardless of position  # line 231
        except:  # line 232
            pass  # line 232
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 233
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 234
        try:  # succeeds, because glob patterns match (differ only in position)  # line 235
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 235
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 235
        except:  # line 236
            pass  # line 236

    def testConvertGlobFiles(_):  # line 238
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 239
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 240

    def testFolderRemove(_):  # line 242
        m = sos.Metadata(os.getcwd())  # line 243
        _.createFile(1)  # line 244
        _.createFile("a", prefix="sub")  # line 245
        sos.offline()  # line 246
        _.createFile(2)  # line 247
        os.unlink("sub" + os.sep + "a")  # line 248
        os.rmdir("sub")  # line 249
        changes = sos.changes()  # line 250
        _.assertEqual(1, len(changes.additions))  # line 251
        _.assertEqual(0, len(changes.modifications))  # line 252
        _.assertEqual(1, len(changes.deletions))  # line 253
        _.createFile("a", prefix="sub")  # line 254
        changes = sos.changes()  # line 255
        _.assertEqual(0, len(changes.deletions))  # line 256

    def testComputeSequentialPathSet(_):  # line 258
        os.makedirs(sos.branchFolder(0, 0))  # line 259
        os.makedirs(sos.branchFolder(0, 1))  # line 260
        os.makedirs(sos.branchFolder(0, 2))  # line 261
        os.makedirs(sos.branchFolder(0, 3))  # line 262
        os.makedirs(sos.branchFolder(0, 4))  # line 263
        m = sos.Metadata(os.getcwd())  # line 264
        m.branch = 0  # line 265
        m.commit = 2  # line 266
        m.saveBranches()  # line 267
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 268
        m.saveCommit(0, 0)  # initial  # line 269
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 270
        m.saveCommit(0, 1)  # mod  # line 271
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 272
        m.saveCommit(0, 2)  # add  # line 273
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 274
        m.saveCommit(0, 3)  # del  # line 275
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 276
        m.saveCommit(0, 4)  # readd  # line 277
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 278
        m.saveBranch(0)  # line 279
        m.computeSequentialPathSet(0, 4)  # line 280
        _.assertEqual(2, len(m.paths))  # line 281

    def testParseRevisionString(_):  # line 283
        m = sos.Metadata(os.getcwd())  # line 284
        m.branch = 1  # line 285
        m.commits = {0: 0, 1: 1, 2: 2}  # line 286
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 287
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 288
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 289
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 290
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 291
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 292
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 293

    def testOfflineEmpty(_):  # line 295
        os.mkdir("." + os.sep + sos.metaFolder)  # line 296
        try:  # line 297
            sos.offline("trunk")  # line 297
            _.fail()  # line 297
        except SystemExit as E:  # line 298
            _.assertEqual(1, E.code)  # line 298
        os.rmdir("." + os.sep + sos.metaFolder)  # line 299
        sos.offline("test")  # line 300
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 301
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 302
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 303
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 304
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 305
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 0))))  # only meta data file  # line 306

    def testOfflineWithFiles(_):  # line 308
        _.createFile(1, "x" * 100)  # line 309
        _.createFile(2)  # line 310
        sos.offline("test")  # line 311
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 312
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 313
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 314
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 315
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 316
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 317
        _.assertEqual(3, len(os.listdir(sos.branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 318

    def testBranch(_):  # line 320
        _.createFile(1, "x" * 100)  # line 321
        _.createFile(2)  # line 322
        sos.offline("test")  # b0/r0  # line 323
        sos.branch("other")  # b1/r0  # line 324
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 325
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 326
        _.assertEqual(list(sorted(os.listdir(sos.branchFolder(0, 0)))), list(sorted(os.listdir(sos.branchFolder(1, 0)))))  # line 328
        _.createFile(1, "z")  # modify file  # line 330
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 331
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 332
        _.createFile(3, "z")  # line 334
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 335
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 336
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 341
        _.createFile(1, "x" * 100)  # line 342
        _.createFile(2)  # line 343
        sos.offline("test")  # line 344
        changes = sos.changes()  # line 345
        _.assertEqual(0, len(changes.additions))  # line 346
        _.assertEqual(0, len(changes.deletions))  # line 347
        _.assertEqual(0, len(changes.modifications))  # line 348
        _.createFile(1, "z")  # size change  # line 349
        changes = sos.changes()  # line 350
        _.assertEqual(0, len(changes.additions))  # line 351
        _.assertEqual(0, len(changes.deletions))  # line 352
        _.assertEqual(1, len(changes.modifications))  # line 353
        sos.commit("message")  # line 354
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 355
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.branchFolder(0, 1)))  # line 356
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # no further files, only the modified one  # line 357
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 358
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 359
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 360
        os.unlink("file2")  # line 361
        changes = sos.changes()  # line 362
        _.assertEqual(0, len(changes.additions))  # line 363
        _.assertEqual(1, len(changes.deletions))  # line 364
        _.assertEqual(1, len(changes.modifications))  # line 365
        sos.commit("modified")  # line 366
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 367
        try:  # expecting Exit due to no changes  # line 368
            sos.commit("nothing")  # expecting Exit due to no changes  # line 368
            _.fail()  # expecting Exit due to no changes  # line 368
        except:  # line 369
            pass  # line 369

    def testGetBranch(_):  # line 371
        m = sos.Metadata(os.getcwd())  # line 372
        m.branch = 1  # current branch  # line 373
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 374
        _.assertEqual(27, m.getBranchByName(27))  # line 375
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 376
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 377
        _.assertIsNone(m.getBranchByName("unknown"))  # line 378
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 379
        _.assertEqual(13, m.getRevisionByName("13"))  # line 380
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 381
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 382

    def testTagging(_):  # line 384
        m = sos.Metadata(os.getcwd())  # line 385
        sos.offline()  # line 386
        _.createFile(111)  # line 387
        sos.commit("tag", ["--tag"])  # line 388
        out = wrapChannels(lambda: sos.log()).replace("\r", "").split("\n")  # line 389
        _.assertTrue(any(("|tag" in line and line.endswith("|TAG") for line in out)))  # line 390
        _.createFile(2)  # line 391
        try:  # line 392
            sos.commit("tag")  # line 392
            _.fail()  # line 392
        except:  # line 393
            pass  # line 393
        sos.commit("tag-2", ["--tag"])  # line 394
        out = wrapChannels(lambda: sos.ls(options=["--tags"])).replace("\r", "")  # line 395
        _.assertIn("TAG tag", out)  # line 396

    def testSwitch(_):  # line 398
        _.createFile(1, "x" * 100)  # line 399
        _.createFile(2, "y")  # line 400
        sos.offline("test")  # file1-2  in initial branch commit  # line 401
        sos.branch("second")  # file1-2  switch, having same files  # line 402
        sos.switch("0")  # no change  switch back, no problem  # line 403
        sos.switch("second")  # no change  # switch back, no problem  # line 404
        _.createFile(3, "y")  # generate a file  # line 405
        try:  # uncommited changes detected  # line 406
            sos.switch("test")  # uncommited changes detected  # line 406
            _.fail()  # uncommited changes detected  # line 406
        except SystemExit as E:  # line 407
            _.assertEqual(1, E.code)  # line 407
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 408
        sos.changes()  # line 409
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 410
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 411
        _.createFile("XXX")  # line 412
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 413
        _.assertIn("File tree has changes", out)  # line 414
        _.assertNotIn("File tree is unchanged", out)  # line 415
        _.assertIn("  * b00   'test'", out)  # line 416
        _.assertIn("    b01 'second'", out)  # line 417
        _.assertIn("(dirty)", out)  # one branch has commits  # line 418
        _.assertIn("(in sync)", out)  # the other doesn't  # line 419
        _.createFile(4, "xy")  # generate a file  # line 420
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 421
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 422
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 423
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 424
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 425
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 426
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 427

    def testAutoDetectVCS(_):  # line 429
        os.mkdir(".git")  # line 430
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 431
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 432
            meta = fd.read()  # line 432
        _.assertTrue("\"master\"" in meta)  # line 433
        os.rmdir(".git")  # line 434

    def testUpdate(_):  # line 436
        sos.offline("trunk")  # create initial branch b0/r0  # line 437
        _.createFile(1, "x" * 100)  # line 438
        sos.commit("second")  # create b0/r1  # line 439

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 441
        _.assertFalse(_.existsFile(1))  # line 442

        sos.update("/1")  # recreate file1  # line 444
        _.assertTrue(_.existsFile(1))  # line 445

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 447
        _.assertTrue(os.path.exists(sos.branchFolder(0, 2)))  # line 448
        _.assertTrue(os.path.exists(sos.branchFolder(0, 2, file=sos.metaFile)))  # line 449
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 2))))  # only meta data file, no differential files  # line 450

        sos.update("/1")  # do nothing, as nothing has changed  # line 452
        _.assertTrue(_.existsFile(1))  # line 453

        _.createFile(2, "y" * 100)  # line 455
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 458
        _.assertTrue(_.existsFile(2))  # line 459
        sos.update("trunk", ["--add"])  # only add stuff  # line 460
        _.assertTrue(_.existsFile(2))  # line 461
        sos.update("trunk")  # nothing to do  # line 462
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 463

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 465
        _.createFile(10, theirs)  # line 466
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 467
        _.createFile(11, mine)  # line 468
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 469
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 470

    def testUpdate2(_):  # line 472
        _.createFile("test.txt", "x" * 10)  # line 473
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 474
        sos.branch("mod")  # line 475
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 476
        time.sleep(FS_PRECISION)  # line 477
        sos.commit("mod")  # create b0/r1  # line 478
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 479
        with open("test.txt", "rb") as fd:  # line 480
            _.assertEqual(b"x" * 10, fd.read())  # line 480
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 481
        with open("test.txt", "rb") as fd:  # line 482
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 482
        _.createFile("test.txt", "x" * 10)  # line 483
        sos.update("mod", ["--ask-lines"])  # won't ask for lines, as it is recognized as a full line replacement  # line 484
        with open("test.txt", "rb") as fd:  # line 485
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 485
# TODO add code with an intra-line replacement when implemented in getIntraLineMarkers, test method also separately
#    _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)
#    import pdb; pdb.set_trace()
#    sos.update("mod", ["--ask-lines"])  # won't ask for lines, as it is recognized as a full line replacement
#    mockInput(["t"], () -> sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)
#    with open("test.txt", "rb") as fd: _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())

    def testIsTextType(_):  # line 493
        m = sos.Metadata(".")  # line 494
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 495
        m.c.bintype = ["*.md.confluence"]  # line 496
        _.assertTrue(m.isTextType("ab.txt"))  # line 497
        _.assertTrue(m.isTextType("./ab.txt"))  # line 498
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 499
        _.assertFalse(m.isTextType("bc/ab."))  # line 500
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 501
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 502
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 503
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 504

    def testEolDet(_):  # line 506
        ''' Check correct end-of-line detection. '''  # line 507
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 508
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 509
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 510
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 511
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 512
        _.assertIsNone(sos.eoldet(b""))  # line 513
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 514

    def testMerge(_):  # line 516
        ''' Check merge results depending on conflict solution options. '''  # line 517
        a = b"a\nb\ncc\nd"  # line 518
        b = b"a\nb\nee\nd"  # line 519
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 520
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 521
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 522
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 524
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 525
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 526
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 527
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 529
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 530
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 531
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 532
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 533
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 534
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 535
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 536

    def testPickyMode(_):  # line 538
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 539
        sos.offline("trunk", ["--picky"])  # line 540
        changes = sos.changes()  # line 541
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 542
        sos.add(".", "./file?", ["--force"])  # line 543
        _.createFile(1, "aa")  # line 544
        sos.commit("First")  # add one file  # line 545
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # line 546
        _.createFile(2, "b")  # line 547
        try:  # add nothing, because picky  # line 548
            sos.commit("Second")  # add nothing, because picky  # line 548
        except:  # line 549
            pass  # line 549
        sos.add(".", "./file?")  # line 550
        sos.commit("Third")  # line 551
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # line 552
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 553
        _.assertIn("  * r2", out)  # line 554
        _.createFile(3, prefix="sub")  # line 555
        sos.add("sub", "sub/file?")  # line 556
        changes = sos.changes()  # line 557
        _.assertEqual(1, len(changes.additions))  # line 558
        _.assertTrue("sub/file3" in changes.additions)  # line 559

    def testTrackedSubfolder(_):  # line 561
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 562
        os.mkdir("." + os.sep + "sub")  # line 563
        sos.offline("trunk", ["--track"])  # line 564
        _.createFile(1, "x")  # line 565
        _.createFile(1, "x", prefix="sub")  # line 566
        sos.add(".", "./file?")  # add glob pattern to track  # line 567
        sos.commit("First")  # line 568
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # one new file + meta file  # line 569
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 570
        sos.commit("Second")  # one new file + meta  # line 571
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # one new file + meta file  # line 572
        os.unlink("file1")  # remove from basefolder  # line 573
        _.createFile(2, "y")  # line 574
        sos.remove(".", "sub/file?")  # line 575
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 576
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 576
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 576
        except:  # line 577
            pass  # line 577
        sos.commit("Third")  # line 578
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # one new file + meta  # line 579
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 582
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 587
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 588
        _.createFile(1)  # line 589
        _.createFile("a123a")  # untracked file "a123a"  # line 590
        sos.add(".", "./file?")  # add glob tracking pattern  # line 591
        sos.commit("second")  # versions "file1"  # line 592
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # one new file + meta file  # line 593
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 594
        _.assertIn("  | ./file?", out)  # line 595

        _.createFile(2)  # untracked file "file2"  # line 597
        sos.commit("third")  # versions "file2"  # line 598
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # one new file + meta file  # line 599

        os.mkdir("." + os.sep + "sub")  # line 601
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 602
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 603
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 604

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 606
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 607
        sos.add(".", "./a*a")  # add tracking pattern  # line 608
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 609
        _.assertEqual(0, len(changes.modifications))  # line 610
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 611
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 612

        sos.commit("Second_2")  # line 614
        _.assertEqual(2, len(os.listdir(sos.branchFolder(1, 1))))  # "a123a" + meta file  # line 615
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 616
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 617

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 619
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 620
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 621

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 623
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 624
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 625

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 627
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 628
        _.assertEqual(3, len(os.listdir(sos.branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 629
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 630
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 631
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 632
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 633
# TODO test switch --meta

    def testLsTracked(_):  # line 636
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 637
        _.createFile(1)  # line 638
        _.createFile("foo")  # line 639
        sos.add(".", "./file*")  # capture one file  # line 640
        sos.ls()  # line 641
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 642
        _.assertInAny("TRK file1  (file*)", out)  # line 643
        _.assertNotInAny("... file1  (file*)", out)  # line 644
        _.assertInAny("... foo", out)  # line 645
        out = sos.safeSplit(wrapChannels(lambda: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 646
        _.assertInAny("TRK file*", out)  # line 647
        _.createFile("a", prefix="sub")  # line 648
        sos.add("sub", "sub/a")  # line 649
        sos.ls("sub")  # line 650
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda: sos.ls("sub")).replace("\r", ""), "\n"))  # line 651

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 653
        _.createFile(1)  # line 654
        sos.offline("master", options=["--force"])  # line 655
        out = wrapChannels(lambda: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # line 656
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 657
        _.assertTrue(_.existsFile(sos.branchFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 658
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 659
        _.createFile(2)  # line 660
        out = wrapChannels(lambda: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # without progress, the output goes to stderr via debug()  # line 661
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 662
        sos.commit("Added file2")  # line 663
        _.assertTrue(_.existsFile(sos.branchFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 664
        _.assertFalse(_.existsFile(sos.branchFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 665

    def testConfigVariations(_):  # line 667
        def makeRepo():  # line 668
            try:  # line 669
                os.unlink("file1")  # line 669
            except:  # line 670
                pass  # line 670
            sos.offline("master", options=["--plain", "--force"])  # line 671
            _.createFile(1)  # line 672
            sos.commit("Added file1")  # line 673
        try:  # line 674
            sos.config("set", ["strict", "on"])  # line 674
        except SystemExit as E:  # line 675
            _.assertEqual(0, E.code)  # line 675
        makeRepo()  # line 676
        _.assertTrue(checkRepoFlag("strict", True))  # line 677
        try:  # line 678
            sos.config("set", ["strict", "off"])  # line 678
        except SystemExit as E:  # line 679
            _.assertEqual(0, E.code)  # line 679
        makeRepo()  # line 680
        _.assertTrue(checkRepoFlag("strict", False))  # line 681
        try:  # line 682
            sos.config("set", ["strict", "yes"])  # line 682
        except SystemExit as E:  # line 683
            _.assertEqual(0, E.code)  # line 683
        makeRepo()  # line 684
        _.assertTrue(checkRepoFlag("strict", True))  # line 685
        try:  # line 686
            sos.config("set", ["strict", "no"])  # line 686
        except SystemExit as E:  # line 687
            _.assertEqual(0, E.code)  # line 687
        makeRepo()  # line 688
        _.assertTrue(checkRepoFlag("strict", False))  # line 689
        try:  # line 690
            sos.config("set", ["strict", "1"])  # line 690
        except SystemExit as E:  # line 691
            _.assertEqual(0, E.code)  # line 691
        makeRepo()  # line 692
        _.assertTrue(checkRepoFlag("strict", True))  # line 693
        try:  # line 694
            sos.config("set", ["strict", "0"])  # line 694
        except SystemExit as E:  # line 695
            _.assertEqual(0, E.code)  # line 695
        makeRepo()  # line 696
        _.assertTrue(checkRepoFlag("strict", False))  # line 697
        try:  # line 698
            sos.config("set", ["strict", "true"])  # line 698
        except SystemExit as E:  # line 699
            _.assertEqual(0, E.code)  # line 699
        makeRepo()  # line 700
        _.assertTrue(checkRepoFlag("strict", True))  # line 701
        try:  # line 702
            sos.config("set", ["strict", "false"])  # line 702
        except SystemExit as E:  # line 703
            _.assertEqual(0, E.code)  # line 703
        makeRepo()  # line 704
        _.assertTrue(checkRepoFlag("strict", False))  # line 705
        try:  # line 706
            sos.config("set", ["strict", "enable"])  # line 706
        except SystemExit as E:  # line 707
            _.assertEqual(0, E.code)  # line 707
        makeRepo()  # line 708
        _.assertTrue(checkRepoFlag("strict", True))  # line 709
        try:  # line 710
            sos.config("set", ["strict", "disable"])  # line 710
        except SystemExit as E:  # line 711
            _.assertEqual(0, E.code)  # line 711
        makeRepo()  # line 712
        _.assertTrue(checkRepoFlag("strict", False))  # line 713
        try:  # line 714
            sos.config("set", ["strict", "enabled"])  # line 714
        except SystemExit as E:  # line 715
            _.assertEqual(0, E.code)  # line 715
        makeRepo()  # line 716
        _.assertTrue(checkRepoFlag("strict", True))  # line 717
        try:  # line 718
            sos.config("set", ["strict", "disabled"])  # line 718
        except SystemExit as E:  # line 719
            _.assertEqual(0, E.code)  # line 719
        makeRepo()  # line 720
        _.assertTrue(checkRepoFlag("strict", False))  # line 721
        try:  # line 722
            sos.config("set", ["strict", "nope"])  # line 722
            _.fail()  # line 722
        except SystemExit as E:  # line 723
            _.assertEqual(1, E.code)  # line 723

    def testLsSimple(_):  # line 725
        _.createFile(1)  # line 726
        _.createFile("foo")  # line 727
        _.createFile("ign1")  # line 728
        _.createFile("ign2")  # line 729
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 730
        try:  # define an ignore pattern  # line 731
            sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 731
        except SystemExit as E:  # line 732
            _.assertEqual(0, E.code)  # line 732
        try:  # additional ignore pattern  # line 733
            sos.config("add", ["ignores", "ign2"])  # additional ignore pattern  # line 733
        except SystemExit as E:  # line 734
            _.assertEqual(0, E.code)  # line 734
        try:  # define a list of ignore patterns  # line 735
            sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 735
        except SystemExit as E:  # line 736
            _.assertEqual(0, E.code)  # line 736
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 737
        _.assertIn("             ignores: ['ign1', 'ign2']", out)  # line 738
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 739
        _.assertInAny('... file1', out)  # line 740
        _.assertInAny('... ign1', out)  # line 741
        _.assertInAny('... ign2', out)  # line 742
        try:  # line 743
            sos.config("rm", ["foo", "bar"])  # line 743
            _.fail()  # line 743
        except SystemExit as E:  # line 744
            _.assertEqual(1, E.code)  # line 744
        try:  # line 745
            sos.config("rm", ["ignores", "foo"])  # line 745
            _.fail()  # line 745
        except SystemExit as E:  # line 746
            _.assertEqual(1, E.code)  # line 746
        try:  # line 747
            sos.config("rm", ["ignores", "ign1"])  # line 747
        except SystemExit as E:  # line 748
            _.assertEqual(0, E.code)  # line 748
        try:  # remove ignore pattern  # line 749
            sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 749
        except SystemExit as E:  # line 750
            _.assertEqual(0, E.code)  # line 750
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 751
        _.assertInAny('... ign1', out)  # line 752
        _.assertInAny('IGN ign2', out)  # line 753
        _.assertNotInAny('... ign2', out)  # line 754

    def testWhitelist(_):  # line 756
# TODO test same for simple mode
        _.createFile(1)  # line 758
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 759
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 760
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 761
        sos.commit(options=["--force"])  # attempt to commit the file  # line 762
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 763
        try:  # Exit because dirty  # line 764
            sos.online()  # Exit because dirty  # line 764
            _.fail()  # Exit because dirty  # line 764
        except:  # exception expected  # line 765
            pass  # exception expected  # line 765
        _.createFile("x2")  # add another change  # line 766
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 767
        try:  # force beyond dirty flag check  # line 768
            sos.online(["--force"])  # force beyond dirty flag check  # line 768
            _.fail()  # force beyond dirty flag check  # line 768
        except:  # line 769
            pass  # line 769
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 770
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 771

        _.createFile(1)  # line 773
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 774
        sos.offline("xx", ["--track"])  # line 775
        sos.add(".", "./file*")  # line 776
        sos.commit()  # should NOT ask for force here  # line 777
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 778

    def testRemove(_):  # line 780
        _.createFile(1, "x" * 100)  # line 781
        sos.offline("trunk")  # line 782
        try:  # line 783
            sos.delete("trunk")  # line 783
            _fail()  # line 783
        except:  # line 784
            pass  # line 784
        _.createFile(2, "y" * 10)  # line 785
        sos.branch("added")  # line 786
        sos.delete("trunk")  # line 787
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 788
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 789
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 790
        sos.branch("next")  # line 791
        _.createFile(3, "y" * 10)  # make a change  # line 792
        sos.delete("added", "--force")  # should succeed  # line 793

    def testUsage(_):  # line 795
        try:  # TODO expect sys.exit(0)  # line 796
            sos.usage()  # TODO expect sys.exit(0)  # line 796
            _.fail()  # TODO expect sys.exit(0)  # line 796
        except:  # line 797
            pass  # line 797
        try:  # line 798
            sos.usage(short=True)  # line 798
            _.fail()  # line 798
        except:  # line 799
            pass  # line 799

    def testOnly(_):  # line 801
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 802
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 803
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 804
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 805
        sos.offline(os.getcwd(), ["--track", "--strict"])  # line 806
        _.createFile(1)  # line 807
        _.createFile(2)  # line 808
        sos.add(".", "./file1")  # line 809
        sos.add(".", "./file2")  # line 810
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 811
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # only meta and file1  # line 812
        sos.commit()  # adds also file2  # line 813
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # only meta and file1  # line 814
        _.createFile(1, "cc")  # modify both files  # line 815
        _.createFile(2, "dd")  # line 816
        try:  # line 817
            sos.config("set", ["texttype", "file2"])  # line 817
        except SystemExit as E:  # line 818
            _.assertEqual(0, E.code)  # line 818
        changes = sos.changes(excps=["./file1"])  # line 819
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 820
        _.assertTrue("./file2" in changes.modifications)  # line 821
        _.assertIn("DIF ./file2", wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 822
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 823

    def testDiff(_):  # line 825
        try:  # line 826
            sos.config("set", ["texttype", "file1"])  # line 826
        except SystemExit as E:  # line 827
            _.assertEqual(0, E.code)  # line 827
        sos.offline(options=["--strict"])  # line 828
        _.createFile(1)  # line 829
        _.createFile(2)  # line 830
        sos.commit()  # line 831
        _.createFile(1, "sdfsdgfsdf")  # line 832
        _.createFile(2, "12343")  # line 833
        sos.commit()  # line 834
        _.createFile(1, "foobar")  # line 835
        _.assertAllIn(["MOD ./file2", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # vs. second last  # line 836
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 837

    def testReorderRenameActions(_):  # line 839
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # line 840
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 841
        try:  # line 842
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 842
            _.fail()  # line 842
        except:  # line 843
            pass  # line 843

    def testMove(_):  # line 845
        sos.offline(options=["--strict", "--track"])  # line 846
        _.createFile(1)  # line 847
        sos.add(".", "./file?")  # line 848
# test source folder missing
        try:  # line 850
            sos.move("sub", "sub/file?", ".", "?file")  # line 850
            _.fail()  # line 850
        except:  # line 851
            pass  # line 851
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 853
        _.assertTrue(os.path.exists("sub"))  # line 854
        _.assertTrue(os.path.exists("sub/file1"))  # line 855
        _.assertFalse(os.path.exists("file1"))  # line 856
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 858
        _.assertTrue(os.path.exists("1file"))  # line 859
        _.assertFalse(os.path.exists("sub/file1"))  # line 860
# test nothing matches source pattern
        try:  # line 862
            sos.move(".", "a*", ".", "b*")  # line 862
            _.fail()  # line 862
        except:  # line 863
            pass  # line 863
        sos.add(".", "*")  # anything pattern  # line 864
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 865
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 865
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 865
        except:  # line 866
            pass  # line 866
# test rename no conflict
        _.createFile(1)  # line 868
        _.createFile(2)  # line 869
        _.createFile(3)  # line 870
        sos.add(".", "./file*")  # line 871
        try:  # define an ignore pattern  # line 872
            sos.config("set", ["ignores", "file3;file4"])  # define an ignore pattern  # line 872
        except SystemExit as E:  # line 873
            _.assertEqual(0, E.code)  # line 873
        try:  # line 874
            sos.config("set", ["ignoresWhitelist", "file3"])  # line 874
        except SystemExit as E:  # line 875
            _.assertEqual(0, E.code)  # line 875
        sos.move(".", "./file*", ".", "fi*le")  # line 876
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 877
        _.assertFalse(os.path.exists("fi4le"))  # line 878
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 880
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 884
        sos.add(".", "./?a?b", ["--force"])  # line 885
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 886
        _.createFile("1a2b")  # should not be tracked  # line 887
        _.createFile("a1b2")  # should be tracked  # line 888
        sos.commit()  # line 889
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # line 890
        _.assertTrue(os.path.exists(sos.branchFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 891
        _.createFile("1a1b1")  # line 892
        _.createFile("1a1b2")  # line 893
        sos.add(".", "?a?b*")  # line 894
        _.assertIn("not unique", wrapChannels(lambda: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 895
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testHashCollision(_):  # line 899
        sos.offline()  # line 900
        _.createFile(1)  # line 901
        os.mkdir(sos.branchFolder(0, 1))  # line 902
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.branchFolder(0, 1))  # line 903
        _.createFile(1)  # line 904
        try:  # should exit with error due to collision detection  # line 905
            sos.commit()  # should exit with error due to collision detection  # line 905
            _.fail()  # should exit with error due to collision detection  # line 905
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 906
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 906

    def testFindBase(_):  # line 908
        old = os.getcwd()  # line 909
        try:  # line 910
            os.mkdir("." + os.sep + ".git")  # line 911
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 912
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 913
            os.chdir("a" + os.sep + "b")  # line 914
            s, vcs, cmd = sos.findSosVcsBase()  # line 915
            _.assertIsNotNone(s)  # line 916
            _.assertIsNotNone(vcs)  # line 917
            _.assertEqual("git", cmd)  # line 918
        finally:  # line 919
            os.chdir(old)  # line 919

# TODO test command line operation --sos vs. --vcs
# check exact output instead of expected fail


if __name__ == '__main__':  # line 925
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or "true" in [os.getenv("DEBUG", "false").strip().lower(), os.getenv("CI", "false").strip().lower()] else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 926
    if configr:  # line 928
        c = configr.Configr("sos")  # line 929
        c.loadSettings()  # line 929
        if len(c.keys()) > 0:  # line 930
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 930
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 931
