"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__ will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time

LABEL = "AIS2"

class PduStats(gr.sync_block):
    """
    Count PDUs and report CRC OK FPS
    """
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='PDU Stats',
            in_sig=None,
            out_sig=[np.float32]
        )
        self._count = 0
        self._total = 0
        self._rate = 0.0
        self._t0 = time.time()
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self._handle_msg)

    def _handle_msg(self, msg):
        self._count += 1
        self._total += 1

    def work(self, input_items, output_items):
        now = time.time()
        dt = now - self._t0
        if dt >= 1.0:
            if dt > 0:
                self._rate = self._count / dt
            else:
                self._rate = 0.0
            print(f"[{LABEL}] CRC_OK_FPS={self._rate:.2f} TOTAL={self._total}")
            self._count = 0
            self._t0 = now
        output_items[0][:] = self._rate
        return len(output_items[0])
