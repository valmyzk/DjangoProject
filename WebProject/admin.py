from django.contrib import admin

from .models import *

admin.site.register(Wallet)
admin.site.register(Asset)
admin.site.register(Transaction)
admin.site.register(Holding)