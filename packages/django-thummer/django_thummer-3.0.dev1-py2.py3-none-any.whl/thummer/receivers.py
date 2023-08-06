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

from sorl.thumbnail import delete

from . import settings, tasks


def capture_image(sender, instance, created, raw, **kwargs):
    if created and not raw:
        task = tasks.capture
        task_kwargs = {'pk': instance.pk}
        if settings.QUEUE_SNAPSHOTS:
            task.delay(**task_kwargs)
        else:
            task(**task_kwargs)


def delete_image(sender, instance, **kwargs):
    if instance.image:
        delete(instance.image)
