import attr


@attr.s
class SshTarget:
    DefaultPort = 22

    host = attr.ib()
    user = attr.ib()
    port = attr.ib(default=DefaultPort)

    def __str__(self):
        host_and_port = self.host
        if self.port != self.DefaultPort:
            host_and_port = '{}:{}'.format(self.host, self.port)
        return '{}@{}'.format(self.user, host_and_port)
