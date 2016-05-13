import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE':'openapi.settings')
from queryapi.models import AreaCode
Data=AreaCode.objects.get(area_code='110000')
print Data