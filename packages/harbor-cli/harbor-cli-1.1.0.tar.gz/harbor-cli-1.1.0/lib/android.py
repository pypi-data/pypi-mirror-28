'''
Manage Android/ReactNative related actions through here.
'''
import os
import fnmatch
import json
import xml.etree.ElementTree as ET

from lib.shell import run
from lib.utils.branch import branch
from lib.exceptions.InvalidAndroidProject import InvalidAndroidProjectException

PWD = os.getcwd()

BASE_MANIFEST = '/app/src/main/AndroidManifest.xml'
BASE_APK_PATH = '/app/build/outputs/apk/'

NATIVE_ANDROID_MANIFEST = ''.join([PWD, BASE_MANIFEST])
REACT_NATIVE_MANIFEST = ''.join([PWD, '/android', BASE_MANIFEST])

SIGNED_ANDROID_PATH = ''.join([PWD, BASE_APK_PATH, 'app-release.apk'])
UNSIGNED_ANDROID_PATH = ''.join(
    [PWD, BASE_APK_PATH, 'app-release-unsigned.apk'])

SIGNED_REACT_NATIVE_PATH = ''.join(
    [PWD, '/android', BASE_APK_PATH, 'app-release.apk'])
UNSIGNED_REACT_NATIVE_PATH = ''.join([
    PWD, '/android', BASE_APK_PATH, 'app-release-unsigned.apk'
])

PACKAGE_JSON = 'package.json'


def is_android():
    ''' Returns true for any android project (native/RN) '''
    return is_native_android() or is_react_native()


def get_manifest_path():
    '''
    Returns native manifest path for native projects,
    and prefixes the native path by a "/android" for RN projects
    '''
    if os.path.isfile(NATIVE_ANDROID_MANIFEST):
        return NATIVE_ANDROID_MANIFEST
    elif os.path.isfile(REACT_NATIVE_MANIFEST):
        return REACT_NATIVE_MANIFEST
    else:
        raise Exception('Not an android project.')


def is_native_android():
    ''' Returns True if the project in cwd is native android project. '''
    return os.path.isfile(NATIVE_ANDROID_MANIFEST)


def is_react_native():
    ''' Returns True if the project in cwd is native android project. '''
    return os.path.isfile(REACT_NATIVE_MANIFEST) and os.path.isfile(PACKAGE_JSON)


def build(is_release=False):
    ''' Builds the android project. '''
    script = branch_buildtype(is_release)(build_release, build_debug)

    return script()


def build_debug():
    ''' Build a 'debug' apk. '''
    buildscript = './gradlew assembleDebug'
    rn_buildscript = './android/gradlew -p android assembleDebug'

    return run(branch_platform(buildscript, rn_buildscript))

def build_release():
    ''' Build a 'release' apk. '''
    buildscript = './gradlew assembleRelease'
    rn_buildscript = './android/gradlew -p android assembleRelease'

    return run(branch_platform(buildscript, rn_buildscript))

def clean():
    ''' Builds the android project. '''
    if is_react_native():
        return run('./android/gradlew -p android clean')
    elif is_native_android():
        return run('./gradlew clean')
    else:
        raise InvalidAndroidProjectException()


def signed(path):
    ''' If path matches signed path returns True, else returns False '''
    if path == UNSIGNED_REACT_NATIVE_PATH or path == UNSIGNED_ANDROID_PATH:
        return False

    if path == SIGNED_REACT_NATIVE_PATH or path == SIGNED_ANDROID_PATH:
        return True

    #raise InvalidAndroidProjectException()
    return False


def find_files(directories, pattern):
    ''' A helper to find by pattern in a directory. '''
    for directory in directories:
        for root, _, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename


def find_apk():
    ''' Fuzzy matches *.apk in the working directory. '''
    basepath = ''.join([PWD, BASE_APK_PATH])
    rn_basepath = ''.join([PWD, '/android', BASE_APK_PATH])

    for filename in find_files([rn_basepath, basepath], '*.apk'):
        return filename

def apk_path():
    ''' Returns path to apk. '''
    apkpath = find_apk()
    paths = [
        UNSIGNED_REACT_NATIVE_PATH,
        UNSIGNED_ANDROID_PATH,
        SIGNED_ANDROID_PATH,
        SIGNED_REACT_NATIVE_PATH,
        apkpath
    ]

    def removenonexisting(path):
        ''' Remove paths that dont exist. '''
        return os.path.isfile(path) is True

    pathexists = list(filter(removenonexisting, paths))

    # Only take the first entry. (there should be only one)
    return pathexists[0]


def apk_size(path):
    ''' Returns size of apk. '''
    # in megabytes.
    return os.path.getsize(path) >> 20


def build_details():
    ''' Returns the build details of the apks currently in output. '''
    path = apk_path()
    size = apk_size(path)
    is_signed = signed(path)

    return {
        'size': size,
        'apk_path': path,
        'is_signed': is_signed
    }


def parse_manifest():
    ''' Parses the manifest XML file and gets relevant information. '''
    manifestpath = get_manifest_path()
    tree = ET.parse(manifestpath)
    root = tree.getroot()

    # Only interested in the root since it has the packagename.
    packagename = root.attrib['package']

    return {
        'packagename': packagename
    }


def parse_packagejson():
    ''' Parse package.json and return relevant information. '''
    with open(PACKAGE_JSON) as packagejson:
        data = json.load(packagejson)

        return {
            'name': data['name']
        }


def project_details():
    ''' Returns the details  of the project in cwd. '''
    manifestdetails = parse_manifest()

    # For react native, parse package.json too
    if is_react_native():
        packagejsondetails = parse_packagejson()

    # Merge the two dictionaries.
    # Cant destructure here since py<3.5 support is required.
    details = manifestdetails.copy()

    if is_react_native():
        details.update(packagejsondetails)
    else:
        details.update({
            'name': manifestdetails['packagename']
        })

    return details


def launcher_icon():
    ''' Finds appropriate launcher icon for the project. '''

    return find('ic_launcher.png', PWD)


def find(name, path):
    ''' A helper to find a filename in a path. '''
    for root, _, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def branch_platform(native, react_native):
    '''
    Returns a function that returns the first value if native android
    and second value if react_native
    '''
    return branch(is_native_android)(native, react_native)

def branch_buildtype(is_release):
    '''
    Returns a function that returns the first value if debug build
    and second value if release build.
    '''
    return branch(is_release)
