#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1a0ffb87

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

    def testFirstofmap(_):  # line 119
        _.assertEqual(2, sos.firstOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 120
        _.assertIsNone(sos.firstOfMap({"a": 1, "b": 2}, []))  # line 121

    def testAjoin(_):  # line 123
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 124
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 125

    def testFindChanges(_):  # line 127
        m = sos.Metadata(os.getcwd())  # line 128
        sos.config("set", ["texttype", "*"])  # line 129
        sos.config("set", ["ignores", "*.cfg;*.cfg.bak"])  # line 130
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 131
        m.loadBranches()  # line 132
        _.createFile(1, "1")  # line 133
        m.createBranch(0)  # line 134
        _.assertEqual(1, len(m.paths))  # line 135
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 136
        _.createFile(1, "2")  # modify existing file  # line 137
        _.createFile(2, "2")  # add another file  # line 138
        m.loadCommit(0, 0)  # line 139
        changes = m.findChanges()  # detect time skew  # line 140
        _.assertEqual(1, len(changes.additions))  # line 141
        _.assertEqual(0, len(changes.deletions))  # line 142
        _.assertEqual(1, len(changes.modifications))  # line 143
        m.integrateChangeset(changes)  # line 144
        _.createFile(2, "12")  # modify file again  # line 145
        changes = m.findChanges(0, 1)  # by size, creating new commit  # line 146
        _.assertEqual(0, len(changes.additions))  # line 147
        _.assertEqual(0, len(changes.deletions))  # line 148
        _.assertEqual(1, len(changes.modifications))  # line 149
        _.assertTrue(os.path.exists(sos.branchFolder(0, 1)))  # line 150
        _.assertTrue(os.path.exists(sos.branchFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 151

    def testDiffFunc(_):  # line 153
        a = {"./a": sos.PathInfo("", 0, 0, "")}  # line 154
        b = {"./a": sos.PathInfo("", 0, 0, "")}  # line 155
        changes = sos.diffPathSets(a, b)  # line 156
        _.assertEqual(0, len(changes.additions))  # line 157
        _.assertEqual(0, len(changes.deletions))  # line 158
        _.assertEqual(0, len(changes.modifications))  # line 159
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # line 160
        changes = sos.diffPathSets(a, b)  # line 161
        _.assertEqual(0, len(changes.additions))  # line 162
        _.assertEqual(0, len(changes.deletions))  # line 163
        _.assertEqual(1, len(changes.modifications))  # line 164
        b = {}  # diff contains no entries -> no change  # line 165
        changes = sos.diffPathSets(a, b)  # line 166
        _.assertEqual(0, len(changes.additions))  # line 167
        _.assertEqual(0, len(changes.deletions))  # line 168
        _.assertEqual(0, len(changes.modifications))  # line 169
        b = {"./a": sos.PathInfo("", None, 1, "")}  # in diff marked as deleted  # line 170
        changes = sos.diffPathSets(a, b)  # line 171
        _.assertEqual(0, len(changes.additions))  # line 172
        _.assertEqual(1, len(changes.deletions))  # line 173
        _.assertEqual(0, len(changes.modifications))  # line 174
        b = {"./b": sos.PathInfo("", 1, 1, "")}  # line 175
        changes = sos.diffPathSets(a, b)  # line 176
        _.assertEqual(1, len(changes.additions))  # line 177
        _.assertEqual(0, len(changes.deletions))  # line 178
        _.assertEqual(0, len(changes.modifications))  # line 179
        a = {"./a": sos.PathInfo("", None, 0, "")}  # mark as deleted  # line 180
        b = {"./a": sos.PathInfo("", 1, 0, "")}  # re-added  # line 181
        changes = sos.diffPathSets(a, b)  # line 182
        _.assertEqual(1, len(changes.additions))  # line 183
        _.assertEqual(0, len(changes.deletions))  # line 184
        _.assertEqual(0, len(changes.modifications))  # line 185
        changes = sos.diffPathSets(b, a)  # line 186
        _.assertEqual(0, len(changes.additions))  # line 187
        _.assertEqual(1, len(changes.deletions))  # line 188
        _.assertEqual(0, len(changes.modifications))  # line 189

    def testPatternPaths(_):  # line 191
        sos.offline(options=["--track"])  # line 192
        os.mkdir("sub")  # line 193
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 194
        sos.add("sub", "sub/file?")  # line 195
        sos.commit("test")  # should pick up sub/file1 pattern  # line 196
        _.assertEqual(2, len(os.listdir(os.path.join(sos.metaFolder, "b0", "r1"))))  # sub/file1 was added  # line 197
        _.createFile(1)  # line 198
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 199
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 199
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 199
        except:  # line 200
            pass  # line 200

    def testTokenizeGlobPattern(_):  # line 202
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 203
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 204
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 205
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 206
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 207
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 208

    def testTokenizeGlobPatterns(_):  # line 210
        try:  # because number of literal strings differs  # line 211
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 211
            _.fail()  # because number of literal strings differs  # line 211
        except:  # line 212
            pass  # line 212
        try:  # because glob patterns differ  # line 213
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 213
            _.fail()  # because glob patterns differ  # line 213
        except:  # line 214
            pass  # line 214
        try:  # glob patterns differ, regardless of position  # line 215
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 215
            _.fail()  # glob patterns differ, regardless of position  # line 215
        except:  # line 216
            pass  # line 216
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 217
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 218
        try:  # succeeds, because glob patterns match (differ only in position)  # line 219
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 219
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 219
        except:  # line 220
            pass  # line 220

    def testConvertGlobFiles(_):  # line 222
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 223
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 224

    def testFolderRemove(_):  # line 226
        m = sos.Metadata(os.getcwd())  # line 227
        _.createFile(1)  # line 228
        _.createFile("a", prefix="sub")  # line 229
        sos.offline()  # line 230
        _.createFile(2)  # line 231
        os.unlink("sub" + os.sep + "a")  # line 232
        os.rmdir("sub")  # line 233
        changes = sos.changes()  # line 234
        _.assertEqual(1, len(changes.additions))  # line 235
        _.assertEqual(0, len(changes.modifications))  # line 236
        _.assertEqual(1, len(changes.deletions))  # line 237
        _.createFile("a", prefix="sub")  # line 238
        changes = sos.changes()  # line 239
        _.assertEqual(0, len(changes.deletions))  # line 240

    def testComputeSequentialPathSet(_):  # line 242
        os.makedirs(sos.branchFolder(0, 0))  # line 243
        os.makedirs(sos.branchFolder(0, 1))  # line 244
        os.makedirs(sos.branchFolder(0, 2))  # line 245
        os.makedirs(sos.branchFolder(0, 3))  # line 246
        os.makedirs(sos.branchFolder(0, 4))  # line 247
        m = sos.Metadata(os.getcwd())  # line 248
        m.branch = 0  # line 249
        m.commit = 2  # line 250
        m.saveBranches()  # line 251
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 252
        m.saveCommit(0, 0)  # initial  # line 253
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 254
        m.saveCommit(0, 1)  # mod  # line 255
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 256
        m.saveCommit(0, 2)  # add  # line 257
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 258
        m.saveCommit(0, 3)  # del  # line 259
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 260
        m.saveCommit(0, 4)  # readd  # line 261
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 262
        m.saveBranch(0)  # line 263
        m.computeSequentialPathSet(0, 4)  # line 264
        _.assertEqual(2, len(m.paths))  # line 265

    def testParseRevisionString(_):  # line 267
        m = sos.Metadata(os.getcwd())  # line 268
        m.branch = 1  # line 269
        m.commits = {0: 0, 1: 1, 2: 2}  # line 270
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 271
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 272
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 273
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 274
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 275
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 276
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 277

    def testOfflineEmpty(_):  # line 279
        os.mkdir("." + os.sep + sos.metaFolder)  # line 280
        try:  # line 281
            sos.offline("trunk")  # line 281
            _.fail()  # line 281
        except SystemExit as E:  # line 282
            _.assertEqual(1, E.code)  # line 282
        os.rmdir("." + os.sep + sos.metaFolder)  # line 283
        sos.offline("test")  # line 284
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 285
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 286
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 287
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 288
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 289
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 0))))  # only meta data file  # line 290

    def testOfflineWithFiles(_):  # line 292
        _.createFile(1, "x" * 100)  # line 293
        _.createFile(2)  # line 294
        sos.offline("test")  # line 295
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 296
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 297
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 298
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 299
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 300
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 301
        _.assertEqual(3, len(os.listdir(sos.branchFolder(0, 0))))  # only meta data file plus branch base file copies  # line 302

    def testBranch(_):  # line 304
        _.createFile(1, "x" * 100)  # line 305
        _.createFile(2)  # line 306
        sos.offline("test")  # b0/r0  # line 307
        sos.branch("other")  # b1/r0  # line 308
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 309
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 310
        _.assertEqual(list(sorted(os.listdir(sos.branchFolder(0, 0)))), list(sorted(os.listdir(sos.branchFolder(1, 0)))))  # line 312
        _.createFile(1, "z")  # modify file  # line 314
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 315
        _.assertNotEqual(os.stat("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size, os.stat("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa").st_size)  # line 316
        _.createFile(3, "z")  # line 318
        sos.branch("from_last_revision", ["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 319
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 320
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 325
        _.createFile(1, "x" * 100)  # line 326
        _.createFile(2)  # line 327
        sos.offline("test")  # line 328
        changes = sos.changes()  # line 329
        _.assertEqual(0, len(changes.additions))  # line 330
        _.assertEqual(0, len(changes.deletions))  # line 331
        _.assertEqual(0, len(changes.modifications))  # line 332
        _.createFile(1, "z")  # size change  # line 333
        changes = sos.changes()  # line 334
        _.assertEqual(0, len(changes.additions))  # line 335
        _.assertEqual(0, len(changes.deletions))  # line 336
        _.assertEqual(1, len(changes.modifications))  # line 337
        sos.commit("message")  # line 338
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 339
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.branchFolder(0, 1)))  # line 340
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # no further files, only the modified one  # line 341
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 342
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 343
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 344
        os.unlink("file2")  # line 345
        changes = sos.changes()  # line 346
        _.assertEqual(0, len(changes.additions))  # line 347
        _.assertEqual(1, len(changes.deletions))  # line 348
        _.assertEqual(1, len(changes.modifications))  # line 349
        sos.commit("modified")  # line 350
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 2))))  # no additional files, only mentions in metadata  # line 351
        try:  # expecting Exit due to no changes  # line 352
            sos.commit("nothing")  # expecting Exit due to no changes  # line 352
            _.fail()  # expecting Exit due to no changes  # line 352
        except:  # line 353
            pass  # line 353

    def testGetBranch(_):  # line 355
        m = sos.Metadata(os.getcwd())  # line 356
        m.branch = 1  # current branch  # line 357
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 358
        _.assertEqual(27, m.getBranchByName(27))  # line 359
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 360
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 361
        _.assertIsNone(m.getBranchByName("unknown"))  # line 362
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 363
        _.assertEqual(13, m.getRevisionByName("13"))  # line 364
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 365
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 366

    def testTagging(_):  # line 368
        m = sos.Metadata(os.getcwd())  # line 369
        sos.offline()  # line 370
        _.createFile(111)  # line 371
        sos.commit("tag", ["--tag"])  # line 372
        _.createFile(2)  # line 373
        try:  # line 374
            sos.commit("tag")  # line 374
            _.fail()  # line 374
        except:  # line 375
            pass  # line 375
        sos.commit("tag-2", ["--tag"])  # line 376

    def testSwitch(_):  # line 378
        _.createFile(1, "x" * 100)  # line 379
        _.createFile(2, "y")  # line 380
        sos.offline("test")  # file1-2  in initial branch commit  # line 381
        sos.branch("second")  # file1-2  switch, having same files  # line 382
        sos.switch("0")  # no change  switch back, no problem  # line 383
        sos.switch("second")  # no change  # switch back, no problem  # line 384
        _.createFile(3, "y")  # generate a file  # line 385
        try:  # uncommited changes detected  # line 386
            sos.switch("test")  # uncommited changes detected  # line 386
            _.fail()  # uncommited changes detected  # line 386
        except SystemExit as E:  # line 387
            _.assertEqual(1, E.code)  # line 387
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 388
        sos.changes()  # line 389
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 390
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 391
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 392
        _.assertIn("  * b00   'test'", out)  # line 393
        _.assertIn("    b01 'second'", out)  # line 394
        _.assertIn("(dirty)", out)  # one branch has commits  # line 395
        _.assertIn("(in sync)", out)  # the other doesn't  # line 396
        _.createFile(4, "xy")  # generate a file  # line 397
        sos.switch("second", "--force")  # avoids warning on uncommited changes, but keeps file4  # line 398
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 399
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 400
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 401
        sos.switch("test", "--force")  # should restore file1 and remove file3  # line 402
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 403
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 404

    def testAutoDetectVCS(_):  # line 406
        os.mkdir(".git")  # line 407
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 408
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 409
            meta = fd.read()  # line 409
        _.assertTrue("\"master\"" in meta)  # line 410
        os.rmdir(".git")  # line 411

    def testUpdate(_):  # line 413
        sos.offline("trunk")  # create initial branch b0/r0  # line 414
        _.createFile(1, "x" * 100)  # line 415
        sos.commit("second")  # create b0/r1  # line 416

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 418
        _.assertFalse(_.existsFile(1))  # line 419

        sos.update("/1")  # recreate file1  # line 421
        _.assertTrue(_.existsFile(1))  # line 422

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 424
        _.assertTrue(os.path.exists(sos.branchFolder(0, 2)))  # line 425
        _.assertTrue(os.path.exists(sos.branchFolder(0, 2, file=sos.metaFile)))  # line 426
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 2))))  # only meta data file, no differential files  # line 427

        sos.update("/1")  # do nothing, as nothing has changed  # line 429
        _.assertTrue(_.existsFile(1))  # line 430

        _.createFile(2, "y" * 100)  # line 432
