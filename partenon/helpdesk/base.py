from oraculo.gods import faveo, exceptions


class BaseEntityHelpDesk(object):
    
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class BaseHelpDesk(object):
    
    def __init__(self):
        self._client = faveo.APIClient()


class BaseManageEntity(BaseHelpDesk):
    def __init__(self, url, entity, key_name='name'):
        self._url = url
        self._entity = entity
        self._client = faveo.APIClient
        self._key_name = key_name

    def get_entitys(self):
        client = self._client()
        response = client.get(self._url)
        entity = [self._entity(**response)
                  for response in response.get('result')]
        return entity

    def get_by_name(self, name):
        client = self._client()
        response = client.get(self._url, {'name': name})
        for item in response.get('result'):
            if item[self._key_name] == name:
                return self._entity(**item)
        else:
            raise exceptions.DoesNotExist('Not exists %s ' % name)

