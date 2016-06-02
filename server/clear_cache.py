#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
from django.core.cache import cache

django.setup() # Needed to make django ready from the external script
cache.clear()  # Flush all the old cache entries

