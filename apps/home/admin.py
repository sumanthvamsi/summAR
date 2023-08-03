# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from .models import summary_file
admin.site.register(summary_file)

from .models import meta_video
admin.site.register(meta_video)

from .models import forum
admin.site.register(forum)

from .models import cloud
admin.site.register(cloud)