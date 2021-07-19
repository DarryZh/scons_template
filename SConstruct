import os
from sys import path
import SCons
import project_config as project
from SCons.Defaults import DefaultEnvironment
import SCons.Tool
import SCons.Environment
import SCons.Builder


APP_TOOLS = None
if project.TOOLS_NAME != '':
    APP_TOOLS = [project.TOOLS_NAME]

DefaultEnvironment(TOOLS=APP_TOOLS,
                   CCFLAGS=project.PROJECT_CCFLAGS,
                   LIBS=project.LIBS,
                   LIBPATH=project.LIBPATH,
                   CPPPATH=project.CPPPATH +
                   [project.joinPath(project.ROOT, 'res')],
                   LINKFLAGS=project.LINKFLAGS,
                   TARGET_ARCH=project.TARGET_ARCH,
                   OS_SUBSYSTEM_CONSOLE=project.OS_SUBSYSTEM_CONSOLE,
                   OS_SUBSYSTEM_WINDOWS=project.OS_SUBSYSTEM_WINDOWS
                   )

SConscriptFiles = [
    'src/SConscript',
    'demos/SConscript',
] + project.OS_PROJECTS

os.environ['ROOT'] = project.ROOT
os.environ['BIN_DIR'] = project.BIN_DIR
os.environ['LIB_DIR'] = project.LIB_DIR

SConscript(SConscriptFiles)