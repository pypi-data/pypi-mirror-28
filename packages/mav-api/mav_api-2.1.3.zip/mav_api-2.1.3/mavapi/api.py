from mavapi.exceptions import MAVAPIError,MAVAPIAuthError
import aiohttp
import asyncio
import re

__version__ = '2.1.3'

class API:
    def __init__(self,server=None):
        self.server = server

    # Делаем все запросы вот этой штукой, фактически сердце модуля
    '''
        Обратите внимание! Все запросы идут корутинами, и их можно получить через event_loop
    '''
    async def getRequest(self,server=None,params=None, data=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(server, params=params, data=data) as request:

                request = await request.text()
                request = re.sub('true','1',request)
                request = re.sub('false', '0', request)
                request = re.sub('null', 'None', request)
                request = eval(request)

                return request['content']
    '''
        Авторизуемся здесь
        По факту, тут нет авторизации, просто проверяем валидность токена, делая запрос на сервер и обрабатываем запрос
        Если токен неверен - поднимаем ошибку и не даём скрипту выполняться дальше
    '''
    def Auth(self,access_token=None):
        # Вызов event loop'а
        loop = asyncio.new_event_loop()
        request = loop.run_until_complete(self.getRequest(self.server, params='getTokenPerms', data={'access_token': access_token}))
        if request['status'] == 'error':
            if request['error_code'] in MAVAPIError.error_list.keys():
                raise MAVAPIAuthError(MAVAPIError.error_list[request['error_code']])
        else:
            self.access_token = access_token
            return self.access_token

    '''
        Тут мы создаем дату из параметров, которые нам будут необходимы
        Проверяем, пустые ли они, или нет
        Если пустые, пропускаем из системы и игнорируем их
    '''
    def getData(self,datas):
        data = {'access_token': self.access_token}
        for param in datas.keys():
            if datas[param] != None:
                data[param] = datas[param]
        return data

    # Делать запросы сюды ---------------------------------------------------

    def getResponse(self,method=None,**kwargs):
        data = self.getData(kwargs)
        loop = asyncio.new_event_loop()
        request = loop.run_until_complete(self.getRequest(self.server,params=method,data=data))
        if request['status'] == 'error':
            raise MAVAPIError(request)
        else:
            return request

    '''
        Ну, как Вам API? В 50 то строчек? :)
    '''