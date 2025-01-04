from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


GroupPermissionMapping = {
    'operator': {
        'include_permissions': [],
        'exclude_models': [
            'logentry', 'permission', 'group', 'user', 'contenttype', 'session', 'token', 'tokenproxy', 'crontabschedule',
            'intervalschedule', 'periodictask', 'periodictasks', 'solarschedule', 'clockedschedule', 'taskresult',
            'chordcounter', 'groupresult', 'requestlog', 'requestlogdetail', 'aeskey', 'gamelog', 'emailconfirm', 'datamapping',
            'websocketconnection', 'omitevent', 'servertoken'
        ],
    },
    'account': {
        'include_permissions': ['add_account', 'change_account', 'delete_account', 'view_account'],
        'exclude_models': []
    }
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for k, v in GroupPermissionMapping.items():
            g, _ = Group.objects.get_or_create(name=k)
            g.permissions.clear()
            if v.get('include_permissions'):
                g.permissions.add(*list(Permission.objects.filter(codename__in=v.get('include_permissions'))))
            if v.get('exclude_models'):
                exclude_permissions = []
                for m in v.get('exclude_models'):
                    exclude_permissions.extend(['add_'+m, 'change_'+m, 'delete_'+m, 'view_'+m])
                g.permissions.add(*list(Permission.objects.exclude(codename__in=exclude_permissions)))
