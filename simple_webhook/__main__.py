from dynatrace_extension import Extension, Status, StatusValue

from .listener import Server
from .utils import port_available

DEFAULT_PORT = 9000


class ExtensionImpl(Extension):

    def initialize(self):
        self.logger.setLevel("INFO")
        self.logger.info(
            "Initializing extension %s version %s",
            self.extension_name, self.activation_config.version,
        )

        port = self.activation_config.get("port", DEFAULT_PORT)
        self.server = Server(port)
        self.server.start()
        self.logger.info("Listener started on port %s", port)

    def fastcheck(self) -> Status:
        port = self.activation_config.get("port", DEFAULT_PORT)
        if not port_available(port):
            return Status(StatusValue.INVALID_CONFIG_ERROR, f"Port {port} is already in use")

        return Status(StatusValue.OK)


def main():
    ExtensionImpl(name="simple_webhook").run()


if __name__ == "__main__":
    main()
