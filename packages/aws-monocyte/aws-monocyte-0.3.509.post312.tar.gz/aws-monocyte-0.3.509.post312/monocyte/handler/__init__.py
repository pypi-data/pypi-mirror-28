# Monocyte - Monocyte - Search and Destroy unwanted AWS Resources relentlessly.
# Copyright 2015 Immobilien Scout GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import warnings
import logging
import boto3


class Resource(object):
    def __init__(self, resource, resource_type, resource_id, creation_date,
                 region=None, reason=None):
        self.wrapped = resource
        self.region = region
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.creation_date = creation_date
        self.reason = reason

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return ("{class_name}({resource}, {resource_type}, {resource_id}, "
                "{creation_date}, region={region}, reason={reason})").format(
                class_name=self.__class__.__name__,
                resource=self.wrapped,
                resource_type=self.resource_type,
                resource_id=self.resource_id,
                creation_date=self.creation_date,
                region=self.region,
                reason=self.reason)

    def __repr__(self):
        return str(self)


HANDLER_PREFIX = "monocyte.handler."


class Handler(object):
    def __init__(self, region_filter, dry_run=True, logger=None, ignored_resources=None, whitelist=None):
        warnings.filterwarnings('error')
        self.region_filter = region_filter
        self.region_names = [region_name for region_name in self.fetch_region_names() if self.region_filter(region_name)]
        self.dry_run = dry_run
        self.ignored_resources = ignored_resources or []
        self.whitelist = whitelist or {}
        self.logger = logger or logging.getLogger(__name__)

    @property
    def resource_type(self):
        full_type = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        return full_type.replace(HANDLER_PREFIX, "")

    @property
    def name(self):
        full_name = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        return full_name.replace(HANDLER_PREFIX, "")

    def get_account_id(self):
        return boto3.client('sts').get_caller_identity().get('Account')

    def get_whitelist(self):
        return self.whitelist.get(self.get_account_id(), {})

    def fetch_region_names(self):
        raise NotImplementedError("Should have implemented this")

    def fetch_unwanted_resources(self):
        raise NotImplementedError("Should have implemented this")

    def to_string(self, resource):
        raise NotImplementedError("Should have implemented this")

    def delete(self, resource):
        raise NotImplementedError("Should have implemented this")
