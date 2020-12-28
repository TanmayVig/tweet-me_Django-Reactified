from django.contrib import admin
from . import models

class TweetLIkeAdmin(admin.TabularInline):
    model = models.TweetLike



class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLIkeAdmin]
    list_display = ['__str__','user']
    search_fields = ['user__username','user__email']
    class Meta:
        model = models.Tweet

admin.site.register(models.Tweet, TweetAdmin)