from django.contrib import admin

from models import Message,Notification,Detail,Location, Organization, Account, Profile, Action



admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Detail)

class LocationAdmin(admin.ModelAdmin):
    fields = ['place', 'postalcode', 'address', 'county', 'country']
    list_display = ('address', 'place', 'postalcode', 'county', 'country')


admin.site.register(Location, LocationAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
        ('Phone', {'fields': ['phone']}),
        ('Location', {'fields': ['location']}),
    ]
    list_display = ('name', 'location', 'phone')


admin.site.register(Organization, OrganizationAdmin)


class AccountAdmin(admin.ModelAdmin):
    fields = ['role', 'profile', 'user','approved']
    list_display = ('role', 'profile')


admin.site.register(Account, AccountAdmin)


class ProfileAdmin(admin.ModelAdmin):
    fields = [
        'firstname',
        'lastname',
        'IDNO',
        'sex',
        'birthday',
        'phone',
        'address',
    ]
    list_display = ('firstname', 'lastname', 'birthday', 'created')


admin.site.register(Profile, ProfileAdmin)


class ActionAdmin(admin.ModelAdmin):
    readonly_fields = ('timePerformed',)
    fields = [
        'type',
        'description',
        'account',
    ]
    list_display = ('account', 'type', 'description', 'timePerformed')
    list_filter = ('account', 'type', 'timePerformed')
    ordering = ('-timePerformed',)


admin.site.register(Action, ActionAdmin)


