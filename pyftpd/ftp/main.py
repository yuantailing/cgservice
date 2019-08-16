import logging
import logging.handlers
import OpenSSL
import os
import pwd
import requests
import settings

from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import AuthenticationFailed, DummyAuthorizer
from pyftpdlib.log import logger


class CgAuthorizer(DummyAuthorizer):
    def __init__(self, base_dir):
        super().__init__()
        self.base_dir = os.path.realpath(base_dir)

    def validate_authentication(self, username, password, handler):
        """Raises AuthenticationFailed if supplied username and
        password don't match the stored credentials, else return
        None.
        """
        res = requests.post(settings.CGSERVER_AUTH_URL, data={
            'username': username,
            'password': password,
            'peerip': handler.socket.getpeername()[0],
            'client_secret': settings.CLIENT_SECRET,
        })
        res.raise_for_status()
        data = res.json()
        if data['error']:
            if username == 'anonymous':
                msg = 'Anonymous access not allowed.'
            else:
                msg = 'Authentication failed.'
            raise AuthenticationFailed(msg)
        cgperms = data['perms']

        localuser = dict(
            home=os.path.normcase(self.base_dir),
            perm='',
            operms={},
            cgperms={},
            msg_login='Login successful.',
            msg_quit='Goodbye.'
        )
        for apath, perm in cgperms.items():
            allowed = os.path.normcase(os.path.realpath(os.path.join(self.base_dir, apath)))
            if self._issubpath(allowed, os.path.normcase(self.base_dir)):
                localuser['cgperms'][allowed] = perm

        self.user_table[username] = localuser

    def has_perm(self, username, perm, path=None):
        """Whether the user has permission over path (an absolute
        pathname of a file or a directory).

        Expected perm argument is one of the following letters:
        "elradfmwMT".
        """
        if path is None:
            return False
        path = os.path.normcase(path)
        flag = False
        for allowed, (cgperm, recursive) in self.user_table[username]['cgperms'].items():
            if recursive:
                if cgperm == 'r':
                    if path == allowed:
                        flag = flag or perm in 'el'
                    elif self._issubpath(path, allowed):
                        flag = flag or perm in 'elr'
                    elif self._issubpath(allowed, path):
                        flag = flag or perm in 'el'
                elif cgperm == 'w':
                    if path == allowed:
                        flag = flag or perm in 'eldfm'
                    elif self._issubpath(path, allowed):
                        flag = flag or perm in 'elradfmw'
                    elif self._issubpath(allowed, path):
                        flag = flag or perm in 'elm'
            else:
                if cgperm == 'r':
                    if path == allowed:
                        flag = flag or perm in 'r'
                    elif self._issubpath(allowed, path):
                        flag = flag or perm in 'el'
                elif cgperm == 'w':
                    if path == allowed:
                        flag = flag or perm in 'radw'
                    elif self._issubpath(allowed, path):
                        flag = flag or perm in 'elm'
        return flag

    def impersonate_user(self, username, password):
        """Change process effective user/group ids to reflect
        logged in user.
        """
        try:
            pwdstruct = pwd.getpwnam('ftp')
        except KeyError:
            raise AuthorizerError(self.msg_no_such_user)
        else:
            os.setegid(pwdstruct.pw_gid)
            os.seteuid(pwdstruct.pw_uid)


def get_cg_handler(Handler):
    class CgHandler(Handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for fact in ['unix.mode', 'unix.uid', 'unix.gid']:
                if fact in self._available_facts:
                    self._current_facts.append(fact)

        def ftp_OPTS(self, line):
            if line.upper() == 'UTF8 ON':
                self.respond('200 Always in UTF8 mode.')
                return
            return super().ftp_OPTS(line)

        def ftp_USER(self, line):
            if not isinstance(self.socket, OpenSSL.SSL.Connection):
                res = requests.post(settings.CGSERVER_INSECURE_CHECK_URL, data={
                    'username': line,
                    'peerip': self.socket.getpeername()[0],
                    'client_secret': settings.CLIENT_SECRET,
                })
                res.raise_for_status()
                data = res.json()
                if data['error'] != 0:
                    self.respond('530 FTPS (SSL/TLS) required for security reasons.', logfun=logger.info)
                    self.close_when_done()
                    return
            return super().ftp_USER(line)

    return CgHandler


if __name__ == '__main__':
    if settings.FTP_TLS_ENABLE:
        handler = get_cg_handler(TLS_FTPHandler)
        handler.certfile = settings.FTP_TLS_CERTFILE
        handler.keyfile = settings.FTP_TLS_KEYFILE
    else:
        handler = get_cg_handler(FTPHandler)
    handler.authorizer = CgAuthorizer(settings.FTP_ROOT)
    handler.use_gmt_times = True

    logging.basicConfig(level=logging.INFO, handlers=[
        logging.handlers.TimedRotatingFileHandler(settings.FTP_LOG_FILE_PATH, when='W0'),
        logging.StreamHandler()
    ])
    server = ThreadedFTPServer(('', settings.FTP_BIND_PORT), handler)
    server.serve_forever()
