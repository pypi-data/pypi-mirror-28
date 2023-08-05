#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1c6705fe

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
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "tags": [], "texttype": [], "bintype": [], "ignoreDirs": [".*", "__pycache__"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout"], "ignoresWhitelist": []})  # line 26
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

    ls [<folder path>] [--patterns]                       List file tree and mark changes and tracking status
    status                                                List branches and display repository status
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
    --only   <tracked pattern>   Restrict operation to specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --except <tracked pattern>   Avoid operation for specified pattern(s). Available for "changes", "commit", "diff", "switch", and "update"
    --{cmd}                      When executing {CMD} not being offline, pass arguments to {CMD} instead (e.g. {cmd} --{cmd} config set key value.)
    --log                        Enable logging details
    --verbose                    Enable verbose output""".format(appname=APPNAME, cmd="sos", CMD="SOS"))  # line 107
    Exit(code=0)  # line 108

# Main data class
#@runtime_validation
class Metadata:  # line 112
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 116

    def __init__(_, path: 'str') -> 'None':  # line 118
        ''' Create empty container object for various repository operations. '''  # line 119
        _.c = loadConfig()  # line 120
        _.root = path  # type: str  # line 121
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 122
        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 123
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 124
        _.tags = []  # type: List[str]  # line 125
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 126
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 127
        _.track = _.c.track  # type: bool  # track file name patterns in the repository (per branch)  # line 128
        _.picky = _.c.picky  # type: bool  # pick files to commit per operation  # line 129
        _.strict = _.c.strict  # type: bool  # be always strict (regarding file contents comparsion)  # line 130
        _.compress = _.c.compress  # type: bool  # these flags are stored in the repository  # line 131

    def isTextType(_, filename: 'str') -> 'bool':  # line 133
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 133

    def listChanges(_, changes: 'ChangeSet') -> 'None':  # line 135
        if len(changes.additions) > 0:  # line 136
            print(ajoin("ADD ", sorted(changes.additions.keys()), "\n"))  # line 136
        if len(changes.deletions) > 0:  # line 137
            print(ajoin("DEL ", sorted(changes.deletions.keys()), "\n"))  # line 137
        if len(changes.modifications) > 0:  # line 138
            print(ajoin("MOD ", sorted(changes.modifications.keys()), "\n"))  # line 138

    def loadBranches(_) -> 'None':  # line 140
        ''' Load list of branches and current branch info from metadata file. '''  # line 141
        try:  # fails if not yet created (on initial branch/commit)  # line 142
            branches = None  # type: List[Tuple]  # line 143
            with codecs.open(os.path.join(_.root, metaFolder, metaFile), "r", encoding=UTF8) as fd:  # line 144
                flags, branches = json.load(fd)  # line 145
            _.tags = flags["tags"]  # list of commit messages to treat as globally unique tags  # line 146
            _.branch = flags["branch"]  # current branch integer  # line 147
            _.track = flags["track"]  # line 148
            _.picky = flags["picky"]  # line 149
            _.strict = flags["strict"]  # line 150
            _.compress = flags["compress"]  # line 151
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 152
        except Exception as E:  # if not found, create metadata folder  # line 153
            _.branches = {}  # line 154
            warn("Couldn't read branches metadata: %r" % E)  # line 155

    def saveBranches(_) -> 'None':  # line 157
        ''' Save list of branches and current branch info to metadata file. '''  # line 158
        with codecs.open(os.path.join(_.root, metaFolder, metaFile), "w", encoding=UTF8) as fd:  # line 159
            json.dump(({"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress}, list(_.branches.values())), fd, ensure_ascii=False)  # line 160

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 162
        ''' Convenience accessor for named revisions (using commit message as name). '''  # line 163
        if name == "":  # line 164
            return -1  # line 164
        try:  # attempt to parse integer string  # line 165
            return longint(name)  # attempt to parse integer string  # line 165
        except ValueError:  # line 166
            pass  # line 166
        found = [number for number, commit in _.commits.items() if name == commit.message]  # line 167
        return found[0] if found else None  # line 168

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 170
        ''' Convenience accessor for named branches. '''  # line 171
        if name == "":  # line 172
            return _.branch  # line 172
        try:  # attempt to parse integer string  # line 173
            return longint(name)  # attempt to parse integer string  # line 173
        except ValueError:  # line 174
            pass  # line 174
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 175
        return found[0] if found else None  # line 176

    def loadBranch(_, branch: 'int') -> 'None':  # line 178
        ''' Load all commit information from a branch meta data file. '''  # line 179
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "r", encoding=UTF8) as fd:  # line 180
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 181
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 182
        _.branch = branch  # line 183

    def saveBranch(_, branch: 'int') -> 'None':  # line 185
        ''' Save all commit information to a branch meta data file. '''  # line 186
        with codecs.open(os.path.join(_.root, metaFolder, "b%d" % branch, metaFile), "w", encoding=UTF8) as fd:  # line 187
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 188

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]') -> 'None':  # line 190
        ''' Create branch from an existing branch/revision. WARN: Caller must have loaded branches information.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch
    '''  # line 195
        debug("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), ("b%d" % branch if name is None else name)))  # line 196
        tracked = [t for t in _.branches[_.branch].tracked]  # copy  # line 197
        os.makedirs(branchFolder(branch, 0, base=_.root))  # line 198
        _.loadBranch(_.branch)  # line 199
        revision = max(_.commits)  # type: int  # line 200
        _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 201
        for path, pinfo in _.paths.items():  # line 202
            _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 203
        _.commits = {0: CommitInfo(0, longint(time.time() * 1000), "Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)))}  # store initial commit  # line 204
        _.saveBranch(branch)  # save branch meta data to branch folder  # line 205
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 206
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, _.branches[_.branch].inSync, tracked)  # save branch info, before storing repo state at caller  # line 207

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 209
        ''' Create a new branch from current file tree. This clears all known commits and modifies the file system.
        branch: target branch (should not exist yet)
        name: optional name of new branch
        _.branch: current branch, must exist already
    '''  # line 214
        simpleMode = not (_.track or _.picky)  # line 215
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # in case of initial branch creation  # line 216
        debug((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 217
        _.paths = {}  # type: Dict[str, PathInfo]  # line 218
        if simpleMode:  # branches from file system state  # line 219
            changes = _.findChanges(branch, 0, progress=simpleMode)  # type: ChangeSet  # creates revision folder and versioned files  # line 220
            _.listChanges(changes)  # line 221
            _.paths.update(changes.additions.items())  # line 222
        else:  # tracking or picky mode: branch from lastest revision  # line 223
            os.makedirs(branchFolder(branch, 0, base=_.root))  # line 224
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 225
                _.loadBranch(_.branch)  # line 226
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 227
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 228
                for path, pinfo in _.paths.items():  # line 229
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 230
        ts = longint(time.time() * 1000)  # line 231
        _.commits = {0: CommitInfo(0, ts, "Branched on %s" % strftime(ts) if initialMessage is None else initialMessage)}  # store initial commit for new branch  # line 232
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 233
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 234
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked)  # save branch info, in case it is needed  # line 235

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 237
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 238
        shutil.rmtree(os.path.join(_.root, metaFolder, "b%d" % branch))  # line 239
        binfo = _.branches[branch]  # line 240
        del _.branches[branch]  # line 241
        _.branch = max(_.branches)  # line 242
        _.saveBranches()  # line 243
        _.commits.clear()  # line 244
        return binfo  # line 245

    def loadCommit(_, branch: 'int', revision: 'int') -> 'None':  # line 247
        ''' Load all file information from a commit meta data. '''  # line 248
        with codecs.open(branchFolder(branch, revision, base=_.root, file=metaFile), "r", encoding=UTF8) as fd:  # line 249
            _.paths = json.load(fd)  # line 250
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 251
        _.branch = branch  # line 252

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 254
        ''' Save all file information to a commit meta data file. '''  # line 255
        target = branchFolder(branch, revision, base=_.root)  # line 256
        try:  # line 257
            os.makedirs(target)  # line 257
        except:  # line 258
            pass  # line 258
        with codecs.open(os.path.join(target, metaFile), "w", encoding=UTF8) as fd:  # line 259
            json.dump(_.paths, fd, ensure_ascii=False)  # line 260

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'ChangeSet':  # line 262
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        The function returns the state of file tree *differences*, unless "inverse" is True -> then return original data
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes
        progress: Show file names during processing
    '''  # line 271
        write = branch is not None and revision is not None  # line 272
        if write:  # line 273
            try:  # line 274
                os.makedirs(branchFolder(branch, revision, base=_.root))  # line 274
            except FileExistsError:  # HINT "try" only necessary for testing hash collisions  # line 275
                pass  # HINT "try" only necessary for testing hash collisions  # line 275
        changes = ChangeSet({}, {}, {})  # type: ChangeSet  # line 276
        counter = Counter(-1)  # type: Counter  # line 277
        timer = time.time()  # line 277
        hashed = None  # type: _coconut.typing.Optional[str]  # line 278
        written = None  # type: longint  # line 278
        compressed = 0  # type: longint  # line 278
        original = 0  # type: longint  # line 278
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 279
        for path, pinfo in _.paths.items():  # line 280
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 281
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 284
        for path, dirnames, filenames in os.walk(_.root):  # line 285
            dirnames[:] = [f for f in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 286
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 287
            dirnames.sort()  # line 288
            filenames.sort()  # line 288
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # line 289
            walk = filenames if considerOnly is None else list(reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # line 290
            if dontConsider:  # line 291
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 292
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 293
                filename = relPath + SLASH + file  # line 294
                filepath = os.path.join(path, file)  # line 295
                stat = os.stat(filepath)  # line 296
                size, mtime, newtime = stat.st_size, longint(stat.st_mtime * 1000), time.time()  # line 297
                if progress and newtime - timer > .1:  # line 298
                    outstring = "\rPreparing %s  %s" % (PROGRESS_MARKER[counter.inc() % 4], filename)  # line 299
                    sys.stdout.write(outstring + " " * max(0, termWidth - len(outstring)))  # TODO could write to new line instead of carriage return (still true?)  # line 300
                    sys.stdout.flush()  # TODO could write to new line instead of carriage return (still true?)  # line 300
                    timer = newtime  # TODO could write to new line instead of carriage return (still true?)  # line 300
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 301
                    nameHash = hashStr(filename)  # line 302
                    hashed, written = hashFile(filepath, _.compress, saveTo=branchFolder(branch, revision, base=_.root, file=nameHash) if write else None) if size > 0 else (None, 0)  # line 303
                    changes.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 304
                    compressed += written  # line 305
                    original += size  # line 305
                    continue  # line 306
                last = _.paths[filename]  # filename is known - check for modifications  # line 307
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 308
                    hashed, written = hashFile(filepath, _.compress, saveTo=branchFolder(branch, revision, base=_.root, file=last.nameHash) if write else None) if size > 0 else (None, 0)  # line 309
                    changes.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 310
                    continue  # line 310
                elif size != last.size or mtime != last.mtime or (checkContent and hashFile(filepath, _.compress)[0] != last.hash):  # detected a modification  # line 311
                    hashed, written = hashFile(filepath, _.compress, saveTo=branchFolder(branch, revision, base=_.root, file=last.nameHash) if write else None) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 312
                    changes.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 313
                else:  # line 314
                    continue  # line 314
                compressed += written  # line 315
                original += last.size if inverse else size  # line 315
            if relPath in knownPaths:  # at least one file is tracked  # line 316
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked  # line 316
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 317
            for file in names:  # line 318
                changes.deletions[path + SLASH + file] = _.paths[path + SLASH + file]  # line 318
        if progress:  # force new line  # line 319
            print("\rPreparation finished. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed").ljust(termWidth), file=sys.stdout)  # force new line  # line 319
        else:  # line 320
            debug("Finished detecting changes. Compression factor %s" % ("is %.1f" % (original * 100. / compressed) if compressed > 0 else "cannot be computed"))  # line 320
        return changes  # line 321

    def integrateChangeset(_, changes: 'ChangeSet', clear=False) -> 'None':  # line 323
        ''' In-memory update from a changeset, marking deleted files with size=None. Use clear = True to start on an empty path set. '''  # line 324
        if clear:  # line 325
            _.paths.clear()  # line 325
        else:  # line 326
            rm = [p for p, info in _.paths.items() if info.size is None]  # remove files deleted in earlier change sets (revisions)  # line 327
            for old in rm:  # remove previously removed entries completely  # line 328
                del _.paths[old]  # remove previously removed entries completely  # line 328
        for d, info in changes.deletions.items():  # mark now removed entries as deleted  # line 329
            _.paths[d] = PathInfo(info.nameHash, None, info.mtime, None)  # mark now removed entries as deleted  # line 329
        _.paths.update(changes.additions)  # line 330
        _.paths.update(changes.modifications)  # line 331

    def computeSequentialPathSet(_, branch: 'int', revision: 'int') -> 'None':  # line 333
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once  # line 334

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[ChangeSet]]':  # line 336
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 337
        _.loadCommit(branch, 0)  # load initial paths  # line 338
        if incrementally:  # line 339
            yield diffPathSets({}, _.paths)  # line 339
        n = Metadata(_.root)  # type: Metadata  # next changes  # line 340
        for revision in range(1, revision + 1):  # line 341
            n.loadCommit(branch, revision)  # line 342
            changes = diffPathSets(_.paths, n.paths)  # type: ChangeSet  # line 343
            _.integrateChangeset(changes)  # line 344
            if incrementally:  # line 345
                yield changes  # line 345
        yield None  # for the default case - not incrementally  # line 346

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 348
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 351
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 352
            return (_.branch, -1)  # no branch/revision specified  # line 352
        argument = argument.strip()  # line 353
        if argument.startswith(SLASH):  # current branch  # line 354
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 354
        if argument.endswith(SLASH):  # line 355
            try:  # line 356
                return (_.getBranchByName(argument[:-1]), -1)  # line 356
            except ValueError:  # line 357
                Exit("Unknown branch label '%s'" % argument)  # line 357
        if SLASH in argument:  # line 358
            b, r = argument.split(SLASH)[:2]  # line 359
            try:  # line 360
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 360
            except ValueError:  # line 361
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 361
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 362
        if branch not in _.branches:  # line 363
            branch = None  # line 363
        try:  # either branch name/number or reverse/absolute revision number  # line 364
            return (_.branch if branch is None else branch, longint(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 364
        except:  # line 365
            Exit("Unknown branch label or wrong number format")  # line 365
        Exit("This should never happen")  # line 366
        return (None, None)  # line 366

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 368
        while True:  # find latest revision that contained the file physically  # line 369
            source = branchFolder(branch, revision, base=_.root, file=nameHash)  # type: str  # line 370
            if os.path.exists(source) and os.path.isfile(source):  # line 371
                break  # line 371
            revision -= 1  # line 372
            if revision < 0:  # line 373
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 373
        return revision, source  # line 374

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo') -> 'None':  # line 376
        ''' Copy versioned file to other branch/revision. '''  # line 377
        target = branchFolder(toBranch, toRevision, base=_.root, file=pinfo.nameHash)  # type: str  # line 378
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 379
        shutil.copy2(source, target)  # line 380

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 382
        ''' Return file contents, or copy contents into file path provided. '''  # line 383
        source = branchFolder(branch, revision, base=_.root, file=nameHash)  # type: str  # line 384
        try:  # line 385
            with openIt(source, "r", _.compress) as fd:  # line 386
                if toFile is None:  # read bytes into memory and return  # line 387
                    return fd.read()  # read bytes into memory and return  # line 387
                with open(toFile, "wb") as to:  # line 388
                    while True:  # line 389
                        buffer = fd.read(bufSize)  # line 390
                        to.write(buffer)  # line 391
                        if len(buffer) < bufSize:  # line 392
                            break  # line 392
                    return None  # line 393
        except Exception as E:  # line 394
            warn("Cannot read versioned file: %r (%d/%d/%s)" % (E, branch, revision, nameHash))  # line 394
        return None  # line 395

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 397
        ''' Recreate file for given revision, or return contents if path is None. '''  # line 398
        if relPath is None:  # just return contents  # line 399
            return _.readOrCopyVersionedFile(branch, _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 399
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 400
        if ensurePath:  #  and not os.path.exists(os.path.dirname(target)):  # line 401
            try:  # line 402
                os.makedirs(os.path.dirname(target))  # line 402
            except:  # line 403
                pass  # line 403
        if pinfo.size == 0:  # line 404
            with open(target, "wb"):  # line 405
                pass  # line 405
            try:  # update access/modification timestamps on file system  # line 406
                os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 406
            except Exception as E:  # line 407
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 407
            return None  # line 408
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 409
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(target, "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 411
            while True:  # line 412
                buffer = fd.read(bufSize)  # line 413
                to.write(buffer)  # line 414
                if len(buffer) < bufSize:  # line 415
                    break  # line 415
        try:  # update access/modification timestamps on file system  # line 416
            os.utime(target, (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 416
        except Exception as E:  # line 417
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 417
        return None  # line 418

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None) -> 'FrozenSet[str]':  # line 420
        ''' Returns list of tracking patterns for provided branch or current branch. '''  # line 421
        return _coconut.frozenset() if not _.track and not _.picky else frozenset(_.branches[_.branch if branch is None else branch].tracked)  # line 422


# Main client operations
def offline(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 426
    ''' Initial command to start working offline. '''  # line 427
    if os.path.exists(metaFolder):  # line 428
        if '--force' not in options:  # line 429
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 429
        try:  # line 430
            for entry in os.listdir(metaFolder):  # line 431
                resource = metaFolder + os.sep + entry  # line 432
                if os.path.isdir(resource):  # line 433
                    shutil.rmtree(resource)  # line 433
                else:  # line 434
                    os.unlink(resource)  # line 434
        except:  # line 435
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 435
    m = Metadata(os.getcwd())  # type: Metadata  # line 436
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 437
        m.compress = True  # plain file copies instead of compressed ones  # line 437
    if '--picky' in options or m.c.picky:  # Git-like  # line 438
        m.picky = True  # Git-like  # line 438
    elif '--track' in options or m.c.track:  # Svn-like  # line 439
        m.track = True  # Svn-like  # line 439
    if '--strict' in options or m.c.strict:  # always hash contents  # line 440
        m.strict = True  # always hash contents  # line 440
    debug("Preparing offline repository...")  # line 441
    m.createBranch(0, str(defaults["defaultbranch"]) if argument is None else argument, initialMessage="Offline repository created on %s" % strftime())  # main branch's name may be None (e.g. for fossil)  # line 442
    m.branch = 0  # line 443
    m.saveBranches()  # no change immediately after going offline, going back online won't issue a warning  # line 444
    info("Offline repository prepared. Use 'sos online' to finish offline work")  # line 445

def online(options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 447
    ''' Finish working offline. '''  # line 448
    force = '--force' in options  # type: bool  # line 449
    m = Metadata(os.getcwd())  # line 450
    m.loadBranches()  # line 451
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 452
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 452
    strict = '--strict' in options or m.strict  # type: bool  # line 453
    if options.count("--force") < 2:  # line 454
        changes = m.findChanges(checkContent=strict, considerOnly=None if not m.track and not m.picky else m.getTrackingPatterns())  # type: ChangeSet  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 455
        if modified(changes):  # line 456
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 456
    try:  # line 457
        shutil.rmtree(metaFolder)  # line 457
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 457
    except Exception as E:  # line 458
        Exit("Error removing offline repository: %r" % E)  # line 458

def branch(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 460
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it. '''  # line 461
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 462
    stay = '--stay' in options  # type: bool  # continue on current branch after branching  # line 463
    force = '--force' in options  # type: bool  # branch even with local modifications  # line 464
    m = Metadata(os.getcwd())  # type: Metadata  # line 465
    m.loadBranches()  # line 466
    m.loadBranch(m.branch)  # line 467
    if argument and m.getBranchByName(argument) is not None:  # create a named branch  # line 468
        Exit("Branch '%s' already exists. Cannot proceed" % argument)  # create a named branch  # line 468
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 469
    debug("Branching to %sbranch b%02d%s%s..." % ("unnamed " if argument is None else "", branch, " '%s'" % argument if argument else "", " from last revision" if last else ""))  # line 470
    if last:  # line 471
        m.duplicateBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from branch's last revision  # line 472
    else:  # from file tree state  # line 473
        m.createBranch(branch, "Branched from r%02d/b%02d" % (m.branch, max(m.commits.keys())) if argument is None else argument)  # branch from current file tree  # line 474
    if not stay:  # line 475
        m.branch = branch  # line 476
        m.saveBranches()  # line 477
    info("%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if argument is None else "", branch, " '%s'" % argument if argument else ""))  # line 478

def changes(argument: 'str'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 480
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 481
    m = Metadata(os.getcwd())  # type: Metadata  # line 482
    branch = None  # type: _coconut.typing.Optional[int]  # line 482
    revision = None  # type: _coconut.typing.Optional[int]  # line 482
    m.loadBranches()  # knows current branch  # line 483
    strict = '--strict' in options or m.strict  # type: bool  # line 484
    branch, revision = m.parseRevisionString(argument)  # line 485
    if branch not in m.branches:  # line 486
        Exit("Unknown branch")  # line 486
    m.loadBranch(branch)  # knows commits  # line 487
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 488
    if revision < 0 or revision > max(m.commits):  # line 489
        Exit("Unknown revision r%02d" % revision)  # line 489
    info("//|\\\\ Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 490
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 491
    changes = m.findChanges(checkContent=strict, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 492
    m.listChanges(changes)  # line 493
    return changes  # for unit tests only  # line 494

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 496
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 497
    m = Metadata(os.getcwd())  # type: Metadata  # line 498
    branch = None  # type: _coconut.typing.Optional[int]  # line 498
    revision = None  # type: _coconut.typing.Optional[int]  # line 498
    m.loadBranches()  # knows current branch  # line 499
    strict = '--strict' in options or m.strict  # type: bool  # line 500
    _from = {None: option.split("--from=")[1] for option in options if options.startswith("--from=")}.get(None, None)  # type: _coconut.typing.Optional[str]  # line 501
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 502
    if branch not in m.branches:  # line 503
        Exit("Unknown branch")  # line 503
    m.loadBranch(branch)  # knows commits  # line 504
    revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 505
    if revision < 0 or revision > max(m.commits):  # line 506
        Exit("Unknown revision r%02d" % revision)  # line 506
    info("//|\\\\ Differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 507
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 508
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps)  # type: ChangeSet  # line 509
    onlyBinaryModifications = dataCopy(ChangeSet, changes, modifications={k: v for k, v in changes.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 510
    if modified(onlyBinaryModifications):  # line 511
        debug("//|\\\\ File changes")  # line 511
    m.listChanges(onlyBinaryModifications)  # only list modified binary files  # line 512

    if changes.modifications:  # line 514
        debug("%s//|\\\\ Textual modifications" % ("\n" if modified(onlyBinaryModifications) else ""))  # line 514
    for path, pinfo in (c for c in changes.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 515
        content = None  # type: _coconut.typing.Optional[bytes]  # ; othr:str[]; curr:str[]  # line 516
        if pinfo.size == 0:  # empty file contents  # line 517
            content = b""  # empty file contents  # line 517
        else:  # versioned file  # line 518
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 518
            assert content is not None  # versioned file  # line 518
        abspath = os.path.join(m.root, path.replace(SLASH, os.sep))  # current file  # line 519
        blocks = merge(file=content, intoname=abspath, diffOnly=True)  # type: List[MergeBlock]  # only determine change blocks  # line 520
        print("DIF %s%s" % (path, " <timestamp only>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else ""))  # line 521
        for block in blocks:  # line 522
            if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:  # line 523
                pass  # TODO print some previous and following lines - which aren't accessible here anymore  # line 524
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 525
                for no, line in enumerate(block.lines):  # line 526
                    print("+++ %04d |%s|" % (no + block.line, line))  # line 527
            elif block.tipe == MergeBlockType.REMOVE:  # line 528
                for no, line in enumerate(block.lines):  # line 529
                    print("--- %04d |%s|" % (no + block.line, line))  # line 530
            elif block.tipe in [MergeBlockType.REPLACE, MergeBlockType.MODIFY]:  # TODO for MODIFY also show intra-line change ranges  # line 531
                for no, line in enumerate(block.replaces.lines):  # line 532
                    print("- | %04d |%s|" % (no + block.replaces.line, line))  # line 533
                for no, line in enumerate(block.lines):  # line 534
                    print("+ | %04d |%s|" % (no + block.line, line))  # line 535
#      elif block.tipe == MergeBlockType.KEEP: pass
#      elif block.tipe == MergeBlockType.MODIFY:  # intra-line modifications
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 540
    ''' Create new revision from file tree changes vs. last commit. '''  # line 541
    m = Metadata(os.getcwd())  # type: Metadata  # line 542
    m.loadBranches()  # knows current branch  # line 543
    if argument is not None and argument in m.tags:  # line 544
        Exit("Illegal commit message. It was already used as a tag name")  # line 544
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 545
    if m.picky and not trackingPatterns:  # line 546
        Exit("No file patterns staged for commit in picky mode")  # line 546
    changes = None  # type: ChangeSet  # line 547
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but abort if no changes  # line 548
    info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 549
    m.integrateChangeset(changes, clear=True)  # update pathset to changeset only  # line 550
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 551
    m.commits[revision] = CommitInfo(revision, longint(time.time() * 1000), argument)  # comment can be None  # line 552
    m.saveBranch(m.branch)  # line 553
    m.loadBranches()  # TODO is it necessary to load again?  # line 554
    if m.picky:  # line 555
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 556
    else:  # track or simple mode  # line 557
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # set branch dirty  # line 558
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 559
        m.tags.append(argument)  # memorize unique tag  # line 559
    m.saveBranches()  # line 560
    info("Created new revision r%02d%s (+%02d/-%02d/*%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changes.additions), len(changes.deletions), len(changes.modifications)))  # line 561

def status() -> 'None':  # line 563
    ''' Show branches and current repository state. '''  # line 564
    m = Metadata(os.getcwd())  # type: Metadata  # line 565
    m.loadBranches()  # knows current branch  # line 566
    current = m.branch  # type: int  # line 567
    info("//|\\\\ Offline repository status")  # line 568
    print("Content checking %sactivated" % ("" if m.strict else "de"))  # line 569
    print("Data compression %sactivated" % ("" if m.compress else "de"))  # line 570
    print("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 571
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 572
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 573
        m.loadBranch(branch.number)  # knows commit history  # line 574
        print("  %s b%02d%s @%s (%s) with %d commits%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), ". Last comment: '%s'" % m.commits[max(m.commits)].message if m.commits[max(m.commits)].message else ""))  # line 575
    if m.track or m.picky and len(m.branches[m.branch].tracked) > 0:  # line 576
        info("\nTracked file patterns:")  # line 577
        print(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 578

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str]]':  # line 580
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were added.
      check: stop program on detected change
      commit: don't stop on changes, because that's what we need in the operation
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags. '''  # line 585
    m = Metadata(os.getcwd())  # type: Metadata  # line 586
    m.loadBranches()  # knows current branch  # line 587
    force = '--force' in options  # type: bool  # line 588
    strict = '--strict' in options or m.strict  # type: bool  # line 589
    if argument is not None:  # line 590
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 591
        if branch is None:  # line 592
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 592
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 593

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 596
    m.computeSequentialPathSet(m.branch, max(m.commits))  # load all commits up to specified revision  # line 597
    changes = m.findChanges(m.branch if commit else None, max(m.commits) + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else conditionalIntersection(onlys, trackingPatterns), dontConsider=excps)  # type: ChangeSet  # line 598
    if check and modified(changes) and not force:  # line 599
        m.listChanges(changes)  # line 600
        if not commit:  # line 601
            Exit("File tree contains changes. Use --force to proceed")  # line 601
    elif commit and not force:  #  and not check  # line 602
        Exit("Nothing to commit")  #  and not check  # line 602

    if argument is not None:  # branch/revision specified  # line 604
        m.loadBranch(branch)  # knows commits of target branch  # line 605
        revision = revision if revision >= 0 else len(m.commits) + revision  # negative indexing  # line 606
        if revision < 0 or revision > max(m.commits):  # line 607
            Exit("Unknown revision r%02d" % revision)  # line 607
        return (m, branch, revision, changes, strict, force, m.getTrackingPatterns(branch))  # line 608
    return (m, m.branch, max(m.commits) + (1 if commit else 0), changes, strict, force, trackingPatterns)  # line 609

def switch(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 611
    ''' Continue work on another branch, replacing file tree changes. '''  # line 612
    changes = None  # type: ChangeSet  # line 613
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options)  # line 614
    info("//|\\\\ Switching to branch %sb%02d/r%02d" % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 615

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 618
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked)  # line 619
    else:  # full file switch  # line 620
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 621
        changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 622
        if not modified(changes):  # line 623
            info("No changes to current file tree")  # line 624
        else:  # integration required  # line 625
            for path, pinfo in changes.deletions.items():  # line 626
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 627
                print("ADD " + path)  # line 628
            for path, pinfo in changes.additions.items():  # line 629
                os.unlink(os.path.join(m.root, path.replace(SLASH, os.sep)))  # is added in current file tree: remove from branch to reach target  # line 630
                print("DEL " + path)  # line 631
            for path, pinfo in changes.modifications.items():  # line 632
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 633
                print("MOD " + path)  # line 634
    m.branch = branch  # line 635
    m.saveBranches()  # store switched path info  # line 636
    info("Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 637

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'None':  # line 639
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add (don't remove), --rm (don't insert), --add-lines/--rm-lines (inside each file)
      User options for conflict resolution: --theirs/--mine/--ask
  '''  # line 644
    mrg = firstOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE}, options, MergeOperation.BOTH)  # type: int  # default operation is replicate remove state for non-conflicting cases (insertions/deletions)  # line 645
    res = firstOfMap({'--theirs': ConflictResolution.THEIRS, '--mine': ConflictResolution.MINE}, options, ConflictResolution.NEXT)  # type: int  # NEXT means deeper level  # line 646
    mrgline = firstOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE}, options, mrg)  # type: int  # default operation for modified files is same as for files  # line 647
    resline = firstOfMap({'--theirs-lines': ConflictResolution.THEIRS, '--mine-lines': ConflictResolution.MINE}, options, ConflictResolution.ASK)  # type: int  # line 648
    m = Metadata(os.getcwd())  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 649
    m.loadBranches()  # line 650
    changes = None  # type: ChangeSet  # line 650
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 651
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 652
    debug("Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 653

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 656
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 657
    changes = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not m.track and not m.picky else conditionalIntersection(onlys, trackingUnion), dontConsider=excps)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 658
    if not (mrg & MergeOperation.INSERT and changes.additions or (mrg & MergeOperation.REMOVE and changes.deletions) or changes.modifications):  # no file ops  # line 659
        if trackingUnion != trackingPatterns:  # nothing added  # line 660
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 661
        else:  # line 662
            info("Nothing to update")  # but write back updated branch info below  # line 663
    else:  # integration required  # line 664
        for path, pinfo in changes.deletions.items():  # deletions mark files not present in current file tree -> needs additon  # line 665
            if mrg & MergeOperation.INSERT:  # deleted in current file tree: restore from branch to reach target  # line 666
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 666
            print("ADD " + path if mrg & MergeOperation.INSERT else "(A) " + path)  # line 667
        for path, pinfo in changes.additions.items():  # line 668
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 669
                Exit("This should never happen")  # because untracked files of other branch cannot be detected (which is good)  # line 669
            if mrg & MergeOperation.REMOVE:  # line 670
                os.unlink(m.root + os.sep + path.replace(SLASH, os.sep))  # line 670
            print("DEL " + path if mrg & MergeOperation.REMOVE else "(D) " + path)  # not contained in other branch, but maybe kept  # line 671
        for path, pinfo in changes.modifications.items():  # line 672
            into = os.path.join(m.root, path.replace(SLASH, os.sep))  # type: str  # line 673
            binary = not m.isTextType(path)  # line 674
            if res & ConflictResolution.ASK or (binary and res == ConflictResolution.NEXT):  # TODO this may ask user even if no interaction was asked for (check line level for interactivity fist)  # line 675
                print(("MOD " + path if not binary else "BIN ") + path)  # line 676
                reso = {"i": ConflictResolution.MINE, "t": ConflictResolution.THEIRS, "m": ConflictResolution.NEXT}.get(user_input(" Resolve: *M[I]ne, [T]heirs, [M]erge: (I)").strip().lower(), ConflictResolution.MINE)  # line 677
                debug("User selected %d" % reso)  # line 678
            else:  # line 679
                reso = res  # line 679
            if reso & ConflictResolution.THEIRS:  # line 680
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 681
                print("THR " + path)  # line 682
            elif reso & ConflictResolution.MINE:  # line 683
                print("MNE " + path)  # nothing to do! same as skip  # line 684
            else:  # NEXT: line-based merge  # line 685
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 686
                if file is not None:  # if None, error message was already logged  # line 687
                    contents = merge(file=file, intoname=into, mergeOperation=mrgline, conflictResolution=resline)  # type: bytes  # line 688
                    with open(path, "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 689
                        fd.write(contents)  # TODO write to temp file first, in case writing fails  # line 689
    info("Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 690
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 691
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 692
    m.saveBranches()  # line 693

def delete(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 695
    ''' Remove a branch entirely. '''  # line 696
    m, branch, revision, changes, strict, force, trackingPatterns = exitOnChanges(None, options)  # line 697
    if len(m.branches) == 1:  # line 698
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 698
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 699
    if branch is None or branch not in m.branches:  # line 700
        Exit("Unknown branch")  # line 700
    debug("Removing branch %d%s..." % (branch, " '%s'" % m.branches[branch].name if m.branches[branch].name else ""))  # line 701
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 702
    info("Branch b%02d%s removed" % (branch, " '%s'" % binfo.name if binfo.name else ""))  # line 703

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 705
    ''' Add a tracked files pattern to current branch's tracked files. '''  # line 706
    force = '--force' in options  # type: bool  # line 707
    m = Metadata(os.getcwd())  # type: Metadata  # line 708
    m.loadBranches()  # line 709
    if not m.track and not m.picky:  # line 710
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' instead")  # line 710
    if pattern in m.branches[m.branch].tracked:  # line 711
        Exit("Pattern '%s' already tracked" % pattern)  # line 711
    if not force and not os.path.exists(relPath.replace(SLASH, os.sep)):  # line 712
        Exit("The pattern folder doesn't exist. Use --force to add it anyway")  # line 712
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 713
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 714
    m.branches[m.branch].tracked.append(pattern)  # line 715
    m.saveBranches()  # line 716
    info("Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 717

def remove(relPath: 'str', pattern: 'str') -> 'None':  # line 719
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 720
    m = Metadata(os.getcwd())  # type: Metadata  # line 721
    m.loadBranches()  # line 722
    if not m.track and not m.picky:  # line 723
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 723
    if pattern not in m.branches[m.branch].tracked:  # line 724
        suggestion = _coconut.set()  # type: Set[str]  # line 725
        for pat in m.branches[m.branch].tracked:  # line 726
            if fnmatch.fnmatch(pattern, pat):  # line 727
                suggestion.add(pat)  # line 727
        if suggestion:  # TODO use same wording as in move  # line 728
            print("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 728
        Exit("Tracked pattern '%s' not found" % pattern)  # line 729
    m.branches[m.branch].tracked.remove(pattern)  # line 730
    m.saveBranches()  # line 731
    info("Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 732

def ls(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]) -> 'None':  # line 734
    ''' List specified directory, augmenting with repository metadata. '''  # line 735
    folder = "." if argument is None else argument  # type: str  # line 736
    m = Metadata(os.getcwd())  # type: Metadata  # line 737
    m.loadBranches()  # line 738
    info("Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 739
    relPath = os.path.relpath(folder, m.root).replace(os.sep, SLASH)  # type: str  # line 740
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 741
    if '--patterns' in options:  # line 742
        out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 743
        if out:  # line 744
            print(out)  # line 744
        return  # line 745
    files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 746
    for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 747
        ignore = None  # type: _coconut.typing.Optional[str]  # line 748
        for ig in m.c.ignores:  # line 749
            if fnmatch.fnmatch(file, ig):  # remember first match  # line 750
                ignore = ig  # remember first match  # line 750
                break  # remember first match  # line 750
        if ig:  # line 751
            for wl in m.c.ignoresWhitelist:  # line 752
                if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 753
                    ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 753
                    break  # found a white list entry for ignored file, undo ignoring it  # line 753
        if not ignore:  # line 754
            matches = []  # type: List[str]  # line 755
            for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 756
                if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 757
                    matches.append(os.path.basename(pattern))  # line 757
        matches.sort(key=lambda element: len(element))  # line 758
        print("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else "..."), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 759

def log(options: '_coconut.typing.Sequence[str]') -> 'None':  # line 761
    ''' List previous commits on current branch. '''  # line 762
    m = Metadata(os.getcwd())  # type: Metadata  # line 763
    m.loadBranches()  # knows current branch  # line 764
    m.loadBranch(m.branch)  # knows commit history  # line 765
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("//|\\\\ Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 766
    nl = len("%d" % max(m.commits))  # determine space needed for revision  # line 767
    changeset = m.computeSequentialPathSetIterator(m.branch, max(m.commits))  # line 768
    maxWidth = max([wcswidth((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) for commit in m.commits.values()])  # type: int  # line 769
    for no in range(max(m.commits) + 1):  # line 770
        commit = m.commits[no]  # type: CommitInfo  # line 771
        changes = next(changeset)  # type: ChangeSet  # side-effect: updates m.paths  # line 772
        newTextFiles = len([file for file in changes.additions.keys() if m.isTextType(file)])  # type: int  # line 773
        print("  %s r%s @%s (+%02d/-%02d/*%02d +%02dT/%05.1f%%) |%s|" % ("*" if commit.number == max(m.commits) else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(changes.additions), len(changes.deletions), len(changes.modifications), newTextFiles, 0. if len(changes.additions) == 0 else newTextFiles * 100. / len(changes.additions), ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)).ljust(maxWidth)))  # line 774
        if '--changes' in options:  # line 775
            m.listChanges(changes)  # line 775

def config(argument: 'str', options: 'List[str]'=[]) -> 'None':  # line 777
    if argument not in ["set", "unset", "show", "list", "add", "rm"]:  # line 778
        Exit("Unknown config command")  # line 778
    if not configr:  # line 779
        Exit("Cannot execute config command. 'configr' module not installed")  # line 779
    c = loadConfig()  # type: Union[configr.Configr, Accessor]  # line 780
    if argument == "set":  # line 781
        if len(options) < 2:  # line 782
            Exit("No key nor value specified")  # line 782
        if options[0] not in (["defaultbranch"] + CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS):  # line 783
            Exit("Unsupported key %r" % options[0])  # line 783
        if options[0] in CONFIGURABLE_FLAGS and options[1].lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 784
            Exit("Cannot set flag to '%s'. Try on/off instead" % options[1].lower())  # line 784
        c[options[0]] = options[1].lower() in TRUTH_VALUES if options[0] in CONFIGURABLE_FLAGS else (options[1].strip() if options[0] not in CONFIGURABLE_LISTS else safeSplit(options[1], ";"))  # TODO sanitize texts?  # line 785
    elif argument == "unset":  # line 786
        if len(options) < 1:  # line 787
            Exit("No key specified")  # line 787
        if options[0] not in c.keys():  # line 788
            Exit("Unknown key")  # line 788
        del c[options[0]]  # line 789
    elif argument == "add":  # line 790
        if len(options) < 2:  # line 791
            Exit("No key nor value specified")  # line 791
        if options[0] not in CONFIGURABLE_LISTS:  # line 792
            Exit("Unsupported key for add %r" % options[0])  # line 792
        if options[0] not in c.keys():  # add list  # line 793
            c[options[0]] = [options[1]]  # add list  # line 793
        elif options[1] in c[options[0]]:  # line 794
            Exit("Value already contained")  # line 794
        c[options[0]].append(options[1])  # line 795
    elif argument == "rm":  # line 796
        if len(options) < 2:  # line 797
            Exit("No key nor value specified")  # line 797
        if options[0] not in c.keys():  # line 798
            Exit("Unknown key specified: %r" % options[0])  # line 798
        if options[1] not in c[options[0]]:  # line 799
            Exit("Unknown value: %r" % options[1])  # line 799
        c[options[0]].remove(options[1])  # line 800
    else:  # Show or list  # line 801
        for k, v in sorted(c.items()):  # line 802
            print("%s: %r" % (k.rjust(20), v))  # line 802
        if len(c.keys()) == 0:  # TODO list defaults instead? Or display [DEFAULT] for each item above if unmodified  # line 803
            info("No configuration stored, using only defaults.")  # TODO list defaults instead? Or display [DEFAULT] for each item above if unmodified  # line 803
        return  # line 804
    f, g = saveConfig(c)  # line 805
    if f is None:  # line 806
        error("Error saving user configuration: %r" % g)  # line 806

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[]) -> 'None':  # line 808
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique. '''  # line 809
    force = '--force' in options  # type: bool  # line 810
    soft = '--soft' in options  # type: bool  # line 811
    if not os.path.exists(relPath.replace(SLASH, os.sep)) and not force:  # line 812
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 812
    m = Metadata(os.getcwd())  # type: Metadata  # line 813
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(relPath.replace(SLASH, os.sep)) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 814
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 815
    if not matching and not force:  # line 816
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 816
    m.loadBranches()  # knows current branch  # line 817
    if not m.track and not m.picky:  # line 818
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 818
    if pattern not in m.branches[m.branch].tracked:  # line 819
        for tracked in (t for t in m.branches[m.branch].tracked if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 820
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 821
            if alternative:  # line 822
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 822
        if not (force or soft):  # line 823
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 823
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 824
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 825
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 826
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 830
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 831
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 831
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 832
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 833
    if len({st[1] for st in matches}) != len(matches):  # line 834
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 834
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 835
    if os.path.exists(newRelPath):  # line 836
        exists = [filename[1] for filename in matches if os.path.exists(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep))]  # type: _coconut.typing.Sequence[str]  # line 837
        if exists and not (force or soft):  # line 838
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 838
    else:  # line 839
        os.makedirs(os.path.abspath(newRelPath.replace(SLASH, os.sep)))  # line 839
    if not soft:  # perform actual renaming  # line 840
        for (source, target) in matches:  # line 841
            try:  # line 842
                shutil.move(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep)), os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep)))  # line 842
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 843
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 843
    m.branches[m.branch].tracked[m.branches[m.branch].tracked.index(pattern)] = newPattern  # line 844
    m.saveBranches()  # line 845

def parse(root: 'str', cwd: 'str'):  # line 847
    ''' Main operation. Main has already chdir into VCS root folder, cwd is original working directory for add, rm. '''  # line 848
    debug("Parsing command-line arguments...")  # line 849
    try:  # line 850
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 851
        argument = sys.argv[2].strip() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None  # line 852
        options = sys.argv[3:] if command == "config" else [c for c in sys.argv[2:] if c.startswith("--")]  # consider second parameter for no-arg command, otherwise from third on  # line 853
        onlys, excps = parseOnlyOptions(cwd, options)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 854
        debug("Processing command %r with argument '%s' and options %r." % ("" if command is None else command, "" if argument is None else argument, options))  # line 855
        if command[:1] in "amr":  # line 856
            relPath, pattern = relativize(root, os.path.join(cwd, "." if argument is None else argument))  # line 856
        if command[:1] == "m":  # line 857
            if not options:  # line 858
                Exit("Need a second file pattern argument as target for move/rename command")  # line 858
            newRelPath, newPattern = relativize(root, os.path.join(cwd, options[0]))  # line 859
        if command[:1] == "a":  # line 860
            add(relPath, pattern, options)  # line 860
        elif command[:1] == "b":  # line 861
            branch(argument, options)  # line 861
        elif command[:2] == "ch":  # line 862
            changes(argument, options, onlys, excps)  # line 862
        elif command[:3] == "com":  # line 863
            commit(argument, options, onlys, excps)  # line 863
        elif command[:2] == "ci":  # line 864
            commit(argument, options, onlys, excps)  # line 864
        elif command[:3] == 'con':  # line 865
            config(argument, options)  # line 865
        elif command[:2] == "de":  # line 866
            delete(argument, options)  # line 866
        elif command[:2] == "di":  # line 867
            diff(argument, options, onlys, excps)  # line 867
        elif command[:1] == "h":  # line 868
            usage()  # line 868
        elif command[:2] == "lo":  # line 869
            log(options)  # line 869
        elif command[:2] == "li":  # TODO handle absolute paths as well, also for Windows? think through  # line 870
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO handle absolute paths as well, also for Windows? think through  # line 870
        elif command[:2] == "ls":  # TODO avoid and/or normalize root super paths (..)  # line 871
            ls(relativize(root, cwd if argument is None else os.path.join(cwd, argument))[1], options)  # TODO avoid and/or normalize root super paths (..)  # line 871
        elif command[:1] == "m":  # line 872
            move(relPath, pattern, newRelPath, newPattern, options[1:])  # line 872
        elif command[:2] == "of":  # line 873
            offline(argument, options)  # line 873
        elif command[:2] == "on":  # line 874
            online(options)  # line 874
        elif command[:1] == "r":  # line 875
            remove(relPath, pattern)  # line 875
        elif command[:2] == "st":  # line 876
            status()  # line 876
        elif command[:2] == "sw":  # line 877
            switch(argument, options, onlys, excps)  # line 877
        elif command[:1] == "u":  # line 878
            update(argument, options, onlys, excps)  # line 878
        elif command[:1] == "v":  # line 879
            usage(short=True)  # line 879
        else:  # line 880
            Exit("Unknown command '%s'" % command)  # line 880
        Exit(code=0)  # line 881
    except (Exception, RuntimeError) as E:  # line 882
        print(str(E))  # line 883
        import traceback  # line 884
        traceback.print_exc()  # line 885
        traceback.print_stack()  # line 886
        try:  # line 887
            traceback.print_last()  # line 887
        except:  # line 888
            pass  # line 888
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 889

def main() -> 'None':  # line 891
    global debug, info, warn, error  # line 892
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 893
    _log = Logger(logging.getLogger(__name__))  # line 894
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 894
    for option in (o for o in ['--log', '--verbose', '-v', '--sos'] if o in sys.argv):  # clean up program arguments  # line 895
        sys.argv.remove(option)  # clean up program arguments  # line 895
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 896
        usage()  # line 896
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 897
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 898
    debug("Found root folders for SOS|VCS: %s|%s" % ("" if root is None else root, "" if vcs is None else vcs))  # line 899
    defaults["defaultbranch"] = vcsBranches.get(cmd, "trunk")  # sets dynamic default with SVN fallback  # line 900
    if force_sos or root is not None or ("" if command is None else command)[:2] == "of" or ("" if command is None else command)[:1] in ["h", "v"]:  # in offline mode or just going offline TODO what about git config?  # line 901
        cwd = os.getcwd()  # line 902
        os.chdir(cwd if command[:2] == "of" else cwd if root is None else root)  # line 903
        parse(root, cwd)  # line 904
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 905
        info("SOS: Running '%s %s'" % (cmd, " ".join(sys.argv[1:])))  # line 906
        import subprocess  # only required in this section  # line 907
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 908
        inp = ""  # type: str  # line 909
        while True:  # line 910
            so, se = process.communicate(input=inp)  # line 911
            if process.returncode is not None:  # line 912
                break  # line 912
            inp = sys.stdin.read()  # line 913
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 914
            if root is None:  # line 915
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 915
            m = Metadata(root)  # line 916
            m.loadBranches()  # read repo  # line 917
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 918
            m.saveBranches()  # line 919
    else:  # line 920
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 920


# Main part
verbose = os.environ.get("DEBUG", "False").lower() == "true" or '--verbose' in sys.argv or '-v' in sys.argv  # imported from utility, and only modified here  # line 924
level = logging.DEBUG if verbose else logging.INFO  # line 925
force_sos = '--sos' in sys.argv  # type: bool  # line 926
force_vcs = '--vcs' in sys.argv  # type: bool  # line 927
_log = Logger(logging.getLogger(__name__))  # type: logging.Logger  # line 928
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 928
if __name__ == '__main__':  # line 929
    main()  # line 929
