class NotAnAdmin(Exception):
    def __init__(self, message="Missing administrator privileges!"):
        self.message = message
        super().__init__(self.message)


class NoAvailableServers(Exception):
    def __init__(self, message="Could not find any available servers!"):
        self.message = message
        super().__init__(self.message)


class NoServersInCountry(Exception):
    def __init__(self, country):
        self.message = f"Could not find any available servers for country [{country}]!"
        super().__init__(self.message)


class InvalidCountryName(Exception):
    def __init__(self, country):
        self.message = f"Country name [{country}] is invalid!"
        super().__init__(self.message)



