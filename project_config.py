import os
import os.path
import platform
import shutil
from shutil import copyfile

TOOLS_PREFIX = ''
OS_NAME = platform.system()
MACH = platform.machine()
ARCH = platform.architecture()
is32bit = (ARCH[0] == '32bit')

if is32bit:
    if MACH == 'i686' or MACH == 'i386' or MACH == 'x86':
        TARGET_ARCH = 'x86'
    else:
        TARGET_ARCH = 'arm'
else:
    TARGET_ARCH = ''

print('MACH=' + MACH + ' ARCH=' + str(ARCH) + ' TARGET_ARCH=' + TARGET_ARCH)


def joinPath(root, subdir):
    return os.path.normpath(os.path.join(root, subdir))


ROOT = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))

PROJECT_RES = 'win32_res/project.res'
if not os.path.exists(PROJECT_RES):
    PROJECT_RES = os.path.join(ROOT, 'win32_res/project.res')

print('ROOT: ' + ROOT)
print('PROJECT_RES: ' + PROJECT_RES)

SRC = joinPath(ROOT, 'src')
BIN_DIR = joinPath(ROOT, 'bin')
LIB_DIR = joinPath(ROOT, 'lib')
THIRDPARTY_ROOT = joinPath(ROOT, '3rd')
TOOLS_ROOT = joinPath(ROOT, 'tools')
DEMO_ROOT = joinPath(ROOT, 'demos')
PROJECT_STATIC_LIBS = ['test_src',]

if not os.path.exists(os.path.abspath(PROJECT_RES)):
    os.makedirs(os.path.abspath(PROJECT_RES))
if not os.path.exists(os.path.abspath(SRC)):
    os.makedirs(os.path.abspath(SRC))
if not os.path.exists(os.path.abspath(BIN_DIR)):
    os.makedirs(os.path.abspath(BIN_DIR))
if not os.path.exists(os.path.abspath(LIB_DIR)):
    os.makedirs(os.path.abspath(LIB_DIR))
if not os.path.exists(os.path.abspath(THIRDPARTY_ROOT)):
    os.makedirs(os.path.abspath(THIRDPARTY_ROOT))
if not os.path.exists(os.path.abspath(TOOLS_ROOT)):
    os.makedirs(os.path.abspath(TOOLS_ROOT))
if not os.path.exists(os.path.abspath(DEMO_ROOT)):
    os.makedirs(os.path.abspath(DEMO_ROOT))

OS_FLAGS = ''
OS_LIBS = []
OS_LIBPATH = []
OS_CPPPATH = []
OS_LINKFLAGS = ''
OS_SUBSYSTEM_CONSOLE = ''
OS_SUBSYSTEM_WINDOWS = ''
OS_PROJECTS = []
OS_WHOLE_ARCHIVE = ''

TOOLS_NAME = ''
COMMON_CCFLAGS = ' -DTK_ROOT=\"\\\"'+ROOT+'\\\"\" '

if OS_NAME == 'Windows':
    if TOOLS_NAME == '':
        OS_LIBS = ['gdi32', 'user32', 'winmm.lib', 'imm32.lib', 'version.lib', 'shell32.lib',
                   'ole32.lib', 'Oleaut32.lib', 'Advapi32.lib', 'DelayImp.lib', 'psapi.lib']
        OS_FLAGS = '-DWIN32 -D_WIN32 -DWINDOWS /EHsc -D_CONSOLE  /DEBUG /Od  /FS /Z7 /utf-8'
        if TARGET_ARCH == 'x86':
            # OS_LINKFLAGS = '/MACHINE:X86 /DEBUG \"' + PROJECT_RES + '\" '
            OS_LINKFLAGS = '/MACHINE:X64 /DEBUG '
            OS_SUBSYSTEM_CONSOLE = '/SUBSYSTEM:CONSOLE,5.01  '
            OS_SUBSYSTEM_WINDOWS = '/SUBSYSTEM:WINDOWS,5.01  '
            COMMON_CCFLAGS = COMMON_CCFLAGS + ' -D_WIN32 '
        else:
            OS_FLAGS = OS_FLAGS + ' -DWITH_64BIT_CPU '
            # OS_LINKFLAGS = '/MACHINE:X64 /DEBUG \"' + PROJECT_RES + '\" '
            OS_LINKFLAGS = '/MACHINE:X64 /DEBUG '
            OS_SUBSYSTEM_CONSOLE = '/SUBSYSTEM:CONSOLE  '
            OS_SUBSYSTEM_WINDOWS = '/SUBSYSTEM:WINDOWS  '
            COMMON_CCFLAGS = COMMON_CCFLAGS + ' -D_WIN64 '
        COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DHAVE_LIBC '
        OS_WHOLE_ARCHIVE = ''
        PROJECT_DLL_DEPS_LIBS = PROJECT_STATIC_LIBS + OS_LIBS

LINKFLAGS = OS_LINKFLAGS
LIBPATH = [LIB_DIR, BIN_DIR] + OS_LIBPATH
CCFLAGS = OS_FLAGS + COMMON_CCFLAGS
PROJECT_CCFLAGS = OS_FLAGS + COMMON_CCFLAGS
STATIC_LIBS = PROJECT_STATIC_LIBS + [''] + OS_LIBS
SHARED_LIBS = [''] + OS_LIBS

LIBS = STATIC_LIBS

CPPPATH = [ROOT,
           SRC,
           THIRDPARTY_ROOT,
           TOOLS_ROOT] + OS_CPPPATH

os.environ['ROOT'] = ROOT
os.environ['CCFLAGS'] = CCFLAGS
os.environ['TOOLS_NAME'] = TOOLS_NAME
os.environ['THIRDPARTY_ROOT'] = THIRDPARTY_ROOT
os.environ['OS_WHOLE_ARCHIVE'] = OS_WHOLE_ARCHIVE
os.environ['PROJECT_DLL_DEPS_LIBS'] = ';'.join(PROJECT_DLL_DEPS_LIBS)
os.environ['STATIC_LIBS'] = ';'.join(STATIC_LIBS)

os.environ['WITH_PROJECT_SO'] = 'true'
os.environ['PROJECT_CCFLAGS'] = PROJECT_CCFLAGS


def copySharedLib(src, dst, name):
    if OS_NAME == 'Darwin':
        src = os.path.join(src, 'bin/lib'+name+'.dylib')
    elif OS_NAME == 'Linux':
        src = os.path.join(src, 'bin/lib'+name+'.so')
    elif OS_NAME == 'Windows':
        src = os.path.join(src, 'bin/'+name+'.dll')
    else:
        print('not support ' + OS_NAME)
        return

    src = os.path.normpath(src)
    dst = os.path.normpath(dst)

    if os.path.dirname(src) == dst:
        return

    if not os.path.exists(src):
        print('Can\'t find ' + src + '. Please build '+name+'before!')
    else:
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copy(src, dst)
        print(src + '==>' + dst)


def isBuildShared():
    return 'WITH_PROJECT_SO' in os.environ and os.environ['WITH_PROJECT_SO'] == 'true'

def genIdlAndDef():
    cmds = [
        'node tools/idl_gen/tkc.js tools/idl_gen/tkc.json',
        'node tools/idl_gen/index.js tools/idl_gen/idl.json',
        'node tools/dll_def_gen/index.js tools/idl_gen/idl.json  dllexports/awtk.def false',
        'node tools/dll_def_gen/index.js tools/idl_gen/tkc.json  dllexports/tkc.def false'
    ]

    for cmd in cmds:
        print(cmd)
        if os.system(cmd) != 0:
            print('exe cmd: ' + cmd + ' failed.')
