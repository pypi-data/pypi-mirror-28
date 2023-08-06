import glob
import os
import platform

import subprocess
from contextlib import contextmanager

from conans.client.tools.env import environment_append
from conans.client.tools.files import unix_path, MSYS2, WSL, which
from conans.client.tools.oss import cpu_count, detected_architecture, os_info
from conans.errors import ConanException
from conans.util.files import decode_text

_global_output = None


def msvc_build_command(settings, sln_path, targets=None, upgrade_project=True, build_type=None,
                       arch=None, parallel=True, force_vcvars=False, toolset=None):
    """ Do both: set the environment variables and call the .sln build
    """
    vcvars = vcvars_command(settings, force=force_vcvars)
    build = build_sln_command(settings, sln_path, targets, upgrade_project, build_type, arch,
                              parallel, toolset=toolset)
    command = "%s && %s" % (vcvars, build)
    return command


def build_sln_command(settings, sln_path, targets=None, upgrade_project=True, build_type=None,
                      arch=None, parallel=True, toolset=None):
    """
    Use example:
        build_command = build_sln_command(self.settings, "myfile.sln", targets=["SDL2_image"])
        command = "%s && %s" % (tools.vcvars_command(self.settings), build_command)
        self.run(command)
    """
    targets = targets or []
    command = "devenv %s /upgrade && " % sln_path if upgrade_project else ""
    build_type = build_type or settings.build_type
    arch = arch or settings.arch
    if not build_type:
        raise ConanException("Cannot build_sln_command, build_type not defined")
    if not arch:
        raise ConanException("Cannot build_sln_command, arch not defined")
    command += "msbuild %s /p:Configuration=%s" % (sln_path, build_type)
    arch = str(arch)
    msvc_arch = {'x86': 'x86',
                 'x86_64': 'x64',
                 'armv7': 'ARM',
                 'armv8': 'ARM64'}.get(arch)
    if msvc_arch:
        command += ' /p:Platform="%s"' % msvc_arch

    if parallel:
        command += ' /m:%s' % cpu_count()

    if targets:
        command += " /target:%s" % ";".join(targets)

    if toolset:
        command += " /p:PlatformToolset=%s" % toolset

    return command


def vs_installation_path(version):
    if not hasattr(vs_installation_path, "_cached"):
        vs_installation_path._cached = dict()

    if version not in vs_installation_path._cached:
        vs_path = None
        program_files = os.environ.get("ProgramFiles(x86)", os.environ.get("ProgramFiles"))
        if program_files:
            vswhere_path = os.path.join(program_files, "Microsoft Visual Studio", "Installer",
                                        "vswhere.exe")
            if os.path.isfile(vswhere_path):
                version_range = "[%d.0, %d.0)" % (int(version), int(version) + 1)
                try:
                    output = subprocess.check_output([vswhere_path, "-version", version_range,
                                                      "-legacy", "-property", "installationPath"])
                    vs_path = output.decode().strip()
                    _global_output.info("vswhere detected VS %s in %s" % (version, vs_path))
                except (ValueError, subprocess.CalledProcessError, UnicodeDecodeError) as e:
                    _global_output.error("vswhere error: %s" % str(e))

        # Remember to cache result
        vs_installation_path._cached[version] = vs_path

    return vs_installation_path._cached[version]


def find_windows_10_sdk():
    """finds valid Windows 10 SDK version which can be passed to vcvarsall.bat (vcvars_command)"""
    # uses the same method as VCVarsQueryRegistry.bat
    from six.moves import winreg  # @UnresolvedImport
    hives = [
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Wow6432Node'),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE')
    ]
    for key, subkey in hives:
        try:
            hkey = winreg.OpenKey(key, r'%s\Microsoft\Microsoft SDKs\Windows\v10.0' % subkey)
            installation_folder, _ = winreg.QueryValueEx(hkey, 'InstallationFolder')
            if os.path.isdir(installation_folder):
                include_dir = os.path.join(installation_folder, 'include')
                for sdk_version in os.listdir(include_dir):
                    if os.path.isdir(os.path.join(include_dir, sdk_version)) and sdk_version.startswith('10.'):
                        windows_h = os.path.join(include_dir, sdk_version, 'um', 'Windows.h')
                        if os.path.isfile(windows_h):
                            return sdk_version
        except EnvironmentError:
            pass
        finally:
            winreg.CloseKey(hkey)
    return None


