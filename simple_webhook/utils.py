import socket
from contextlib import closing


def port_available(port: int) -> bool:
    """Check whether `port` can be bound on all interfaces.

    Mirrors the bind performed by `listener.Server` (host "0.0.0.0") so that
    fastcheck and the actual server agree on what "available" means.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False
