# -*- coding: utf-8 -*-
#
# Copyright 2011-2018 Matt Austin
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


from __future__ import absolute_import, unicode_literals

from django import apps
from django.db.models import signals

from . import receivers


class AppConfig(apps.AppConfig):

    name = 'thummer'

    verbose_name = 'thummer'

    def ready(self):
        signals.post_save.connect(
            receivers.capture_image, sender='thummer.WebPageSnapshot',
            dispatch_uid='thummer.WebPageSnapshot.capture_image')
        signals.pre_delete.connect(
            receivers.delete_image, sender='thummer.WebpageSnapshot',
            dispatch_uid='thummer.WebpageSnapshot.delete_image')