def vcvars_command(settings, arch=None, compiler_version=None, force=False):
    arch_setting = arch or settings.get_safe("arch")
    compiler_version = compiler_version or settings.get_safe("compiler.version")
    os_setting = settings.get_safe("os")
    if not compiler_version:
        raise ConanException("compiler.version setting required for vcvars not defined")

    # https://msdn.microsoft.com/en-us/library/f2ccy3wt.aspx
    arch_setting = arch_setting or 'x86_64'
    if detected_architecture() == 'x86_64':
        vcvars_arch = {'x86': 'x86',
                       'x86_64': 'amd64',
                       'armv7': 'amd64_arm',
                       'armv8': 'amd64_arm64'}.get(arch_setting)
    elif detected_architecture() == 'x86':
        vcvars_arch = {'x86': 'x86',
                       'x86_64': 'x86_amd64',
                       'armv7': 'x86_arm',
                       'armv8': 'x86_arm64'}.get(arch_setting)
    if not vcvars_arch:
        raise ConanException('unsupported architecture %s' % arch_setting)
    existing_version = os.environ.get("VisualStudioVersion")
    if existing_version:
        command = "echo Conan:vcvars already set"
        existing_version = existing_version.split(".")[0]
        if existing_version != compiler_version:
            message = "Visual environment already set to %s\n " \
                      "Current settings visual version: %s" % (existing_version, compiler_version)
            if not force:
                raise ConanException("Error, %s" % message)
            else:
                _global_output.warn(message)
    else:
        env_var = "vs%s0comntools" % compiler_version

        if env_var == 'vs150comntools':
            vs_path = os.getenv(env_var)
            if not vs_path:  # Try to locate with vswhere
                vs_root = vs_installation_path("15")
                if vs_root:
                    vs_path = os.path.join(vs_root, "Common7", "Tools")
                else:
                    raise ConanException("VS2017 '%s' variable not defined, "
                                         "and vswhere didn't find it" % env_var)
            if not os.path.isdir(vs_path):
                _global_output.warn('VS variable %s points to the non-existing path "%s",'
                    'please check that you have set it correctly' % (env_var, vs_path))
            vcvars_path = os.path.join(vs_path, "../../VC/Auxiliary/Build/vcvarsall.bat")
            command = ('set "VSCMD_START_DIR=%%CD%%" && '
                       'call "%s" %s' % (vcvars_path, vcvars_arch))
        else:
            try:
                vs_path = os.environ[env_var]
            except KeyError:
                raise ConanException("VS '%s' variable not defined. Please install VS" % env_var)
            if not os.path.isdir(vs_path):
                _global_output.warn('VS variable %s points to the non-existing path "%s",'
                    'please check that you have set it correctly' % (env_var, vs_path))
            vcvars_path = os.path.join(vs_path, "../../VC/vcvarsall.bat")
            command = ('call "%s" %s' % (vcvars_path, vcvars_arch))

    if os_setting == 'WindowsStore':
        os_version_setting = settings.get_safe("os.version")
        if os_version_setting == '8.1':
            command += ' store 8.1'
        elif os_version_setting == '10.0':
            windows_10_sdk = find_windows_10_sdk()
            if not windows_10_sdk:
                raise ConanException("cross-compiling for WindowsStore 10 (UWP), "
                                     "but Windows 10 SDK wasn't found")
            command += ' store ' + windows_10_sdk
        else:
            raise ConanException('unsupported Windows Store version %s' % os_version_setting)
    return command


def vcvars_dict(settings, arch=None, compiler_version=None, force=False, filter_known_paths=True):
    cmd = vcvars_command(settings, arch=arch,
                         compiler_version=compiler_version, force=force) + " && echo __BEGINS__ && set"
    ret = decode_text(subprocess.check_output(cmd, shell=True))
    new_env = {}
    start_reached = False
    for line in ret.splitlines():
        if not start_reached:
            if "__BEGINS__" in line:
                start_reached = True
            continue
        name_var, value = line.split("=", 1)
        new_env[name_var] = value

    if filter_known_paths:
        def relevant_path(path):
            path = path.replace("\\", "/").lower()
            keywords = "msbuild", "visual", "microsoft", "/msvc/", "/vc/", "system32", "windows"
            return any(word in path for word in keywords)

        path = new_env.get("PATH", "").split(";")
        path = [entry for entry in path if relevant_path(entry)]
        new_env["PATH"] = ";".join(path)

    return new_env


