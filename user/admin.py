from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class StatusListFilter(admin.SimpleListFilter):
    title = _(u'学生状态')
    parameter_name = 'userid'

    def lookups(self, request, model_admin):
        return (
            ('0', _(u'硕士组')),
            ('1', _(u'博士组')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(userid__startswith='3')
        if self.value() == '1':
            return queryset.filter(userid__startswith='2')


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('userid', 'password')}),
        (_('Personal info'), {'fields': ('username', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userid', 'email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('userid', 'username', 'email', 'is_staff')
    list_filter = ('is_superuser', 'is_active', 'groups', StatusListFilter)
    search_fields = ('userid', 'username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def status(self):
        # pdb.set_trace()
        if self.userid.startswith('2'):
            return format_html('<p>博士组</p>')
        elif self.userid.startswith('3'):
            return format_html('<p">硕士组</p>')

    status.short_description = u'状态'


# Register your models here.
admin.site.register(User, MyUserAdmin)
