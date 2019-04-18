class LoginInfoModel:
    def __init__(self, host, port, session_key):
        self.__host = host
        self.__port = port
        self.__session_key = session_key

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def session_key(self):
        return self.__session_key
