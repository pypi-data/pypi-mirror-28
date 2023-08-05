"""
Send a message by invoking 'sendmail' program

Provides smtplib compatible API for sending Internet mail messages.
Compatible with 'sendmail' and 'postfix' MTAs.
"""

__author__ = 'Phil Budne <phil@ultimate.com>'
__version__ = '1.0'
__revision__ = '$Id: sendmail.py,v 1.6 2018/01/11 16:50:22 phil Exp $'

#       Copyright (c) 2009,2018 Philip Budne (phil@ultimate.com)
#       Licensed under the MIT licence: 
#       
#       Permission is hereby granted, free of charge, to any person
#       obtaining a copy of this software and associated documentation
#       files (the "Software"), to deal in the Software without
#       restriction, including without limitation the rights to use,
#       copy, modify, merge, publish, distribute, sublicense, and/or sell
#       copies of the Software, and to permit persons to whom the
#       Software is furnished to do so, subject to the following
#       conditions:
#       
#       The above copyright notice and this permission notice shall be
#       included in all copies or substantial portions of the Software.
#       
#       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#       EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#       OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#       NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#       HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#       WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#       FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#       OTHER DEALINGS IN THE SOFTWARE.

import subprocess
import smtplib                  # for exceptions
import os

OS_OK = getattr(os, 'OS_OK', 0)

class Sendmail(object):
    """smtplib compatible object for queuing e-mail messages
       using local sendmail program"""

    # take as initializer arg? search for it?
    SENDMAIL = '/usr/sbin/sendmail'
    debug = False

    def set_debuglevel(self, debug):
        """enable debug output"""
        self.debug = debug

    def sendmail(self, from_addr, to_addrs, msg, mail_options=()):
        """invoke sendmail program to send a message.
        `from_addr' is envelope sender string (may be empty)
        `to_addrs' is list of envelope recipient addresses
                   string will be treated as a list with 1 address.
        `msg' is headers and body of message to be sent
        `mail_options' is list of options ('8bitmime')"""

        cmd = [self.SENDMAIL]
        if from_addr:
            cmd.append('-f%s' % from_addr)
        if isinstance(to_addrs, basestring):
            to_addrs = [to_addrs]
        elif isinstance(to_addrs, tuple): # be liberal
            to_addrs = list(to_addrs)
        if '8bitmime' in mail_options:
            cmd.append('-B8BITMIME')
        # avoid shell / quoting issues
        proc = subprocess.Popen(cmd + to_addrs, shell=False,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.stdin.write(msg.replace('\n.\n', '\n..\n'))
        proc.stdin.close()
        ret = proc.wait()
        out = proc.stdout.readlines()
        err = proc.stderr.readlines()

        if self.debug:
            for line in out:
                print "stdout:", line
            for line in err:
                print "stderr:", line

        # complain if out or error are non-empty?
        if ret != OS_OK:
            raise smtplib.SMTPException()
        return {}

    def quit(self):
        """for SMTP compatibility"""
