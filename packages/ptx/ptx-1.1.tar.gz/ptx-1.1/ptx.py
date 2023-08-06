import datetime
import hmac
import base64


def getDatetimeString(dt=datetime.datetime.utcnow()):
    return datetime.datetime.strftime(dt, '%a, %d %b %Y %H:%M:%S GMT')


def getSignature(dt_str, app_id, app_key):
    dt_str = 'x-date: ' + dt_str
    h = hmac.new(app_key.encode('utf-8'),
                 msg=dt_str.encode('utf-8'),
                 digestmod='SHA1')

    return base64.b64encode(h.digest()).decode('utf-8')


def getAuthorization(dt_str,
                  app_id='FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF',
                  app_key='FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'):
    signature = getSignature(dt_str, app_id, app_key)
    return 'hmac username="{}", algorithm="hmac-sha1", headers="x-date", signature="{}"'.format(app_id, signature)
