"""Test kernel for signalling subprocesses"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

from subprocess import Popen, PIPE
import sys
import time

from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp


class SignalTestKernel(Kernel):
    """Kernel for testing subprocess signaling"""
    implementation = 'signaltest'
    implementation_version = '0.0'
    banner = ''
    
    def __init__(self, **kwargs):
        super(SignalTestKernel, self).__init__(**kwargs)
        self.children = []
        

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        code = code.strip()
        reply = {'status': 'ok'}
        if code == 'start':
            child = Popen(['bash', '-i', '-c', 'sleep 30'], stderr=PIPE)
            self.children.append(child)
            reply['pid'] = self.children[-1].pid
        elif code == 'check':
            reply['poll'] = [ child.poll() for child in self.children ]
        elif code == 'sleep':
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                reply['interrupted'] = True
            else:
                reply['interrupted'] = False
        else:
            reply['status'] = 'error'
            reply['ename'] = 'Error'
            reply['evalue'] = code
            reply['traceback'] = ['no such command: %s' % code]
        return reply

class SignalTestApp(IPKernelApp):
    kernel_class = SignalTestKernel
    def init_io(self):
        pass # disable stdout/stderr capture
    
if __name__ == '__main__':
    SignalTestApp.launch_instance()
