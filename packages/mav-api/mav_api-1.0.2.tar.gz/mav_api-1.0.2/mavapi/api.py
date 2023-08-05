from mavapi.exceptions import MAVAPIError,MAVAPIAuthError

class API:
    import requests
    import random
    import json
    import re
    import base64

    # API сервер MAV
    server = 'https://mav-server.ru/api?'
    access_token = None

    def getResponse(url, data=None):
        result = API.requests.post(url, data=data)
        result = result.text
        result = result.replace('true', '1')
        result = result.replace('null', 'None')
        result = API.re.sub('true','1',result)
        result = API.re.sub('false', '0', result)
        result = API.re.sub('null', 'None', result)
        result = eval(result)
        return result['content']

        # Выше был представлен очень костыльный код, характерный только для Питона

    def getRequestData(datas):
        # Пример ввода даты: {'mav_id': mav_id, 'vk': vk}
        data = {'access_token': API.access_token}
        for item in datas.keys():
            if datas[item] != None:
                data[item] = datas[item]
        return data

    def Auth(access_token):
        # Генерируем дату для запроса
        data = {'access_token': access_token}
        result = API.getResponse(url=API.server+'getTokenPerms', data=data)
        # Проверяем, если есть ошибка в ответе
        if result['status'] == 'error':
            if result['error_code'] in MAVAPIError.error_list:
                error = {'status': 'error', 'error_code': result['error_code'], 'response': result['error_msg']}
                raise MAVAPIAuthError(error)
        else:
            response = {'status': 'okey', 'response': access_token}
            API.access_token = access_token
            return response
            # При успешной авторизации вовзвращаем токен

    def isValidAuth(access_token):
        # Проверяем валидность токена
        if API.Auth(access_token)['status'] == 'okey':
            return True
        else:
            return False

    def getUser(mav_id=None,vk=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk})
        result = API.getResponse(url=API.server+"getUser", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getTokenPerms():
        data = API.getRequestData()
        result = API.getResponse(url=API.server + "getTokenPerms", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getMavStats():
        data = API.getRequestData()
        result = API.getResponse(url=API.server + "getMavStats", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getPointsTop(entries=None):
        data = API.getRequestData({'entries': entries})
        result = API.getResponse(url=API.server + "getPointsTop", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getPointsOperations(mav_id=None):
        data = API.getRequestData({'mav_id': mav_id})
        result = API.getResponse(url=API.server + "getPointsOperations", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getBalanceByPurpose(mav_id=None,vk=None,purpose=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk, 'purpose': purpose})
        result = API.getResponse(url=API.server + "getBalanceByPurpose", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getMavStatus():
        data = API.getRequestData()
        result = API.getResponse(url=API.server + "getMavStatus", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getMavBans():
        data = API.getRequestData()
        result = API.getResponse(url=API.server + "getMavBans", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def isVerified(mav_id=None):
        data = API.getRequestData({'mav_id': mav_id})
        result = API.getResponse(url=API.server + "isVerified", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getBalance(mav_id=None,vk=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk})
        result = API.getResponse(url=API.server + "getBalance", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getMonthGames(date=None):
        if len(date) == 7:
            date = date.split("-")
            month, year = date[0],date[1]
        else:
            raise MAVAPIError(MAVAPIError.DATE_WRONG_FORMAT)
        data = API.getRequestData({'month': month, 'year': year})
        result = API.getResponse(url=API.server + "getMonthGames", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getGame(date):
        if len(date) == 10:
            date = API.re.sub('-', '', date)
        else:
            raise MAVAPIError(MAVAPIError.DATE_WRONG_FORMAT)
        data = API.getRequestData({'date': date})
        result = API.getResponse(url=API.server + "getGame", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getRole(mav_id=None,vk=None,mine=None,discord_id=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk, 'mine': mine, 'discord_id': discord_id})
        result = API.getResponse(url=API.server+"getRole", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getServerUser(mav_id=None,vk=None,mine=None,discord_id=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk, 'mine': mine, 'discord_id': discord_id})
        result = API.getResponse(url=API.server+"getServerUser", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getUserGames(mav_id=None,vk=None,mine=None,discord_id=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk, 'mine': mine, 'discord_id': discord_id})
        result = API.getResponse(url=API.server+"getUserGames", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getUserDaysLimits(mav_id=None,vk=None,mine=None,discord_id=None):
        data = API.getRequestData({'mav_id': mav_id, 'vk': vk, 'mine': mine, 'discord_id': discord_id})
        result = API.getResponse(url=API.server+"getUserDaysLimits", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getMavDetailedStats(date=None):
        if len(date) == 7:
            data = API.getRequestData({'date': date})
        else:
            raise MAVAPIError(MAVAPIError.DATE_WRONG_FORMAT)
        result = API.getResponse(url=API.server+"getMavDetailedStats", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def getActiveMembers():
        data = API.getRequestData()
        result = API.getResponse(url=API.server + "getActiveMembers", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def createUser(mine=None,vk=None,confirmMethod=None):
        data = API.getRequestData({'mine': mine, 'vk': vk, 'confirmMethod': confirmMethod})
        result = API.getResponse(url=API.server + "createUser", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def updateUserUUID(mav_id=None,mine=None):
        data = API.getRequestData({'mine': mine, 'mav_id': mav_id})
        result = API.getResponse(url=API.server + "updateUserUUID", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def addPoints(mav_id=None,points=None,service=None,purpose=None,comment=None,comment_version=2):
        comment = API.base64.encodestring(bytes(comment, 'utf-8'))
        #comment = API.base64.decodestring(comment)
        #return comment.decode('utf-8')
        data = API.getRequestData({'mav_id': mav_id, 'points': points, 'service': service, 'purpose': purpose,'comment': comment, 'comment_version': comment_version})
        result = API.getResponse(url=API.server + "addPoints", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def takePoints(mav_id=None,points=None,service=None,purpose=None,comment=None,comment_version=2):
        comment = API.base64.encodestring(bytes(comment, 'utf-8'))
        #comment = API.base64.decodestring(comment)
        #return comment.decode('utf-8')
        data = API.getRequestData({'mav_id': mav_id, 'points': points, 'service': service, 'purpose': purpose,'comment': comment, 'comment_version': comment_version})
        result = API.getResponse(url=API.server + "takePoints", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def banAccount(mav_id=None,vk=None):
        data = API.getRequestData(
            {'mav_id': mav_id, 'vk': vk})
        result = API.getResponse(url=API.server + "banAccount", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def pardonAccount(mav_id=None,vk=None):
        data = API.getRequestData(
            {'mav_id': mav_id, 'vk': vk})
        result = API.getResponse(url=API.server + "pardonAccount", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def updateUserVk(mav_id=None,vk=None):
        data = API.getRequestData(
            {'mav_id': mav_id, 'vk': vk})
        result = API.getResponse(url=API.server + "updateUserVk", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def updateUserDiscord(mav_id=None,discord_id=None):
        data = API.getRequestData(
            {'mav_id': mav_id, 'discord_id': discord_id})
        result = API.getResponse(url=API.server + "updateUserDiscord", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def setRole(mav_id=None,role=None):
        data = API.getRequestData(
            {'mav_id': mav_id, 'role': role})
        result = API.getResponse(url=API.server + "setRole", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def addUserGame(mav_id=None,date=None,service=None):
        if len(date) == 7:
            data = API.getRequestData({'date': date, 'mav_id': mav_id, 'service': service})
        else:
            raise MAVAPIError(MAVAPIError.DATE_WRONG_FORMAT)
        result = API.getResponse(url=API.server + "addUserGame", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

    def removeUserGame(mav_id=None,date=None,service=None):
        if len(date) == 7:
            data = API.getRequestData({'date': date, 'mav_id': mav_id, 'service': service})
        else:
            raise MAVAPIError(MAVAPIError.DATE_WRONG_FORMAT)
        result = API.getResponse(url=API.server + "removeUserGame", data=data)
        if result['status'] == 'error':
            raise MAVAPIError(result)
        return result

