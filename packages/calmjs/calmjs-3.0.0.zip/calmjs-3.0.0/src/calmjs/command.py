# -*- coding: utf-8 -*-
"""
Module for providing various distutil command that integrates with
setuptools, and for setting up the build environments and building
JavaScript artifacts.
"""

from __future__ import absolute_import

import sys
import logging

# from distutils.errors import DistutilsOptionError
from distutils.core import Command
from distutils import log

from calmjs.ui import prompt_overwrite_json
from calmjs.registry import get


class DistutilsLogHandler(logging.Handler):
    """
    A handler that streams the logs to the distutils logger.
    """

    def __init__(self, distutils_log=log):
        logging.Handler.__init__(self)
        self.log = distutils_log
        # Basic numeric table
        self.level_table = {
            logging.CRITICAL: distutils_log.FATAL,
            logging.ERROR: distutils_log.ERROR,
            logging.WARNING: distutils_log.WARN,
            logging.INFO: distutils_log.INFO,
            logging.DEBUG: distutils_log.DEBUG,
        }
        self.setFormatter(logging.Formatter('%(message)s'))

    def _to_distutils_level(self, level):
        return self.level_table.get(level, level // 10)

    def emit(self, record):
        level = self._to_distutils_level(record.levelno)
        try:
            msg = self.format(record)
            self.log.log(level, msg)
        except Exception:
            # LogRecord.__str__ shouldn't fail... probably.
            self.log.warn('Failed to convert %s' % record)


distutils_log_handler = DistutilsLogHandler()


def use_distutils_logger(logger_ids=('calmjs',)):
    def decorator(method):
        def run(cmd):
            root_logger = logging.getLogger()
            old_level = root_logger.level
            root_logger.setLevel(logging.DEBUG)

            for logger_id in logger_ids:
                logger = logging.getLogger(logger_id)
                logger.addHandler(distutils_log_handler)

            try:
                method(cmd)
            finally:
                # Remove the logging handlers and restore the level.
                for logger_id in logger_ids:
                    logger = logging.getLogger(logger_id)
                    logger.removeHandler(distutils_log_handler)

                root_logger.setLevel(old_level)

        return run
    return decorator


class PackageManagerCommand(Command):
    """
    Simple compatibility hook for a package manager runtime.
    """

    # subclasses need to define these
    runtime = None
    # description = "base command for package manager compatibility helper"

    indent = 4

    @classmethod
    def _initialize_user_options(cls):
        cls.user_options = []
        for full, short, desc in cls.runtime.pkg_manager_options:
            if short is None:
                cls.user_options.append((full, short, 'action: ' + desc))
            else:
                cls.user_options.append((full, short, desc))

    # keywords that are actions that result in effects that we support
    # TODO derive this like how the runtime does.
    actions = ('view', 'init', 'install')

    def _opt_keys(self):
        for opt in self.user_options:
            yield opt[0]

    def initialize_options(self):
        for key in self._opt_keys():
            setattr(self, key, False)
        self.stream = None  # extra output
        self.callback = None

    def do_view(self):
        pkg_name = self.distribution.get_name()
        self.cli_driver.pkg_manager_view(pkg_name, stream=self.stream)

    def do_init(self):
        pkg_name = self.distribution.get_name()
        self.cli_driver.pkg_manager_init(
            pkg_name,
            overwrite=self.overwrite, merge=self.merge,
            callback=self.callback,
            stream=self.stream,
        )

    def do_install(self):
        pkg_name = self.distribution.get_name()
        self.cli_driver.pkg_manager_install(
            pkg_name,
            overwrite=self.overwrite, merge=self.merge,
            callback=self.callback,
            production=self.production, development=self.development,
            stream=self.stream,
        )

    def finalize_options(self):
        opts = [i for i in (getattr(self, k) for k in self.actions) if i]
        if not opts:
            # default to view
            self.view = True
        if self.view or self.dry_run:
            self.stream = sys.stdout
        self.callback = prompt_overwrite_json if self.interactive else None
        # require explicit boolean value.
        self.production = True if self.production else None
        self.development = True if self.development else None

    @use_distutils_logger()
    def run(self):
        if self.dry_run:
            # Do the default action and finish, as everything else may
            # cause permanent changes.
            self.do_view()
            return
        self.run_command('egg_info')
        if self.install:
            self.do_install()
        elif self.init:
            self.do_init()
        elif self.view:
            self.do_view()


class BuildArtifactCommand(Command):
    """
    Command for building artifacts for the given package.
    """

    user_options = []

    def initialize_options(self):
        """
        Implement items that could go into the spec, such as setting of
        build dir prefix.
        """

    def finalize_options(self):
        """
        If finalization is needed.
        """

    # TODO make use of cli_driver rather than probing for registry

    @use_distutils_logger()
    def run(self):
        if self.dry_run:
            return
        get('calmjs.artifacts').process_package(self.distribution.get_name())
