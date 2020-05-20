from django.contrib import admin

# UserProfile Model Import
from account.models import UserProfile


# Admin Site Customization
admin.site.site_header = "TrendsUp Admin"
admin.site.index_title = 'TrendsUp Administration'
admin.site.site_title = 'TrendsUp Admin'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone')

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('user',)
        return queryset


# UserProfile Model Registration
admin.site.register(UserProfile, UserProfileAdmin)
