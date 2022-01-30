#!python3
from argparse import ArgumentParser
from re import sub
import subprocess

PKG_UTIL = 'pkgutil'
PKG_INFO = '--pkg-info'
PKGS = '--pkgs'
FILES = '--files'
ONLY_FILES = '--only-files'
ONLY_DIRS = '--only-dirs'
FORGET = '--forget'

RM = 'rm'
RM_IF = '-if'
RM_IFR = '-ifr'
SUDO  = 'sudo'

VOLUME = 'volume: '
LOCATION = 'location: '


def find_pkgs(pkg_keyword):
    result = subprocess.check_output([PKG_UTIL, PKGS]).decode()
    return [r for r in result.split('\n') if pkg_keyword.lower() in r.lower()]


def find_location(pkg_name):
    volume = ''
    location = ''

    result = subprocess.check_output([PKG_UTIL, PKG_INFO, pkg_name]).decode()
    for line in result.split('\n'):
        if VOLUME in line:
            volume = line.replace(VOLUME, '')
        elif LOCATION in line:
            location = line.replace(LOCATION, '')
    return f'{volume}{location}'


def get_pkg_files(pkg_name, pkg_location):
    return subprocess.check_output([PKG_UTIL, ONLY_FILES, FILES, pkg_name], cwd=pkg_location).decode().split('\n')


def get_pkg_folders(pkg_name, pkg_location):
    return subprocess.check_output([PKG_UTIL, ONLY_DIRS, FILES, pkg_name], cwd=pkg_location).decode().split('\n')


def preview_will_remove(pkg_name, pkg_location):
    files = get_pkg_files(pkg_name, pkg_location)
    print('Will remove files:')
    for file in files:
        print(file)
    print('---------------------')

    folders = get_pkg_folders(pkg_name, pkg_location)
    print('Will remove folders:')
    for folder in folders:
        print(folder)
    print('---------------------')


def remove_pkg_files(pkg_name, pkg_location):
    files = get_pkg_files(pkg_name, pkg_location)
    subprocess.call([SUDO, RM, RM_IF] + files, cwd=pkg_location)


def remove_pkg_folders(pkg_name, pkg_location):
    folders = get_pkg_folders(pkg_name, pkg_location)
    subprocess.call([SUDO, RM, RM_IFR] + folders, cwd=pkg_location)


def remove_pkg_reg(pkg_name, pkg_location):
    return subprocess.check_output([SUDO, PKG_UTIL, FORGET, pkg_name], cwd=pkg_location).decode()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('pkg_keyword', help='Keyword of pkg which you want to remove', type=str)
    parser.add_argument('--apply', action='store_true', help='Apply to macOS')
    parser.add_argument('--preview', action='store_true', help='Preview which file or folder will be delete')
    parser.add_argument('--no-folders', action='store_true', help='Do not delete folders')
    return  parser.parse_args()


def main():
    args = parse_args()
    pkg_keyword = args.pkg_keyword
    is_apply = args.apply
    is_preview = args.preview
    no_folders = args.no_folders

    pkg_names = find_pkgs(pkg_keyword)
    
    print('Will remove follows:')
    print('---------------------')

    for pkg_name in pkg_names:
        location = find_location(pkg_name)
        print(f'Name: {pkg_name}\nLocation: {location}')
        print('---------------------')
        if is_preview:
            preview_will_remove(pkg_name, location)
        if is_apply:
            remove_pkg_files(pkg_name, location)
            if not no_folders:
                remove_pkg_folders(pkg_name, location)
            rm_rest = remove_pkg_reg(pkg_name, location)
            print(rm_rest)

    if is_apply:
        print('Removed successfully!')
    else:
        print('Is dryrun, use --apply to remove from macOS.')


main()
