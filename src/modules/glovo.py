import uuid, time, random, string

from .client import Session
from .utilities import between

def generate_perseus():
    first = str(time.time() * 1000)
    
    second = ''.join(random.choices(string.digits, k=18))
    third = ''.join(random.choices(string.ascii_lowercase, k=10))
    client_id = f'{first}.{second}.{third}'
    
    fourth = ''.join(random.choices(string.digits, k=18))
    fifth = ''.join(random.choices(string.ascii_lowercase, k=10))
    session_id = f'{first}.{fourth}.{fifth}'
    
    return client_id, session_id, first

class Glovo:
    def __init__(self, proxy: str | None = None):
        self.fingerprint: dict = {
            'client-identifier': 'chrome_131',
            'headers': {
                'Accept-Language' : 'en-US,en;q=0.9',
                'Sec-Ch-Ua'       : '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
        }

        self.session = Session(self.fingerprint['client-identifier'], proxy)
        
    def request(self, method: str, url: str, **args):
        try:
            return self.session.request(method, url, **args)
        except Exception as e:
            raise Exception(f'Failed to send request. ({e})')
        
    def index(self):
        headers = {
            'Accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language'           : self.fingerprint['headers']['Accept-Language'],
            'Priority'                  : 'u=0, i',
            'Referer'                   : 'https://www.google.com/',
            'Sec-Ch-Ua'                 : self.fingerprint['headers']['Sec-Ch-Ua'],
            'Sec-Ch-Ua-Mobile'          : '?0',
            'Sec-Ch-Ua-Platform'        : '"Windows"',
            'Sec-Fetch-Dest'            : 'document',
            'Sec-Fetch-Mode'            : 'navigate',
            'Sec-Fetch-Site'            : 'cross-site',
            'Sec-Fetch-User'            : '?1',
            'Upgrade-Insecure-Requests' : '1',
            'User-Agent'                : self.fingerprint['headers']['User-Agent']
        }
        try:
            response = self.request('GET', 'https://glovoapp.com/', headers=headers)
        except Exception as e:
            return False, e
        try:
            self.api_version = between(response.text, 'apiVersion:', ',')
        except:
            return False, 'Failed to fetch api version.'
        self.dyn_sess_id = str(uuid.uuid4())
        self.request_id = str(uuid.uuid4())
        self.client_id, self.session_id, self.timestamp = generate_perseus()
        return True, response
        
    def identity_devices(self):
        headers = {
            'Accept'                      : 'application/json',
            'Accept-Language'             : self.fingerprint['headers']['Accept-Language'],
            'Content-Type'                : 'application/json',
            'Glovo-Api-Version'           : self.api_version,
            'Glovo-App-Development-State' : 'Production',
            'Glovo-App-Platform'          : 'web',
            'Glovo-App-Type'              : 'customer',
            'Glovo-App-Version'           : '7',
            'Glovo-Client-Info'           : 'web-customer-web/7 project:customer-web',
            'Glovo-Language-Code'         : 'en',
            'Glovo-Request-Id'            : self.request_id,
            'Glovo-Request-Ttl'           : '7500',
            'Origin'                      : 'https://glovoapp.com',
            'Priority'                    : 'u=1, i',
            'Referer'                     : 'https://glovoapp.com/',
            'Sec-Ch-Ua'                   : self.fingerprint['headers']['Sec-Ch-Ua'],
            'Sec-Ch-Ua-Mobile'            : '?0',
            'Sec-Ch-Ua-Platform'          : '"Windows"',
            'Sec-Fetch-Dest'              : 'empty',
            'Sec-Fetch-Mode'              : 'cors',
            'Sec-Fetch-Site'              : 'same-site',
            'User-Agent'                  : self.fingerprint['headers']['User-Agent']
        }
        payload = {
            'fingerprints': [
                {
                    'fingerprint': str(uuid.uuid4()),
                    'provider': 'CWUID'
                }
            ]
        }
        try:
            response = self.request('POST', 'https://api.glovoapp.com/identity/v4/devices', headers=headers, json=payload)
        except Exception as e:
            return False, e
        try:
            self.device_urn = response.json().get('urn', f'glv:device:{str(uuid.uuid4())}')
        except:
            self.device_urn = f'glv:device:{str(uuid.uuid4())}'
        return True, response
        
    def get_auth_methods(self, name: str):
        headers = {
            'Accept'                          : 'application/json',
            'Accept-Language'                 : self.fingerprint['headers']['Accept-Language'],
            'Glovo-Api-Version'               : self.api_version,
            'Glovo-App-Development-State'     : 'Production',
            'Glovo-App-Platform'              : 'web',
            'Glovo-App-Type'                  : 'customer',
            'Glovo-App-Version'               : '7',
            'Glovo-Client-Info'               : 'web-customer-web/7 project:customer-web',
            'Glovo-Device-Urn'                : self.device_urn,
            'Glovo-Dynamic-Session-Id'        : self.dyn_sess_id,
            'Glovo-Language-Code'             : 'en',
            'Glovo-Perseus-Client-Id'         : self.client_id,
            'Glovo-Perseus-Session-Id'        : self.session_id,
            'Glovo-Perseus-Session-Timestamp' : self.timestamp,
            'Glovo-Request-Id'                : self.request_id,
            'Glovo-Request-Ttl'               : '7500',
            'Origin'                          : 'https://glovoapp.com',
            'Priority'                        : 'u=1, i',
            'Referer'                         : 'https://glovoapp.com/',
            'Sec-Ch-Ua'                       : self.fingerprint['headers']['Sec-Ch-Ua'],
            'Sec-Ch-Ua-Mobile'                : '?0',
            'Sec-Ch-Ua-Platform'              : '"Windows"',
            'Sec-Fetch-Dest'                  : 'empty',
            'Sec-Fetch-Mode'                  : 'cors',
            'Sec-Fetch-Site'                  : 'same-site',
            'User-Agent'                      : self.fingerprint['headers']['User-Agent']
        }
        try:
            response = self.request('GET', f'https://api.glovoapp.com/v3/customers/auth/{name}/methods', headers=headers)
        except Exception as e:
            return False, e
        return True, response
    
    def get_auth_token(self, name: str, password: str):
        headers = {
            'Accept'                          : 'application/json',
            'Accept-Language'                 : self.fingerprint['headers']['Accept-Language'],
            'Content-Type'                    : 'application/json',
            'Glovo-Api-Version'               : self.api_version,
            'Glovo-App-Development-State'     : 'Production',
            'Glovo-App-Platform'              : 'web',
            'Glovo-App-Type'                  : 'customer',
            'Glovo-App-Version'               : '7',
            'Glovo-Client-Info'               : 'web-customer-web/7 project:customer-web',
            'Glovo-Device-Urn'                : self.device_urn,
            'Glovo-Dynamic-Session-Id'        : self.dyn_sess_id,
            'Glovo-Language-Code'             : 'en',
            'Glovo-Perseus-Client-Id'         : self.client_id,
            'Glovo-Perseus-Session-Id'        : self.session_id,
            'Glovo-Perseus-Session-Timestamp' : self.timestamp,
            'Glovo-Request-Id'                : self.request_id,
            'Glovo-Request-Ttl'               : '7500',
            'Origin'                          : 'https://glovoapp.com',
            'Priority'                        : 'u=1, i',
            'Referer'                         : 'https://glovoapp.com/',
            'Sec-Ch-Ua'                       : self.fingerprint['headers']['Sec-Ch-Ua'],
            'Sec-Ch-Ua-Mobile'                : '?0',
            'Sec-Ch-Ua-Platform'              : '"Windows"',
            'Sec-Fetch-Dest'                  : 'empty',
            'Sec-Fetch-Mode'                  : 'cors',
            'Sec-Fetch-Site'                  : 'same-site',
            'User-Agent'                      : self.fingerprint['headers']['User-Agent']
        }
        payload = {
            'grantType': 'password',
            'username': name,
            'password': password
        }
        try:
            response = self.request('POST', 'https://api.glovoapp.com/oauth/token', headers=headers, json=payload)
        except Exception as e:
            return False, e
        return True, response
    
    def get_user_info(self):
        headers = {
            'Accept'                          : 'application/json',
            'Accept-Language'                 : self.fingerprint['headers']['Accept-Language'],
            'Authorization'                   : self.access_token,
            'Glovo-Api-Version'               : self.api_version,
            'Glovo-App-Development-State'     : 'Production',
            'Glovo-App-Platform'              : 'web',
            'Glovo-App-Type'                  : 'customer',
            'Glovo-App-Version'               : '7',
            'Glovo-Client-Info'               : 'web-customer-web/7 project:customer-web',
            'Glovo-Dynamic-Session-Id'        : self.dyn_sess_id,
            'Glovo-Language-Code'             : 'en',
            'Glovo-Perseus-Client-Id'         : self.client_id,
            'Glovo-Perseus-Session-Id'        : self.session_id,
            'Glovo-Perseus-Session-Timestamp' : self.timestamp,
            'Glovo-Request-Id'                : self.request_id,
            'Glovo-Request-Ttl'               : '7500',
            'Origin'                          : 'https://glovoapp.com',
            'Priority'                        : 'u=1, i',
            'Referer'                         : 'https://glovoapp.com/',
            'Sec-Ch-Ua'                       : self.fingerprint['headers']['Sec-Ch-Ua'],
            'Sec-Ch-Ua-Mobile'                : '?0',
            'Sec-Ch-Ua-Platform'              : '"Windows"',
            'Sec-Fetch-Dest'                  : 'empty',
            'Sec-Fetch-Mode'                  : 'cors',
            'Sec-Fetch-Site'                  : 'same-site',
            'User-Agent'                      : self.fingerprint['headers']['User-Agent']
        }
        try:
            response = self.request('GET', 'https://api.glovoapp.com/v3/me', headers=headers)
        except Exception as e:
            return False, e
        return True, response
    
    def get_payment_methods(self):
        headers = {
            'Accept'                          : 'application/json',
            'Accept-Language'                 : self.fingerprint['headers']['Accept-Language'],
            'Authorization'                   : self.access_token,
            'Glovo-Api-Version'               : self.api_version,
            'Glovo-App-Development-State'     : 'Production',
            'Glovo-App-Platform'              : 'web',
            'Glovo-App-Type'                  : 'customer',
            'Glovo-App-Version'               : '7',
            'Glovo-Client-Info'               : 'web-customer-web/7 project:customer-web',
            'Glovo-Dynamic-Session-Id'        : self.dyn_sess_id,
            'Glovo-Language-Code'             : 'en',
            'Glovo-Perseus-Client-Id'         : self.client_id,
            'Glovo-Perseus-Session-Id'        : self.session_id,
            'Glovo-Perseus-Session-Timestamp' : self.timestamp,
            'Glovo-Request-Id'                : self.request_id,
            'Glovo-Request-Ttl'               : '7500',
            'Origin'                          : 'https://glovoapp.com',
            'Priority'                        : 'u=1, i',
            'Referer'                         : 'https://glovoapp.com/',
            'Sec-Ch-Ua'                       : self.fingerprint['headers']['Sec-Ch-Ua'],
            'Sec-Ch-Ua-Mobile'                : '?0',
            'Sec-Ch-Ua-Platform'              : '"Windows"',
            'Sec-Fetch-Dest'                  : 'empty',
            'Sec-Fetch-Mode'                  : 'cors',
            'Sec-Fetch-Site'                  : 'same-site',
            'User-Agent'                      : self.fingerprint['headers']['User-Agent']
        }
        try:
            response = self.request('GET', 'https://api.glovoapp.com/v3/payment_methods', headers=headers)
        except Exception as e:
            return False, e
        return True, response
    