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
from datetime import datetime
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from infuse.database import db


class Job(db.Model):
    """Rerpresents a job."""
    __tablename__ = 'job'

    id = db.Column(db.Integer, Sequence('job_id_seq'), primary_key=True)
    name = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    builds = relationship("Build", back_populates="job")

    def __repr__(self):
        return "<Job(id='{0}', name='{1}', timestamp='{2}'".format(
            self.id, self.name, self.timestamp)


class Build(db.Model):
    """Rerpresents a build."""
    __tablename__ = 'build'

    id = db.Column(db.Integer, Sequence('build_id_seq'), primary_key=True)
    number = db.Column(db.Integer)
    status = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    tests = relationship("Test", back_populates="builds")

    def __repr__(self):
        return "<Build(id='{0}', number='{1}', status='{2}', " \
               "timestamp='{3}'".format(self.id, self.number,
                                        self.status, self.timestamp)


class Test(db.Model):
    """Rerpresents a test."""
    __tablename__ = 'test'

    id = db.Column(db.Integer, Sequence('test_id_seq'), primary_key=True)
    name = db.Column(db.String(128))
    class_name = db.Column(db.String(128))
    status = db.Column(db.String(64))
    duration = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    build_id = db.Column(db.Integer, db.ForeignKey('build.id'))
    test = relationship("Build", back_populates="tests")

    def __repr__(self):
        return "<Test(id='{0}', name='{1}', status='{2}', timestamp='{3}', " \
               "class_name='{4}', duration='{5}'".format(self.id, self.name,
                                                         self.status,
                                                         self.timestamp,
                                                         self.class_name,
                                                         self.duration)
