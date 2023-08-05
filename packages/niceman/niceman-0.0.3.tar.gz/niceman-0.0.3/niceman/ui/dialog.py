# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the NICEMAN package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Basic dialog-like interface for interactions in the terminal window

"""

__docformat__ = 'restructuredtext'

from logging import getLogger
lgr = getLogger('niceman.ui.dialog')

lgr.log(5, "Starting importing ui.dialog")

import os
import sys
import time

from six import PY2
import getpass

#!!! OPT adds >100ms to import time!!!
# from mock import patch
from collections import deque
from copy import copy

from ..utils import auto_repr
from ..utils import on_windows
from .base import InteractiveUI
from ..support.exceptions import MissingConfigError

# Example APIs which might be useful to look for "inspiration"
#  man debconf-devel
#  man zenity
#
# "Fancy" output of progress etc in the terminal:
# - docker has multiple simultaneous progressbars.  Apparently "navigation"
#   is obtained with escape characters in the terminal.
#   see docker/pkg/jsonmessage/jsonmessage.go or following snippet
"""
from time import sleep
import sys

out = sys.stderr
for i in range(10):
  diff = 2
  if i:
      out.write("%c[%dA" % (27, diff))
  out.write("%d\n%d\n" % (i, i ** 2))
  sleep(0.5)
"""
# They also use JSON representation for the message which might provide a nice abstraction
# Other useful codes
#         // <ESC>[2K = erase entire current line
#        fmt.Fprintf(out, "%c[2K\r", 27)
# and code in docker: pkg/progressreader/progressreader.go pkg/streamformatter/streamformatter.go
#
# reference for ESC codes: http://ascii-table.com/ansi-escape-sequences.php



@auto_repr
class ConsoleLog(object):

    progressbars = None

    def __init__(self, out=sys.stdout):
        self.out = out

    def message(self, msg, cr='\n'):
        self.out.write(msg)
        if cr:
            self.out.write(cr)

    def error(self, error):
        self.out.write("ERROR: %s\n" % error)

    def get_progressbar(self, *args, **kwargs):
        """Return a progressbar.  See e.g. `tqdmProgressBar` about the interface

        Additional parameter is backend to choose among available
        """
        backend = kwargs.pop('backend', None)
        # Delay imports of progressbars until actually needed
        if ConsoleLog.progressbars is None:
            from .progressbars import progressbars
            ConsoleLog.progressbars = progressbars
        else:
            progressbars = ConsoleLog.progressbars

        if backend is None:
            try:
                pbar = progressbars['tqdm']
            except KeyError:
                pbar = progressbars.values()[0]  # any
        else:
            pbar = progressbars[backend]
        return pbar(*args, out=self.out, **kwargs)


def getpass_echo(prompt='Password: ', stream=None):
    """Q&D workaround until we have proper 'centralized' UI -- just use getpass BUT enable echo
    """
    if on_windows:
        # Can't do anything fancy yet, so just ask the one without echo
        return getpass.getpass(prompt=prompt, stream=stream)
    else:
        # We can mock patch termios so that ECHO is not turned OFF.
        # Side-effect -- additional empty line is printed

        # def _no_emptyline_write(out):
        #     # Additional mock to prevent not needed empty line print since we do have echo
        #     # doesn't work since we don't know the stream here really
        #     if out == '\n':
        #         return
        #     stream.write(out)
        from mock import patch
        with patch('termios.ECHO', 255**2):
            #patch.object(stream, 'write', _no_emptyline_write(stream)):
            return getpass.getpass(prompt=prompt, stream=stream)


@auto_repr
class DialogUI(ConsoleLog, InteractiveUI):

    def __init__(self, *args, **kwargs):
        super(DialogUI, self).__init__(*args, **kwargs)
        # ATM doesn't make sense to print the same title for subsequent questions
        # so we will store previous one and not show it if was the previous one shown
        # within 5 seconds from prev question
        self._prev_title = None
        self._prev_title_time = 0

    def question(self, text,
                 title=None, choices=None,
                 default=None,
                 error_message=None,
                 hidden=False):
        # Do initial checks first
        if default and choices and default not in choices:
            raise ValueError("default value %r is not among choices: %s"
                             % (default, choices))

        msg = ''
        if title and not (title == self._prev_title and time.time() - self._prev_title_time < 5):
            # might not actually get displayed if all in/out redirected
            # self.out.write(title + "\n")
            # so merge into msg for getpass
            msg += title + os.linesep

        def mark_default(x):
            return "[%s]" % x \
                if default is not None and x == default \
                else x

        if choices is not None:
            msg += "%s (choices: %s)" % (text, ', '.join(map(mark_default, choices)))
        else:
            msg += text
            if default:
                msg += ' ' + mark_default(default)
        """
        Anaconda format:

Question? [choice1|choice2]
[default] >>> yes
        """
        attempt = 0
        while True:
            attempt += 1
            if attempt >= 100:
                raise RuntimeError("This is 100th attempt. Something really went wrong")
            # if not hidden:
            #     self.out.write(msg + ": ")
            #     self.out.flush()  # not effective for stderr for some reason under annex
            #
            #     # TODO: raw_input works only if stdin was not controlled by
            #     # (e.g. if coming from annex).  So we might need to do the
            #     # same trick as get_pass() does while directly dealing with /dev/pty
            #     # and provide per-OS handling with stdin being override
            #     response = (raw_input if PY2 else input)()
            # else:
            response = (getpass.getpass if hidden else getpass_echo)(msg + ": ")

            if not response:
                if default:
                    response = default
                    break
                elif error_message:
                    raise MissingConfigError(error_message)

            if choices and response not in choices:
                self.error("%r is not among choices: %s. Repeat your answer"
                           % (response, choices))
                continue
            break

        self._prev_title = title
        self._prev_title_time = time.time()

        return response


# poor man thingie for now
@auto_repr
class UnderAnnexUI(DialogUI):
    def __init__(self, **kwargs):
        if 'out' not in kwargs:
            # to avoid buffering
            # http://stackoverflow.com/a/181654/1265472
            #kwargs['out'] = os.fdopen(sys.stderr.fileno(), 'w', 0)
            # but wasn't effective! sp kist straogjt for now
            kwargs['out'] = sys.stderr
        super(UnderAnnexUI, self).__init__(**kwargs)


@auto_repr
class UnderTestsUI(DialogUI):
    """UI to help with testing functionality requiring interaction

    It will provide additional method to push responses to be provided,
    and could be used as a context manager
    """

    def __init__(self, **kwargs):
        super(UnderTestsUI, self).__init__(**kwargs)
        self._responses = deque()

    # TODO: possibly allow to provide expected messages etc, so we could
    # test that those are the actual ones which were given
    def add_responses(self, responses):
        if not isinstance(responses, (list, tuple)):
            responses = [responses]
        self._responses += list(responses)
        return self  # so we could use it as a context manager

    def get_responses(self):
        return self._responses

    def clear_responses(self):
        self._responses = deque()

    def question(self, *args, **kwargs):
        if not self._responses:
            raise AssertionError(
                "We are asked for a response whenever none is left to give"
            )
        return self._responses.popleft()

    # Context manager mode of operation which would also verify that
    # no responses left upon exiting
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        responses = copy(self._responses)
        # we should clear the state so there is no side-effect
        self.clear_responses()
        assert not len(responses), \
            "Still have some responses left: %s" % repr(self._responses)

lgr.log(5, "Done importing ui.dialog")
