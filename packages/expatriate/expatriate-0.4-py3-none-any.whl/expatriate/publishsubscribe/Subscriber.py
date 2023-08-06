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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Subscriber(object):
    def _data_added(self, publisher, id_, item):
        '''
        Notification received from a Publisher when data has been added.
        Subclasses of Subscriber should override this.

        :param expatriate.publishsubscribe.Publisher publisher: The publishing object
        :param id_: The added id. Can be index for a list or key for a dict.
        :param item: The added item.
        '''
        pass

    def _data_updated(self, publisher, id_, old_item, new_item):
        '''
        Notification received from a Publisher when data has been updated.
        Subclasses of Subscriber should override this.

        :param expatriate.publishsubscribe.Publisher publisher: The publishing object
        :param id_: The updated id. Can be index for a list or key for a dict.
        :param old_item: The old item, before the update.
        :param new_item: The new item, after the update.
        '''
        pass

    def _data_deleted(self, publisher, id_, item):
        '''
        Notification received from a Publisher when data has been deleted.
        Subclasses of Subscriber should override this.

        :param expatriate.publishsubscribe.Publisher publisher: The publishing object
        :param id_: The deleted ids. Can be index for a list or key for a dict.
        :param item: The deleted item.
        '''
        pass
