import sys
import argparse
import os
import http.cookiejar
import requests
from limedio import LimedioLibrary
import limedio
from limedio.cli import Authenticator, get_parser, parse_args_with_handler
from uecauth.shibboleth import ShibbolethAuthenticator
from uecauth.password import DefaultPasswordProvider
from uecauth.mfa import AutoTOTPMFAuthCodeProvider


class UECLibraryAuthenticator(Authenticator):
    def __init__(self) -> None:
        self.url = 'https://www.lib.uec.ac.jp/opac/user/top'

        # Shibboleth Login
        self.shibboleth_host = 'shibboleth.cc.uec.ac.jp'
        self.shibboleth = ShibbolethAuthenticator(
            shibboleth_host=self.shibboleth_host,
            mfa_code_provider=AutoTOTPMFAuthCodeProvider(os.environ['UEC_MFA_SECRET']),
            password_provider=DefaultPasswordProvider(
                os.environ['UEC_USERNAME'],
                os.environ['UEC_PASSWORD']
            ),
            debug=False,
        )

    def login(self) -> LimedioLibrary:
        return LimedioLibrary(
            'https://www.lib.uec.ac.jp',
            cookies=self.shibboleth.get_cookies()
        )

    def refresh(self) -> LimedioLibrary:
        print('refreshing...', file=sys.stderr)
        self.shibboleth.login(self.url)
        return LimedioLibrary(
            'https://www.lib.uec.ac.jp',
            cookies=self.shibboleth.get_cookies()
        )


if __name__ == '__main__':
    parser = get_parser(authenticator=UECLibraryAuthenticator())
    parse_args_with_handler(parser)
