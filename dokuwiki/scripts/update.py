import fcntl
import logging
import operator
import os
import requests
import settings
import shutil
import subprocess
import urllib.parse


def check_name(name):
    if not (2 <= len(name) <= 40):
        return False
    for c in name.lower():
        if c not in '0123456789abcdefghijklmnopqrstuvwxyz-_':
            return False
    return True


if __name__ == '__main__':
    # set logging and lock
    var_dir = '/var/lib/cgnas'
    if not os.path.isdir(var_dir):
        os.makedirs(var_dir)
    stat = os.stat(var_dir)
    if stat.st_mode & 0o7777 != 0o700:
        os.chmod(var_dir, 0o700)
    log_filename = os.path.join(var_dir, 'recent')
    handlers = [logging.FileHandler(log_filename, mode='w'), logging.StreamHandler()]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        handlers=handlers,
    )

    passwd_lock_created = False
    try:
        # communicate with API
        latest_password_update_filename = os.path.join(var_dir, 'latest_password_update')
        latest_password_update = 0
        if os.path.isfile(latest_password_update_filename):
            with open(latest_password_update_filename) as f:
                try:
                    latest_password_update = float(f.read())
                except ValueError:
                    pass
        try:
            r = requests.post(settings.CGNAS_API_URL, data={
                'api_secret': settings.CGNAS_API_SECRET,
                'latest_password_update': latest_password_update,
            }, timeout=(5., 65.))
        except requests.exceptions.ConnectionError:
            logging.error('cgserver connection error')
            raise
        if 200 != r.status_code:
            logging.error('cgserver API failed')
        assert 200 == r.status_code
        data = r.json()
        users = data['users']
        users.sort(key=operator.itemgetter('staff_number'))

        # save latest password update
        latest_password_update = 0 if 0 == len(users) else max([user['password_updated_at'] for user in users])
        with open(latest_password_update_filename, 'w') as f:
            f.write('{:f}'.format(latest_password_update))

        # check valid usersnames
        # note that staff_number and username MUST NOT duplicate
        forbidden_names = ['admin']
        valid_users = []
        username_taken = set()
        for user in users:
            if not user['shadow_password']:
                continue
            if not check_name(user['username']):
                logging.info('username "{:s}" is invalid'.format(user['username']))
                continue
            if user['username'] in forbidden_names:
                logging.info('username "{:s}" is prohibited'.format(user['username']))
                continue
            username_taken.add(user['username'])
            valid_users.append(user)
        users = valid_users

        # set users.auth.php
        users_auth = [
            '# users.auth.php',
            '# <?php exit()?>',
            '# Don\'t modify the lines above'
        ]
        for user in users:
            users_auth.append('{:s}:{:s}:{:s}::user'.format(user['username'], user['shadow_password'], user['username']))
        with open('/srv/dokuwiki/conf/users.auth.tmp.php', 'w') as f:
            f.write('\n'.join(users_auth))
            f.write('\n')
        os.rename('/srv/dokuwiki/conf/users.auth.tmp.php', '/srv/dokuwiki/conf/users.auth.php')

        logging.info('Everything up-to-date.')
    except:
        logging.error('Error occurred, please contact administrator.')
        raise
    finally:
        # write status to apache
        html_dir = '/var/www/html'
        path = os.path.join(html_dir, '.index.html.tmp')
        url = urllib.parse.urljoin(settings.CGNAS_API_URL, '/serverlist/profile')
        with open(path, 'w') as f:
            f.write('<!DOCTYPE html>')
            f.write('<html><head><meta charset="UTF-8"></head><body>')
            f.write('<h1>Dokuwiki Status</h1>')
            f.write('<pre>')
            with open(log_filename) as log_f:
                f.write(log_f.read())
            f.write('</pre><hr>')
            f.write('<p><a href="."><button>refresh</button></a></p>')
            f.write('<p>Please go to <a href="{:s}">{:s}</a> to setup your account.</p>'.format(url, url))
            f.write('<p>&copy; <script>document.write((new Date()).getFullYear());</script> CSCG Group</p>')
            f.write('</body></html>')
        os.rename(path, os.path.join(html_dir, 'index.html'))
