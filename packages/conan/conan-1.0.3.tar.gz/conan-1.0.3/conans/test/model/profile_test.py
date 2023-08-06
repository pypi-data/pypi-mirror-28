import unittest

from conans.client.profile_loader import _load_profile
from conans.model.profile import Profile
from collections import OrderedDict


class ProfileTest(unittest.TestCase):

    def profile_settings_update_test(self):
        prof = '''[settings]
os=Windows
'''
        new_profile, _ = _load_profile(prof, None, None)

        new_profile.update_settings(OrderedDict([("OTHER", "2")]))
        self.assertEquals(new_profile.settings, OrderedDict([("os", "Windows"), ("OTHER", "2")]))

        new_profile.update_settings(OrderedDict([("compiler", "2"), ("compiler.version", "3")]))
        self.assertEquals(new_profile.settings,
                          OrderedDict([("os", "Windows"), ("OTHER", "2"),
                                       ("compiler", "2"), ("compiler.version", "3")]))

    def profile_subsettings_update_test(self):
        prof = '''[settings]
os=Windows
compiler=Visual Studio
compiler.runtime=MT
'''
        new_profile, _ = _load_profile(prof, None, None)
        new_profile.update_settings(OrderedDict([("compiler", "gcc")]))
        self.assertEquals(dict(new_profile.settings), {"compiler": "gcc", "os": "Windows"})

        new_profile, _ = _load_profile(prof, None, None)
        new_profile.update_settings(OrderedDict([("compiler", "Visual Studio"),
                                                 ("compiler.subsetting", "3"),
                                                 ("other", "value")]))

        self.assertEquals(dict(new_profile.settings), {"compiler": "Visual Studio",
                                                       "os": "Windows",
                                                       "compiler.runtime": "MT",
                                                       "compiler.subsetting": "3",
                                                       "other": "value"})

    def package_settings_update_test(self):
        prof = '''[settings]
MyPackage:os=Windows

    # In the previous line there are some spaces
'''
        np, _ = _load_profile(prof, None, None)

        np.update_package_settings({"MyPackage": [("OTHER", "2")]})
        self.assertEquals(np.package_settings_values,
                          {"MyPackage": [("os", "Windows"), ("OTHER", "2")]})

        np.update_package_settings({"MyPackage": [("compiler", "2"), ("compiler.version", "3")]})
        self.assertEquals(np.package_settings_values,
                          {"MyPackage": [("os", "Windows"), ("OTHER", "2"),
                                         ("compiler", "2"), ("compiler.version", "3")]})

    def profile_dump_order_test(self):
        # Settings
        profile = Profile()
        profile.package_settings["zlib"] = {"compiler": "gcc"}
        profile.settings["arch"] = "x86_64"
        profile.settings["compiler"] = "Visual Studio"
        profile.settings["compiler.version"] = "12"
        profile.build_requires["*"] = ["zlib/1.2.8@lasote/testing"]
        profile.build_requires["zlib/*"] = ["aaaa/1.2.3@lasote/testing", "bb/1.2@lasote/testing"]
        self.assertEqual("""[build_requires]
*: zlib/1.2.8@lasote/testing
zlib/*: aaaa/1.2.3@lasote/testing, bb/1.2@lasote/testing
[settings]
arch=x86_64
compiler=Visual Studio
compiler.version=12
zlib:compiler=gcc
[options]
[env]""".splitlines(), profile.dumps().splitlines())

    def apply_test(self):
        # Settings
        profile = Profile()
        profile.settings["arch"] = "x86_64"
        profile.settings["compiler"] = "Visual Studio"
        profile.settings["compiler.version"] = "12"

        profile.env_values.add("CXX", "path/to/my/compiler/g++")
        profile.env_values.add("CC", "path/to/my/compiler/gcc")

        profile.update_settings(OrderedDict([("compiler.version", "14")]))

        self.assertEqual('[build_requires]\n[settings]\narch=x86_64\ncompiler=Visual Studio\ncompiler.version=14\n'
                         '[options]\n'
                         '[env]\nCC=path/to/my/compiler/gcc\nCXX=path/to/my/compiler/g++',
                         profile.dumps())
