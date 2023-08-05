#!/usr/bin/env python

# Copyright (c) 2016 aos Limited, All Rights Reserved
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied.


import argparse
import collections
import json
import filecmp
import traceback
import urllib2
import zipfile

from repo import *


def get_aosder_dir():
    # Find the aos_toolchain directory
    builtin_aosder = os.path.join(Program().path, 'aos/aos_toolchain')
    aosder_dir = Program().get_cfg('aos_toolchain') or Global().get_cfg('aos_toolchain') or \
                 (builtin_aosder if os.path.isdir(builtin_aosder) else None)
    if not aosder_dir:
        error('Can not find aos_toolchain!')
    return aosder_dir


def _run_make(arg_list):
    # aosder_dir = get_aosder_dir()
    aosder_dir = os.path.join(os.getcwd(), 'build').replace('\\', '/')

    # Decide which make to use according to the platform system 
    win_make = os.path.join(aosder_dir, 'cmd/win32/make.exe').replace('\\', '/')
    mac_make = os.path.join(aosder_dir, 'cmd/osx/make')
    linux_make = os.path.join(aosder_dir, 'cmd/linux64/make')
    make_cmd = mac_make if sys.platform == 'darwin' else (
    linux_make if sys.platform == 'linux2' else (win_make if sys.platform == 'win32' else None))
    if not make_cmd:
        error('Unsupported system!')

    # Run make command
    host_os = 'OSX' if sys.platform == 'darwin' else 'Linux64' if sys.platform == 'linux2' else 'Win32'
    make_cmd_str = ' '.join([make_cmd, 'HOST_OS=' + host_os, 'TOOLS_ROOT=' + aosder_dir] + list(arg_list))
    popen(make_cmd_str, shell=True, cwd=os.getcwd())


def is_path_component(path):
    if not os.path.exists(path):
        return False

    for f in os.listdir(path):
        tmp_file = os.path.join(path, f)
        if os.path.isfile(tmp_file) and tmp_file.endswith('.mk') and os.path.basename(path) == f[:-3]:
            return True

    return False


def get_component_ref(lib):
    ref = (formaturl(lib.url, 'https').rstrip('/') + '/' +
           (('' if lib.is_build else '#') +
            lib.rev if lib.rev else ''))
    return ref


def copy_directory(src_dir, dst_dir, sub_dir=False):
    if not os.path.exists(src_dir):
        return

    if os.path.exists(dst_dir):
        if sub_dir:
            dcmp = filecmp.dircmp(src_dir, dst_dir)
            if dcmp.left_only:
                order_dir = sorted(dcmp.left_only)
                for od in order_dir:
                    copy_directory(os.path.join(src_dir, od), os.path.join(dst_dir, od))
        return

    try:
        shutil.copytree(src_dir, dst_dir)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src_dir, dst_dir)
        else:
            raise


def copy_file(src_file, dst_file):
    if os.path.exists(dst_file): return
    try:
        shutil.copy(src_file, dst_file)
    except IOError as io_err:  # python >2.5
        if io_err.errno != errno.ENOENT:
            raise
        os.makedirs(os.path.dirname(dst_file))
        shutil.copy(src_file, dst_file)


default_dir_list = ['build', 'include', 'LICENSE', 'NOTICE', 'README.md', 'app', os.path.join('framework', 'fsyscall'),
                    os.path.join('kernel', 'ksyscall')]


def get_target_program(project_path, aos_sdk_path, target):
    pd = Program(project_path)

    with cd(aos_sdk_path):
        _run_make(['-e', '-f build/Makefile', 'clean', '>' + os.path.join(project_path, '.logcat.txt')])
        _run_make(['-e', '-f build/Makefile', target, '>' + os.path.join(project_path, '.logcat.txt')])

    # copyp os default dir
    for d in default_dir_list:
        src = os.path.join(aos_sdk_path, d)
        dst = os.path.join(project_path, 'aos', d)
        copy_directory(src, dst)

    # get all component through config.mk
    config_dict = {}

    with open(os.path.join(aos_sdk_path, 'out', target, 'config.mk'), 'r') as f:
        for line in f:
            config = re.split(r'\s*.=\s*', line)
            if len(config) == 2:
                config_dict[config[0].strip()] = config[1].strip()

    copy_dir_dict = {}
    # sdk makefile dir
    sdk_makefiles = config_dict['AOS_SDK_MAKEFILES'].split(' ')
    for sm in sdk_makefiles:
        sm = sm.strip()
        if sm:
            copy_dir_dict[os.path.abspath(os.path.dirname(os.path.join(aos_sdk_path, sm)))] = os.path.abspath(
                os.path.dirname(os.path.join(project_path, 'aos', sm)))

    # sdk prebuild libraries dir
    sdk_prebuild_libs = config_dict['AOS_SDK_PREBUILT_LIBRARIES'].split(' ')
    for sp in sdk_prebuild_libs:
        sp = sp.strip()
        if sp:
            copy_dir_dict[os.path.abspath(os.path.dirname(os.path.join(aos_sdk_path, sp)))] = os.path.abspath(
                os.path.dirname(os.path.join(project_path, 'aos', sp)))

    # sdk include dir
    sdk_includes = config_dict['AOS_SDK_INCLUDES'].split('-I')
    for si in sdk_includes:
        si = si.strip()
        if si:
            copy_dir_dict[os.path.abspath(os.path.join(aos_sdk_path, si))] = os.path.abspath(
                os.path.join(project_path, 'aos', si))

    # all component dir
    components = config_dict[COMPONENTS].split(' ')
    for co in components:
        # component dir
        src_dir = os.path.abspath(os.path.join(aos_sdk_path, config_dict[co + '_LOCATION']))
        dst_dir = os.path.abspath(os.path.join(project_path, 'aos', config_dict[co + '_LOCATION']))
        copy_dir_dict[src_dir] = dst_dir

        # component c file dir
        src_files = config_dict[co + '_SOURCES'].split(' ')
        for sf in src_files:
            sf = sf.strip()
            if sf:
                copy_dir_dict[os.path.abspath(os.path.dirname(os.path.join(src_dir, sf)))] = os.path.abspath(
                    os.path.dirname(os.path.join(dst_dir, sf)))

        # component include dir
        src_includes = config_dict[co + '_INCLUDES'].split('-I')
        for si in src_includes:
            si = si.strip()
            if si:
                copy_dir_dict[os.path.abspath(os.path.join(aos_sdk_path, si))] = os.path.abspath(
                    os.path.join(project_path, 'aos', si))

    # application dir, must last copy because app target dir isn't the same as src dir
    app = config_dict['APP']
    copy_dir_dict[os.path.abspath(os.path.join(aos_sdk_path, config_dict[app + '_LOCATION']))] = os.path.abspath(
        os.path.join(project_path, app))
    pd.set_cfg(APP_PATH, os.path.join(project_path, app))

    order_copy_dir_dict = collections.OrderedDict(sorted(copy_dir_dict.items()))
    for src_dir, dst_dir in order_copy_dir_dict.items():
        is_component = is_path_component(src_dir)
        while not is_component and src_dir != aos_sdk_path:
            src_dir = os.path.dirname(src_dir)
            dst_dir = os.path.dirname(dst_dir)
            is_component = is_path_component(src_dir)

        if is_component:
            copy_directory(src_dir, dst_dir)

    component_dep = {}
    with open(os.path.join(aos_sdk_path, 'out', target, 'dependency.json'), 'r') as fin:
        dep_dict = json.loads(fin.read())
        for co in components:
            location = os.path.join('aos', relpath(aos_sdk_path, os.path.abspath(
                os.path.join(aos_sdk_path, config_dict[co + '_LOCATION'])))) if co != app else app
            if os.path.join('out', target) not in location:
                ref = ''
                aos_sdk_path = Global().get_cfg(AOS_SDK_PATH)
                if Repo.isrepo(aos_sdk_path):
                    ref = get_component_ref(Repo.fromrepo(aos_sdk_path))
                origin = 'local'
                component_dep[co] = {'location': location, 'status': 'used', 'dependencies': dep_dict[co], 'origin': origin, 'ref': ref}

    with open(os.path.join(project_path, COMPONENTS), 'w') as fout:
        fout.write(json.dumps(component_dep, sort_keys=True, indent=4))

    pd.set_cfg(OS_PATH, os.path.join(project_path, 'aos'))
    pd.set_cfg(PATH_TYPE, 'program')


