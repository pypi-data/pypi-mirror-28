# -*- coding: utf-8 -*-
#
# Copyright 2010-2018 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2010-2018 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

import io
import sys, os
import locale # required to encode file paths
import binascii

import py, pytest

import ghostscript as gslib


postscript_img = b"""
    /Helvetica findfont 12 scalefont setfont
    0 0 moveto
    (Hello World) show
    showpage
    """

HELLO_WORLD = ''.join(('%x' % ord(c) for c in 'Hello World'))
postscript_doc = ('<%s> = flush' % HELLO_WORLD).encode('ascii')

STDARGS = [b'test.py', b'-dNOPAUSE', b'-dBATCH', b'-dSAFER', b'-q',
           b'-sDEVICE=bmp16', b'-g80x12']

TEST_PIC_FILENAME = os.path.join(os.path.dirname(__file__), 'hello_world.bmp')
TEST_PIC_DATA = py.path.local(TEST_PIC_FILENAME).read('rb')

def _encode(*args):
    encoding = locale.getpreferredencoding()
    return [a.encode(encoding) for a in args]


# Ensure the instanse is removed after all high-level tests have been
# done. Otherwise low-level tests will fail if run afterwards.
@pytest.fixture(scope='module')
def instance(request):
    def fin():
        gslib.cleanup()
    request.addfinalizer(fin)

def test_revision_func(instance):
    rev = gslib.revision()
    assert type(rev) is dict
    assert type(rev['copyright']) is bytes
    assert type(rev['product']) is bytes
    assert type(rev['revision']) is int
    assert type(rev['revisiondate']) is int
    assert 'Copyright' in str(rev['copyright'])
    assert 'ghostscript' in str(rev['product']).lower()
    assert rev['revisiondate'] > 19900101
    assert rev['revision'] > 700


def test_revision_instance(instance):
    with gslib.Ghostscript( b'-dBATCH', b'-q') as gs:
        rev1 = gs.revision()
    rev2 = gslib.revision()
    assert rev1 == rev2


def test_simple(instance, tmpdir):
    """Let ghostscript read from a file and write to a file"""
    infile = tmpdir.join('in.ps')
    infile.write(postscript_img)
    outfile = tmpdir.join('out.bmp')

    args = STDARGS + _encode('-sOutputFile=%s' % outfile, str(infile))

    # Using a context with an empty body looks not like good code, So
    # do not use a ``with``-stmt.
    gs = gslib.Ghostscript(*args)
    gs.exit()

    data = outfile.read('rb')
    assert data == TEST_PIC_DATA


def test_run_string_empty(instance, tmpdir):
    """Let ghostscript read from a file and write to a file"""
    infile = tmpdir.join('in.ps')
    infile.write(postscript_img)
    outfile = tmpdir.join('out.bmp')

    args = STDARGS + _encode('-sOutputFile=%s' % outfile)

    with gslib.Ghostscript(*args) as gs:
        gs.run_string(b'')

    # It depends on the ghostscript implementation, whether the file
    # if created. As of gs 9.14 the file is not created, but this
    # could change.
    if outfile.exists():
        # But if the file exists, it must be empty
        data = outfile.read('rb')
        assert data == ''


def test_run_string(instance, tmpdir):
    """Let ghostscript read from a file and write to a file"""
    infile = tmpdir.join('in.ps')
    infile.write(postscript_img)
    outfile = tmpdir.join('out.bmp')

    args = STDARGS + _encode('-sOutputFile=%s' % outfile)

    with gslib.Ghostscript(*args) as gs:
        gs.run_string(postscript_img)

    data = outfile.read('rb')
    assert data == TEST_PIC_DATA


def test_stdin(tmpdir):
    """Let ghostscript read from stdin and write to a file"""
    outfile = tmpdir.join('out.bmp')
    args = STDARGS + _encode('-sOutputFile=%s' % outfile, '-')

    gs = gslib.Ghostscript(*args, stdin=io.BytesIO(postscript_img))
    gs.exit()

    data = outfile.read('rb')
    assert data == TEST_PIC_DATA


def test_stdout(tmpdir):
    """Let ghostscript read from a file and write to stdout"""
    infile = tmpdir.join('in.ps')
    infile.write(postscript_doc)

    args = STDARGS + _encode(str(infile))
    stdout = io.BytesIO() # buffer for collecting the output

    gs = gslib.Ghostscript(*args, stdout=stdout)
    gs.exit()

    data = stdout.getvalue()
    assert data == b'Hello World\n'


def test_stdin_stdout(tmpdir):
    """Let ghostscript read from stdin and write to stdout"""
    args = STDARGS + _encode('-')

    stdout = io.BytesIO() # buffer for collecting the output

    gs = gslib.Ghostscript(*args,
                           stdin=io.BytesIO(postscript_doc),
                           stdout=stdout)
    gs.exit()

    data = stdout.getvalue()
    assert data == b'Hello World\n'


def test_stderr(tmpdir):
    """
    Make ghostscript write some error message to stderr and
    keep stdout on the console.
    """
    args = STDARGS + _encode('-')

    stderr = io.BytesIO() # buffer for collecting stderr

    try:
        with gslib.Ghostscript(*args,
                               stdin=io.BytesIO(b'foobar'),
                               stderr=stderr):
            # this call is expected to fail due to the intented error in
            # the postscript code
            pass
    except gslib.GhostscriptError:
        pass

    data = stderr.getvalue()
    assert b'Unrecoverable error' in data


def test_stdout_stderr(tmpdir):
    """
    Make ghostscript write some error message to stderr and
    catch stdout, too.
    """
    args = STDARGS + _encode('-')

    stdout = io.BytesIO() # buffer for collecting the output
    stderr = io.BytesIO() # buffer for collecting stderr

    try:
        with gslib.Ghostscript(*args,
                               stdin=io.BytesIO(b'foobar'),
                               stdout=stdout, stderr=stderr):
            # this call is expected to fail due to the intented error in
            # the postscript code
            pass
    except gslib.GhostscriptError:
        pass

    data = stdout.getvalue()
    assert b'Error: /undefined in foobar' in data

    data = stderr.getvalue()
    assert b'Unrecoverable error' in data
