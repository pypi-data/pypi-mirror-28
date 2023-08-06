# Copyright 2016 Casey Jaymes

# This file is part of PublishSubscribe.
#
# PublishSubscribe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PublishSubscribe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PublishSubscribe.  If not, see <http://www.gnu.org/licenses/>.

import logging

from .exceptions import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Publisher(object):
    ''' Class for a generic data structure that publishes data content changes to a list of subscribers '''

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        '''
        Add a subscriber of this data structure that receives updates via _data_added, _data_deleted and _data_updated calls.

        :param expatriate.publishsubscribe.Subscriber subscriber: The subscriber that wishes to listen to change events from this publisher.
        :raises SubscriberException: if the *subscriber* does not subclass Subscriber
        '''
        from .Subscriber import Subscriber
        if isinstance(subscriber, Subscriber):
            self._subscribers.append(subscriber)
        else:
            raise SubscriberException(str(subscriber) + ' does not inherit from Subscriber')

    def _publish_added(self, id_, item):
        '''
        Subclasses should call this method to publish additions to subscribers.

        :param id_: The added id. Can be index for a list or key for a dict.
        :param item: The added item.
        '''
        for subscriber in self._subscribers:
            subscriber._data_added(self, id_, item)

    def _publish_updated(self, id_, old_item, new_item):
        '''
        Subclasses should call this method to publish updates to subscribers.

        :param id_: The updated id. Can be index for a list or key for a dict.
        :param old_item: The old item, before the update.
        :param new_item: The new item, after the update.
        '''
        for subscriber in self._subscribers:
            subscriber._data_updated(self, id_, old_item, new_item)

    def _publish_deleted(self, id_, item):
        '''
        Subclasses should call this method to publish deletions to subscribers.

        :param id_: The deleted ids. Can be index for a list or key for a dict.
        :param item: The deleted item.
        '''
        for subscriber in self._subscribers:
            subscriber._data_deleted(self, id_, item)
