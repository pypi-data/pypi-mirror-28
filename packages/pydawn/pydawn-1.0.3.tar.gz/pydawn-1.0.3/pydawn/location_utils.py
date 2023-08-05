# coding=utf-8
import requests


def get_coordinate(location):
    url_format = "http://api.map.baidu.com/geocoder/v2/?output=json&ak=SjDhGSaC0GTQfhL7ezS9Qb0MoTWk49hO&address=%s"
    url = url_format % location
    response = requests.get(url)
    answer = response.json()
    try:
        x, y = answer['result']['location']['lng'], answer['result']['location']['lat']
        return x, y
    except:
        print 'query location %s fail, %s' % (location, answer)
        return None, None
