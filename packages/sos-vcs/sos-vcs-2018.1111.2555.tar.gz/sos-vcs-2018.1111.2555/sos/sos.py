#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xccb884e9

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

# Standard modules
import codecs  # line 6
import collections  # line 6
import fnmatch  # line 6
import json  # line 6
import logging  # line 6
import mimetypes  # line 6
import os  # line 6
import shutil  # line 6
sys = _coconut_sys  # line 6
import time  # line 6
try:  # line 7
    from typing import Any  # only required for mypy  # line 8
    from typing import Dict  # only required for mypy  # line 8
    from typing import FrozenSet  # only required for mypy  # line 8
    from typing import IO  # only required for mypy  # line 8
    from typing import Iterator  # only required for mypy  # line 8
    from typing import List  # only required for mypy  # line 8
    from typing import Set  # only required for mypy  # line 8
    from typing import Tuple  # only required for mypy  # line 8
    from typing import Type  # only required for mypy  # line 8
    from typing import Union  # only required for mypy  # line 8
except:  # typing not available (e.g. Python 2)  # line 9
    pass  # typing not available (e.g. Python 2)  # line 9
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # line 10
try:  # line 11
    from sos import version  # line 12
    from sos.utility import *  # line 13
except:  # line 14
    import version  # line 15
    from utility import *  # line 16

# External dependencies
try:  # optional dependency  # line 19
    import configr  # optional dependency  # line 19
except:  # declare as undefined  # line 20
    configr = None  # declare as undefined  # line 20
#from enforce import runtime_validation  # https://github.com/RussBaz/enforce  TODO doesn't work for "data" types


# Constants
APPNAME = "Subversion Offline Solution V%s (C) Arne Bachmann" % version.__release_version__  # type: str  # line 25
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_"], "ignoresWhitelist": []})  # line 26
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 27


# Functions
def loadConfig() -> 'Union[configr.Configr, Accessor]':  # Simplifies loading config from file system or returning the defaults  # line 31
    config = None  # type: Union[configr.Configr, Accessor]  # line 32
    if not configr:  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 33
        return defaults  # this only applies for the case that configr is not available, thus no settings will be persisted anyway  # line 33
    config = configr.Configr("sos", defaults=defaults)  # defaults are used if key is not configured, but won't be saved  # line 34
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 35
    if f is None:  # line 36
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 36
    return config  # line 37

@_coconut_tco  # line 39
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 39
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # line 40

