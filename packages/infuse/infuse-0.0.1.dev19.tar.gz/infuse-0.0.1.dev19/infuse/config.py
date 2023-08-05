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
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    INFUSE_SERVER_PORT = 5000
    INFUSE_DEBUG = False
    INFUSE_CONFIG_FILE = '/etc/infuse/infuse.conf'

    SQLALCHEMY_DATABASE_URI = os.environ.get('INFUSE_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'infuse.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
