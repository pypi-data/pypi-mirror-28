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
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from infuse import app
from infuse import Config

# Initialize our DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class InfuseDatabase(object):
    """Represents Infuse server application."""

    def __init__(self, name=__name__, args=None):
        self.db_uri = Config.SQLALCHEMY_DATABASE_URI

    @staticmethod
    def init():
        """Run Infuse server."""
        from infuse.database import models # noqa
        db.create_all()
