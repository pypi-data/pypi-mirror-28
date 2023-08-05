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
import argparse

from infuse.database import InfuseDatabase


def create_database_parser():
    """Returns argparse parser."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        dest="INFUSE_DEBUG", help='Turn DEBUG on')

    return parser


def main():
    """Main entry for running the server."""
    parser = create_database_parser()
    args = parser.parse_args()
    infuse_database = InfuseDatabase(args=args)
    infuse_database.init()
