"""A simple read-only PyPI static index server generator."""
import argparse
import collections
import contextlib
import json
import operator
import os
import os.path
import re
import sys
import tempfile
from datetime import datetime

import jinja2
import packaging.utils
import packaging.version
import pkg_resources
from pip.wheel import Wheel


jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader('dumb_pypi', 'templates'),
    autoescape=True,
)


def remove_extension(name):
    if name.endswith(('gz', 'bz2')):
        name, _ = name.rsplit('.', 1)
    name, _ = name.rsplit('.', 1)
    return name


def guess_name_version_from_filename(filename):
    if filename.endswith('.whl'):
        wheel = Wheel(filename)
        return wheel.name, wheel.version
    else:
        # These don't have a well-defined format like wheels do, so they are
        # sort of "best effort", with lots of tests to back them up.
        # The most important thing is to correctly parse the name.
        name = remove_extension(filename)
        version = None

        if '-' in name:
            if name.count('-') == 1:
                name, version = name.split('-')
            else:
                parts = name.split('-')
                for i in range(len(parts) - 1, 0, -1):
                    part = parts[i]
                    if '.' in part and re.search('[0-9]', part):
                        name, version = '-'.join(parts[0:i]), '-'.join(parts[i:])

        # possible with poorly-named files
        if len(name) <= 0:
            raise ValueError(f'Invalid package name: {filename}')

        # impossible
        assert version is None or len(version) > 0, version

        return name, version


class Package(collections.namedtuple('Package', (
    'filename',
    'name',
    'version',
    'hash',
    'upload_timestamp',
    'uploaded_by',
))):

    __slots__ = ()

    def __lt__(self, other):
        assert isinstance(other, Package), type(other)
        return self.sort_key < other.sort_key

    @property
    def sort_key(self):
        """Sort key for a filename."""
        return (
            self.name,
            pkg_resources.parse_version(self.version or '0'),

            # This looks ridiculous, but it's so that like extensions sort
            # together when the name and version are the same (otherwise it
            # depends on how the filename is normalized, which means sometimes
            # wheels sort before tarballs, but not always).
            # Alternatively we could just grab the extension, but that's less
            # amusing, even though it took 6 lines of comments to explain this.
            self.filename[::-1],
        )

    @property
    def formatted_upload_time(self):
        return _format_datetime(datetime.fromtimestamp(self.upload_timestamp))

    @property
    def info_string(self):
        # TODO: I'd like to remove this "info string" and instead format things
        # nicely for humans (e.g. in a table or something).
        #
        # This might mean changing the web interface to use different pages for
        # humans than the /simple/ ones it currently links to. (Even if pip can
        # parse links from a <table>, it might add significantly more bytes.)
        info = self.version or 'unknown version'
        if self.upload_timestamp is not None:
            info += f', {self.formatted_upload_time}'
        if self.uploaded_by is not None:
            info += f', {self.uploaded_by}'
        return info

    def url(self, base_url):
        return f'{base_url.rstrip("/")}/{self.filename}'

    @classmethod
    def create(
            cls,
            *,
            filename,
            hash=None,
            upload_timestamp=None,
            uploaded_by=None,
    ):
        if not re.match('[a-zA-Z0-9_\-\.]+$', filename) or '..' in filename:
            raise ValueError('Unsafe package name: {}'.format(filename))

        name, version = guess_name_version_from_filename(filename)
        return cls(
            filename=filename,
            name=packaging.utils.canonicalize_name(name),
            version=version,
            hash=hash,
            upload_timestamp=upload_timestamp,
            uploaded_by=uploaded_by,
        )


@contextlib.contextmanager
def atomic_write(path):
    tmp = tempfile.mktemp(
        prefix='.' + os.path.basename(path),
        dir=os.path.dirname(path),
    )
    try:
        with open(tmp, 'w') as f:
            yield f
    except BaseException:
        os.remove(tmp)
        raise
    else:
        os.rename(tmp, path)


def _format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# TODO: at some point there will be so many options we'll want to make a config
# object or similar instead of adding more arguments here
def build_repo(packages, output_path, packages_url, title, logo, logo_width):
    simple = os.path.join(output_path, 'simple')
    os.makedirs(simple, exist_ok=True)

    current_date = _format_datetime(datetime.now())

    # /index.html
    with atomic_write(os.path.join(output_path, 'index.html')) as f:
        f.write(jinja_env.get_template('index.html').render(
            title=title,
            packages=sorted(
                (
                    package,
                    sorted(packages[package])[-1].version,
                )
                for package in packages
            ),
            logo=logo,
            logo_width=logo_width,
        ))

    # /simple/index.html
    with atomic_write(os.path.join(simple, 'index.html')) as f:
        f.write(jinja_env.get_template('simple.html').render(
            date=current_date,
            package_names=sorted(packages),
        ))

    for package_name, versions in packages.items():
        package_dir = os.path.join(simple, package_name)
        os.makedirs(package_dir, exist_ok=True)

        # /simple/{package}/index.html
        with atomic_write(os.path.join(package_dir, 'index.html')) as f:
            f.write(jinja_env.get_template('package.html').render(
                date=current_date,
                package_name=package_name,
                versions=sorted(
                    versions,
                    key=operator.attrgetter('sort_key'),
                    # Newer versions should sort first.
                    reverse=True,
                ),
                packages_url=packages_url,
            ))


def _lines_from_path(path):
    f = sys.stdin if path == '-' else open(path)
    return f.read().splitlines()


def _create_packages(package_infos):
    packages = collections.defaultdict(set)
    for package_info in package_infos:
        try:
            package = Package.create(**package_info)
        except ValueError as ex:
            # TODO: this should really be optional; i'd prefer it to fail hard
            print('{} (skipping package)'.format(ex), file=sys.stderr)
        else:
            packages[package.name].add(Package.create(**package_info))

    return packages


def package_list(path):
    return _create_packages({'filename': line} for line in _lines_from_path(path))


def package_list_json(path):
    return _create_packages(json.loads(line) for line in _lines_from_path(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)

    package_input_group = parser.add_mutually_exclusive_group(required=True)
    package_input_group.add_argument(
        '--package-list',
        help='path to a list of packages (one per line)',
        type=package_list,
        dest='packages',
    )
    package_input_group.add_argument(
        '--package-list-json',
        help='path to a list of packages (one JSON object per line)',
        type=package_list_json,
        dest='packages',
    )

    parser.add_argument(
        '--output-dir', help='path to output to', required=True,
    )
    parser.add_argument(
        '--packages-url',
        help='url to packages (can be absolute or relative)', required=True,
    )
    parser.add_argument(
        '--title',
        help='site title (for web interface)', default='My Private PyPI',
    )
    parser.add_argument(
        '--logo',
        help='URL for logo to display (defaults to no logo)',
    )
    parser.add_argument(
        '--logo-width', type=int,
        help='width of logo to display', default=0,
    )
    args = parser.parse_args(argv)

    build_repo(
        args.packages,
        args.output_dir,
        args.packages_url,
        args.title,
        args.logo,
        args.logo_width,
    )


if __name__ == '__main__':
    exit(main())
