import sys
import threading


def _make_id(target):
    if hasattr(target, '__func__'):
        return (id(target.__self__), id(target.__func__))
    return id(target)

NONE_ID = _make_id(None)


class Signal(object):
    """
    Base class for all signals

    Internal attributes:

        receivers
            { receiverkey(id): receiver }
    """
    def __init__(self):
        self.receivers = []
        self.lock = threading.Lock()

    def connect(self, receiver, sender=None, dispatch_uid=None):
        """
        Connect receiver to sender for signal.

        Arguments:

            receiver
                A function or an instance method which is to recieve signals.

            sender
                The sender to which the receiver should respond. Must be None to recieve events
                from any sender.

            dispatch_uid
                An identifier used to uniquely identify a particular instance of a receiver. This
                will usually be a string, though it may be anything hashable.

        """
        if dispatch_uid:
            lookup_key = (dispatch_uid, _make_id(sender))
        else:
            lookup_key = (_make_id(receiver), _make_id(sender))

        with self.lock:
            for r_key, _ in self.receivers:
                if r_key == lookup_key:
                    break
            else:
                self.receivers.append((lookup_key, receiver))

    def disconnect(self, receiver=None, sender=None, dispatch_uid=None):
        """
        Disconnect receiver from sender for signal.

        Arguments:

            receiver
                The registered receiver to disconnect. May be none if
                dispatch_uid is specified.

            sender
                The registered sender to disconnect

            dispatch_uid
                the unique identifier of the receiver to disconnect
        """
        if dispatch_uid:
            lookup_key = (dispatch_uid, _make_id(sender))
        else:
            lookup_key = (_make_id(receiver), _make_id(sender))

        with self.lock:
            for index in range(len(self.receivers)):
                (r_key, _) = self.receivers[index]
                if r_key == lookup_key:
                    del self.receivers[index]
                    break

    def has_listeners(self, sender=None):
        return bool(self._receivers(sender))

    def send(self, sender, **named):
        """
        Send signal from sender to all connected receivers.

        If any receiver raises an error, the error propagates back through send,
        terminating the dispatch loop, so it is quite possible to not have all
        receivers called if a raises an error.

        Arguments:

            sender
                The sender of the signal Either a specific object or None.

            named
                Named arguments which will be passed to receivers.

        Returns a list of tuple pairs [(receiver, response), ... ].
        """
        responses = []
        for receiver in self._receivers(sender):
            response = receiver(signal=self, sender=sender, **named)
            responses.append((receiver, response))
        return responses

    def send_robust(self, sender, **named):
        """
        Send signal from sender to all connected receivers catching errors.

        Arguments:

            sender
                The sender of the signal. Can be any python object (normally one
                registered with a connect if you actually want something to
                occur).

            named
                Named arguments which will be passed to receivers. These
                arguments must be a subset of the argument names defined in
                providing_args.

        Return a list of tuple pairs [(receiver, response), ... ].

        If any receiver raises an error (specifically any subclass of
        Exception), the error instance is returned as the result for that
        receiver. The traceback is always attached to the error at
        ``__traceback__``.
        """
        responses = []

        # Call each receiver with whatever arguments it can accept.
        # Return a list of tuple pairs [(receiver, response), ... ].
        for receiver in self._receivers(sender):
            try:
                response = receiver(signal=self, sender=sender, **named)
            except Exception as err:
                if not hasattr(err, '__traceback__'):
                    err.__traceback__ = sys.exc_info()[2]
                responses.append((receiver, err))
            else:
                responses.append((receiver, response))
        return responses

    def _receivers(self, sender):
        """
        Filter sequence of receivers to get receivers for sender.
        """
        with self.lock:
            senderkey = _make_id(sender)
            receivers = []
            for (_, r_senderkey), receiver in self.receivers:
                if r_senderkey == NONE_ID or r_senderkey == senderkey:
                    receivers.append(receiver)
        return receivers


def receiver(signal, **kwargs):
    """
    A decorator for connecting receivers to signals. Used by passing in the
    signal (or list of signals) and keyword arguments to connect::

        @receiver(goal_achieved)
        def signal_receiver(sender, **kwargs):
            ...

        @receiver([goal_achieved, level_increased], sender=tracker)
        def signals_receiver(sender, **kwargs):
            ...

    """
    def _decorator(func):
        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(func, **kwargs)
        else:
            signal.connect(func, **kwargs)
        return func
    return _decorator


goal_achieved = Signal()
level_increased = Signal()
highest_level_achieved = Signal()