# Subparser handling
parser = argparse.ArgumentParser(prog='aos',
                                 description="Code management tool for aos - https://code.aliyun.com/aos/aos\nversion %s\n\nUse 'aos <command> -h|--help' for detailed help.\nOnline manual and guide available at https://code.aliyun.com/aos/aos-cube" % ver,
                                 formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers(title="Commands", metavar="           ")
parser.add_argument("--version", action="store_true", dest="version", help="print version number and exit")
subcommands = {}


# Process handling
def subcommand(name, *args, **kwargs):
    def __subcommand(command):
        if not kwargs.get('description') and kwargs.get('help'):
            kwargs['description'] = kwargs['help']
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = argparse.RawDescriptionHelpFormatter

        subparser = subparsers.add_parser(name, **kwargs)
        subcommands[name] = subparser

        for arg in args:
            arg = dict(arg)
            opt = arg['name']
            del arg['name']

            if isinstance(opt, basestring):
                subparser.add_argument(opt, **arg)
            else:
                subparser.add_argument(*opt, **arg)

        subparser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Verbose diagnostic output")
        subparser.add_argument("-vv", "--very_verbose", action="store_true", dest="very_verbose",
                               help="Very verbose diagnostic output")

        def thunk(parsed_args):
            argv = [arg['dest'] if 'dest' in arg else arg['name'] for arg in args]
            argv = [(arg if isinstance(arg, basestring) else arg[-1]).strip('-').replace('-', '_')
                    for arg in argv]
            argv = {arg: vars(parsed_args)[arg] for arg in argv
                    if vars(parsed_args)[arg] is not None}

            return command(**argv)

        subparser.set_defaults(command=thunk)
        return command

    return __subcommand


# New command
@subcommand('new',
            dict(name='name', help='The program or component name'),
            dict(name='path', nargs='?', help='path of the program, default current directory'),
            dict(name=['-c', '--component'], action='store_true',
                 help='Force creation of an aos component. Default: auto.'),
            dict(name=['-p', '--program'], action='store_true',
                 help='Force creation of an aos program. Default: auto.'),
            dict(name='--scm', nargs='?',
                 help='Source control management. Currently supported: %s. Default: git' % ', '.join(
                     [s.name for s in scms.values()])),
            dict(name='--aoslib', action='store_true', help='Add the aos component instead of aos into the program.'),
            dict(name='--create-only', action='store_true',
                 help='Only create a program, do not import aos or aos component.'),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch the aos OS repository when creating new program. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol when fetching the aos OS repository when creating new program. Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Create new aos program or component',
            description=(
                    "Create a new aos program (aos new helloworld@mk360 helloworld) or component(aos new helloworld)\n"
                    "Supported source control management: git, hg"))
def new(name, path='.', scm='git', program=False, component=False, aoslib=False, create_only=False, depth=None,
        protocol=None):
    global cwd_root

    if program and component:
        error("Cannot use both --program and --component options.", 1)
    elif program or component:
        d_type = 'component' if component else 'program'
    else:
        d_type = 'component' if len(name.split('@')) != 2 else 'program'

    if d_type == 'program' and len(name.split('@')) != 2:
        error("Program need set application and board, example: helloworld@mk3060!!!")

    d_path = path if os.path.isabs(path) else os.path.abspath(path or os.getcwd() if d_type == 'program' else name)

    if os.path.exists(d_path):
        p = Program(d_path)
        if (d_type == 'program' and not p.is_cwd) or (d_type == 'component' and Repo.isrepo(d_path)):
            error("A %s with name \"%s\" already exists." % (d_type, os.path.basename(d_path)), 1)

    if scm and scm != 'none':
        if os.path.isdir(d_path) and Repo.isrepo(d_path):
            repo = Repo.fromrepo(d_path)
            if repo.scm.name != scm:
                error(
                    "A repository already exists in \"%s\" based on %s. Please select a different name or location." % (
                        d_path, scm), 1)
        else:
            repo_scm = [s for s in scms.values() if s.name == scm.lower()]
            if not repo_scm:
                error(
                    "You have specified invalid source control management system\n"
                    "Please specify one of the following SCMs: %s" % ', '.join([s.name for s in scms.values()]), 1)
            repo_scm[0].init(d_path)
    else:
        scm = 'folder'
        if not os.path.isdir(d_path):
            os.mkdir(d_path)

    if len(os.listdir(d_path)) > 1:
        warning("Directory \"%s\" is not empty." % d_path)

    action("Create new %s \"%s\" (%s) in %s" % (d_type, name.split('@')[0], scm, d_path))
    p = Program(d_path)
    if d_type == 'program':
        # This helps sub-commands to display relative paths to the created program
        cwd_root = os.path.abspath(d_path)
        p.path = cwd_root
        p.set_root()
        d = ''

        if not create_only and not p.get_os_dir() and not p.get_aoslib_dir():
            url = aos_lib_url if aoslib else aos_os_url + '#master'
            d = aoslib if aoslib else 'aos'
            if d == 'aos' and Global().get_cfg(AOS_SDK_PATH):
                action('AOS_SDK_PATH is set as components src.')
            else:
                try:
                    change_path = Global().get_path() if d == 'aos' else d_path
                    with cd(change_path):
                        add(url, depth=depth, protocol=protocol, top=False)
                except Exception as e:
                    if os.path.isdir(os.path.join(d_path, d)):
                        rmtree_readonly(os.path.join(d_path, d))
                    raise e
        if d_path:
            os.chdir(d_path)
            Repo.fromrepo().ignores()

        if d == 'aos':
            build_path = os.path.join(Global().get_cfg(AOS_SDK_PATH), 'build')
            with cd(build_path):
                if not os.path.exists(os.path.join(build_path, 'OpenOCD')):
                    open_ocd_in = urllib2.urlopen(open_ocd_url)
                    open_ocd_zip = 'OpenOCD.zip'
                    with open(open_ocd_zip, 'wb') as fout:
                        fout.write(open_ocd_in.read())

                    if zipfile.is_zipfile(open_ocd_zip):
                        zipfile.ZipFile(open_ocd_zip).extractall()

            get_target_program(d_path, Global().get_cfg(AOS_SDK_PATH), name)
            p.set_cfg(PROGRAM_PATH, d_path)
            p.set_cfg('target', name)
    else:
        p.unset_root(d_path)
        with cd(d_path):
            with open(os.path.join(d_path, name + '.mk'), 'w') as fm:
                makefile_content = 'NAME := %s\n$(NAME)_SOURCES := %s\n$(NAME)_COMPONENTS :=\n$(NAME)_INCLUDES := .\n' % (
                    name, name + '.c')
                fm.write(makefile_content)

            with open(os.path.join(d_path, name + '.c'), 'w') as fc:
                fc.write('//source code file\n')

            with open(os.path.join(d_path, name + '.h'), 'w') as fh:
                fh.write('//head file\n')

    action("Successfully created %s %s in %s" % (d_type, name, d_path))


def get_support_target():
    print("\n                             AliOS-Things PROGRAM TARGET                 ")
    print '|==========================================================================|'
    print '| %-20s | %-50s|' % ('BOARD', 'APP',)
    print '|==========================================================================|'
    for board, app in BOARD_APPS.items():
        print '| %-20s | %-50s|' % (board, ' '.join(app))
    print '|==========================================================================|'


def get_all_official_component():
    makefile_dict = {}
    aos_sdk_path = Global().get_cfg(AOS_SDK_PATH)
    if aos_sdk_path:
        for (dir_path, dir_names, file_names) in os.walk(aos_sdk_path):
            for f in file_names:
                if ('out' not in dir_path) and ('build' not in dir_path) and f.endswith('.mk'):
                    makefile_dict[os.path.join(dir_path, f)] = f[:-3]
    else:
        action(
            'Please set AOS_SDK_PATH when try to get official component or when new an AliOS-Things program default AOS_SDK_PATH set')

    component_mk_dict = {}
    component_name_dict = {}
    for path, name in makefile_dict.items():
        with open(path, 'r') as f:
            s = f.read()
            component_name = re.findall('\s*NAME\s*:=\s*(\S+)\s*\n', s)
            if len(component_name) == 1:
                component_mk_dict[path] = name
                component_name_dict[component_name[0]] = path

    return component_name_dict


def print_component_status():
    official_component_dict = get_all_official_component()
    aos_sdk_path = Global().get_cfg(AOS_SDK_PATH)
    cwd_type = Repo().pathtype()
    if cwd_type != 'program':
        print '\nCurrent directory isn\'t AliOS-Things program, just list all components.'

    print("\n                                                      AliOS-Things COMPONENTS                ")
    print '|===================================================================================================================|'

    if cwd_type != 'program':
        print '| %-30s | %-80s |' % ('NAME', 'LOCATION',)
        for component, path in official_component_dict.items():
            print '| %-30s | %-80s |' % (component, os.path.dirname(os.path.join(OS_NAME, relpath(aos_sdk_path, path))))
    else:
        print '| %-30s | %-70s | %-7s |' % ('NAME', 'LOCATION', 'STATUS')
        pd = Program(os.getcwd())
        with open(os.path.join(pd.get_cfg(PROGRAM_PATH), COMPONENTS), 'r') as f:
            program_component = json.loads(f.read())
        for component, path in official_component_dict.items():
            print '| %-30s | %-70s | %-7s |' % (
            component, os.path.dirname(os.path.join(OS_NAME, relpath(aos_sdk_path, path))),
            'used' if component in program_component else "unused")

    print '|===================================================================================================================|'


BOARD_APPS = {'mk3060': ['alinkapp', 'helloworld', 'linuxapp', 'meshapp', 'tls'],
              'b_l475e': ['mqttapp', 'helloworld', 'tls'],
              'esp32devkitc': ['alinkapp', 'helloworld'],
              'linux': ['alinkapp', 'helloworld', 'linuxapp', 'meshapp', 'tls', 'yts']}


# List command
@subcommand('ls',
            dict(name=['-t', '--target'], action='store_true', help='List AliOS-Things support target.'),
            dict(name=['-c', '--component'], action='store_true', help='List AliOS-Things official components.'),
            help='List cube info',
            description=(
                    "List the aos cube information."))
def list_(target=False, component=False):
    if target:
        get_support_target()
    if component:
        print_component_status()
    # repo = Repo.fromrepo()

    # print "%s (%s)" % (prefix + (relpath(p_path, repo.path) if p_path else repo.name), ((repo.url+('#'+str(repo.rev)[:12] if repo.rev else '') if detailed else str(repo.rev)[:12]) or 'no revision'))

    # for i, lib in enumerate(sorted(repo.libs, key=lambda l: l.path)):
    #     if prefix:
    #         nprefix = prefix[:-3] + ('|  ' if prefix[-3] == '|' else '   ')
    #     else:
    #         nprefix = ''
    #     nprefix += '|- ' if i < len(repo.libs)-1 else '`- '

    #     if lib.check_repo(ignore):
    #         with cd(lib.path):
    #             list_(detailed, nprefix, repo.path, ignore=ignore)


# Import command
@subcommand('import',
            dict(name='url', help='URL of the program'),
            dict(name='path', nargs='?', help='Destination name or path. Default: current directory.'),
            dict(name=['-I', '--ignore'], action='store_true', help='Ignore errors related to cloning and updating.'),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch from the remote repository. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol for the source control management. Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Import program from URL',
            description=(
                    "Imports aos program and its dependencies from a source control based URL\n"
                    "(GitHub, Bitbucket, aos.org) into the current directory or specified\npath.\n"
                    "Use 'aos add <URL>' to add a component into an existing program."))
def import_(url, path=None, ignore=False, depth=None, protocol=None, top=True):
    global cwd_root

    # translate 'aos' to https://code.aliyun.com/aos
    if not Repo.isurl(url) and not os.path.exists(url):
        url = AOS_COMPONENT_BASE_URL + '/' + url + '.git'

    repo = Repo.fromurl(url, path)
    if top:
        p = Program(path)
        if p and not p.is_cwd:
            error(
                "Cannot import program in the specified location \"%s\" because it's already part of a program \"%s\".\n"
                "Please change your working directory to a different location or use \"aos add\" to import the URL as a component." % (
                    os.path.abspath(repo.path), p.name), 1)

    protocol = Program().get_cfg('PROTOCOL', protocol)

    if os.path.isdir(repo.path) and len(os.listdir(repo.path)) > 1 and is_path_component(repo.path):
        # error("Directory \"%s\" is not empty. Please ensure that the destination folder is empty." % repo.path, 1)
        info("Directory \"%s\" is a component." % repo.path, 1)
        return True

    text = "Importing program" if top else "Add component"
    action("%s \"%s\" from \"%s\"%s" % (
        text, os.path.basename(repo.path), formaturl(repo.url, protocol), ' at ' + (repo.revtype(repo.rev, True))))
    if repo.clone(repo.url, repo.path, rev=repo.rev, depth=depth, protocol=protocol):
        with cd(repo.path):
            Program(repo.path).set_root()
            try:
                if repo.rev and repo.getrev() != repo.rev:
                    repo.checkout(repo.rev, True)
            except ProcessException as e:
                err = "Unable to update \"%s\" to %s" % (repo.name, repo.revtype(repo.rev, True))
                if depth:
                    err = err + (
                            "\nThe --depth option might prevent fetching the whole revision tree and checking out %s." % (
                    repo.revtype(repo.rev, True)))
                warning(err)
                return False
    else:
        err = "Unable to clone repository (%s)" % url
        warning(err)
        return False

    if os.path.isdir(repo.path):
        repo.sync()

        if top:  # This helps sub-commands to display relative paths to the imported program
            cwd_root = repo.path

        # if repo.name == 'aos':
        #     target_dir = Program().path
        #     target_name = Program().name
        #     target_file_list = ('.project', '.cproject')
        #     eclipse_subdir = 'Win32' if sys.platform == 'win32' else ('OSX' if sys.platform == 'darwin' else 'Linux64')
        #     temp_dir = os.path.join(Program().path, 'aos/makefiles/eclipse_project', eclipse_subdir)
        #     for file in target_file_list:
        #         with open(os.path.join(temp_dir, file), 'r') as f:
        #             content = f.read()
        #         target_file_name = file
        #         target_file_content = content.replace('template', target_name)
        #         target_file_path = os.path.join(target_dir, target_file_name)
        #         with open(target_file_path, 'w') as f:
        #             f.write(target_file_content)

        with cd(repo.path):
            deploy(ignore=ignore, depth=depth, protocol=protocol, top=False)

#    if top:
#        Program(repo.path).post_action()
    return True


def get_component_official_info(official_component_dict, name):
    component_makefile = ''
    component_name = ''

    if '.' in name or '/' in name:
        name = name.replace('.', os.path.sep)
        rel_makefile = os.path.join(name, os.path.basename(name) + '.mk')
    else:
        rel_makefile = os.path.join(name, name + '.mk')

    if name in official_component_dict:
        component_name = name
        component_makefile = official_component_dict[name]
    else:
        for component, make_file in official_component_dict.items():
            if make_file.endswith(rel_makefile):
                component_name = component
                component_makefile = make_file
                break
    return component_name, component_makefile


def get_component_dependencies(makefile):
    dependencies = []
    if makefile and makefile.endswith('.mk') and os.path.isfile(makefile):
        with open(makefile) as fin:
            for line in fin:
                line = line.strip('\n')
                while line.endswith('\\'):
                    line = line[:-1] + next(fin).rstrip('\n')
                if '$(NAME)_COMPONENTS' in line and not line.strip().startswith('#'):
                    line = line[line.rfind('=') + 1:].strip()
                    components = re.split(r'\s+', line)
                    for co in components:
                        if co:
                            dependencies.append(co)
    return dependencies


def get_component_includes(makefile):
    includes = []
    if makefile and makefile.endswith('.mk') and os.path.isfile(makefile):
        with open(makefile) as fin:
            for line in fin:
                line = line.strip('\n')
                while line.endswith('\\'):
                    line = line[:-1] + next(fin).rstrip('\n')
                if '$(NAME)_INCLUDES' in line and not line.strip().startswith('#'):
                    line = line[line.rfind('=') + 1:].strip()
                    heads = re.split(r'\s+', line)
                    for head in heads:
                        if head:
                            includes.append(head)
    return includes


def add_components_local(name):
    official_component_dict = get_all_official_component()
    component_name, component_makefile = get_component_official_info(official_component_dict, name)

    if component_name not in official_component_dict:
        warning("Component %s isn\'t in AliOS-Things." % (name))
        # error("component (%s) must be in AliOS-Things." % (name))
        return False

    with open(COMPONENTS, 'r') as fin:
        program_component = json.loads(fin.read())
    if component_name in program_component:
        # action("component (%s) is already in current program." % (name))
        return True

    sdk_component_dir = os.path.dirname(component_makefile)
    copy_directory(sdk_component_dir, os.path.abspath(
        os.path.join(os.getcwd(), 'aos', relpath(Global().get_cfg(AOS_SDK_PATH), sdk_component_dir))), True)

    includes = get_component_includes(component_makefile)

    copy_dir_dict = {}
    for include in includes:
        src_dir = os.path.join(os.path.dirname(component_makefile), include)
        dst_dir = os.path.join(os.getcwd(), 'aos', relpath(Global().get_cfg(AOS_SDK_PATH), src_dir))
        copy_dir_dict[src_dir] = dst_dir

    aos_sdk_path = Global().get_cfg(AOS_SDK_PATH)
    order_copy_dir_dict = collections.OrderedDict(sorted(copy_dir_dict.items()))
    for src_dir, dst_dir in order_copy_dir_dict.items():
        is_component = is_path_component(src_dir)
        while not is_component and src_dir != aos_sdk_path:
            src_dir = os.path.dirname(src_dir)
            dst_dir = os.path.dirname(dst_dir)
            is_component = is_path_component(src_dir)

        if is_component:
            copy_directory(src_dir, dst_dir)

    location = os.path.join('aos', relpath(Global().get_cfg(AOS_SDK_PATH), sdk_component_dir))
    dependencies = get_component_dependencies(component_makefile)
    origin = 'local'

    ref = ''
    aos_sdk_path = Global().get_cfg(AOS_SDK_PATH)
    if Repo.isrepo(aos_sdk_path):
        ref = get_component_ref(Repo.fromrepo(aos_sdk_path))

    action('Add component %s (%s) in %s' % (component_name, origin, location))
    program_component[component_name] = {'location': location, 'dependencies': dependencies, 'status': 'used',
                                         'origin': origin, 'ref': ref}
    with open(COMPONENTS, 'w') as fout:
        fout.write(json.dumps(program_component, sort_keys=True, indent=4))

    for dep in dependencies:
        add_components_local(dep)

    return True


def add_components_remote(base_url, scm, name):
    is_local = add_components_local(name)
    if not is_local:
        # clone from the same as name base url
        lib = Repo.fromurl(base_url + '/' + name + '.' + scm.name)
        is_import_success = import_(lib.fullurl, lib.path, True, None, None, False)
        if not is_import_success and base_url != AOS_COMPONENT_BASE_URL:
            # clone from aos component url
            lib = Repo.fromurl(AOS_COMPONENT_BASE_URL + '/' + name + '.' + scm.name)
            is_import_success = import_(lib.fullurl, lib.path, True, None, None, False)

        if not is_import_success:
            error('Component %s can\'t find in AOS_SDK_PATH && %s && %s' % (name, base_url, AOS_COMPONENT_BASE_URL))

        lib.sync()

        pd = Program(os.getcwd())
        with open(COMPONENTS, 'r') as fin:
            program_component = json.loads(fin.read())
        if lib.name in program_component:
            action("Component %s has added in current program." % (lib.name))
            return True
        else:
            location = relpath(pd.get_cfg(PROGRAM_PATH), lib.path)
            dependencies = get_component_dependencies(os.path.join(location, lib.name + '.mk'))
            ref = get_component_ref(lib)
            origin = 'remote'
            action('Add component %s (%s) in %s' % (lib.name, origin, location))
            program_component[lib.name] = {'location': location, 'dependencies': dependencies, 'status': 'used',
                                           'origin': origin, 'ref': ref}
            with open(COMPONENTS, 'w') as fout:
                fout.write(json.dumps(program_component, sort_keys=True, indent=4))

            for dep in dependencies:
                add_components_remote(lib.url[:lib.url.rfind('/')], lib.scm, dep)

    return True


# Add component command
@subcommand('add',
            dict(name='name', help='The component name or URL of the component'),
            # dict(name='url', nargs='?', help='URL of the component'),
            # dict(name='path', nargs='?', help='Destination name or path. Default: current folder.'),
            dict(name=['-I', '--ignore'], action='store_true', help='Ignore errors related to cloning and updating.'),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch from the remote repository. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol for the source control management. Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Add component from AOS_SDK_PATH or URL',
            description=(
                    "Add AliOS-Things component from AOS_SDK_PATH(with dependencies) or GitHub URL(no dependencies) into an existing program.\n"
                    "Use 'aos new TARGET' to new as a program"))
def add(name, path=None, ignore=False, depth=None, protocol=None, top=True):
    # translate 'aos' to https://code.aliyun.com/aos
    # if not Repo.isurl(url) and not os.path.exists(url):
    #     url = AOS_COMPONENT_BASE_URL+'/'+url+'.git'

    if Repo.isurl(name):
        # repo = Repo.fromrepo()

        lib = Repo.fromurl(name, path)
        if lib.name != OS_NAME and Repo().pathtype() != 'program':
            error('Add component must in AliOS-Things program directory')

        import_(lib.fullurl, lib.path, ignore=ignore, depth=depth, protocol=protocol, top=False)
        # repo.ignore(relpath(repo.path, lib.path))
        lib.sync()

        if lib.name != OS_NAME:
            pd = Program(os.getcwd())
            with cd(pd.get_cfg(PROGRAM_PATH)):
                with open(COMPONENTS, 'r') as fin:
                    program_component = json.loads(fin.read())
                if lib.name in program_component:
                    action("Component %s has added in current program." % (lib.name))
                    return
                else:
                    location = relpath(pd.get_cfg(PROGRAM_PATH), lib.path)
                    dependencies = get_component_dependencies(os.path.join(location, lib.name + '.mk'))
                    ref = get_component_ref(lib)
                    origin = 'remote'
                    action('Add component %s (%s) in %s' % (lib.name, origin, location))
                    program_component[lib.name] = {'location': location, 'dependencies': dependencies, 'status': 'used',
                                                   'origin': origin, 'ref': ref}
                    with open(COMPONENTS, 'w') as fout:
                        fout.write(json.dumps(program_component, sort_keys=True, indent=4))

                    for dep in dependencies:
                        add_components_remote(lib.url[:lib.url.rfind('/')], lib.scm, dep)

        # lib.write()
        # repo.add(lib.lib)

    else:
        cwd_type = Repo().pathtype()
        if cwd_type != 'program':
            error('Add component must in AliOS-Things program directory')

        pd = Program(os.getcwd())
        with cd(pd.get_cfg(PROGRAM_PATH)):
            with open(COMPONENTS, 'r') as fin:
                program_component = json.loads(fin.read())
            if name in program_component:
                action("Component %s has added in current program." % (name))
                return
            else:
                add_components_local(name)


#    if top:
#        Program(repo.path).post_action()

def remove_components(name, recursive=False):
    official_component_dict = get_all_official_component()
    component_name, component_makefile = get_component_official_info(official_component_dict, name)

    with open(COMPONENTS, 'r') as fin:
        program_component = json.loads(fin.read())

    if component_name in program_component:
        location = program_component[component_name]['location']
        dependencies = program_component[component_name]['dependencies']
        origin = program_component[component_name]['origin']

        action('Remove component %s (%s) in %s' % (component_name, origin, location))
        del program_component[component_name]

        with open(COMPONENTS, 'w') as fout:
            fout.write(json.dumps(program_component, sort_keys=True, indent=4))

        if recursive:
            for dep in dependencies:
                only_subtree = True
                for component, component_info in program_component.items():
                    if component_info and (dep in component_info['dependencies']):
                        only_subtree = False
                        break
                if only_subtree:
                    remove_components(dep, True)
    elif name in program_component:
        origin = program_component[name]['origin']
        if origin == 'remote':
            location = program_component[name]['location']
            action('Remove component %s (%s) in %s' % (name, origin, location))
            del program_component[name]
            with open(COMPONENTS, 'w') as fout:
                fout.write(json.dumps(program_component, sort_keys=True, indent=4))
        else:
            action("Component %s isn't in current program." % (name))


# Remove component
@subcommand('rm',
            dict(name='name', help='Component name'),
            help='Remove component',
            description=(
                    "Remove specified component, its dependencies and references from the current\n"
                    "You can re-add the component from AOS_SDK_PATH or URL via 'aos add name>'."))
def remove(name):
    cwd_type = Repo().pathtype()
    if cwd_type != 'program':
        error('Remove component must in AliOS-Things program directory')

    pd = Program(os.getcwd())
    with cd(pd.get_cfg(PROGRAM_PATH)):
        with open(COMPONENTS, 'r') as fin:
            program_component = json.loads(fin.read())
        if name not in program_component:
            action("Component %s isn't in current program." % (name))
            return
        else:
            remove_components(name, True)

    # repo = Repo.fromrepo()
    # if not Repo.isrepo(path):
    #     error("Could not find component in path (%s)" % path, 1)

    # lib = Repo.fromrepo(path)
    # action("Removing component \"%s\" in \"%s\"" % (lib.name, lib.path))
    # rmtree_readonly(lib.path)
    # repo.remove(lib.lib)
    # repo.unignore(relpath(repo.path, lib.path))


# Deploy command
@subcommand('deploy',
            dict(name=['-I', '--ignore'], action='store_true', help='Ignore errors related to cloning and updating.'),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch from the remote repository. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol for the source control management. Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Find and add missing components and source codes',
            description=(
                    "Import missing dependencies in an existing program or component.\n"
                    "Use 'aos import <URL>' and 'aos add <URL>' instead of cloning manually and\n"
                    "then running 'aos deploy'"))
def deploy(ignore=False, depth=None, protocol=None, top=True):
    repo = Repo.fromrepo()
    repo.ignores()

    for lib in repo.libs:
        if os.path.isdir(lib.path):
            if lib.check_repo():
                with cd(lib.path):
                    update(lib.rev, ignore=ignore, depth=depth, protocol=protocol, top=False)
        else:
            import_(lib.fullurl, lib.path, ignore=ignore, depth=depth, protocol=protocol, top=False)
            repo.ignore(relpath(repo.path, lib.path))


#    if top:
#        program = Program(repo.path)
#        program.post_action()
#        if program.is_classic:
#            program.update_tools('.temp')

# Source command
@subcommand('codes',
            dict(name='name', help='Destination component name without suffix'),
            dict(name=['-I', '--ignore'], action='store_true', help='Ignore errors related to cloning and updating.'),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch from the remote repository. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol for the source control management. Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Import the optional component from the remote repository',
            description=(
                    "Import optional component defined by .codes file.\n"
                    "name of the .codes file should be specified ."))
def codes(name, ignore=False, depth=None, protocol=None, top=True):
    repo = Repo.fromrepo()
    code = Repo.fromcode(os.path.join(os.getcwd(), name + '.codes'))

    if os.path.isdir(code.path):
        if code.check_repo():
            with cd(code.path):
                update(code.rev, ignore=ignore, depth=depth, protocol=protocol, top=False)
    else:
        import_(code.fullurl, code.path, ignore=ignore, depth=depth, protocol=protocol, top=False)
        print '>>>>', repo.path, code.path
        repo.ignore(relpath(repo.path, code.path))


# Publish command
@subcommand('publish',
            dict(name=['-A', '--all'], dest='all_refs', action='store_true',
                 help='Publish all branches, including new ones. Default: push only the current branch.'),
            dict(name=['-M', '--message'], dest='msg', type=str, nargs='?',
                 help='Commit message. Default: prompts for commit message.'),
            help='Publish program or component',
            description=(
                    "Publishes the current program or component and all dependencies to their\nassociated remote repository URLs.\n"
                    "This command performs various consistency checks for local uncommitted changes\n"
                    "and unpublished revisions and encourages to commit/push them.\n"
                    "Online guide about collaboration is available at:\n"
                    "www.aos.com/collab_guide"))
def publish(all_refs=None, msg=None, top=True):
    if top:
        action("Checking for local modifications...")

    repo = Repo.fromrepo()
    if repo.is_local:
        error(
            "%s \"%s\" in \"%s\" with %s is a local repository.\nPlease associate it with a remote repository URL before attempting to publish.\n"
            "Read more about publishing local repositories here:\nhttps://code.aliyun.com/aos/aos-cube/#publishing-local-program-or-component" % (
            "Program" if top else "Library", repo.name, repo.path, repo.scm.name), 1)

    for lib in repo.libs:
        if lib.check_repo():
            with cd(lib.path):
                progress()
                publish(all_refs, msg=msg, top=False)

    sync(recursive=False)

    if repo.dirty():
        action("Uncommitted changes in %s \"%s\" in \"%s\"" % (repo.pathtype(repo.path), repo.name, repo.path))
        if msg:
            repo.commit(msg)
        else:
            raw_input('Press enter to commit and publish: ')
            repo.commit()

    try:
        outgoing = repo.outgoing()
        if outgoing > 0:
            action("Pushing local repository \"%s\" to remote \"%s\"" % (repo.name, repo.url))
            repo.publish(all_refs)
        else:
            if top:
                action("Nothing to publish to the remote repository (the source tree is unmodified)")
    except ProcessException as e:
        if e[0] != 1:
            raise e


# Update command
@subcommand('update',
            dict(name='rev', nargs='?', help='Revision, tag or branch'),
            dict(name=['-C', '--clean'], action='store_true',
                 help='Perform a clean update and discard all modified or untracked files. WARNING: This action cannot be undone. Use with caution.'),
            dict(name='--clean-files', action='store_true',
                 help='Remove any local ignored files. Requires \'--clean\'. WARNING: This will wipe all local uncommitted, untracked and ignored files. Use with extreme caution.'),
            dict(name='--clean-deps', action='store_true',
                 help='Remove any local libraries and also libraries containing uncommitted or unpublished changes. Requires \'--clean\'. WARNING: This action cannot be undone. Use with caution.'),
            dict(name=['-I', '--ignore'], action='store_true',
                 help='Ignore errors related to unpublished libraries, unpublished or uncommitted changes, and attempt to update from associated remote repository URLs.'),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch from the remote repository. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol for the source control management. Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Update to branch, tag, revision or latest',
            description=(
                    "Updates the current program or component and its dependencies to specified\nbranch, tag or revision.\n"
                    "Alternatively fetches from associated remote repository URL and updates to the\n"
                    "latest revision in the current branch."))
def update(rev=None, clean=False, clean_files=False, clean_deps=False, ignore=False, top=True, depth=None,
           protocol=None):
    if top and clean:
        sync()

    cwd_type = Repo.pathtype(cwd_root)
    cwd_dest = "program" if cwd_type == "directory" else "component"

    repo = Repo.fromrepo()
    # A copy of repo containing the .lib layout before updating
    repo_orig = Repo.fromrepo()

    if top and not rev and repo.isdetached():
        error(
            "This %s is in detached HEAD state, and you won't be able to receive updates from the remote repository until you either checkout a branch or create a new one.\n"
            "You can checkout a branch using \"%s checkout <branch_name>\" command before running \"aos update\"." % (
            cwd_type, repo.scm.name), 1)

    if repo.is_local and not repo.rev:
        action("Skipping unpublished empty %s \"%s\"" % (
            cwd_type if top else cwd_dest,
            os.path.basename(repo.path) if top else relpath(cwd_root, repo.path)))
    else:
        # Fetch from remote repo
        action("Updating %s \"%s\" to %s" % (
            cwd_type if top else cwd_dest,
            os.path.basename(repo.path) if top else relpath(cwd_root, repo.path),
            repo.revtype(rev, True)))

        try:
            repo.update(rev, clean, clean_files, repo.is_local)
        except ProcessException as e:
            err = "Unable to update \"%s\" to %s" % (repo.name, repo.revtype(rev, True))
            if depth:
                err = err + (
                        "\nThe --depth option might prevent fetching the whole revision tree and checking out %s." % (
                repo.revtype(repo.rev, True)))
            if ignore:
                warning(err)
            else:
                error(err, e[0])

        repo.rm_untracked()
        if top and cwd_type == 'component':
            repo.sync()
            repo.write()

    # Compare component references (.lib) before and after update, and remove libraries that do not have references in the current revision
    for lib in repo_orig.libs:
        if not os.path.isfile(lib.lib) and os.path.isdir(
                lib.path):  # Library reference doesn't exist in the new revision. Will try to remove component to reproduce original structure
            gc = False
            with cd(lib.path):
                lib_repo = Repo.fromrepo(lib.path)
                gc, msg = lib_repo.can_update(clean, clean_deps)
            if gc:
                action("Remove component \"%s\" (obsolete)" % (relpath(cwd_root, lib.path)))
                rmtree_readonly(lib.path)
                repo.unignore(relpath(repo.path, lib.path))
            else:
                if ignore:
                    warning(msg)
                else:
                    error(msg, 1)

    # Reinitialize repo.libs() to reflect the component files after update
    repo.sync()

    # Recheck libraries as their urls might have changed
    for lib in repo.libs:
        if os.path.isdir(lib.path) and Repo.isrepo(lib.path):
            lib_repo = Repo.fromrepo(lib.path)
            if (not lib.is_local and not lib_repo.is_local and
                    formaturl(lib.url, 'https') != formaturl(lib_repo.url, 'https')):  # Repository URL has changed
                gc = False
                with cd(lib.path):
                    gc, msg = lib_repo.can_update(clean, clean_deps)
                if gc:
                    action(
                        "Remove component \"%s\" (changed URL). Will add from new URL." % (relpath(cwd_root, lib.path)))
                    rmtree_readonly(lib.path)
                    repo.unignore(relpath(repo.path, lib.path))
                else:
                    if ignore:
                        warning(msg)
                    else:
                        error(msg, 1)

    # Import missing repos and update to revs
    for lib in repo.libs:
        if not os.path.isdir(lib.path):
            import_(lib.fullurl, lib.path, ignore=ignore, depth=depth, protocol=protocol, top=False)
            repo.ignore(relpath(repo.path, lib.path))
        else:
            with cd(lib.path):
                update(lib.rev, clean=clean, clean_files=clean_files, clean_deps=clean_deps, ignore=ignore, top=False)


#    if top:
#        program = Program(repo.path)
#        program.set_root()
#        program.post_action()
#        if program.is_classic:
#            program.update_tools('.temp')


# Synch command
@subcommand('sync',
            help='Synchronize aos component references',
            description=(
                    "Synchronizes all component and dependency references (.component files) in the\n"
                    "current program or component.\n"
                    "Note that this will remove all invalid component references."))
def sync(recursive=True, keep_refs=False, top=True):
    if top and recursive:
        action("Synchronizing dependency references...")

    repo = Repo.fromrepo()
    repo.ignores()

    for lib in repo.libs:
        if os.path.isdir(lib.path):
            lib.check_repo()
            lib.sync()
            lib.write()
            repo.ignore(relpath(repo.path, lib.path))
            progress()
        else:
            if not keep_refs:
                action("Remove reference \"%s\" -> \"%s\"" % (lib.name, lib.fullurl))
                repo.remove(lib.lib)
                repo.unignore(relpath(repo.path, lib.path))

    for code in repo.codes:
        if os.path.isdir(code.path):
            code.check_repo()
            code.sync()
            code.write_codes()
            repo.ignore(relpath(repo.path, code.path))
            progress()

    for root, dirs, files in os.walk(repo.path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        for d in list(dirs):
            if not Repo.isrepo(os.path.join(root, d)):
                continue

            lib = Repo.fromrepo(os.path.join(root, d))
            if os.path.isfile(lib.lib) or os.path.isfile(lib.code):
                dirs.remove(d)
                continue

            dirs.remove(d)
            lib.write()
            repo.ignore(relpath(repo.path, lib.path))
            repo.add(lib.lib)
            progress()

    repo.sync()

    if recursive:
        for lib in repo.libs:
            if lib.check_repo():
                with cd(lib.path):
                    sync(keep_refs=keep_refs, top=False)

    # Update the .lib reference in the parent repository
    cwd_type = Repo.pathtype(cwd_root)
    if top and cwd_type == "component":
        repo = Repo.fromrepo()
        repo.write()


# Command status for cross-SCM status of repositories
@subcommand('status',
            dict(name=['-I', '--ignore'], action='store_true', help='Ignore errors related to missing libraries.'),
            help='Show version control status\n\n',
            description=(
                    "Show uncommitted changes a program or component and its dependencies."))
def status_(ignore=False):
    repo = Repo.fromrepo()
    if repo.dirty():
        action("Status for \"%s\":" % repo.name)
        log(repo.status() + "\n")

    for lib in repo.libs:
        if lib.check_repo(ignore):
            with cd(lib.path):
                status_(ignore)


# Make command
@subcommand('make',
            help='Make aos program/component',
            description=(
                    "Make aos program/component."))
def make():
    # Get the make arguments
    make_args = ' '.join(sys.argv[2:])

    # aos new program
    if os.path.isfile(os.path.join(os.getcwd(), Cfg.file)):
        pd = Program(os.getcwd())
        program_path = pd.get_cfg(PROGRAM_PATH)

        program_components = 'auto_component'
        with open(os.path.join(program_path, COMPONENTS), 'r') as fin:
            json_components = json.loads(fin.read())
            root_dir = ['example', 'board', 'kernel', 'platform', 'utility', 'framework', 'tools', 'test', 'device',
                        'security']
            for component, info in json_components.items():
                location = relpath('aos', info['location']) if info['location'].startswith('aos') else info['location']
                for root in root_dir:
                    if location.startswith(root + os.sep) and len(location) >= (len(root) + 1):
                        location = location[len(root) + 1:]
                program_components += '@' + location if program_components else location

        program_components = 'DEFAULT_ALL_COMPONENTS=' + program_components
        app_path = 'APPDIR=' + os.path.dirname(pd.get_cfg(APP_PATH))
        os_path = pd.get_cfg(OS_PATH)
        out_path = 'BUILD_DIR=' + os.path.join(os.getcwd(), 'out')

        with cd(os_path):
            _run_make(['-e', '-f build/Makefile', make_args, program_components, app_path, out_path])
    else:
        # aos source code
        _run_make(['-e', '-f build/Makefile', make_args])


# Make command
@subcommand('makelib',
            dict(name='path', nargs='?', help='Library directory path.'),
            dict(name=['-N', '--new'], dest='new', action='store_true', help='Create a library configure makefile .'),
            dict(name=['-r', '--arch'],
                 help='The arch for static library compiling. E.g. "Cortex-M3", "Cortex-M4", "Cortex-M4F", "ARM968E-S", "linux"'),
            help='Compile static library\n\n',
            description=(
                    "Compile static library."))
def makelib(path, arch=None, new=False):
    if new:
        root_dir = Program().path
        with open(os.path.join(root_dir, 'build/template.mk'), 'r') as f:
            content = f.read()
        with open(os.path.join(root_dir, path, os.path.basename(path) + '_src.mk'), 'w') as f:
            f.write(content.replace('template', os.path.basename(path)))
        return

    if arch:
        _run_make(['-e', 'LIB_DIR=' + path, 'TARGET_ARCH=' + arch, '-f build/aos_library_makefile.mk'])
        return

    host_arch = ['Cortex-M3', 'Cortex-M4', 'Cortex-M4F', 'ARM968E-S', 'linux']
    for arch in host_arch:
        _run_make(['-e', 'LIB_DIR=' + path, 'TARGET_ARCH=' + arch, '-f build/aos_library_makefile.mk'])


# Generic config command
@subcommand('config',
            dict(name='var', nargs='?', help='Variable name. E.g. "AOS_SDK_PATH"'),
            dict(name='value', nargs='?',
                 help='Value. Will show the currently set default value for a variable if not specified.'),
            dict(name=['-g', '--global'], dest='global_cfg', action='store_true',
                 help='Use global settings, not local'),
            dict(name=['-u', '--unset'], dest='unset', action='store_true', help='Unset the specified variable.'),
            dict(name=['-l', '--list'], dest='list_config', action='store_true', help='List aos tool configuration.'),
            help='Tool configuration\n\n',
            description=(
                    "Gets, sets or unsets aos tool configuration options.\n"
                    "Options can be global (via the --global switch) or local (per program)\n"
                    "Global options are always overridden by local/program options.\n"
                    "Currently supported options: aosder, protocol, depth, cache"))
def config_(var=None, value=None, global_cfg=False, unset=False, list_config=False):
    name = var
    var = str(var).upper()

    if list_config:
        g = Global()
        g_vars = g.list_cfg().items()
        action("Global config:")
        if g_vars:
            for v in g_vars:
                log("%s=%s\n" % (v[0], v[1]))
        else:
            log("No global configuration is set\n")
        log("\n")

        p = Program(os.getcwd())
        action("Local config (%s):" % p.path)
        if not p.is_cwd:
            p_vars = p.list_cfg().items()
            if p_vars:
                for v in p_vars:
                    log("%s=%s\n" % (v[0], v[1]))
            else:
                log("No local configuration is set\n")
        else:
            log("Couldn't find valid aos program in %s\n" % p.path)

    elif name:
        if global_cfg:
            # Global configuration
            g = Global()
            if unset:
                g.set_cfg(var, None)
                action('Unset global %s' % name)
            elif value:
                g.set_cfg(var, value)
                action('%s now set as global %s' % (value, name))
            else:
                value = g.get_cfg(var)
                action(('%s' % value) if value else 'No global %s set' % (name))
        else:
            # Find the root of the program
            program = Program(os.getcwd())
            if program.is_cwd and not var == 'ROOT':
                error(
                    "Could not find aos program in current path \"%s\".\n"
                    "Change the current directory to a valid aos program, set the current directory as an aos program with 'aos config root .', or use the '--global' option to set global configuration." % program.path)
            with cd(program.path):
                if unset:
                    program.set_cfg(var, None)
                    action('Unset default %s in program "%s"' % (name, program.name))
                elif value:
                    program.set_cfg(var, value)
                    action('%s now set as default %s in program "%s"' % (value, name, program.name))
                else:
                    value = program.get_cfg(var)
                    action(('%s' % value) if value else 'No default %s set in program "%s"' % (name, program.name))
    else:
        subcommands['config'].error("too few arguments")


@subcommand('help',
            help='This help screen')
def help_():
    return parser.print_help()


def main():
    global verbose, very_verbose, remainder, cwd_root

    reload(sys)
    sys.setdefaultencoding('UTF8')

    # Help messages adapt based on current dir
    cwd_root = os.getcwd()

    if sys.version_info[0] != 2 or sys.version_info[1] < 7:
        error(
            "aos cube is compatible with Python version >= 2.7 and < 3.0\n"
            "Please refer to the online guide available at https://code.aliyun.com/aos/aos-cube")

    # Parse/run command
    if len(sys.argv) <= 1:
        help_()
        sys.exit(1)

    if '--version' in sys.argv:
        log(ver + "\n")
        sys.exit(0)

    pargs, remainder = parser.parse_known_args()
    status = 1

    try:
        very_verbose = pargs.very_verbose
        verbose = very_verbose or pargs.verbose
        info('Working path \"%s\" (%s)' % (os.getcwd(), Repo.pathtype(cwd_root)))
        status = pargs.command(pargs)
    except ProcessException as e:
        error(
            "\"%s\" returned error code %d.\n"
            "Command \"%s\" in \"%s\"" % (e[1], e[0], e[2], e[3]), e[0])
    except OSError as e:
        if e[0] == errno.ENOENT:
            error(
                "Could not detect one of the command-line tools.\n"
                "You could retry the last command with \"-v\" flag for verbose output\n", e[0])
        else:
            error('OS Error: %s' % e[1], e[0])
    except KeyboardInterrupt as e:
        info('User aborted!', -1)
        sys.exit(255)
    except Exception as e:
        if very_verbose:
            traceback.print_exc(file=sys.stdout)
        error("Unknown Error: %s" % e, 255)
    sys.exit(status or 0)


if __name__ == "__main__":
    main()