def usage(short: 'bool'=False) -> 'None':  # line 42
    print("//|\\\\ {appname}{version} //|\\\\".format(appname=APPNAME, version="" if not short else " (PyPI: %s)" % version.__version__))  # line 43
    if not short:  # line 44
        print("""

Usage: {cmd} <command> [<argument>] [<option1>, ...]        When operating in offline mode, or command is one of "help", "offline", "version"
       {cmd} --sos <sos command and arguments>              When operating in offline mode, forced passthrough to SOS
       {cmd} --vcs <underlying vcs command and arguments>   When operating in offline mode, forced passthrough to traditional VCS
       {cmd} <underlying vcs command and arguments>         When operating in online mode, automatic passthrough to traditional VCS

  Available commands:
    offline [<name>]                                      Start working offline, creating a branch (named <name>), default name depending on VCS
      --compress                                            Compress versioned files (same as `sos config set compress on && sos offline`)
      --track                                               Setup SVN-style mode: users add/remove tracking patterns per branch
      --picky                                               Setup Git-style mode: users pick files for each operation
    online                                                Finish working offline

    branch [<name>]                                       Create a new branch from current file tree and switch to it
      --last                                                Use last revision, not current file tree, but keep file tree unchanged
      --stay                                                Don't switch to new branch, continue on current one
    destroy [<branch>]                                    Remove (current or specified) branch entirely
    switch [<branch>][/<revision>]                        Continue work on another branch
      --meta                                                Only switch file tracking patterns for current branch, don't update any files
    update [<branch>][/<revision>]                        Integrate work from another branch  TODO add many merge and conflict resolution options

    commit [<message>]                                    Create a new revision from current state file tree, with an optional commit message
      --tag                                               Memorizes commit message as a tag that can be used instead of numeric revisions
    changes [<branch>][/<revision>]                       List changed paths vs. last or specified revision
    diff [<branch>][/<revision>]                          List changes in file tree (or `--from` specified revision) vs. last (or specified) revision
      --to=branch/revision                                Take "to" revision as target to compare against (instead of current file tree state)
    add <file pattern>                                    Add a tracking pattern to current branch (file pattern)
    mv <oldpattern> <newPattern>                          Rename, move, or move and rename tracked files according to tracked file patterns
      --soft                                                Don't move or rename files, only the tracking pattern
    rm <file pattern>                                     Remove a tracking pattern. Only useful after "offline --track" or "offline --picky"

    ls [<folder path>] [--patterns|--tags]                List file tree and mark changes and tracking status
    status [-v]                                           List branches and display repository status
    log                                                   List commits of current branch
      --changes                                             Also list file differences
      --diff                                                Also show textual version differences
    config [set/unset/show/add/rm] [<param> [<value>]]    Configure user-global defaults.
                                                          Flags (1/0, on/off, true/false, yes/no):
                                                            strict, track, picky, compress
                                                          Lists (semicolon-separated when set; single values for add/rm):
                                                            texttype, bintype, ignores, ignoreDirs, ignoresWhitelist, ignoreDirsWhitelist
                                                          Supported texts:
                                                            defaultbranch (has a dynamic default value, depending on VCS discovered)
    config show|list flags|lists|texts                    Enumerates all configurable settings for specified type
    help, --help                                          Show this usage information
    version                                               Display version and package information

  Arguments:
    <branch>/<revision>          Revision string. Branch is optional (defaulting to current branch) and may be label or number
                                 Revision is an optional integer and may be negative to reference from the latest commits (-1 is most recent revision), or a tag

  Common options:
    --force                      Executes potentially harmful operations. SOS will tell you, when it needs you to confirm an operation with "--force"
                                   for offline: ignore being already offline, start from scratch (same as 'sos online --force && sos offline')
                                   for online: ignore uncommitted branches, just go online and remove existing offline repository
                                   for commit, switch, update, add: ignore uncommitted changes before executing command
    --strict                     Always perform full content comparison, don't rely only on file size and timestamp
                                   for offline command: memorize strict mode setting in repository
                                   for changes, diff, commit, switch, update, delete: perform operation in strict mode, regardless of repository setting
    --progress                   Display file names during file tree traversal
    --only   <tracked pattern>   Restrict operation to specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --except <tracked pattern>   Avoid operation for specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --{cmd}                      When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                        Enable logging details
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 109
    Exit(code=0)  # line 110

# Main data class
#@runtime_validation
class Metadata:  # line 114
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 118

    def __init__(_, path: 'str') -> 'None':  # line 120
        ''' Create empty container object for various repository operations. '''  # line 121
        _.c = loadConfig()  # line 122
        _.root = path  # type: str  # line 123
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 124
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 125
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 126
        _.tags = []  # type: List[str]  # line 127
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 128
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 129
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 130
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 131
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 132
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 133

    def isTextType(_, filename: 'str') -> 'bool':  # line 135
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 135

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 137
        if len(changes.additions) > 0:  # line 138
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 138
        if len(changes.deletions) > 0:  # line 139
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 139
        if len(changes.modifications) > 0:  # line 140
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 140

    def loadBranches(_) -> 'None':  # line 142
        ''' Load list of branches and current branch info from metadata file. '''  # line 143
        try:  # fails if not yet created (on initial branch/commit)  # line 144
            branches = None  # type: List[Tuple]  # line 145
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 146
                flags, branches = json.load(fd)  # line 147
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 148
            _.branch = flags["branch"]  # current branch integer  # line 149
            _.track = flags["track"]  # line 150
            _.picky = flags["picky"]  # line 151
            _.strict = flags["strict"]  # line 152
            _.compress = flags["compress"]  # line 153
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 154
        except Exception as E:  # if not found, create metadata folder  # line 155
            _.branches = {}  # line 156
            warn("Couldn't read branches metadata: %r" % E)  # line 157

    def saveBranches(_) -> 'None':  # line 159
        ''' Save list of branches and current branch info to metadata file. '''  # line 160
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 161
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 162

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 164
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 165
        if name == "":  # line 166
            return -1  # line 166
        try:  # attempt to parse integer string  # line 167
            return longint(name)  # attempt to parse integer string  # line 167
        except ValueError:  # line 168
            pass  # line 168
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # TODO only allow finding real tags?  # line 169
        return found[0] if found else None  # line 170

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 172
        ''' Convenience accessor for named branches. '''  # line 173
        if name == "":  # line 174
            return _.branch  # line 174
        try:  # attempt to parse integer string  # line 175
            return longint(name)  # attempt to parse integer string  # line 175
        except ValueError:  # line 176
            pass  # line 176
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 177
        return found[0] if found else None  # line 178

    def loadBranch(_, branch: 'int') -> 'None':  # line 180
        ''' Load all commit information from a branch meta data file. '''  # line 181
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 182
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 183
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 184
        _.branch = branch  # line 185

    def saveBranch(_, branch: 'int') -> 'None':  # line 187
        ''' Save all commit information to a branch meta data file. '''  # line 188
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 189
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 190

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 192
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 197
        debug("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), ("b%d" % branch if name is None else name)))  # line 198
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 199
        os.makedirs(branchFolder(branch, 0, base=_.root))  # line 200
        _.loadBranch(_.branch)  # line 201
        revision = max(_.commits)  # type: int  # line 202
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 203
        for path, pinfo in _.paths.items():  # line 204
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 205
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 206
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 207
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 208
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 209

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 211
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 216
        simpleMode = not (_.track or _.picky)  # line 217
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 218
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 219
        _.paths = {}  # type: Dict[str, PathInfo]  # line 220
        if simpleMode:  # branches from file system state  # line 221
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 222
            _.listChanges(changes)  # line 223
            _.paths.update(changes.additions.items())  # line 224
        else:  # tracking or picky mode: branch from lastest revision  # line 225
            os.makedirs(branchFolder(branch, 0, base=_.root))  # line 226
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 227
                _.loadBranch(_.branch)  # line 228
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 229
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 230
                for path, pinfo in _.paths.items():  # line 231
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 232
        ts = longint(time.time() * 1000)  # line 233
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 234
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 235
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 236
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 237

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 239
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 240
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 241
        binfo = _.branches[branch]  # line 242
        del _.branches[branch]  # line 243
        _.branch = max(_.branches)  # line 244
        _.saveBranches()  # line 245
        _.commits.clear()  # line 246
        return binfo  # line 247

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 249
        ''' Load all file information from a commit meta data. '''  # line 250
        with codecs.open(branchFolder(branch, revision, base=_.root, file=metaFile), "r", encoding=UTF8) as fd:  # line 251
            _.paths = json.load(fd)  # line 252
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 253
        _.branch = branch  # line 254

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 256
        ''' Save all file information to a commit meta data file. '''  # line 257
        target = branchFolder(branch, revision, base=_.root)  # line 258
        try:  # line 259
            os.makedirs(target)  # line 259
        except:  # line 260
            pass  # line 260
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 261
            json.dump(_.paths, fd, ensure_ascii=False)  # line 262

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 264
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 273
        write = branch is not None and revision is not None  # line 274
        if write:  # line 275
            try:  # line 276
                os.makedirs(branchFolder(branch, revision, base=_.root))  # line 276
            except FileExistsError:  # HINT "try" only necessary for testing hash collisions  # line 277
                pass  # HINT "try" only necessary for testing hash collisions  # line 277
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 278
        counter = Counter(-1)  # type: Counter  # line 279
        timer = time.time()  # line 279
        hashed = None  # type: _coconut.typing.Optional[str]  # line 280
        written = None  # type: longint  # line 280
        compressed = 0  # type: longint  # line 280
        original = 0  # type: longint  # line 280
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 281
        for path, pinfo in _.paths.items():  # line 282
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 283
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 286
        for path, dirnames, filenames in os.walk(_.root):  # line 287
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 288
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 289
            dirnames.sort()  # line 290
            filenames.sort()  # line 290
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 291
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 292
            if dontConsider:  # line 293
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 294
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 295
                filename = relPath + SLASH + file  # line 296
                filepath = os.path.join(path, file)  # line 297
                stat = os.stat(filepath)  # line 298
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 299
                if progress and newtime - timer > .1:  # line 300
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 301
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return (still true?)  # line 302
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return (still true?)  # line 302
                    timer = newtime  # TODO could write to new line instead of carriage return (still true?)  # line 302
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 303
                    nameHash = hashStr(filename)  # line 304
                    hashed, written = hashFile(filepath, _.compress, saveTo=branchFolder(branch, revision, base=_.root, file=nameHash) if write else None) if size > 0 else (None, 0)  # line 305
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 306
                    compressed += written  # line 307
                    original += size  # line 307
                    continue  # line 308
                last = _.paths[filename]  # filename is known - check for modifications  # line 309
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 310
                    hashed, written = hashFile(filepath, _.compress, saveTo=branchFolder(branch, revision, base=_.root, file=last.nameHash) if write else None) if size > 0 else (None, 0)  # line 311
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 312
                    continue  # line 312
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 313
                    hashed, written = hashFile(filepath, _.compress, saveTo=branchFolder(branch, revision, base=_.root, file=last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 314
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 315
                else:  # line 316
                    continue  # line 316
                compressed += written  # line 317
                original += last.size if inverse else size  # line 317
            if relPath in knownPaths:  # at least one file is tracked  # line 318
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 318
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 319
            for file in names:  # line 320
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 320
        if progress:  # force new line  # line 321
            print("\rPreparation finished.%s" % (" Compression advantage %s" % ("is %.1f%%" % (original * 100. / compressed - 100.) if compressed > 0 else "cannot be computed") if _.compress else "").ljust(termWidth), file=sys.stdout)  # force new line  # line 321
        else:  # line 322
            debug("Finished detecting changes.%s" % (" Compression advantage %s" % ("is %.1f%%" % (original * 100. / compressed - 100.) if compressed > 0 else "cannot be computed") if _.compress else ""))  # line 322
        return changes  # line 323

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 325
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 326
        if clear:  # line 327
            _.paths.clear()  # line 327
        else:  # line 328
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 329
            for old in rm:  # remove previously removed entries completely  # line 330
                del _.paths[old]  # remove previously removed entries completely  # line 330
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 331
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 331
        _.paths.update(changes.additions)  # line 332
        _.paths.update(changes.modifications)  # line 333

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 335
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 336

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 338
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 339
        _.loadCommit(branch, 0)  # load initial paths  # line 340
        if incrementally:  # line 341
            yield diffPathSets({}, _.paths)  # line 341
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 342
        for revision in range(1, revision + 1):  # line 343
            n.loadCommit(branch, revision)  # line 344
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 345
            _.integrateChangeset(changes)  # line 346
            if incrementally:  # line 347
                yield changes  # line 347
        yield None  # for the default case - not incrementally  # line 348

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 350
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 353
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 354
            return (_.branch, -1)  # no branch/revision specified  # line 354
        argument = argument.strip()  # line 355
        if argument.startswith(SLASH):  # current branch  # line 356
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 356
        if argument.endswith(SLASH):  # line 357
            try:  # line 358
                return (_.getBranchByName(argument[:-1]), -1)  # line 358
            except ValueError:  # line 359
                Exit("Unknown branch label '%s'" % argument)  # line 359
        if SLASH in argument:  # line 360
            b, r = argument.split(SLASH)[:2]  # line 361
            try:  # line 362
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 362
            except ValueError:  # line 363
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 363
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 364
        if branch not in _.branches:  # line 365
            branch = None  # line 365
        try:  # either branch name/number or reverse/absolute revision number  # line 366
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 366
        except:  # line 367
            Exit("Unknown branch label or wrong number format")  # line 367
        Exit("This should never happen. Please create a issue report")  # line 368
        return (None, None)  # line 368

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 370
        while True:  # find latest revision that contained the file physically  # line 371
            source = branchFolder(branch, revision, base=_.root, file=nameHash)  # type: str  # line 372
            if os.path.exists(source) and os.path.isfile(source):  # line 373
                break  # line 373
            revision -= 1  # line 374
            if revision < 0:  # line 375
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 375
        return revision, source  # line 376

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 378
        ''' Copy versioned file to other branch/revision. '''  # line 379
        target = branchFolder(toBranch, toRevision, base=_.root, file=pinfo.nameHash)  # type: str  # line 380
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 381
        shutil.copy2(source, target)  # line 382

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 384
        ''' Return file contents, or copy contents into file path provided. '''  # line 385
        source = branchFolder(branch, revision, base=_.root, file=nameHash)  # type: str  # line 386
        try:  # line 387
            with openIt(source, "r", _.compress) as fd:  # line 388
                if toFile is None:  # read bytes into memory and return  # line 389
                    return fd.read()  # read bytes into memory and return  # line 389
                with open(toFile, "wb") as to:  # line 390
                    while True:  # line 391
                        buffer = fd.read(bufSize)  # line 392
                        to.write(buffer)  # line 393
                        if len(buffer) < bufSize:  # line 394
                            break  # line 394
                    return None  # line 395
        except Exception as E:  # line 396
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 396
        return None  # line 397

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 399
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 400
        if relPath is None:  # just return contents  # line 401
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 401
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 402
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 403
            try:  # line 404
                os.makedirs(os.path.dirname(target))  # line 404
            except:  # line 405
                pass  # line 405
        if pinfo.size == 0:  # line 406
            with open(target, "wb"):  # line 407
                pass  # line 407
            try:  # update access/modification timestamps on file system  # line 408
                os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 408
            except Exception as E:  # line 409
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 409
            return None  # line 410
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 411
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 413
            while True:  # line 414
                buffer = fd.read(bufSize)  # line 415
                to.write(buffer)  # line 416
                if len(buffer) < bufSize:  # line 417
                    break  # line 417
        try:  # update access/modification timestamps on file system  # line 418
            os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 418
        except Exception as E:  # line 419
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 419
        return None  # line 420

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 422
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 423
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 424


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 428
    ''' Initial command to start working offline. '''  # line 429
    if os.path.exists(metaFolder):  # line 430
        if '--force' not in options:  # line 431
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 431
        try:  # line 432
            for entry in os.listdir(metaFolder):  # line 433
                resource = metaFolder + os.sep + entry  # line 434
                if os.path.isdir(resource):  # line 435
                    shutil.rmtree(resource)  # line 435
                else:  # line 436
                    os.unlink(resource)  # line 436
        except:  # line 437
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 437
    m = Metadata(os.getcwd())  # type: Metadata  # line 438
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 439
        m.compress = True  # plain file copies instead of compressed ones  # line 439
    if '--picky' in options or m.c.picky:  # Git-like  # line 440
        m.picky = True  # Git-like  # line 440
    elif '--track' in options or m.c.track:  # Svn-like  # line 441
        m.track = True  # Svn-like  # line 441
    if '--strict' in options or m.c.strict:  # always hash contents  # line 442
        m.strict = True  # always hash contents  # line 442
    debug("Preparing offline repository...")  # line 443
    m.createBranch(0, defaults["defaultbranch"] if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 444
    m.branch = 0  # line 445
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 446
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 447

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 449
    ''' Finish working offline. '''  # line 450
    force = '--force' in options  # type: bool  # line 451
    m = Metadata(os.getcwd())  # line 452
    m.loadBranches()  # line 453
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 454
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 454
    strict = '--strict' in options or m.strict  # type: bool  # line 455
    if options.count("--force") < 2:  # line 456
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns(), progress='--progress' in options)  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 457
        if modified(changes):  # line 458
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 458
    try:  # line 459
        shutil.rmtree(metaFolder)  # line 459
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 459
    except Exception as E:  # line 460
        Exit("Error removing offline repository: %r" % E)  # line 460

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 462
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 463
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 464
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 465
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 466
    m = Metadata(os.getcwd())  # type: Metadata  # line 467
    m.loadBranches()  # line 468
    m.loadBranch(m.branch)  # line 469
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 470
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 470
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 471
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 472
    if last:  # line 473
        m.duplicateBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from branch's last revision  # line 474
    else:  # from file tree state  # line 475
        m.createBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from current file tree  # line 476
    if not stay:  # line 477
        m.branch = branch  # line 478
        m.saveBranches()  # line 479
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 480

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 482
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 483
    m = Metadata(os.getcwd())  # type: Metadata  # line 484
    branch = None  # type: _coconut.typing.Optional[int]  # line 484
    revision = None  # type: _coconut.typing.Optional[int]  # line 484
    m.loadBranches()  # knows current branch  # line 485
    strict = '--strict' in options or m.strict  # type: bool  # line 486
    branch, revision = m.parseRevisionString(argument)  # line 487
    if branch not in m.branches:  # line 488
        Exit("Unknown branch")  # line 488
    m.loadBranch(branch)  # knows commits  # line 489
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 490
    if revision < 0 or revision > max(m.commits):  # line 491
        Exit("Unknown revision r%02d" % revision)  # line 491
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 492
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 493
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps, progress='--progress' in options)  # type: ChangeSet  # line 494
    m.listChanges(changes)  # line 495
    return changes  # for unit tests only  # line 496

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 498
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 499
    m = Metadata(os.getcwd())  # type: Metadata  # line 500
    branch = None  # type: _coconut.typing.Optional[int]  # line 500
    revision = None  # type: _coconut.typing.Optional[int]  # line 500
    m.loadBranches()  # knows current branch  # line 501
    strict = '--strict' in options or m.strict  # type: bool  # line 502
    _from = {None: option.split("--from=")[1] for option in options if options.startswith("--from=")}.get(None, None)  # type: _coconut.typing.Optional[str]  # line 503
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 504
    if branch not in m.branches:  # line 505
        Exit("Unknown branch")  # line 505
    m.loadBranch(branch)  # knows commits  # line 506
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 507
    if revision < 0 or revision > max(m.commits):  # line 508
        Exit("Unknown revision r%02d" % revision)  # line 508
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 509
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 510
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps, progress='--progress' in options)  # type: ChangeSet  # line 511
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 512
    if modified(onlyBinaryModifications):  # line 513
        debug("//|\\\\ File changes")  # line 513
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 514

    if changes.modifications:  # line 516
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # line 516
    for path, pinfo in (c for c in changes.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 517
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 518
        if pinfo.size == 0:  # empty file contents  # line 519
            content = b""  # empty file contents  # line 519
        else:  # versioned file  # line 520
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 520
            assert content is not None  # versioned file  # line 520
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 521
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 522
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 523
        for block in blocks:  # line 524
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 525
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 526
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 527
                for no, line in enumerate(block.lines):  # line 528
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 529
            elif block.tipe == MergeBlockType.REMOVE:  # line 530
                for no, line in enumerate(block.lines):  # line 531
                    print("--- %04d |%s|" % (no + block.line, line))  # line 532
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 533
                for no, line in enumerate(block.replaces.lines):  # line 534
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 535
                for no, line in enumerate(block.lines):  # line 536
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 537
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 542
    ''' Create new revision from file tree changes vs. last commit. '''  # line 543
    m = Metadata(os.getcwd())  # type: Metadata  # line 544
    m.loadBranches()  # knows current branch  # line 545
    if argument is not None and argument in m.tags:  # line 546
        Exit("Illegal commit message. It was already used as a tag name")  # line 546
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 547
    if m.picky and not trackingPatterns:  # line 548
        Exit("No file patterns staged for commit in picky mode")  # line 548
    changes = None  # type: ChangeSet  # line 549
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 550
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 551
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 552
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 553
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 554
    m.saveBranch(m.branch)  # line 555
    m.loadBranches()  # TODO is it necessary to load again?  # line 556
    if m.picky:  # line 557
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 558
    else:  # track or simple mode  # line 559
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 560
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 561
        m.tags.append(argument)  # memorize unique tag  # line 561
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 561
    m.saveBranches()  # line 562
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 563

def status(options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 565
    ''' Show branches and current repository state. '''  # line 566
    m = Metadata(os.getcwd())  # type: Metadata  # line 567
    m.loadBranches()  # knows current branch  # line 568
    current = m.branch  # type: int  # line 569
    strict = '--strict' in options or m.strict  # type: bool  # line 570
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 571
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps, progress='--progress' in options)  # type: ChangeSet  # line 572
    info("//|\\\\ Offline repository status")  # line 573
    debug("Content checking %sactivated" % ("" if m.strict else "de"))  # line 574
    debug("Data compression %sactivated" % ("" if m.compress else "de"))  # line 575
    debug("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 576
    print("File tree %s" % ("has changes vs. last revision of current branch" if modified(changes) else "is unchanged"))  # line 577
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 578
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 579
        m.loadBranch(branch.number)  # knows commit history  # line 580
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 581
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 582
        info("\nTracked file patterns:")  # line 583
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 584

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 586
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 591
    m = Metadata(os.getcwd())  # type: Metadata  # line 592
    m.loadBranches()  # knows current branch  # line 593
    force = '--force' in options  # type: bool  # line 594
    strict = '--strict' in options or m.strict  # type: bool  # line 595
    if argument is not None:  # line 596
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 597
        if branch is None:  # line 598
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 598
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 599

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 602
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 603
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps, progress='--progress' in options)  # type: ChangeSet  # line 604
    if check and modified(changes) and not force:  # line 605
        m.listChanges(changes)  # line 606
        if not commit:  # line 607
            Exit("File tree contains changes. Use --force to proceed")  # line 607
    elif commit and not force:  #  and not check  # line 608
        Exit("Nothing to commit")  #  and not check  # line 608

    if argument is not None:  # branch/revision specified  # line 610
        m.loadBranch(branch)  # knows commits of target branch  # line 611
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 612
        if revision < 0 or revision > max(m.commits):  # line 613
            Exit("Unknown revision r%02d" % revision)  # line 613
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 614
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 615

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 617
    ''' Continue work on another branch, replacing file tree changes. '''  # line 618
    changes = None  # type: ChangeSet  # line 619
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 620
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 621

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 624
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 625
    else:  # full file switch  # line 626
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 627
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps, progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 628
        if not modified(changes):  # line 629
            info("No changes to current file tree")  # line 630
        else:  # integration required  # line 631
            for path, pinfo in changes.deletions.items():  # line 632
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 633
                print("ADD " + path)  # line 634
            for path, pinfo in changes.additions.items():  # line 635
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 636
                print("DEL " + path)  # line 637
            for path, pinfo in changes.modifications.items():  # line 638
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 639
                print("MOD " + path)  # line 640
    m.branch = branch  # line 641
    m.saveBranches()  # store switched path info  # line 642
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 643

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 645
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 650
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 651
    res = getAnyOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE, '--ask': ConflictResolution.ASK}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 652
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 653
    resline = getAnyOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE, '--ask-lines': ConflictResolution.ASK}, options, ConflictResolution.ASK)  # type: int  # line 654
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 655
    m.loadBranches()  # line 656
    changes = None  # type: ChangeSet  # line 656
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 657
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 658
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 659

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 662
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 663
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps, progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 664
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 665
        if trackingUnion != trackingPatterns:  # nothing added  # line 666
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 667
        else:  # line 668
            info("Nothing to update")  # but write back updated branch info below  # line 669
    else:  # integration required  # line 670
        for path, pinfo in changes.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 671
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 672
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 672
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 673
        for path, pinfo in changes.additions.items():  # line 674
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 675
                Exit("This should never happen. Please create an issue report")  # because untracked files of other branch cannot be detected (which is good)  # line 675
            if mrg & MergeOperation.REMOVE:  # line 676
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 676
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 677
        for path, pinfo in changes.modifications.items():  # line 678
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # TODO normalize \.\  # line 679
            binary = not m.isTextType(path)  # line 680
            if res == ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 681
                print(("MOD " + path if not binary else "BIN ") + path)  # line 682
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: ").strip().lower(), ConflictResolution.MINE)  # TODO add unicode variants?  # line 683
                debug("User selected %d" % reso)  # TODO this is a place to have a real enum  # line 684
            else:  # TODO this sets to next even already was next per file?  # line 685
                reso = res  # TODO this sets to next even already was next per file?  # line 685
            if reso == ConflictResolution.THEIRS:  # line 686
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 687
                print("THR " + path)  # line 688
            elif reso == ConflictResolution.MINE:  # line 689
                print("MNE " + path)  # nothing to do! same as skip  # line 690
            else:  # file-resolution is NEXT: continue with line-based merge. will ask in case of intra-line conflict  # line 691
                current = None  # type: bytes  # line 692
                with open(into, "rb") as fd:  # line 693
                    current = fd.read()  # line 693
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 694
                if current == file:  # line 695
                    debug("No difference to versioned file")  # line 695
                elif file is not None:  # if None, error message was already logged  # line 696
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 697
                    if contents != current:  # line 698
                        with open(path, "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 699
                            fd.write(contents)  # TODO write to temp file first, in case writing fails  # line 699
                    else:  # line 700
                        debug("No change")  # line 700
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 701
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 702
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 703
    m.saveBranches()  # line 704

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 706
    ''' Remove a branch entirely. '''  # line 707
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 708
    if len(m.branches) == 1:  # line 709
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 709
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 710
    if branch is None or branch not in m.branches:  # line 711
        Exit("Cannot delete unknown branch %r" % branch)  # line 711
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 712
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 713
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 714

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 716
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 717
    force = '--force' in options  # type: bool  # line 718
    m = Metadata(os.getcwd())  # type: Metadata  # line 719
    m.loadBranches()  # line 720
    if not m.track and not m.picky:  # line 721
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 721
    if pattern in m.branches[m.branch].tracked:  # line 722
        Exit("Pattern '%s' already tracked" % pattern)  # line 722
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 723
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 723
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 724
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 725
    m.branches[m.branch].tracked.append(pattern)  # line 726
    m.saveBranches()  # line 727
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 728

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 730
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 731
    m = Metadata(os.getcwd())  # type: Metadata  # line 732
    m.loadBranches()  # line 733
    if not m.track and not m.picky:  # line 734
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 734
    if pattern not in m.branches[m.branch].tracked:  # line 735
        suggestion = _coconut.set()  # type: Set[str]  # line 736
        for pat in m.branches[m.branch].tracked:  # line 737
            if fnmatch.fnmatch(pattern, pat):  # line 738
                suggestion.add(pat)  # line 738
        if suggestion:  # TODO use same wording as in move  # line 739
            print("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 739
        Exit("Tracked pattern '%s' not found" % pattern)  # line 740
    m.branches[m.branch].tracked.remove(pattern)  # line 741
    m.saveBranches()  # line 742
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 743

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 745
    ''' List specified directory, augmenting with repository metadata. '''  # line 746
    folder = "." if argument is None else argument  # type: str  # line 747
    m = Metadata(os.getcwd())  # type: Metadata  # line 748
    m.loadBranches()  # line 749
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 750
    relPath = os.path.relpath(folder, m.root).replace(os.sep, SLASH)  # type: str  # line 751
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 752
    if '--tags' in options:  # line 753
        print(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 754
        return  # line 755
    if '--patterns' in options:  # line 756
        out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 757
        if out:  # line 758
            print(out)  # line 758
        return  # line 759
    files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 760
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 761
        ignore = None  # type: _coconut.typing.Optional[str]  # line 762
        for ig in m.c.ignores:  # line 763
            if fnmatch.fnmatch(file, ig):  # remember first match  # line 764
                ignore = ig  # remember first match  # line 764
                break  # remember first match  # line 764
        if ig:  # line 765
            for wl in m.c.ignoresWhitelist:  # line 766
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 767
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 767
                    break  # found a white list entry for ignored file, undo ignoring it  # line 767
        if not ignore:  # line 768
            matches = []  # type: List[str]  # line 769
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 770
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 771
                    matches.append(os.path.basename(pattern))  # line 771
        matches.sort(key=lambda element: len(element))  # line 772
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 773

def log(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 775
    ''' List previous commits on current branch. '''  # line 776
    m = Metadata(os.getcwd())  # type: Metadata  # line 777
    m.loadBranches()  # knows current branch  # line 778
    m.loadBranch(m.branch)  # knows commit history  # line 779
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 780
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 781
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 782
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 783
    for no in range(max(m.commits) + 1):  # line 784
        commit = m.commits[no]  # type: CommitInfo  # line 785
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 786
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 787
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%5.1f%%) |%s|%s" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth), "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else ""))  # line 788
        if '--changes' in options:  # line 789
            m.listChanges(changes)  # line 789
        if '--diff' in options:  # needs to extract code from diff first to be reused here  # line 790
            pass  # needs to extract code from diff first to be reused here  # line 790

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 792
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 793
        Exit("Unknown config command")  # line 793
    if not configr:  # line 794
        Exit("Cannot execute config command. 'configr' module not installed")  # line 794
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 795
    if argument == "set":  # line 796
        if len(options) < 2:  # line 797
            Exit("No key nor value specified")  # line 797
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 798
            Exit("Unsupported key %r" % options[0])  # line 798
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 799
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 799
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 800
    elif argument == "unset":  # line 801
        if len(options) < 1:  # line 802
            Exit("No key specified")  # line 802
        if options[0] not in c.keys():  # line 803
            Exit("Unknown key")  # line 803
        del c[options[0]]  # line 804
    elif argument == "add":  # line 805
        if len(options) < 2:  # line 806
            Exit("No key nor value specified")  # line 806
        if options[0] not in CONFIGURABLE_LISTS:  # line 807
            Exit("Unsupported key for add %r" % options[0])  # line 807
        if options[0] not in c.keys():  # add list  # line 808
            c[options[0]] = [options[1]]  # add list  # line 808
        elif options[1] in c[options[0]]:  # line 809
            Exit("Value already contained")  # line 809
        c[options[0]].append(options[1])  # line 810
    elif argument == "rm":  # line 811
        if len(options) < 2:  # line 812
            Exit("No key nor value specified")  # line 812
        if options[0] not in c.keys():  # line 813
            Exit("Unknown key specified: %r" % options[0])  # line 813
        if options[1] not in c[options[0]]:  # line 814
            Exit("Unknown value: %r" % options[1])  # line 814
        c[options[0]].remove(options[1])  # line 815
    else:  # Show or list  # line 816
        if "flags" in options:  # line 817
            print(", ".join(CONFIGURABLE_FLAGS))  # line 817
        elif "lists" in options:  # line 818
            print(", ".join(CONFIGURABLE_LISTS))  # line 818
        elif "texts" in options:  # line 819
            print(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 819
        else:  # normal value listing  # line 820
            for k, v in sorted(c.items()):  # line 821
                print("%s: %r" % (k.rjust(20), v))  # line 821
            if len(c.keys()) == 0:  # TODO list defaults instead? Or display [DEFAULT] for each item above if unmodified  # line 822
                info("No configuration stored, using only defaults.")  # TODO list defaults instead? Or display [DEFAULT] for each item above if unmodified  # line 822
        return  # line 823
    f, g = saveConfig(c)  # line 824
    if f is None:  # line 825
        error("Error saving user configuration: %r" % g)  # line 825
    else:  # line 826
        Exit("OK", code=0)  # line 826

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 828
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 829
    force = '--force' in options  # type: bool  # line 830
    soft = '--soft' in options  # type: bool  # line 831
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 832
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 832
    m = Metadata(os.getcwd())  # type: Metadata  # line 833
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 834
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 835
    if not matching and not force:  # line 836
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 836
    m.loadBranches()  # knows current branch  # line 837
    if not m.track and not m.picky:  # line 838
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 838
    if pattern not in m.branches[m.branch].tracked:  # line 839
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 840
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 841
            if alternative:  # line 842
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 842
        if not (force or soft):  # line 843
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 843
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 844
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 845
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 846
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 850
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 851
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 851
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 852
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 853
    if len({st[1] for st in matches}) != len(matches):  # line 854
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 854
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 855
    if os.path.exists(newRelPath):  # line 856
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 857
        if exists and not (force or soft):  # line 858
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 858
    else:  # line 859
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 859
    if not soft:  # perform actual renaming  # line 860
        for (source, target) in matches:  # line 861
            try:  # line 862
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 862
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 863
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 863
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 864
    m.saveBranches()  # line 865

def parse(root: 'str', cwd: 'str'):  # line 867
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 868
    debug("Parsing command-line arguments...")  # line 869
    try:  # line 870
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 871
        argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 872
        options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 873
        onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 874
        debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 875
        if command[:1] in "amr":  # line 876
            relPath, pattern = relativize(root, os.path.join(cwd, "." if argument is None else argument))  # line 876
        if command[:1] == "m":  # line 877
            if not options:  # line 878
                Exit("Need a second file pattern argument as target for move/rename command")  # line 878
            newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # line 879
        if command[:1] == "a":  # line 880
            add(relPath, pattern, options)  # line 880
        elif command[:1] == "b":  # line 881
            branch(argument, options)  # line 881
        elif command[:2] == "ch":  # line 882
            changes(argument, options, onlys, excps)  # line 882
        elif command[:3] == "com":  # line 883
            commit(argument, options, onlys, excps)  # line 883
        elif command[:2] == "ci":  # line 884
            commit(argument, options, onlys, excps)  # line 884
        elif command[:3] == 'con':  # line 885
            config(argument, options)  # line 885
        elif command[:2] == "de":  # line 886
            delete(argument, options)  # line 886
        elif command[:2] == "di":  # line 887
            diff(argument, options, onlys, excps)  # line 887
        elif command[:1] == "h":  # line 888
            usage()  # line 888
        elif command[:2] == "lo":  # line 889
            log(options)  # line 889
        elif command[:2] == "li":  # TODO handle absolute paths as well, also for Windows? think through  # line 890
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO handle absolute paths as well, also for Windows? think through  # line 890
        elif command[:2] == "ls":  # TODO avoid and/or normalize root super paths (..)  # line 891
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO avoid and/or normalize root super paths (..)  # line 891
        elif command[:1] == "m":  # line 892
            move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 892
        elif command[:2] == "of":  # line 893
            offline(argument, options)  # line 893
        elif command[:2] == "on":  # line 894
            online(options)  # line 894
        elif command[:1] == "r":  # line 895
            remove(relPath, pattern)  # line 895
        elif command[:2] == "st":  # line 896
            status(options, onlys, excps)  # line 896
        elif command[:2] == "sw":  # line 897
            switch(argument, options, onlys, excps)  # line 897
        elif command[:1] == "u":  # line 898
            update(argument, options, onlys, excps)  # line 898
        elif command[:1] == "v":  # line 899
            usage(short=True)  # line 899
        else:  # line 900
            Exit("Unknown command '%s'" % command)  # line 900
        Exit(code=0)  # line 901
    except (Exception, RuntimeError) as E:  # line 902
        print(str(E))  # line 903
        import traceback  # line 904
        traceback.print_exc()  # line 905
        traceback.print_stack()  # line 906
        try:  # line 907
            traceback.print_last()  # line 907
        except:  # line 908
            pass  # line 908
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 909

def main() -> 'None':  # line 911
    global debug, info, warn, error  # line 912
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 913
    _log = Logger(logging.getLogger(__name__))  # line 914
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 914
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 915
        sys.argv.remove(option)  # clean up program arguments  # line 915
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 916
        usage()  # line 916
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 917
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 918
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 919
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, "trunk"))  # sets dynamic default with SVN fallback  # line 920
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] in ["h", "v"]:  # in offline mode or just going offline TODO what about git config?  # line 921
        cwd = os.getcwd()  # line 922
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 923
        parse(root, cwd)  # line 924
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 925
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 926
        import subprocess  # only required in this section  # line 927
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 928
        inp = ""  # type: str  # line 929
        while True:  # line 930
            so, se = process.communicate(input=inp)  # line 931
            if process.returncode is not None:  # line 932
                break  # line 932
            inp = sys.stdin.read()  # line 933
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 934
            if root is None:  # line 935
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 935
            m = Metadata(root)  # line 936
            m.loadBranches()  # read repo  # line 937
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 938
            m.saveBranches()  # line 939
    else:  # line 940
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 940


# Main part
verbose = os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv  # imported from utility, and only modified here  # line 944
level = logging.DEBUG if verbose else logging.INFO  # line 945
force_sos = '--sos' in sys.argv  # type: bool  # line 946
force_vcs = '--vcs' in sys.argv  # type: bool  # line 947
_log = Logger(logging.getLogger(__name__))  # type: logging.Logger  # line 948
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 948
if __name__ == '__main__':  # line 949
    main()  # line 949
