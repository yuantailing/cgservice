import fcntl
import logging
import os
import shutil
import subprocess
import sys


BACKUP_CACHE_ROOT = '/mnt/backup_cache'
BACKUP_STORAGE_ROOT = '/mnt/backup_storage'
STORAGE_TEMP_DIR = 'repo.tmp'
STORAGE_PERMANENT_DIR = 'repo'


CONFIG = [
    {
        'src': '/mnt/ftp/cscg',
        'repo': 'cscg',
    },
    {
        'src': '/mnt/ftp/oslab',
        'repo': 'oslab',
    },
    {
        'src': '/mnt/csvn/data',
        'repo': 'csvn',
    },
]


def call(*args, **kwargs):
    ret = subprocess.call(*args, **kwargs)
    if ret != 0:
        logging.info('[BACKUP] error in calling', args, kwargs)
        exit(ret)


def check():
    temp = os.path.join(BACKUP_STORAGE_ROOT, STORAGE_TEMP_DIR)
    perm = os.path.join(BACKUP_STORAGE_ROOT, STORAGE_PERMANENT_DIR)
    assert not os.path.exists(temp)


def rsync(*, checksum):
    for src, repo in [[o[k] for k in ('src', 'repo')] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : rsync : start'.format(repo))
        dst = os.path.join(BACKUP_CACHE_ROOT, repo)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        call(['rsync', '-avc' if checksum else '-av', '--delete', src + '/', dst + '/data'])
        logging.info('[BACKUP] {:s} : rsync : success'.format(repo))


def commit():
    for repo in [o['repo'] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : commit : start'.format(repo))
        os.chdir(os.path.join(BACKUP_CACHE_ROOT, repo))
        for filename in os.listdir('.'):
            if filename not in ('.git', '.gitignore', 'data'):
                if os.path.isdir(filename):
                    shutil.rmtree(filename)
                else:
                    os.unlink(filename)
        if not os.path.isdir('.git'):
            ret = subprocess.call(['git', 'init'])
            if ret != 0:
                return ret
        shutil.copy(os.path.join('/etc/cgservice/backup/ignore', repo), '.gitignore')
        call('git ls-files --ignored --exclude-standard -z | xargs -0 -r git rm --cached', shell=True)
        call(['git', 'add', '--all'])
        output = subprocess.check_output(['git', 'status', '--porcelain'])
        if output:
            print(output.decode('utf-8', 'ignore'))
            call(['git', 'commit', '-m', 'backup'])
        else:
            logging.info('[BACKUP] {:s} : commit : status is clean'.format(repo))
        logging.info('[BACKUP] {:s} : commit : success'.format(repo))



def store(*, checksum, includegit):
    temp = os.path.join(BACKUP_STORAGE_ROOT, STORAGE_TEMP_DIR)
    perm = os.path.join(BACKUP_STORAGE_ROOT, STORAGE_PERMANENT_DIR)
    if not os.path.isdir(perm):
        os.makedirs(perm)
    os.rename(perm, temp)
    temp = os.path.join(BACKUP_STORAGE_ROOT, STORAGE_TEMP_DIR)
    perm = os.path.join(BACKUP_STORAGE_ROOT, STORAGE_PERMANENT_DIR)
    for repo in [o['repo'] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : store : start'.format(repo))
        src = os.path.join(BACKUP_CACHE_ROOT, repo)
        if includegit:
            call(['rsync', '-avc' if checksum else '-av', '--delete', src, temp + '/'])
        else:
            dst = os.path.join(temp, repo)
            if not os.path.isdir(dst):
                os.makedirs(dst)
            call(['rsync', '-avc' if checksum else '-av', '--delete', os.path.join(src, 'data'), dst + '/'])
        logging.info('[BACKUP] {:s} : store : success'.format(repo))
    os.rename(temp, perm)


def gc():
    for repo in [o['repo'] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : gc : start'.format(repo))
        os.chdir(os.path.join(BACKUP_CACHE_ROOT, repo))
        call(['git', 'gc'])
        logging.info('[BACKUP] {:s} : gc : success'.format(repo))


def main(action):
    assert os.path.ismount(BACKUP_CACHE_ROOT)
    assert os.path.ismount(BACKUP_STORAGE_ROOT)

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    with open(os.path.join(BACKUP_STORAGE_ROOT, 'backup.lock'), 'w') as lockf:
        fcntl.flock(lockf, fcntl.LOCK_EX)
        if action == 'nothing':
            pass
        elif action == 'shell':
            call(['bash'])
        elif action == 'rsync-only':
            check()
            rsync(checksum=False)
            store(checksum=False, includegit=False)
        elif action == 'commit-timestamp':
            check()
            rsync(checksum=False)
            commit()
            store(checksum=False, includegit=True)  # cache is OK is error occurs
        elif action == 'commit-checksum':
            check()
            rsync(checksum=True)   # perm is OK is error occurs
            commit()               # temp is OK is error occurs
            store(checksum=True, includegit=True)   # cache is OK is error occurs
        elif action == 'gc':
            check()
            gc()                   # temp is OK is error occurs
            store(checksum=False)  # cache is OK is error occurs
        else:
            raise ValueError('invalid action {:s}'.format(action))


if __name__ == '__main__':
    main(sys.argv[1])
