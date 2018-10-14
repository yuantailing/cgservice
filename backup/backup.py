import logging
import os
import shutil
import subprocess
import sys


BACKUP_CACHE_ROOT = '/mnt/backup_cache'
BACKUP_STORAGE_ROOT = '/mnt/backup_storage'


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


def rsync(*, checksum):
    for src, repo in [[o[k] for k in ('src', 'repo')] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : rsync : start'.format(repo))
        with open(os.path.join('/etc/cgservice/backup/exclude', repo)) as f:
            exclude = f.readlines()
        exclude_args = []
        for path in exclude:
            assert '\n' == path[-1]
            exclude_args += ['--exclude', path[:-1]]
        dst = os.path.join(BACKUP_CACHE_ROOT, repo)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        call(['rsync', '-avc' if checksum else '-av', '--delete', src + '/', dst + '/data'] + exclude_args)
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
        shutil.copy(os.path.join('/etc/cgservice/backup/ignore', repo), os.path.join('data', '.gitignore'))
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
    for repo in [o['repo'] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : store : start'.format(repo))
        src = os.path.join(BACKUP_CACHE_ROOT, repo)
        if includegit:
            call(['rsync', '-avc' if checksum else '-av', '--delete', src, BACKUP_STORAGE_ROOT + '/'])
        else:
            dst = os.path.join(BACKUP_STORAGE_ROOT, repo)
            if not os.path.isdir(dst):
                os.makedirs(dst)
            call(['rsync', '-avc' if checksum else '-av', '--delete', os.path.join(src, 'data'), dst + '/'])
        logging.info('[BACKUP] {:s} : store : success'.format(repo))


def gc():
    for repo in [o['repo'] for o in CONFIG]:
        logging.info('[BACKUP] {:s} : gc : start'.format(repo))
        os.chdir(os.path.join(BACKUP_CACHE_ROOT, repo))
        call(['git', 'gc'])
        logging.info('[BACKUP] {:s} : gc : success'.format(repo))


def main():
    assert os.path.ismount(BACKUP_CACHE_ROOT)
    assert os.path.ismount(BACKUP_STORAGE_ROOT)

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    action = sys.argv[1]
    if action == 'shell':
        exit(call(['bash'] + sys.argv[2:]))

    lock_filename = os.path.join(BACKUP_STORAGE_ROOT, 'backup.lock')
    with open(lock_filename, 'x') as lockf:
        if action == 'nothing':
            pass
        elif action == 'rsync-only':
            rsync(checksum=False)
            store(checksum=False, includegit=False)
        elif action == 'commit-timestamp':
            rsync(checksum=False)
            commit()
            store(checksum=False, includegit=True)
        elif action == 'commit-checksum':
            rsync(checksum=True)
            commit()
            store(checksum=True, includegit=True)
        elif action == 'gc':
            gc()
            store(checksum=False)
        else:
            raise ValueError('invalid action {:s}'.format(action))
    os.unlink(lock_filename)


if __name__ == '__main__':
    main()
