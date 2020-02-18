# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Book,Publication,Author

# Register your models here.
admin.site.register(Book)
admin.site.register(Publication)
admin.site.register(Author)