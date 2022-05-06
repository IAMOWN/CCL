from django.contrib import admin

from .models import (
    Tag,
    CosmicAuthor,
    LibraryRecord,
)
admin.site.register(Tag)
admin.site.register(CosmicAuthor)
admin.site.register(LibraryRecord)
