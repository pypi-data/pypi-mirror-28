#! /usr/bin/env python
# -*- coding: utf-8 -*-
# >>
#   Copyright 2018 Vivint, inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#    vivint-selenium-docker, 20017
# <<

from aenum import auto
from selenium.webdriver import DesiredCapabilities, FirefoxProfile

from selenium_docker.drivers import DockerDriverBase, VideoDriver
from selenium_docker.helpers import JsonFlags

__all__ = [
    'Flags',
    'FirefoxDriver',
    'FirefoxVideoDriver'
]


class Flags(JsonFlags):
    DISABLED    = 0
    X_IMG       = auto()
    X_FLASH     = auto()
    ALL         = ~DISABLED


class FirefoxDriver(DockerDriverBase):
    """ Firefox browser inside Docker.

    Inherits from :obj:`~selenium_docker.drivers.DockerDriverBase`.
    """

    BROWSER = 'Firefox'
    CONTAINER = dict(
        image='selenium/standalone-firefox',
        detach=True,
        labels={'role': 'browser',
                'dynamic': 'true',
                'browser': 'firefox',
                'hub': 'false'},
        mem_limit='512mb',
        volumes=['/dev/shm:/dev/shm'],
        ports={DockerDriverBase.SELENIUM_PORT: None},
        publish_all_ports=True)
    DEFAULT_ARGUMENTS = [
        ('browser.startup.homepage', 'about:blank')
    ]

    Flags = Flags

    def _capabilities(self, arguments, extensions, proxy, user_agent):
        """ Compile the capabilities of FirefoxDriver inside the Container.

        Args:
            arguments (list): unused.
            extensions (list): unused.
            proxy (Proxy): adds proxy instance to DesiredCapabilities.
            user_agent (str): unused.

        Returns:
            dict
        """
        self.logger.debug('building capabilities')
        c = DesiredCapabilities.FIREFOX.copy()
        if proxy:
            proxy.add_to_capabilities(c)
        return c

    def _profile(self, arguments, extensions, proxy, user_agent):
        """ Compile the capabilities of ChromeDriver inside the Container.

        Args:
            arguments (list):
            extensions (list):
            proxy (Proxy): unused.
            user_agent (str):

        Returns:
            FirefoxProfile
        """
        self.logger.debug('building browser profile')
        profile = FirefoxProfile()
        args = list(self.DEFAULT_ARGUMENTS)

        if self.f(Flags.X_IMG):
            args.append(
                ('permissions.default.image', '2'))

        if self.f(Flags.X_FLASH):
            args.append(
                ('dom.ipc.plugins.enabled.libflashplayer.so', 'false'))

        for ext in extensions:
            profile.add_extension(ext)

        args.extend(arguments)
        for arg_k, value in args:
            profile.set_preference(arg_k, value)
        if user_agent:
            profile.set_preference('general.useragent.override', user_agent)
        return profile

    def _final(self, arguments, extensions, proxy, user_agent):
        """ Configuration applied after the driver has been created.

        Args:
            arguments (list): unused.
            extensions (list): unused.
            proxy (Proxy): adds proxy instance to DesiredCapabilities.
            user_agent (str): unused.

        Returns:
            None
        """
        self.logger.debug('applying final configuration')
        return None


class FirefoxVideoDriver(VideoDriver, FirefoxDriver):
    """ Firefox browser inside Docker with video recording.

    Inherits from :obj:`~selenium_docker.drivers.VideoDriver`.
    """
    CONTAINER = dict(
        image='standalone-firefox-ffmpeg',
        detach=True,
        labels={'role': 'browser',
                'dynamic': 'true',
                'browser': 'firefox',
                'hub': 'false'},
        mem_limit='768mb',
        volumes=['/dev/shm:/dev/shm'],
        ports={DockerDriverBase.SELENIUM_PORT: None},
        publish_all_ports=True)
