# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
from superdesk import get_resource_service
from superdesk.media.crop import CropService
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE, EMBARGO, SCHEDULE_SETTINGS
from superdesk.utc import utcnow
from eve.utils import config
from apps.archive.common import set_sign_off, ITEM_OPERATION, insert_into_versions
from apps.archive.archive import update_associations
from .common import BasePublishService, BasePublishResource, ITEM_CORRECT


logger = logging.getLogger(__name__)


class CorrectPublishResource(BasePublishResource):

    def __init__(self, endpoint_name, app, service):
        super().__init__(endpoint_name, app, service, 'correct')


class CorrectPublishService(BasePublishService):
    publish_type = 'correct'
    published_state = 'corrected'

    def set_state(self, original, updates):
        updates[ITEM_STATE] = self.published_state

        if original.get(EMBARGO) or updates.get(EMBARGO):
            # embargo time elapsed
            utc_embargo = updates.get(SCHEDULE_SETTINGS, {}).get('utc_{}'.format(EMBARGO)) or \
                original.get(SCHEDULE_SETTINGS, {}).get('utc_{}'.format(EMBARGO))
            if utc_embargo and utc_embargo < utcnow():
                # remove embargo information. so the next correction is without embargo.
                updates[EMBARGO] = None
                super().set_state(original, updates)
        else:
            super().set_state(original, updates)

    def on_update(self, updates, original):
        update_associations(updates)
        CropService().validate_multiple_crops(updates, original)
        super().on_update(updates, original)
        updates[ITEM_OPERATION] = ITEM_CORRECT
        updates['versioncreated'] = utcnow()
        updates['correction_sequence'] = original.get('correction_sequence', 1) + 1
        set_sign_off(updates, original)

    def on_updated(self, updates, original):
        """Runs on update

        Locates the published or corrected packages containing the corrected item
        and corrects them

        :param updates: correction
        :param original: original story
        """
        original_updates = dict()
        original_updates['operation'] = updates['operation']
        original_updates[ITEM_STATE] = updates[ITEM_STATE]
        super().on_updated(updates, original)
        packages = self.package_service.get_packages(original[config.ID_FIELD])
        if packages and packages.count() > 0:
            archive_correct = get_resource_service('archive_correct')
            processed_packages = []
            for package in packages:
                if package[ITEM_STATE] in [CONTENT_STATE.PUBLISHED, CONTENT_STATE.CORRECTED] and \
                        str(package[config.ID_FIELD]) not in processed_packages:
                    original_updates['groups'] = package['groups']

                    if updates.get('headline'):
                        self.package_service.update_field_in_package(original_updates, original[config.ID_FIELD],
                                                                     'headline', updates.get('headline'))

                    if updates.get('slugline'):
                        self.package_service.update_field_in_package(original_updates, original[config.ID_FIELD],
                                                                     'slugline', updates.get('slugline'))

                    archive_correct.patch(id=package[config.ID_FIELD], updates=original_updates)
                    insert_into_versions(id_=package[config.ID_FIELD])
                    processed_packages.append(package[config.ID_FIELD])

    def update(self, id, updates, original):
        CropService().create_multiple_crops(updates, original)
        super().update(id, updates, original)