#    out = wrapChannels(() -> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", ["--force"])  # automatically including file 2 (as we are in simple mode)  # line 435
        _.assertTrue(_.existsFile(2))  # line 436
        sos.update("trunk", ["--add"])  # only add stuff  # line 437
        _.assertTrue(_.existsFile(2))  # line 438
        sos.update("trunk")  # nothing to do  # line 439
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 440

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 442
        _.createFile(10, theirs)  # line 443
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 444
        _.createFile(11, mine)  # line 445
        _.assertEqual(b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # completely recreated other file  # line 446
        _.assertEqual(b"a\nb\nc\nd\ne\ng\nf\ng\nx\nh\nx\nx\ny\ny\nj\nk", sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT, conflictResolution=sos.ConflictResolution.MINE))  # line 447

    def testUpdate2(_):  # line 449
        _.createFile("test.txt", "x" * 10)  # line 450
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 451
        sos.branch("mod")  # line 452
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 453
        time.sleep(FS_PRECISION)  # line 454
        sos.commit("mod")  # create b0/r1  # line 455
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 456
        with open("test.txt", "rb") as fd:  # line 457
            _.assertEqual(b"x" * 10, fd.read())  # line 457
        sos.update("mod", ["--theirs"])  # integrate changes TODO same with ask -> theirs  # line 458
        with open("test.txt", "rb") as fd:  # line 459
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 459
        _.createFile("test.txt", "x" * 10)  # line 460
        mockInput(["t"], lambda: sos.update("mod", ["--ask"]))  # same as above with interaction -> theirs  # line 461
        with open("test.txt", "rb") as fd:  # line 462
            _.assertEqual(b"x" * 5 + b"y" * 5, fd.read())  # line 462

    def testIsTextType(_):  # line 464
        m = sos.Metadata(".")  # line 465
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 466
        m.c.bintype = ["*.md.confluence"]  # line 467
        _.assertTrue(m.isTextType("ab.txt"))  # line 468
        _.assertTrue(m.isTextType("./ab.txt"))  # line 469
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 470
        _.assertFalse(m.isTextType("bc/ab."))  # line 471
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 472
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 473
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 474
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 475

    def testEolDet(_):  # line 477
        ''' Check correct end-of-line detection. '''  # line 478
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 479
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 480
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 481
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 482
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 483
        _.assertIsNone(sos.eoldet(b""))  # line 484
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 485

    def testMerge(_):  # line 487
        ''' Check merge results depending on conflict solution options. '''  # line 488
        a = b"a\nb\ncc\nd"  # line 489
        b = b"a\nb\nee\nd"  # line 490
        _.assertEqual(b"a\nb\ncc\nee\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT))  # means insert changes from a into b, but don't replace  # line 491
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE))  # line 492
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH))  # line 493
# Now test intra-line merging without conflicts
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.INSERT))  # because it's a deletion ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 495
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbc d\ne", b"a\nbcd\ne", mergeOperation=sos.MergeOperation.REMOVE))  # ['  a', '- bc d', '?   -\n', '+ bcd', '  e']  # line 496
        _.assertEqual(b"a\nbc d\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.INSERT))  # nothing to insert  # line 497
        _.assertEqual(b"a\nbcd\ne", sos.merge(b"a\nbcd\ne", b"a\nbc d\ne", mergeOperation=sos.MergeOperation.REMOVE))  # remove space  # line 498
# Test with change + insert (conflict)
        _.assertEqual(b"a\nb fdd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.MINE))  # line 500
        _.assertEqual(b"a\nb cd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.THEIRS))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 501
        _.assertEqual(b"a\nb fdd d\ne", mockInput(["i"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 502
        _.assertEqual(b"a\nb cd d\ne", mockInput(["t"], lambda: sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", conflictResolution=sos.ConflictResolution.ASK)))  # ['  a', '- b cd d', '?   ^\n', '+ b fdd d', '?   ^^\n', '  e']  # line 503
        _.assertEqual(b"abbc", sos.merge(b"abbc", b"addc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 504
        _.assertEqual(b"a\nbb\nc", sos.merge(b"a\nbb\nc", b"a\ndd\nc", mergeOperation=sos.MergeOperation.BOTH, conflictResolution=sos.ConflictResolution.THEIRS))  # line 505
        _.assertIn("Differing EOL-styles", wrapChannels(lambda: sos.merge(b"a\nb", b"a\r\nb")))  # expect warning  # line 506
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb"))  # in doubt, use "mine" CR-LF  # line 507

    def testPickyMode(_):  # line 509
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 510
        sos.offline("trunk", ["--picky"])  # line 511
        changes = sos.changes()  # line 512
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 513
        sos.add(".", "./file?", ["--force"])  # line 514
        _.createFile(1, "aa")  # line 515
        sos.commit("First")  # add one file  # line 516
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # line 517
        _.createFile(2, "b")  # line 518
        try:  # add nothing, because picky  # line 519
            sos.commit("Second")  # add nothing, because picky  # line 519
        except:  # line 520
            pass  # line 520
        sos.add(".", "./file?")  # line 521
        sos.commit("Third")  # line 522
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # line 523
        out = wrapChannels(lambda: sos.log([])).replace("\r", "")  # line 524
        _.assertIn("  * r2", out)  # line 525
        _.createFile(3, prefix="sub")  # line 526
        sos.add("sub", "sub/file?")  # line 527
        changes = sos.changes()  # line 528
        _.assertEqual(1, len(changes.additions))  # line 529
        _.assertTrue("sub/file3" in changes.additions)  # line 530

    def testTrackedSubfolder(_):  # line 532
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 533
        os.mkdir("." + os.sep + "sub")  # line 534
        sos.offline("trunk", ["--track"])  # line 535
        _.createFile(1, "x")  # line 536
        _.createFile(1, "x", prefix="sub")  # line 537
        sos.add(".", "./file?")  # add glob pattern to track  # line 538
        sos.commit("First")  # line 539
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # one new file + meta file  # line 540
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 541
        sos.commit("Second")  # one new file + meta  # line 542
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # one new file + meta file  # line 543
        os.unlink("file1")  # remove from basefolder  # line 544
        _.createFile(2, "y")  # line 545
        sos.remove(".", "sub/file?")  # line 546
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 547
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 547
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 547
        except:  # line 548
            pass  # line 548
        sos.commit("Third")  # line 549
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # one new file + meta  # line 550
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 553
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 558
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 559
        _.createFile(1)  # line 560
        _.createFile("a123a")  # untracked file "a123a"  # line 561
        sos.add(".", "./file?")  # add glob tracking pattern  # line 562
        sos.commit("second")  # versions "file1"  # line 563
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # one new file + meta file  # line 564
        out = wrapChannels(lambda: sos.status()).replace("\r", "")  # line 565
        _.assertIn("  | ./file?", out)  # line 566

        _.createFile(2)  # untracked file "file2"  # line 568
        sos.commit("third")  # versions "file2"  # line 569
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # one new file + meta file  # line 570

        os.mkdir("." + os.sep + "sub")  # line 572
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 573
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 574
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 3))))  # meta file only, no other tracked path/file  # line 575

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 577
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 578
        sos.add(".", "./a*a")  # add tracking pattern  # line 579
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 580
        _.assertEqual(0, len(changes.modifications))  # line 581
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 582
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 583

        sos.commit("Second_2")  # line 585
        _.assertEqual(2, len(os.listdir(sos.branchFolder(1, 1))))  # "a123a" + meta file  # line 586
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 587
        _.assertTrue(os.path.exists("." + os.sep + "file2"))  # line 588

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 590
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 591
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # should not have been touched so far  # line 592

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 594
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 595
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 596

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 598
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 599
        _.assertEqual(3, len(os.listdir(sos.branchFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 600
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 601
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 602
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 603
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 604
# TODO test switch --meta

    def testLsTracked(_):  # line 607
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 608
        _.createFile(1)  # line 609
        _.createFile("foo")  # line 610
        sos.add(".", "./file*")  # capture one file  # line 611
        sos.ls()  # line 612
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 613
        _.assertInAny("TRK file1  (file*)", out)  # line 614
        _.assertNotInAny("... file1  (file*)", out)  # line 615
        _.assertInAny("... foo", out)  # line 616
        out = sos.safeSplit(wrapChannels(lambda: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 617
        _.assertInAny("TRK file*", out)  # line 618
        _.createFile("a", prefix="sub")  # line 619
        sos.add("sub", "sub/a")  # line 620
        sos.ls("sub")  # line 621
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda: sos.ls("sub")).replace("\r", ""), "\n"))  # line 622

    def testCompression(_):  # line 624
        _.createFile(1)  # line 625
        sos.offline("master", options=["--force"])  # line 626
        _.assertTrue(_.existsFile(sos.branchFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 627
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 628
        _.createFile(2)  # line 629
        sos.commit("Added file2")  # line 630
        _.assertTrue(_.existsFile(sos.branchFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 631
        _.assertFalse(_.existsFile(sos.branchFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 632

    def testConfigVariations(_):  # line 634
        def makeRepo():  # line 635
            try:  # line 636
                os.unlink("file1")  # line 636
            except:  # line 637
                pass  # line 637
            sos.offline("master", options=["--plain", "--force"])  # line 638
            _.createFile(1)  # line 639
            sos.commit("Added file1")  # line 640
        sos.config("set", ["strict", "on"])  # line 641
        makeRepo()  # line 642
        _.assertTrue(checkRepoFlag("strict", True))  # line 643
        sos.config("set", ["strict", "off"])  # line 644
        makeRepo()  # line 645
        _.assertTrue(checkRepoFlag("strict", False))  # line 646
        sos.config("set", ["strict", "yes"])  # line 647
        makeRepo()  # line 648
        _.assertTrue(checkRepoFlag("strict", True))  # line 649
        sos.config("set", ["strict", "no"])  # line 650
        makeRepo()  # line 651
        _.assertTrue(checkRepoFlag("strict", False))  # line 652
        sos.config("set", ["strict", "1"])  # line 653
        makeRepo()  # line 654
        _.assertTrue(checkRepoFlag("strict", True))  # line 655
        sos.config("set", ["strict", "0"])  # line 656
        makeRepo()  # line 657
        _.assertTrue(checkRepoFlag("strict", False))  # line 658
        sos.config("set", ["strict", "true"])  # line 659
        makeRepo()  # line 660
        _.assertTrue(checkRepoFlag("strict", True))  # line 661
        sos.config("set", ["strict", "false"])  # line 662
        makeRepo()  # line 663
        _.assertTrue(checkRepoFlag("strict", False))  # line 664
        sos.config("set", ["strict", "enable"])  # line 665
        makeRepo()  # line 666
        _.assertTrue(checkRepoFlag("strict", True))  # line 667
        sos.config("set", ["strict", "disable"])  # line 668
        makeRepo()  # line 669
        _.assertTrue(checkRepoFlag("strict", False))  # line 670
        sos.config("set", ["strict", "enabled"])  # line 671
        makeRepo()  # line 672
        _.assertTrue(checkRepoFlag("strict", True))  # line 673
        sos.config("set", ["strict", "disabled"])  # line 674
        makeRepo()  # line 675
        _.assertTrue(checkRepoFlag("strict", False))  # line 676
        try:  # line 677
            sos.config("set", ["strict", "nope"])  # line 677
            _.fail()  # line 677
        except:  # line 678
            pass  # line 678

    def testLsSimple(_):  # line 680
        _.createFile(1)  # line 681
        _.createFile("foo")  # line 682
        _.createFile("ign1")  # line 683
        _.createFile("ign2")  # line 684
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 685
        sos.config("set", ["ignores", "ign1"])  # define an ignore pattern  # line 686
        sos.config("add", ["ignores", "ign2"])  # additional ignore pattern  # line 687
        sos.config("set", ["ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 688
        out = wrapChannels(lambda: sos.config("show")).replace("\r", "")  # line 689
        _.assertIn("             ignores: ['ign1', 'ign2']", out)  # line 690
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 691
        _.assertInAny('... file1', out)  # line 692
        _.assertInAny('... ign1', out)  # line 693
        _.assertInAny('... ign2', out)  # line 694
        try:  # line 695
            sos.config("rm", ["foo", "bar"])  # line 695
            _.fail()  # line 695
        except:  # line 696
            pass  # line 696
        try:  # line 697
            sos.config("rm", ["ignores", "foo"])  # line 697
            _.fail()  # line 697
        except:  # line 698
            pass  # line 698
        sos.config("rm", ["ignores", "ign1"])  # line 699
        sos.config("unset", ["ignoresWhitelist"])  # remove ignore pattern  # line 700
        out = sos.safeSplit(wrapChannels(lambda: sos.ls()).replace("\r", ""), "\n")  # line 701
        _.assertInAny('... ign1', out)  # line 702
        _.assertInAny('IGN ign2', out)  # line 703
        _.assertNotInAny('... ign2', out)  # line 704

    def testWhitelist(_):  # line 706
# TODO test same for simple mode
        _.createFile(1)  # line 708
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 709
        sos.offline("xx", ["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 710
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 711
        sos.commit(options=["--force"])  # attempt to commit the file  # line 712
        _.assertEqual(1, len(os.listdir(sos.branchFolder(0, 1))))  # only meta data, file1 was ignored  # line 713
        try:  # Exit because dirty  # line 714
            sos.online()  # Exit because dirty  # line 714
            _.fail()  # Exit because dirty  # line 714
        except:  # exception expected  # line 715
            pass  # exception expected  # line 715
        _.createFile("x2")  # add another change  # line 716
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 717
        try:  # force beyond dirty flag check  # line 718
            sos.online(["--force"])  # force beyond dirty flag check  # line 718
            _.fail()  # force beyond dirty flag check  # line 718
        except:  # line 719
            pass  # line 719
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 720
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 721

        _.createFile(1)  # line 723
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 724
        sos.offline("xx", ["--track"])  # line 725
        sos.add(".", "./file*")  # line 726
        sos.commit()  # should NOT ask for force here  # line 727
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 728

    def testRemove(_):  # line 730
        _.createFile(1, "x" * 100)  # line 731
        sos.offline("trunk")  # line 732
        try:  # line 733
            sos.delete("trunk")  # line 733
            _fail()  # line 733
        except:  # line 734
            pass  # line 734
        _.createFile(2, "y" * 10)  # line 735
        sos.branch("added")  # line 736
        sos.delete("trunk")  # line 737
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # meta data file and "b1"  # line 738
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 739
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 740
        sos.branch("next")  # line 741
        _.createFile(3, "y" * 10)  # make a change  # line 742
        sos.delete("added", "--force")  # should succeed  # line 743

    def testUsage(_):  # line 745
        try:  # TODO expect sys.exit(0)  # line 746
            sos.usage()  # TODO expect sys.exit(0)  # line 746
            _.fail()  # TODO expect sys.exit(0)  # line 746
        except:  # line 747
            pass  # line 747
        try:  # line 748
            sos.usage(short=True)  # line 748
            _.fail()  # line 748
        except:  # line 749
            pass  # line 749

    def testOnly(_):  # line 751
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 752
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 753
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 754
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 755
        sos.offline(os.getcwd(), ["--track", "--strict"])  # line 756
        _.createFile(1)  # line 757
        _.createFile(2)  # line 758
        sos.add(".", "./file1")  # line 759
        sos.add(".", "./file2")  # line 760
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 761
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # only meta and file1  # line 762
        sos.commit()  # adds also file2  # line 763
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 2))))  # only meta and file1  # line 764
        _.createFile(1, "cc")  # modify both files  # line 765
        _.createFile(2, "dd")  # line 766
        sos.config("set", ["texttype", "file2"])  # line 767
        changes = sos.changes(excps=["./file1"])  # line 768
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 769
        _.assertTrue("./file2" in changes.modifications)  # line 770
        _.assertIn("DIF ./file2", wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 771
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 772

    def testDiff(_):  # line 774
        sos.config("set", ["texttype", "file1"])  # line 775
        sos.offline(options=["--strict"])  # line 776
        _.createFile(1)  # line 777
        _.createFile(2)  # line 778
        sos.commit()  # line 779
        _.createFile(1, "sdfsdgfsdf")  # line 780
        _.createFile(2, "12343")  # line 781
        sos.commit()  # line 782
        _.createFile(1, "foobar")  # line 783
        _.assertAllIn(["MOD ./file2", "DIF ./file1", "- | 0000 |xxxxxxxxxx|", "+ | 0000 |foobar|"], wrapChannels(lambda: sos.diff("/-2")))  # vs. second last  # line 784
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 785

    def testReorderRenameActions(_):  # line 787
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # line 788
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 789
        try:  # line 790
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 790
            _.fail()  # line 790
        except:  # line 791
            pass  # line 791

    def testMove(_):  # line 793
        sos.offline(options=["--strict", "--track"])  # line 794
        _.createFile(1)  # line 795
        sos.add(".", "./file?")  # line 796
# test source folder missing
        try:  # line 798
            sos.move("sub", "sub/file?", ".", "?file")  # line 798
            _.fail()  # line 798
        except:  # line 799
            pass  # line 799
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 801
        _.assertTrue(os.path.exists("sub"))  # line 802
        _.assertTrue(os.path.exists("sub/file1"))  # line 803
        _.assertFalse(os.path.exists("file1"))  # line 804
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 806
        _.assertTrue(os.path.exists("1file"))  # line 807
        _.assertFalse(os.path.exists("sub/file1"))  # line 808
# test nothing matches source pattern
        try:  # line 810
            sos.move(".", "a*", ".", "b*")  # line 810
            _.fail()  # line 810
        except:  # line 811
            pass  # line 811
        sos.add(".", "*")  # anything pattern  # line 812
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 813
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 813
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 813
        except:  # line 814
            pass  # line 814
# test rename no conflict
        _.createFile(1)  # line 816
        _.createFile(2)  # line 817
        _.createFile(3)  # line 818
        sos.add(".", "./file*")  # line 819
        sos.config("set", ["ignores", "file3;file4"])  # define an ignore pattern  # line 820
        sos.config("set", ["ignoresWhitelist", "file3"])  # line 821
        sos.move(".", "./file*", ".", "fi*le")  # line 822
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 823
        _.assertFalse(os.path.exists("fi4le"))  # line 824
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 826
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 830
        sos.add(".", "./?a?b", ["--force"])  # line 831
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 832
        _.createFile("1a2b")  # should not be tracked  # line 833
        _.createFile("a1b2")  # should be tracked  # line 834
        sos.commit()  # line 835
        _.assertEqual(2, len(os.listdir(sos.branchFolder(0, 1))))  # line 836
        _.assertTrue(os.path.exists(sos.branchFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 837
        _.createFile("1a1b1")  # line 838
        _.createFile("1a1b2")  # line 839
        sos.add(".", "?a?b*")  # line 840
        _.assertIn("not unique", wrapChannels(lambda: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 841
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testHashCollision(_):  # line 845
        sos.offline()  # line 846
        _.createFile(1)  # line 847
        os.mkdir(sos.branchFolder(0, 1))  # line 848
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.branchFolder(0, 1))  # line 849
        _.createFile(1)  # line 850
        try:  # should exit with error due to collision detection  # line 851
            sos.commit()  # should exit with error due to collision detection  # line 851
            _.fail()  # should exit with error due to collision detection  # line 851
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 852
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 852

    def testFindBase(_):  # line 854
        old = os.getcwd()  # line 855
        try:  # line 856
            os.mkdir("." + os.sep + ".git")  # line 857
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 858
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 859
            os.chdir("a" + os.sep + "b")  # line 860
            s, vcs, cmd = sos.findSosVcsBase()  # line 861
            _.assertIsNotNone(s)  # line 862
            _.assertIsNotNone(vcs)  # line 863
            _.assertEqual("git", cmd)  # line 864
        finally:  # line 865
            os.chdir(old)  # line 865

# TODO test command line operation --sos vs. --vcs
# check exact output instead of expected fail


if __name__ == '__main__':  # line 871
    logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv or os.getenv("DEBUG", "false").strip().lower() == "true" or os.getenv("CI", "false").strip().lower() == "true" else logging.INFO, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '-v' in sys.argv or os.getenv("DEBUG", "false") == "true" else "%(message)s")  # line 872
    if configr:  # line 873
        c = configr.Configr("sos")  # line 874
        c.loadSettings()  # line 874
        if len(c.keys()) > 0:  # line 875
            sos.Exit("Cannot run test suite with existing local SOS user configuration (would affect results)")  # line 875
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 876
