# Copyright 2017 Infuse Team
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from flask import Flask
import os
from configparser import ConfigParser

from infuse.server.routes import bp
from infuse.config import Config


class InfuseServer(object):
    """Represents Infuse server application."""

    def __init__(self, name=__name__, args=None):
        self.name = name
        self.args = args
        self.app = Flask(__name__)
        self.load_config()
        self.app.register_blueprint(bp)

    def run(self):
        """Run Infuse server."""
        self.app.run(port=int(self.app.config['INFUSE_SERVER_PORT']))

    def load_config(self):
        """Loads configuration from different sources."""
        self.app.config.from_object(Config)

        if vars(self.args)['INFUSE_CONFIG_FILE']:
            self.app.config['INFUSE_CONFIG_FILE'] = vars(self.args)[
                'INFUSE_CONFIG_FILE']
        elif 'INFUSE_CONFIG_FILE' in os.environ:
            self.app.config['INFUSE_CONFIG_FILE'] = os.environ[
                'INFUSE_CONFIG_FILE']

        self.load_config_from_env()
        self.load_config_from_file()
        self.load_config_from_parser()

    def load_config_from_env(self):
        """Loads configuration from environment variables."""
        infuse_envs = filter(
            lambda s: s.startswith('INFUSE_'), os.environ.keys())
        for env_key in infuse_envs:
            if os.environ[env_key]:
                self.app.config[env_key] = os.environ[env_key]

    def load_config_from_file(self):
        """Loads configuration from a file."""
        cfg_parser = ConfigParser()
        cfg_parser.read(self.app.config['INFUSE_CONFIG_FILE'])

        for section in cfg_parser.sections():
            for key in cfg_parser.options(section):
                k = "INFUSE_%s" % key.upper()
                self.app.config[k] = cfg_parser.get(section, key)

    def load_config_from_parser(self):
        """Loads configuration based on provided arguments by the user."""
        for k, v in vars(self.args).items():
            if v:
                self.app.config[k] = v
