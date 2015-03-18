import threading

from tulip.futures import Future
from tulip import set_event_loop
from guievents import GuiEventLoop

class TkEventLoop(GuiEventLoop):
    _default_executor = None

    def __init__(self, app):
        super().__init__()
        self.app = app

    def mainloop(self):
        set_event_loop(self)
        try:
            self.run_forever()
        finally:
            set_event_loop(None)

    # Event Loop API
    def run(self):
        """Run the event loop.  Block until there is nothing left to do."""
        self.app.mainloop()

    def run_forever(self):
        """Run the event loop.  Block until stop() is called."""
        self.app.mainloop()

    def run_once(self, timeout=None):  # NEW!
        """Run one complete cycle of the event loop."""
        self.app.update()

    def stop(self):  # NEW!
        """Stop the event loop as soon as reasonable.

        Exactly how soon that is may depend on the implementation, but
        no more I/O callbacks should be scheduled.
        """
        super().stop()
        self.app.quit()

    def call_later(self, delay, callback, *args):
        res = self.app.after(int(delay*1000), 
                             lambda cb, a : cb(*a), 
                             callback, 
                             args)
        return _CancelJob(self, res)



class _CancelJob(object):
    """Object that allows cancelling of a call_later"""

    def __init__(self, event_loop, after_id):
        self.event_loop = event_loop
        self.after_id = after_id

    def cancel(self):
        self.event_loop.app.after_cancel(self.after_id)

