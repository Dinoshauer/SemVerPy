import re

__version__ = '0.1.1'
__author__ = 'Kasper Jacobsen'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Kasper Jacobsen'

_start = r'^[v=]?'
_major = r'(?P<major>\d+)'
_minor = r'(\.(?P<minor>(\d+|[x*])))?'
_patch = r'(\.(?P<patch>(\d+|[x*])))?'
_build = r'(?:[:+-](?P<build>\w+))?'
_end = r'$'

_regex = _start + _major + _minor + _patch + _build + _end


class InvalidVersionException(Exception):
    pass


class SemVerPy():
    _pattern = re.compile(_regex, re.IGNORECASE)

    def __init__(self, version, dependency=False):
        version = self._parse(version, dependency)
        self.dependency = dependency
        if self.dependency:
            fill = None
        else:
            fill = 0

        self._major = version['major']

        self._minor = version['minor'] or fill
        self._patch = version['patch'] or fill

        self._build = version['build']

    def __str__(self):
        res = '{major}.{minor}.{patch}'.format(
            major=self._major,
            minor=self._minor if self._minor is not None else 'x',
            patch=self._patch if self._patch is not None else 'x',
        )

        if self._build:
            res += '-{}'.format(self._build)
        return res

    def __repr__(self):
        return '<{name}({info})>'.format(
            name=self.__class__.__name__,
            info=str(self),
        )

    def _tuple(self, fill=0):
        return (
            self._major or fill,
            self._minor or fill,
            self._patch or fill,
            self._build or fill,
        )

    def satisfies(self, item):
        for s, o in zip(self._tuple(fill='x'), item._tuple(fill='x')):
            if o != 'x' and s != o:
                return False
        return True

    def __eq__(self, other):
        if not isinstance(other, SemVerPy):
            return False
        else:
            return self._tuple() == other._tuple()

    def __ne__(self, other):
        return self._tuple() != other._tuple()

    def __lt__(self, other):
        if not isinstance(other, SemVerPy):
            return False
        else:
            return self._tuple() < other._tuple()

    def __gt__(self, other):
        if not isinstance(other, SemVerPy):
            return False
        else:
            return self._tuple() > other._tuple()

    def __le__(self, other):
        return self._tuple() <= other._tuple()

    def __ge__(self, other):
        return self._tuple() >= other._tuple()

    def _get_dict(self, string):
        return self._pattern.search(string).groupdict()

    def _parse(self, version_string, dependency):
        res = self._pattern.search(version_string)
        if res is None:
            msg = 'Not a valid version: {}'.format(version_string)
            raise InvalidVersionException(msg)
        else:
            return self._convert_fields(res.groupdict(), dependency)

    def _convert_fields(self, version_dict, dependency):
        for key in ['major', 'minor', 'patch']:
            value = version_dict[key]
            if dependency:
                if value == 'x':
                    version_dict[key] = None
            else:
                try:
                    version_dict[key] = int(version_dict[key])
                except TypeError:
                    pass
        return version_dict

    def bump_major(self, build=None):
        self._major += 1
        self._minor = 0
        self._patch = 0
        self._build = build
        return self

    def bump_minor(self, build=None):
        self._minor += 1
        self._patch = 0
        self._build = build
        return self

    def bump_patch(self, build=None):
        self._patch += 1
        self._build = build
        return self

    def set_build(self, build_string):
        self._build = build_string
        return self
