import inflection
import requests

class UserLocalCache(object):
    '''Login logic.  '''

    def __getattr__(self, variable_name):
        
        cleaned_name = self.check_name_is_known(variable_name = variable_name)
        if cleaned_name == None:
            raise AttributeError("UserCache instance has no attribute '{name}'".format(name = variable_name))
        
        if self.cache.get(cleaned_name):
            return self.cache[cleaned_name]
        
        else:
            response = self.session.get('/{name}/models/'.format(name = cleaned_name))
            if response.status_code == 200:
                response = response.json()
                self.cache[cleaned_name] = response['data']
                return self.cache[cleaned_name]

            raise ValueError('Failed to retrieve requested variable!' + variable_name)
        
        raise ValueError('You have reached a point in the code that is not expected and should be an error.')
    
    
    def override_variable(self, variable_name, value):
        self.cache[variable_name] = value
        return True
    
    def clear_variable(self, variable_name):
        
        cache_variable = self.check_name_is_known(name = variable_name)
        if cache_variable != None:
            
            self.cache.pop(cache_variable, None)
            return 
        else:
            if hasattr(self, variable_name):
                variable_name = None
                return
        raise AttributeError('The variable requested to be cleared is not found!')
    
    def check_name_is_known(self, variable_name):
        if variable_name in self.MICROSERVICE_MODELS.keys():
            return variable_name
        
        if inflection.camelize(string = variable_name) in self.MICROSERVICE_MODELS.keys():
            return inflection.camelize(string = variable_name)
        return None

    @property
    def cache(self):
        if getattr(self, '_cache', None) == None:
            self._cache = None
            
        if self._cache == None:
            self._cache = {}
            
        return self._cache


if __name__ == '__main__':
    
    uc = UserLocalCache()
    
    ss = uc.profile
    
    ss = uc.profile

    ss = uc.clear_variable('profile')
    
    ss = uc.profile

#     print(uc.un.KNOWN_MODELS.keys())