import aiohttp
import asyncio
import re

from urllib.parse import quote

class Xeoma():
    def __init__(self, base_url, new_version, login=None, password=None):
        """
            Create a Xeoma Object for interacting with Xeoma web server

            Arguments:
                base_url: the url of the Xeoma web server
                new_version: True if the Xeoma version > 17.5
                login: the Xeoma web server username
                password: the Xeoma web server password
        """

        if base_url[-1] == '/':
            self._base_url = base_url[:-1]
        else:
            self._base_url = base_url
        self._login = login
        self._password = password
        self._cookie = None
        self._new_version = new_version

    @asyncio.coroutine
    def async_test_connection(self):
        try:
            with aiohttp.ClientSession() as session:
                resp = yield from session.get(self._base_url, timeout=5)
                assert resp.status == 200
        except asyncio.TimeoutError:
            raise XeomaError('Connection to Xeoma server timed out')
        except AssertionError:
            raise XeomaError('Received bad response from Xeoma server')

    @asyncio.coroutine
    def async_get_camera_image(self, image_name):
        """
            Grab a single image from the Xeoma web server

            Arguments:
                image_name: the name of the image to fetch (i.e. image01)
        """

        if self._cookie is None:
            self._cookie = yield from self.get_session_cookie()
        try:
            data = yield from self.async_fetch_image_data(image_name)
            if data is None:
                self._cookie = yield from self.get_session_cookie()
                data = yield from self.async_fetch_image_data(image_name)
                if data is None:
                    raise XeomaError('Unable to authenticate with Xeoma web '
                                     'server')
            return data
        except asyncio.TimeoutError:
            raise XeomaError('Connection timeout while fetching camera image.')
        except aiohttp.ClientError as e:
            raise XeomaError('Unable to fetch image: {}'.format(e))

    @asyncio.coroutine
    def async_fetch_image_data(self, image_name):
        """
            Fetch image data from the Xeoma web server

            Arguments:
                image_name: the name of the image to fetch (i.e. image01)
        """
        params = {}
        if not self._new_version:
            params['login'] = ''
        with aiohttp.ClientSession(cookies=self._cookie) as session:
            resp = yield from session.get(
                '{}/{}.jpg'.format(self._base_url, image_name),
                params=params
            )
            if resp.headers['Content-Type'] == 'image/jpeg':
                data = yield from resp.read()
            else:
                data = None
        return data

    @asyncio.coroutine
    def async_get_image_names(self):
        """
            Parse web server camera view for camera image names
        """

        self._cookie = yield from self.get_session_cookie()
        params = {}
        try:
            with aiohttp.ClientSession(cookies=self._cookie) as session:
                resp = yield from session.get(
                    self._base_url,
                    params=params
                )
                t = yield from resp.text()
                match = re.findall('(?:\w|\d)/(.*?).(?:mjpg|jpg)', t)
                if len(match) == 0:
                    raise XeomaError('Unable to find any camera image names')
                return set(match)
        except asyncio.TimeoutError as e:
            raise XeomaError("Unable to connect to Xeoma web server")

    @asyncio.coroutine
    def async_get_session_key(self):
        """
            Retrieve the Xeoma web server sessionkey
        """

        try:
            with aiohttp.ClientSession() as session:
                params = {'getsessionkey': ' '}
                if self._login is not None:
                    params['login'] = self._login
                if self._password is not None:
                    params['password'] = self._password

                resp = yield from session.get(
                    self._base_url,
                    params=params,
                    allow_redirects=False
                )
                t = yield from resp.text()
                match = re.search('\'sessionkey\', "(.*)"', t)
                if match:
                    session_key = match.group(1)
                    return session_key
                else:
                    return None
        except asyncio.TimeoutError:
            raise XeomaError('Connection timeout while fetching session key.')
        except aiohttp.ClientError as e:
            raise XeomaError('Unable to obtain session key: {}.'.format(e))

    @asyncio.coroutine
    def get_session_cookie(self):
        """
            Create a session cookie object for use by aiohttp
        """

        cookies = {}
        if self._login is not None and self._password is not None:
            session_key = yield from self.async_get_session_key()
            if session_key is None:
                raise XeomaError('Unable to obtain session key.')
            cookies['sessionkey'] = quote(session_key)
        return cookies

class XeomaError(Exception):
    def __init__(self, message):
        self.message = message
