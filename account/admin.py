from django.contrib import admin

from .models import*

admin.site.register(Reader)
admin.site.register(Author)
admin.site.register(Administrator)