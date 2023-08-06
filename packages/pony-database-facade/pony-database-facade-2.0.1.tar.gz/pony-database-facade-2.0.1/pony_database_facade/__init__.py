# coding: utf-8
#
# Copyright 2017 Kirill Vercetti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import copy
import os

from pony.orm import Database

from .loader import Loader


class DatabaseFacade(object):
    """PonyORM Database object Facade"""

    def __init__(self, *args, **kwargs):
        self.__db = Database()
        self.__update_config(*args, **kwargs)

    def __init_defaults(self, config):
        """Initializes the default connection settings."""

        provider = self.__provider

        if provider == 'sqlite':
            config.setdefault('dbname', ':memory:')
            config.setdefault('create_db',  True)
        elif provider == 'mysql':
            config.setdefault('port', 3306)
            config.setdefault('charset', 'utf8')
        elif provider == 'postgres':
            config.setdefault('port', 5432)
        elif provider == 'oracle':
            config.setdefault('port', 1521)
        else:
            raise ValueError('Unsupported provider "{}"'.format(provider))

        if provider != 'sqlite':
            config.setdefault('host', 'localhost')
            config.setdefault('user', None)
            config.setdefault('password', None)
            config.setdefault('dbname', None)

    def __update_config(self, *args, **kwargs):
        if 'provider' in kwargs:
            self.__provider = kwargs.pop('provider')
        elif args:
            self.__provider, args = args[0], args[1:]
        else:
            self.__provider = 'sqlite'

        self.__init_defaults(kwargs)

        self.__config_args = list(args)
        self.__config_kwargs = kwargs

    def bind(self, *args, **kwargs):
        if args or kwargs:
            self.__update_config(*args, **kwargs)

        provider = self.__provider
        args = [provider] + self.__config_args
        kwargs = copy(self.__config_kwargs)
        # kwargs = {}

        if provider == 'sqlite':
            filename = kwargs.pop('dbname')

            if filename != ':memory:' and not os.path.dirname(filename):
                filename = os.path.join(os.getcwd(), filename)

            kwargs.update({
                'filename': filename,
                'create_db': kwargs.pop('create_db')
            })
        elif provider == 'mysql':
            kwargs.update({
                'host': kwargs.pop('host'),
                'port': kwargs.pop('port'),
                'user': kwargs.pop('user'),
                'passwd': kwargs.pop('password'),
                'db': kwargs.pop('dbname'),
                'charset': kwargs.pop('charset')
            })
        elif provider == 'postgres':
            kwargs.update({
                'host': kwargs.pop('host'),
                'port': kwargs.pop('port'),
                'user': kwargs.pop('user'),
                'password': kwargs.pop('password'),
                'database': kwargs.pop('dbname')
            })
        elif provider == 'oracle':
            args.append('{user}/{password}@{host}:{port}/{dbname}'.format(user=kwargs.pop('user'),
                                                                          password=kwargs.pop('password'),
                                                                          host=kwargs.pop('host'),
                                                                          port=kwargs.pop('port'),
                                                                          dbname=kwargs.pop('dbname')
                                                                          ))

        self.original.bind(*args, **kwargs)

    def connect(self, create_tables=True, *args, **kwargs):
        # postgresql://scott:tiger@localhost/test
        if self.original.provider is None:
            self.bind()
        self.original.generate_mapping(*args, create_tables=create_tables, **kwargs)

    @property
    def original(self):
        """Returns Database instance"""
        return self.__db

    @property
    def Entity(self):
        """Returns base class for all entities"""
        return self.original.Entity

    @staticmethod
    def load_module_with_entities(name):
        assert isinstance(name, str)
        return Loader().load_and_registry(name)
