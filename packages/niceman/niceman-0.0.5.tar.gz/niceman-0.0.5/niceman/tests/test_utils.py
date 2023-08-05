# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the niceman package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Test testing utilities

"""

import os
import shutil
import sys
import logging
from mock import patch
from six import PY3
import six.moves.builtins as __builtin__

from operator import itemgetter
from os.path import dirname, normpath, pardir, basename
from os.path import isabs, expandvars, expanduser
from collections import OrderedDict

from ..dochelpers import exc_str
from ..utils import updated, HashableDict, batch_process_list
from os.path import join as opj, abspath, exists
from ..utils import rotree, swallow_outputs, swallow_logs, setup_exceptionhook, md5sum
from ..utils import getpwd, chpwd
from ..utils import auto_repr
from ..utils import find_files
from ..utils import line_profile
from ..utils import not_supported_on_windows
from ..utils import file_basename
from ..utils import expandpath, is_explicit_path
from ..utils import any_re_search
from ..utils import unique
from ..utils import get_func_kwargs_doc
from ..utils import make_tempfile
from ..utils import on_windows
from ..utils import _path_
from ..utils import to_unicode
from ..utils import generate_unique_name

from nose.tools import ok_, eq_, assert_false, assert_equal, assert_true

from .utils import with_tempfile, assert_in, with_tree, to_binarystring, \
    is_unicode, is_binarystring
from .utils import SkipTest
from .utils import assert_cwd_unchanged, skip_if_on_windows
from .utils import assure_dict_from_str, assure_list_from_str
from .utils import ok_generator
from .utils import assert_not_in
from .utils import assert_raises
from .utils import ok_startswith
from .utils import skip_if_no_module


@with_tempfile(mkdir=True)
def __test_rotree(d):  # TODO: redo without AnnexRepo
    d2 = opj(d, 'd1', 'd2')  # deep nested directory
    f = opj(d2, 'f1')
    os.makedirs(d2)
    with open(f, 'w') as f_:
        f_.write("LOAD")
    with swallow_logs():
        pass # ar = AnnexRepo(d2)
    rotree(d)
    # we shouldn't be able to delete anything UNLESS in "crippled" situation:
    # root, or filesystem is FAT etc
    # Theoretically annex should declare FS as crippled when ran as root, but
    # see http://git-annex.branchable.com/bugs/decides_that_FS_is_crippled_under_cowbuilder___40__symlinks_supported_etc__41__/#comment-60c3cbe2710d6865fb9b7d6e247cd7aa
    # so explicit 'or'
    if not (ar.is_crippled_fs() or (os.getuid() == 0)):
        assert_raises(OSError, os.unlink, f)
        assert_raises(OSError, shutil.rmtree, d)
        # but file should still be accessible
        with open(f) as f_:
            eq_(f_.read(), "LOAD")
    # make it RW
    rotree(d, False)
    os.unlink(f)
    shutil.rmtree(d)


def test_swallow_outputs():
    with swallow_outputs() as cm:
        eq_(cm.out, '')
        sys.stdout.write("out normal")
        sys.stderr.write("out error")
        eq_(cm.out, 'out normal')
        sys.stdout.write(" and more")
        eq_(cm.out, 'out normal and more')  # incremental
        eq_(cm.err, 'out error')
        eq_(cm.err, 'out error')  # the same value if multiple times


def test_swallow_logs():
    lgr = logging.getLogger('niceman')
    with swallow_logs(new_level=9) as cm:
        eq_(cm.out, '')
        lgr.log(8, "very heavy debug")
        eq_(cm.out, '')  # not even visible at level 9
        lgr.log(9, "debug1")
        eq_(cm.out, 'debug1\n')  # not even visible at level 9
        lgr.info("info")
        eq_(cm.out, 'debug1\ninfo\n')  # not even visible at level 9


def _check_setup_exceptionhook(interactive=None):
    old_exceptionhook = sys.excepthook

    post_mortem_tb = []

    def our_post_mortem(tb):
        post_mortem_tb.append(tb)

    with patch('sys.excepthook'), \
            patch('niceman.utils.is_interactive', lambda: interactive), \
            patch('pdb.post_mortem', our_post_mortem):
        setup_exceptionhook()
        our_exceptionhook = sys.excepthook
        ok_(old_exceptionhook != our_exceptionhook)
        #out = sys.stdout
        with swallow_logs() as cml, swallow_outputs() as cmo:
            # we need to call our_exceptionhook explicitly b/c nose
            # swallows all Exceptions and hook never gets executed
            try:
                raise RuntimeError
            except Exception as e:  # RuntimeError:
                type_, value_, tb_ = sys.exc_info()
            our_exceptionhook(type_, value_, tb_)
            if PY3:
                # Happens under tox environment but not in manually crafted ones -- not yet sure
                # what it is about but --dbg does work with python3 so lettting it skip for now
                raise SkipTest("TODO: Not clear why in PY3 calls cleanup if we try to access the beast")
            assert_in('Traceback (most recent call last)', cmo.err)
            assert_in('in _check_setup_exceptionhook', cmo.err)
            if interactive:
                assert_equal(post_mortem_tb[0], tb_)
            else:
                assert_equal(post_mortem_tb, [])
                # assert_in('We cannot setup exception hook', cml.out)

    eq_(old_exceptionhook, sys.excepthook)


def test_setup_exceptionhook():
    for tval in [True, False]:
        yield _check_setup_exceptionhook, tval


def test_md5sum():
    # just a smoke (encoding/decoding) test for md5sum
    _ = md5sum(__file__)


# archives support in with_tree disabled in niceman's copy
# @with_tree([('1.tar.gz', (('1 f.txt', '1 f load'),))])
# def test_md5sum_archive(d):
#     # just a smoke (encoding/decoding) test for md5sum
#     _ = md5sum(opj(d, '1.tar.gz'))

def test_updated():
    d = {}
    eq_(updated(d, {1: 2}), {1: 2})
    eq_(d, {})

    d = {'a': 'b'}
    eq_(updated(d, ((0, 1), (2, 3))), {0: 1, 'a': 'b', 2: 3})
    eq_(d, {'a': 'b'})

    # and that it would maintain the type
    d = OrderedDict(((99, 0), ('z', 0), ('a', 0)))
    d_ = updated(d, {0: 1})
    ok_(isinstance(d_, OrderedDict))
    eq_(d_, OrderedDict(((99, 0), ('z', 0), ('a', 0), (0, 1))))


def test_get_local_file_url_windows():
    raise SkipTest("TODO")

@assert_cwd_unchanged
def test_getpwd_basic():
    pwd = getpwd()
    ok_(isabs(pwd))
    eq_(os.getcwd(), abspath(pwd))

    # that we do not chdir anywhere if None provided
    with patch('os.chdir') as oschdir:
        with chpwd(None):
            eq_(getpwd(), pwd)
        assert_false(oschdir.called)


@skip_if_on_windows
@with_tempfile(mkdir=True)
@assert_cwd_unchanged
def test_getpwd_symlink(tdir=None):
    sdir = opj(tdir, 's1')
    pwd_orig = getpwd()
    os.symlink('.', sdir)
    s1dir = opj(sdir, 's1')
    s2dir = opj(sdir, 's2')
    try:
        chpwd(sdir)
        pwd = getpwd()
        eq_(pwd, sdir)
        chpwd('s1')
        eq_(getpwd(), s1dir)
        chpwd('.')
        eq_(getpwd(), s1dir)
        chpwd('..')
        eq_(getpwd(), sdir)
    finally:
        chpwd(pwd_orig)

    # test context handler way of use
    with chpwd(s1dir):
        eq_(getpwd(), s1dir)
    eq_(getpwd(), pwd_orig)

    assert_false(exists(s2dir))
    with assert_raises(OSError):
        with chpwd(s2dir):
            pass
    with chpwd(s2dir, mkdir=True):
        ok_(exists(s2dir))
        eq_(getpwd(), s2dir)


def test_auto_repr():

    class withoutrepr:
        def __init__(self):
            self.a = "does not matter"

    @auto_repr
    class buga:
        def __init__(self):
            self.a = 1
            self.b = list(range(100))
            self.c = withoutrepr()
            self._c = "protect me"

        def some(self):
            return "some"

    assert_equal(repr(buga()), "buga(a=1, b=<<[0, 1, 2, 3, 4, 5, 6, ...>>, c=<withoutrepr>)")
    assert_equal(buga().some(), "some")


def test_assure_list_from_str():
    assert_equal(assure_list_from_str(''), None)
    assert_equal(assure_list_from_str([]), None)
    assert_equal(assure_list_from_str('somestring'), ['somestring'])
    assert_equal(assure_list_from_str('some\nmultiline\nstring'), ['some', 'multiline', 'string'])
    assert_equal(assure_list_from_str(['something']), ['something'])
    assert_equal(assure_list_from_str(['a', 'listof', 'stuff']), ['a', 'listof', 'stuff'])


def test_assure_dict_from_str():
    assert_equal(assure_dict_from_str(''), None)
    assert_equal(assure_dict_from_str({}), None)
    assert_equal(assure_dict_from_str(
            '__ac_name={user}\n__ac_password={password}\nsubmit=Log in\ncookies_enabled='), dict(
             __ac_name='{user}', __ac_password='{password}', cookies_enabled='', submit='Log in'))
    assert_equal(assure_dict_from_str(
        dict(__ac_name='{user}', __ac_password='{password}', cookies_enabled='', submit='Log in')), dict(
             __ac_name='{user}', __ac_password='{password}', cookies_enabled='', submit='Log in'))


def test_any_re_search():
    assert_true(any_re_search('a', 'a'))
    assert_true(any_re_search('a', 'bab'))
    assert_false(any_re_search('^a', 'bab'))
    assert_true(any_re_search(['b', '.ab'], 'bab'))
    assert_false(any_re_search(['^b', 'bab'], 'ab'))


def test_find_files():
    tests_dir = dirname(__file__)
    proj_dir = normpath(opj(dirname(__file__), pardir))

    ff = find_files('.*', proj_dir)
    ok_generator(ff)
    files = list(ff)
    assert(len(files) > 10)  # we have more than 10 test files here
    assert_in(opj(tests_dir, 'test_utils.py'), files)
    # and no directories should be mentioned
    assert_not_in(tests_dir, files)

    ff2 = find_files('.*', proj_dir, dirs=True)
    files2 = list(ff2)
    assert_in(opj(tests_dir, 'test_utils.py'), files2)
    assert_in(tests_dir, files2)

    # now actually matching the path
    ff3 = find_files('.*/test_.*\.py$', proj_dir, dirs=True)
    files3 = list(ff3)
    assert_in(opj(tests_dir, 'test_utils.py'), files3)
    assert_not_in(tests_dir, files3)
    for f in files3:
        ok_startswith(basename(f), 'test_')

from .utils import with_tree
@with_tree(tree={
    '.git': {
        '1': '2'
    },
    'd1': {
        '.git': 'possibly a link from submodule'
    },
    'git': 'just a file'
})
def test_find_files_exclude_vcs(repo=None):
    ff = find_files('.*', repo, dirs=True)
    files = list(ff)
    assert_equal({basename(f) for f in files}, {'d1', 'git'})
    assert_not_in(opj(repo, '.git'), files)

    ff = find_files('.*', repo, dirs=True, exclude_vcs=False)
    files = list(ff)
    assert_equal({basename(f) for f in files}, {'d1', 'git', '.git', '1'})
    assert_in(opj(repo, '.git'), files)


def test_line_profile():
    skip_if_no_module('line_profiler')

    @line_profile
    def f(j):
        i = j + 1  # xyz
        return i

    with swallow_outputs() as cmo:
        assert_equal(f(3), 4)
        assert_equal(cmo.err, '')
        assert_in('i = j + 1  # xyz', cmo.out)


def test_not_supported_on_windows():
    with patch('niceman.utils.on_windows', True):
        assert_raises(NotImplementedError, not_supported_on_windows)
        assert_raises(NotImplementedError, not_supported_on_windows, "msg")

    with patch('niceman.utils.on_windows', False):
        assert_equal(not_supported_on_windows(), None)
        assert_equal(not_supported_on_windows("msg"), None)


def test_file_basename():
    eq_(file_basename('1'), '1')
    eq_(file_basename('d1/1'), '1')
    eq_(file_basename('/d1/1'), '1')
    eq_(file_basename('1.'), '1.')
    eq_(file_basename('1.tar.gz'), '1')
    eq_(file_basename('1.Tar.gz'), '1')
    eq_(file_basename('1._bak.gz'), '1')
    eq_(file_basename('1.tar.gz', return_ext=True), ('1', 'tar.gz'))
    eq_(file_basename('/tmp/1.tar.gz'), '1')
    eq_(file_basename('/tmp/1.longish.gz'), '1.longish')
    eq_(file_basename('1_R1.1.1.tar.gz'), '1_R1.1.1')
    eq_(file_basename('ds202_R1.1.1.tgz'), 'ds202_R1.1.1')


def test_expandpath():
    eq_(expandpath("some", False), expanduser('some'))
    eq_(expandpath("some", False), expandvars('some'))
    assert_true(isabs(expandpath('some')))
    # this may have to go because of platform issues
    eq_(expandpath("$HOME"), expanduser('~'))


def test_is_explicit_path():
    # by default expanded paths are absolute, hence explicit
    assert_true(is_explicit_path(expandpath('~')))
    assert_false(is_explicit_path("here"))


def test_make_tempfile():
    # check if mkdir, content conflict caught
    with assert_raises(ValueError):
        with make_tempfile(content="blah", mkdir=True):  # pragma: no cover
            pass


def test_unique():
    eq_(unique(range(3)), [0, 1, 2])
    eq_(unique((1, 0, 1, 3, 2, 0, 1)), [1, 0, 3, 2])
    eq_(unique([]), [])
    eq_(unique([(1, 2), (1,), (1, 2), (0, 3)]), [(1, 2), (1,), (0, 3)])

    # with a key now
    eq_(unique([(1, 2), (1,), (1, 2), (0, 3)], key=itemgetter(0)), [(1, 2), (0, 3)])
    eq_(unique([(1, 2), (1, 3), (1, 2), (0, 3)], key=itemgetter(1)), [(1, 2), (1, 3)])


def test_path_():
    eq_(_path_('a'), 'a')
    if on_windows:
        eq_(_path_('a/b'), r'a\b')
    else:
        p = 'a/b/c'
        assert(_path_(p) is p)  # nothing is done to it whatsoever


def test_unicode_and_binary_conversion():
    s = "Test String"
    s_unicode = to_unicode(s)
    s_binary = to_binarystring(s)
    assert (is_unicode(s_unicode))
    assert (not(is_binarystring(s_unicode)))
    assert (is_binarystring(s_binary))
    assert (not(is_unicode(s_binary)))


def test_generate_unique_set():
    names = set()
    n = generate_unique_name("test_%d", names)
    assert(n == "test_0")
    names.add(n)
    n = generate_unique_name("test_%d", names)
    assert(n == "test_1")


def test_hashable_dict():
    key_a = HashableDict({"a": 1, "b": "test"})
    key_b = HashableDict({"a": 1, "b": "test"})
    key_c = HashableDict({"a": "dog", "b": "boo"})
    d = dict()
    d[key_a] = 1
    assert(key_b in d)
    assert(key_c not in d)


def test_batch_process_list():
    # Let's sum the numbers from 1 to 100 in different batches
    l = list(range(1,101))
    f = lambda b, p: sum(b) + p
    s = sum(l)  # I know, it should be 5050 :)
    assert(batch_process_list(f, l, 200, 0) == s)
    assert(batch_process_list(f, l, 50, 0) == s)
    assert(batch_process_list(f, l, 10, 0) == s)
    assert(batch_process_list(f, l, 1, 0) == s)
