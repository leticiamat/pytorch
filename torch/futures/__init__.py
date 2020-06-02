"""
The ``torch.futures`` package contains a ``Future`` type and corresponding
utility functions.
"""
import torch


class Future(torch._C.Future):
    r"""
    Wrapper around a ``torch._C.Future`` which encapsulates an asynchronous
    execution of a callable, e.g. :meth:`~torch.distributed.rpc.rpc_async`.
    """
    def __new__(cls):
        return super(Future, cls).__new__(cls)

    def wait(self):
        r"""
        Block until the value of this ``Future`` is ready.

        Return:
            The value held by this ``Future``. If the function (callback or RPC)
            creating the value thrown an error, this ``wait`` method will also
            throw the error.
        """
        return super(Future, self).wait()

    def then(self, callback):
        r"""
        Append the given callback function to this ``Future``, which will be run
        when the ``Future`` is completed.  Multiple callbacks can be added to
        the same ``Future``, and will be invoked in the same order as they were
        added. The callback must take one argument, which is the reference to
        this ``Future``. The callback function can use the ``Future.wait()`` API
        to get the value.

        Argument:
            callback(``Callable``): a ``Callable`` that takes this ``Future`` as
                                    the only argument.

        Return:
            A new ``Future`` object that holds the return value of the
            ``callback`` and will be marked as completed when the given
            ``callback`` finishes.

        Example::
            >>> import torch
            >>>
            >>> def callback(fut):
            >>>     print(f"RPC return value is {fut.wait()}.")
            >>>
            >>> fut = torch.futures.Future()
            >>> # The inserted callback will print the return value when
            >>> # receiving the response from "worker1"
            >>> cb_fut = fut.then(callback)
            >>> chain_cb_fut = cb_fut.then(lambda x : print(f"Chained cb done. {x.wait()}"))
            >>> fut.set_result(5)
            >>>
            >>> # Outputs are:
            >>> # RPC return value is 5.
            >>> # Chained cb done. None
        """
        return super(Future, self).then(callback)

    def set_result(self, result):
        r"""
        Set the result for this ``Future``, which will mark this ``Future`` as
        completed and trigger all attached callbacks. Note that a ``Future``
        cannot be marked completed twice.

        Arguments:
            result (object): the result object of this ``Future``.

        Example::
            >>> import threading
            >>> import time
            >>> import torch
            >>>
            >>> def slow_set_future(fut, value):
            >>>     time.sleep(0.5)
            >>>     fut.set_result(value)
            >>>
            >>> fut = torch.futures.Future()
            >>> t = threading.Thread(
            >>>     target=slow_set_future,
            >>>     args=(fut, torch.ones(2) * 3)
            >>> )
            >>> t.start()
            >>>
            >>> print(fut.wait())  # tensor([3., 3.])
            >>> t.join()
        """
        super(Future, self).set_result(result)
