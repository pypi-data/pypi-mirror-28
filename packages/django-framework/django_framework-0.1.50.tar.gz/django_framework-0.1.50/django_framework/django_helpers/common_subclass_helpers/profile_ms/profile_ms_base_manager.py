import operator
from inflector import Inflector
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import QuerySet, ManyToManyField, Q, F
from django.core.exceptions import ObjectDoesNotExist
# from app_models import get_model_name
# from app_serializers import get_serializer_name
# from django_framework.helpers.time_helpers import now
# from django_framework.helpers.cache_helpers import invalidate_model_cache

from django_framework.django_helpers.cache_helpers import ManagerCache, APICache
import collections



from django.conf import settings
import arrow
import copy

from django_framework.django_helpers.model_helpers.model_registry import get_model_name

from django_framework.django_helpers.manager_helpers import BaseManager 

class ProfileMSBaseManager(BaseManager):
    '''The purpose of this subclassed manager is to provide a Manager specifically for
    linking multiple microservers together.
    
    We expect that each Microserver has an "access table" that is 1-1 with a given
    Profile.  The access table which this Manager governs, must have a UUID that matches
    the Profile.UUID.  This ensures that when the Microserver requests other information from
    this server, it can do so by matching UUID's.
    
    We currently do not enable lookups by "Profile.ID" as authentication.
    
    '''
    