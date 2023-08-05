import os
import subprocess as sp
import json
import yaml


class PackageManager():

    def __init__(self):
        _, LANG = os.environ['LANG'].split('.')
        self.lang = LANG

    def load_status(self):
        p = sp.run(["julia", "-e", "Pkg.status()"], stdout=sp.PIPE)
        res = str(p.stdout.decode(self.lang))
        required, additional = self._parse_pkg_status(res)

        self.required = required
        self.additional = additional
        self.packages = {
            'requiredPackages': required,
            'additionalPackages': additional
        }

    def _parse_pkg_status(self, pkg_status):
        required = {}
        additional = {}

        status = 0
        for row in pkg_status.split('\n'):
            if ':' in row:
                status += 1
                continue
            if not row.strip():
                break

            _, package, version = row.split()
            if status == 1:
                required[package] = version
            else:
                additional[package] = version
        return required, additional

    def to_REQUIRE(self):  # dict -> str
        return '\n'.join([
            ' '.join((package, version))
            for (package, version) in self.packages['requiredPackages'].items()
        ])

    def to_json(self):
        return json.dumps(
            self.packages, indent=1, sort_keys=True, encoding=self.lang)

    def to_yaml(self):
        return yaml.dump(self.packages, default_flow_style=False)

    def from_REQUIRE(self, filename):
        with open(filename, 'r') as f:
            required = {}
            for line in f.readlines():
                package, version = line.split()
                required[package] = version
        self.packages = {'requiredPackages': required}
        self._install_required()

    def from_yaml(self, filename):
        with open(filename, 'r') as f:
            self.packages = yaml.load(f.read())
        self._install_required()

    def from_json(self, filename):
        with open(filename, 'r') as f:
            self.packages = json.load(f)
        self._install_required()

    def _install_required(self):
        for (package, version) in self.packages['requiredPackages'].items():
            pkg_add = 'Pkg.add("%s", v"%s")' % (package, version)
            p = sp.run(["julia", "-e", pkg_add], stdout=sp.PIPE)
            print(p.stdout)

    def install_package(self, packages_with_version):
        for package_with_version in packages_with_version:
            if '==' in package_with_version:
                package, version = package_with_version.split('==')
                pkg_add = 'Pkg.add("%s", v"%s")' % (package, version)
            else:
                package = package_with_version
                pkg_add = 'Pkg.add("%s")' % (package)
            p = sp.run(["julia", "-e", pkg_add], stdout=sp.PIPE)
            res = str(p.stdout.decode(self.lang))
            print(res)

    def uninstall_package(self, packages):
        for package in packages:
            pkg_rm = 'Pkg.rm("%s")' % (package)
            p = sp.run(["julia", "-e", pkg_rm], stdout=sp.PIPE)
            res = str(p.stdout.decode(self.lang))
            print(res)

    def update_packages(self):
        sp.run(["julia", "-e", "Pkg.status()"], stdout=sp.STDOUT)


def command_install(args):
    pkg_manager = PackageManager()

    if args.requirement is None:
        pkg_manager.install_package(args.packages_with_version)
    elif args.requirement.endswith('json'):
        pkg_manager.from_json(args.requirement)
    elif args.requirement.endswith(('yaml', 'yml')):
        pkg_manager.from_yaml(args.requirement)
    else:
        pkg_manager.from_REQUIRE(args.requirement)


def command_uninstall(args):
    pkg_manager = PackageManager()
    pkg_manager.uninstall_package(args.packages_with_version)


def command_freeze(args):
    pkg_manager = PackageManager()
    pkg_manager.load_status()
    if args.format == 'json':
        print(pkg_manager.to_json())
    elif args.format == 'yaml':
        print(pkg_manager.to_yaml())
    else:
        print(pkg_manager.to_REQUIRE())


def command_update(args):
    pkg_manager = PackageManager()
    pkg_manager.update_packages()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_install = subparsers.add_parser(\
        'install',
        help='Install packages.')
    parser_install.add_argument(
        'packages_with_version', nargs='*',\
        help='Install target packages.')
    parser_install.add_argument(
        '-r',
        '--requirement',
        default=None,
        help='<file> Install from the given requirements file.')
    parser_install.set_defaults(handler=command_install)

    parser_uninstall = subparsers.add_parser(
        'uninstall', aliases=['remove'],\
        help='Uninstall packages.')
    parser_uninstall.add_argument(
        'packages_with_version', nargs='*',\
        help='Uninstall target packages.')
    parser_uninstall.set_defaults(handler=command_uninstall)

    parser_freeze = subparsers.add_parser(
        'freeze', aliases=['list'],\
        help='Output installed packages.')
    parser_freeze.add_argument(
        '-f',
        '--format',
        default='REQUIRE',
        choices=['REQUIRE', 'json', 'yaml'],
        help='STDOUT in the specified format.')
    parser_freeze.set_defaults(handler=command_freeze)

    parser_update = subparsers.add_parser(
        'update',\
        help='Update installed packages.')
    parser_update.set_defaults(handler=command_update)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
