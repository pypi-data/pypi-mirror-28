
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
    Model = None

    @classmethod
    def create(cls, Serializer=None, data=None, clear_cache=True):
        # this can be done because the DjangoFramework automatically adds profile_uuid to ALL incoming query data
        
        if data.get('uuid') == None:
            data['uuid'] = data.get('profile_uuid')
            
        if data['uuid'] == None:
            raise ValueError('The uuid cannot be none.  This is caught at a higher level than the serializer because this is a linking model')
        return super(ProfileMSBaseManager, cls).create(Serializer=Serializer, data=data, clear_cache=clear_cache)

    @classmethod
    def _relationship_name_format(cls, relationship_name=None, relationship_list=None):
        if relationship_name == 'profile':
            query_key = "profile_id__in"
        return query_key, relationship_list

    @classmethod
    def _get_related_model(cls, models, relationship_name):
        if relationship_name == 'profile':
             
            profile_uuids = [model.profile_uuid for model in models]
            return profile_uuids
        else:
            raise ValueError('The relationship name requested was not understood')
 
        return models