@contextmanager
def vcvars(*args, **kwargs):
    new_env = vcvars_dict(*args, **kwargs)
    with environment_append(new_env):
        yield


def escape_windows_cmd(command):
    """ To use in a regular windows cmd.exe
        1. Adds escapes so the argument can be unpacked by CommandLineToArgvW()
        2. Adds escapes for cmd.exe so the argument survives cmd.exe's substitutions.

        Useful to escape commands to be executed in a windows bash (msys2, cygwin etc)
    """
    quoted_arg = subprocess.list2cmdline([command])
    return "".join(["^%s" % arg if arg in r'()%!^"<>&|' else arg for arg in quoted_arg])


def get_cased_path(name):
    if platform.system() != "Windows":
        return name
    if not os.path.isabs(name):
        raise ConanException("get_cased_path requires an absolute path")
    dirs = name.split('\\')
    # disk letter
    test_name = [dirs[0].upper()]
    for d in dirs[1:]:
        test_name += ["%s[%s]" % (d[:-1], d[-1])]  # This brackets do the trick to match cased

    res = glob.glob('\\'.join(test_name))
    if not res:
        # File not found
        return None
    return res[0]


def run_in_windows_bash(conanfile, bashcmd, cwd=None, subsystem=None, msys_mingw=True, env=None):
    """ Will run a unix command inside a bash terminal
        It requires to have MSYS2, CYGWIN, or WSL
    """
    env = env or {}
    if platform.system() != "Windows":
        raise ConanException("Command only for Windows operating system")
    subsystem = subsystem or os_info.detect_windows_subsystem()

    if not subsystem:
        raise ConanException("Cannot recognize the Windows subsystem, install MSYS2/cygwin or specify a build_require "
                             "to apply it.")

    if subsystem == MSYS2 and msys_mingw:
        # This needs to be set so that msys2 bash profile will set up the environment correctly.
        env_vars = {"MSYSTEM": "MINGW32" if conanfile.settings.get_safe("arch") == "x86" else "MINGW64",
                    "MSYS2_PATH_TYPE": "inherit"}
    else:
        env_vars = {}

    with environment_append(env_vars):
        hack_env = ""
        if subsystem != WSL:  # In the bash.exe from WSL this trick do not work, always the /usr/bin etc at first place
            inherited_path = conanfile.env.get("PATH", None)
            if isinstance(inherited_path, list):
                paths = [unix_path(path, path_flavor=subsystem) for path in inherited_path]
                inherited_path = ":".join(paths)
            else:
                inherited_path = unix_path(inherited_path, path_flavor=subsystem)

            if "PATH" in env:
                tmp = unix_path(env["PATH"].replace(";", ":"), path_flavor=subsystem)
                inherited_path = "%s:%s" % (tmp, inherited_path) if inherited_path else tmp

            # Put the build_requires and requires path at the first place inside the shell
            hack_env = ' && PATH="%s:$PATH"' % inherited_path if inherited_path else ""

        for var_name, value in env.items():
            if var_name == "PATH":
                continue
            hack_env += ' && %s=%s' % (var_name, value)

        # Needed to change to that dir inside the bash shell
        if cwd and not os.path.isabs(cwd):
            cwd = os.path.join(os.getcwd(), cwd)

        curdir = unix_path(get_cased_path(cwd or os.getcwd()), path_flavor=subsystem)
        to_run = 'cd "%s"%s && %s ' % (curdir, hack_env, bashcmd)
        bash_path = os_info.bash_path()
        bash_path = '"%s"' % bash_path if " " in bash_path else bash_path
        wincmd = '%s --login -c %s' % (bash_path, escape_windows_cmd(to_run))
        conanfile.output.info('run_in_windows_bash: %s' % wincmd)
        return conanfile.run(wincmd, win_bash=False)
