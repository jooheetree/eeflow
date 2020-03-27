from django.contrib import admin

from ea.models import Push, Document, Sign, Attachment, DefaulSignList, Invoice

admin.site.register(Push)
admin.site.register(Invoice)
admin.site.register(Document)
admin.site.register(Attachment)
admin.site.register(Sign)
admin.site.register(DefaulSignList)











