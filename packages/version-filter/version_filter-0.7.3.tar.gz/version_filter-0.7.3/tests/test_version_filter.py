from __future__ import unicode_literals
import pytest

from version_filter import VersionFilter
from version_filter import SpecItemMask, SpecMask
from version_filter.version_filter import _parse_semver, InvalidSemverError, YesVersion
from semantic_version import Version, Spec


def test_specitemmask_asterisk():
    s = SpecItemMask('*')
    assert(Spec('*') == s.spec)
    assert(Version('0.0.1') in s.spec)
    assert(Version('0.1.1-alpha') in s.spec)


def test_specitemmask_asterisk_forms():
    s = SpecItemMask(' *')
    assert s.kind == '*'

    s = SpecItemMask(' *  ')
    assert s.kind == '*'

    s = SpecItemMask('*')
    assert s.kind == '*'

    with pytest.raises(ValueError):
        SpecItemMask('bad*')

    with pytest.raises(ValueError):
        SpecItemMask('* bad')


def test_specitemmask_lock1():
    s = SpecItemMask('L.0.0', current_version=Version('1.0.0'))
    assert(Spec('1.0.0') == s.spec)


def test_specitemmask_lock2():
    s = SpecItemMask('L.L.0', current_version=Version('1.8.0'))
    assert(Spec('1.8.0') == s.spec)


def test_specitemmask_lock3():
    s = SpecItemMask('L.L.L', current_version=Version('1.8.3'))
    assert(Spec('1.8.3') == s.spec)


def test_specitemmask_lock4():
    s = SpecItemMask('L1.L.L', current_version=Version('1.8.3'))
    assert(Spec('2.8.3') == s.spec)


def test_specitemmask_lock5():
    s = SpecItemMask('L1.L999.L', current_version=Version('1.8.3'))
    assert(Spec('2.1007.3') == s.spec)


def test_specitemmask_lock6():
    with pytest.raises(ValueError):
        SpecItemMask('L-1.L999.L', current_version=Version('1.8.3'))


def test_specitemmask_yes1():
    s = SpecItemMask('Y.Y.0', current_version=Version('1.8.3'))
    assert(Spec('*') == s.spec)


def test_specitemmask_yes2():
    s = SpecItemMask('L.Y.0', current_version=Version('1.8.3'))
    assert(Spec('*') == s.spec)


def test_specitemmask_yes3():
    s = SpecItemMask('L.L.Y', current_version=Version('1.8.3'))
    assert(Spec('*') == s.spec)


def test_specitemmask_modifiers_1():
    s = SpecItemMask('>1.0.0')
    assert(Spec('>1.0.0') == s.spec)


def test_coerceable_version():
    s = SpecItemMask('1')
    assert(Spec('1') == s.spec)


def test_specmask():
    s = SpecMask('1.0.0')
    assert(Spec('1.0.0') == s.specs[0].spec)


def test_specmask_one_or():
    s = SpecMask('1.0.0 || 2.0.0')
    assert(Spec('1.0.0') == s.specs[0].spec)
    assert(Spec('2.0.0') == s.specs[1].spec)


def test_specmask_multi_ors():
    s = SpecMask('1.0.0 || 2.0.0 || 3.0.0 || 4.0.0')
    assert(Spec('1.0.0') == s.specs[0].spec)
    assert(Spec('2.0.0') == s.specs[1].spec)
    assert(Spec('3.0.0') == s.specs[2].spec)
    assert(Spec('4.0.0') == s.specs[3].spec)


def test_specmask_one_and():
    s = SpecMask('1.0.0 && 2.0.0')
    assert(Spec('1.0.0') == s.specs[0].spec)
    assert(Spec('2.0.0') == s.specs[1].spec)


def test_specmask_multi_ands():
    s = SpecMask('1.0.0 && 2.0.0 && 3.0.0 && 4.0.0')
    assert(Spec('1.0.0') == s.specs[0].spec)
    assert(Spec('2.0.0') == s.specs[1].spec)
    assert(Spec('3.0.0') == s.specs[2].spec)
    assert(Spec('4.0.0') == s.specs[3].spec)


def test_mixed_boolean_will_assert():
    with pytest.raises(ValueError):
        SpecMask('1.0.0 && 2.0.0 || 3.0.0')


def test_specmask_match():
    mask = '1.0.0'
    s = SpecMask(mask)
    assert(s.match('1.0.0') is True)
    assert(s.match('1.0.1') is False)


def test_specmask_contains():
    mask = '1.0.0'
    s = SpecMask(mask)
    assert('1.0.0' in s)
    assert('1.0.1' not in s)


def test_partial_versions_1():
    mask = '1.0'
    s = SpecItemMask(mask)
    assert(s.spec == Spec('1.0'))


def test_partial_versions_2():
    mask = '1'
    s = SpecItemMask(mask)
    assert(s.spec == Spec('1'))


def test_partial_versions_3():
    mask = 'L'
    current_version = '1'
    s = SpecItemMask(mask, current_version)
    assert(s.spec == Spec('==1'))


def test_partial_versions_4():
    mask = 'L.Y'
    versions = ['1.8', '1.8.1', '1.8.2', '1.9', '1.9.1', '1.10', 'nightly']
    current_version = '1.8'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('1.9' in subset)
    assert('1.10' in subset)


def test_partial_versions_5():
    mask = 'L.Y.Y'
    versions = ['1.8', '1.8.1', '1.8.2', '1.9', '1.9.1', '1.10', 'nightly']
    current_version = '1.8'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(5 == len(subset))
    assert('1.8' not in subset)
    assert('nightly' not in subset)


def test_readme_example_semver():
    mask = 'L.Y.Y'
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', 'nightly']
    current_version = '1.9.0'

    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('1.9.1' in subset)
    assert('1.10.0' in subset)


def test_readme_example_regex():
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', 'nightly']

    subset = VersionFilter.regex_filter(r'^night', versions)
    assert(1 == len(subset))
    assert('nightly' in subset)


def test_major_updates_only_1():
    mask = 'Y.0.0'
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.9.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('2.0.0' in subset)


def test_major_updates_only_2():
    mask = 'Y.0.0'  # tell me major version changes only once per major version
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.1', '2.0.2']
    current_version = '1.9.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(0 == len(subset))


def test_minor_updates_1():
    mask = 'Y.Y.0'  # tell me minor version changes only once per minor version, exclude all patch updates
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.8.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(3 == len(subset))
    assert('1.9.0' in subset)
    assert('1.10.0' in subset)
    assert('2.0.0' in subset)


def test_minor_updates_2():
    mask = 'L.Y.0'  # give me minor version changes only for my current major version, exclude all patch updates
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.8.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('1.9.0' in subset)
    assert('1.10.0' in subset)


def test_all_updates_1():
    mask = 'Y.Y.Y'  # Give me every patch, minor and major update
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.8.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(7 == len(subset))
    assert('1.8.0' not in subset)


def test_explicit_major_updates_only_1():
    mask = '2.0.0'
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.9.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('2.0.0' in subset)


def test_python_filter():
    mask = 'Y.Y.Y'
    versions = ['0.1.0', '1.1.0', '1.2.1.dev0', '1.2.dev0', '1.2.post0', '1.2.0a1']
    subset = VersionFilter.semver_filter(mask, versions)
    assert(2 == len(subset))
    assert('0.1.0' in subset)
    assert('1.1.0' in subset)


def test_django_config_example_1():
    mask = '1.8.Y'
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    subset = VersionFilter.semver_filter(mask, versions)
    assert(3 == len(subset))
    assert('1.8.0' in subset)
    assert('1.8.1' in subset)
    assert('1.8.2' in subset)


def test_django_config_example_2():
    mask = '1.8.Y || 1.10.Y'
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    subset = VersionFilter.semver_filter(mask, versions)
    assert(4 == len(subset))
    assert('1.8.0' in subset)
    assert('1.8.1' in subset)
    assert('1.8.2' in subset)
    assert('1.10.0' in subset)


def test_django_current_example_1():
    mask = 'Y.Y.0 || L.L.Y'  # new major and minors, patches to my minor
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.8.1'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(4 == len(subset))
    assert('1.8.2' in subset)
    assert('1.9.0' in subset)
    assert('1.10.0' in subset)
    assert('2.0.0' in subset)


def test_modifier_example_1():
    mask = '>1.8.0 && <2.0.0'  # all releases between 1.8.0 and 2.0.0
    versions = ['1.8.0', '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.10.0', '2.0.0', '2.0.1']
    current_version = '1.8.1'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(4 == len(subset))
    assert('1.8.2' in subset)
    assert('1.9.0' in subset)
    assert('1.9.1' in subset)
    assert('1.10.0' in subset)


def test_prerelease_1():
    mask = 'L.Y.Y'
    versions = ['0.9.5', '1.0.0-alpha.e2', '1.0.0-alpha.12', '1.0.0-alpha.58']
    current_version = '0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(0 == len(subset))


def test_prerelease_2():
    mask = 'L.Y.Y-Y'
    versions = ['0.9.5', '1.0.0-alpha.e2', '1.0.0-alpha.12', '1.0.0-alpha.58']
    current_version = '0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(0 == len(subset))


def test_prerelease_3():
    mask = 'L.Y.Y-Y'
    versions = ['0.9.5', '1.0.0-alpha.e2', '1.0.0-alpha.12', '1.0.0-alpha.58', '0.9.6-alpha.ef']
    current_version = '0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.9.6-alpha.ef' in subset)


def test_prerelease_4():
    mask = 'L.Y.Y'
    versions = ['0.9.5', '1.0.0-alpha.e2', '1.0.0-alpha.12', '1.0.0-alpha.58', '0.9.6', '1.0.0']
    current_version = '0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.9.6' in subset)


def test_prerelease_5():
    mask = 'Y.Y.Y'
    versions = ['0.9.5', '1.0.0-alpha.e2', '1.0.0-alpha.12', '1.0.0-alpha.58', '0.9.6', '1.0.0']
    subset = VersionFilter.semver_filter(mask, versions)
    assert(3 == len(subset))
    assert('0.9.5' in subset)
    assert('0.9.6' in subset)
    assert('1.0.0' in subset)


def test_prerelease_6():
    mask = 'Y.Y.Y-Y'
    versions = ['0.9.5', '1.0.0-alpha.e2', '1.0.0-alpha.12', '1.0.0-alpha.58', '0.9.6', '1.0.0']
    subset = VersionFilter.semver_filter(mask, versions)
    assert(6 == len(subset))


def test_prerelease_matching():
    mask = 'L.L.Y-alpine'
    versions = ['3.6', '3.6-alpine', '3.6-onbuild', '3.6.1', '3.6.1-alpine', '3.6.1-alpine3.6', '3.6.1-onbuild']
    current_version = '3.6-alpine'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('3.6.1-alpine' in subset)


def test_prerelease_matching_2():
    mask = 'L.L.Y-alpine3.6'
    versions = ['3.6', '3.6-alpine', '3.6-alpine3.6', '3.6-onbuild', '3.6.1', '3.6.1-alpine', '3.6.1-alpine3.6',
                '3.6.1-onbuild']
    current_version = '3.6-alpine3.6'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('3.6.1-alpine3.6' in subset)


def test_prerelease_lock():
    mask = 'L.L.Y-L'
    versions = ['3.6', '3.6-alpine', '3.6-onbuild', '3.6.1', '3.6.1-alpine', '3.6.1-alpine3.6', '3.6.1-onbuild']
    current_version = '3.6-alpine'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('3.6.1-alpine' in subset)


def test_prerelease_lock_2():
    mask = 'L.L.Y-L'
    versions = ['3.6', '3.6-alpine', '3.6-alpine3.6', '3.6-onbuild', '3.6.1', '3.6.1-alpine', '3.6.1-alpine3.6',
                '3.6.1-onbuild']
    current_version = '3.6-alpine3.6'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('3.6.1-alpine3.6' in subset)


def test_v_prefix_on_versions():
    mask = 'L.L.Y'
    versions = ['v0.9.5', 'v0.9.6', 'v1.0.0']
    current_version = '0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('v0.9.6' in subset)


def test_v_prefix_on_current_version():
    mask = 'L.L.Y'
    versions = ['0.9.5', '0.9.6', '1.0.0']
    current_version = 'v0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.9.6' in subset)


def test_eq_prefix_on_versions():
    mask = 'L.L.Y'
    versions = ['=0.9.5', '=0.9.6', '=1.0.0']
    current_version = '0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('=0.9.6' in subset)


def test_eq_prefix_on_current_version():
    mask = 'L.L.Y'
    versions = ['0.9.5', '0.9.6', '1.0.0']
    current_version = '=0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.9.6' in subset)


def test_v_and_eq_prefix_on_current_version():
    mask = 'L.L.Y'
    versions = ['0.9.5', '0.9.6', '1.0.0']
    current_version = 'v=0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.9.6' in subset)
    
    
def test_eq_and_eq_prefix_on_current_version():
    mask = 'L.L.Y'
    versions = ['0.9.5', '0.9.6', '1.0.0']
    current_version = '==0.9.5'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.9.6' in subset)


def test_caret():
    mask = '^1.0.0'
    versions = ['1.0.0', '1.0.1', '1.1.0', '1.2.0-alpha', '2.0.0', '2.0.0-beta']
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('1.0.1' in subset)
    assert('1.1.0' in subset)


def test_caret_babel_cli_example():
    mask = '^L.L.L'
    versions = [
        '6.24.0',
        '7.0.0-alpha.3',
        '7.0.0-alpha.4',
        '7.0.0-alpha.6',
        '7.0.0-alpha.7',
        '6.24.1',
        '7.0.0-alpha.8',
        '7.0.0-alpha.9',
        '7.0.0-alpha.10',
        '7.0.0-alpha.11',
        '7.0.0-alpha.12',
        '7.0.0-alpha.14',
    ]
    current_version = '6.24.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('6.24.1' in subset)


def test_semver_caret():
    spec = Spec('^1.0.0')
    assert(Version('1.1.0') in spec)
    assert(Version('1.1.0-alpha') not in spec)

    assert(Version('2.0.0') not in spec)
    assert(Version('2.0.0-alpha') not in spec)


def test_semver_caret_with_zero_major():
    spec = Spec('^0.3.0')
    assert(Version('0.4.0') not in spec)
    assert(Version('0.3.1') in spec)
    assert(Version('1.3.0') not in spec)


def test_semver_caret_with_locks():
    mask = '^L.L.L'
    versions = ['0.3.0', '0.3.1', '0.4.0', '1.0.0', '1.3.0']
    current_version = '0.3.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('0.3.1' in subset)


def test_semver_filter_sorted_return():
    mask = 'Y.Y.Y'
    versions = ['0.9.6', '1.0.0', '0.9.5']
    current_version = None
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(3 == len(subset))
    assert('0.9.5' == subset[0])
    assert('0.9.6' == subset[1])
    assert('1.0.0' == subset[2])


def test_valid_version_parsing_1():
    assert(Version('0.0.1') == _parse_semver('0.0.1'))
    assert(Version('0.0.1-dev0') == _parse_semver('0.0.1-dev0'))
    assert(Version('0.0.1-dev0.build0') == _parse_semver('0.0.1-dev0.build0'))
    assert(Version('0.0.1+something') == _parse_semver('0.0.1+something'))


def test_invalid_version_parsing_1():
    with pytest.raises(InvalidSemverError):
        _parse_semver('0.0.1.build0')  # invalid build string


def test_next_best_specitemmask():
    s = SpecItemMask('-1.0.0')
    assert(Spec('1.0.0') == s.spec)
    assert s.has_next_best


def test_next_best_specitemmask_matching_versions_literal1():
    mask = '-1.0.0'
    versions = [
        '1.0.1',
        '2.0.1',
    ]
    subset = VersionFilter.semver_filter(mask, versions)
    assert(1 == len(subset))
    assert('1.0.1' in subset)


def test_next_best_specitemmask_matching_versions_literal2():
    mask = '-1.0.0'
    versions = [
        '1.1.0',
        '2.0.1',
    ]
    subset = VersionFilter.semver_filter(mask, versions)
    assert(1 == len(subset))
    assert('1.1.0' in subset)


def test_next_best_specitemmask_matching_versions_literal3():
    mask = '-1.0.0'
    versions = [
        '1.0.0',
        '2.0.1',
    ]
    subset = VersionFilter.semver_filter(mask, versions)
    assert(0 == len(subset))


def test_next_best_specitemmask_matching_versions_lock1():
    mask = '-L.0.0'
    versions = [
        '1.0.1',
        '2.0.1',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('1.0.1' in subset)


def test_next_best_specitemmask_matching_versions_lock2():
    mask = '-L.0.0'
    versions = [
        '1.1.0',
        '2.0.1',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('1.1.0' in subset)


def test_next_best_specitemmask_matching_versions_lock3():
    mask = '-L.0.0'
    versions = [
        '1.0.0',
        '2.0.1',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(0 == len(subset))


def test_get_next_best_versions1():
    y = YesVersion('*', 'Y.0.0')
    versions = [
        '1.0.0',
        '1.0.1',
        '2.0.1',
        '2.1.0'
    ]
    versions = [_parse_semver(x) for x in versions]

    result = y.get_next_best_versions(versions)
    assert(1 == len(result))
    assert(_parse_semver('2.0.0') in result)


def test_get_next_best_versions2():
    y = YesVersion('*', 'Y.Y.0')
    versions = [
        '1.0.0',
        '1.0.1',
        '1.1.1',
        '2.0.1',
        '2.1.1'
    ]
    versions = [_parse_semver(x) for x in versions]

    result = y.get_next_best_versions(versions)
    assert(3 == len(result))
    assert(_parse_semver('1.1.0') in result)
    assert(_parse_semver('2.0.0') in result)
    assert(_parse_semver('2.1.0') in result)


def test_get_next_best_versions3():
    y = YesVersion('*', '1.0.0')
    versions = [
        '1.0.0',
        '1.0.1',
        '1.1.1',
        '2.0.1',
        '2.1.1'
    ]
    versions = [_parse_semver(x) for x in versions]

    result = y.get_next_best_versions(versions)
    assert(0 == len(result))


def test_get_next_best_versions4():
    y = YesVersion('*', 'Y.Y.Y')
    versions = [
        '1.0.0',
        '1.0.1',
        '1.0.5',
        '1.1.1',
        '2.0.1',
        '2.1.1'
    ]
    versions = [_parse_semver(x) for x in versions]

    result = y.get_next_best_versions(versions)
    assert(3 == len(result))
    assert(_parse_semver('1.0.2') in result)
    assert(_parse_semver('1.0.3') in result)
    assert(_parse_semver('1.0.4') in result)


def test_next_best_specitemmask_matching_versions_yes1():
    mask = '-Y.0.0'
    versions = [
        '1.0.1',
        '2.0.1',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('1.0.1' in subset)  # how could the 1.0.0 current version exists if this is the first version in list
    assert('2.0.1' in subset)


def test_next_best_specitemmask_matching_versions_yes2():
    mask = '-Y.0.0'
    versions = [
        '1.1.0',
        '1.2.0',
        '1.3.0',
        '2.0.1',
        '3.1.2',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(3 == len(subset))
    assert('1.1.0' in subset)  # Surprising, but it's only here because 1.0.0 (current_version) is not in the list
    assert('2.0.1' in subset)
    assert('3.1.2' in subset)


def test_next_best_specitemmask_matching_versions_yes3():
    mask = '-Y.0.0'
    versions = [
        '1.0.0',
        '1.1.0',
        '1.2.0',
        '1.3.0',
        '2.0.1',
        '3.1.2',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('2.0.1' in subset)
    assert('3.1.2' in subset)


def test_next_best_specitemmask_matching_versions_yes4():
    mask = '-Y.0.0'
    versions = [
        '1.0.0',
        '2.0.1',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('2.0.1' in subset)


def test_next_best_specitemmask_matching_versions_yes5():
    mask = '-Y.Y.0'
    versions = [
        '1.0.0',
        '1.1.0',
        '1.1.1',
        '1.2.1',
        '2.0.1',
    ]
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('1.2.1' in subset)
    assert('2.0.1' in subset)


def test_next_best_specitemmask_matching_versions_yes6():
    mask = '-Y.0.0'
    versions = [
        '1.0.0',
        '1.1.0',
        '1.1.1',
        '1.2.1',
        '2.0.1',
    ]
    current_version = '1.2.1'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(1 == len(subset))
    assert('2.0.1' in subset)


def test_next_best_specitemmask_with_range_1():
    """Mixing semver range operators and next_best matching is not allowed"""
    mask = '-^1.0.0'
    versions = [
        '1.0.0',
    ]
    with pytest.raises(ValueError):
        VersionFilter.semver_filter(mask, versions)


def test_next_best_example():
    versions = ['1.0.0', '2.0.0', '3.0.1']
    current_version = '2.0.0'
    assert VersionFilter.semver_filter('Y.0.0', versions, current_version) == []
    # but with next_best ...
    assert VersionFilter.semver_filter('-Y.0.0', versions, current_version) == ['3.0.1']


def test_greater_than_next_major():
    mask = '>=L1.0.0'
    versions = ['1.0.0', '1.0.1', '1.1.0', '1.2.0', '2.0.0', '2.0.1', '3.0.0']
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(3 == len(subset))
    assert('2.0.0' in subset)
    assert('2.0.1' in subset)
    assert('3.0.0' in subset)


def test_in_next_major():
    mask = 'L1.Y.Y'
    versions = ['1.0.0', '1.0.1', '1.1.0', '1.2.0', '2.0.0', '2.0.1', '3.0.0']
    current_version = '1.0.0'
    subset = VersionFilter.semver_filter(mask, versions, current_version)
    assert(2 == len(subset))
    assert('2.0.0' in subset)
    assert('2.0.1' in subset)


def test_validate_only():
    invalid_masks = ['L1.Y.Y', '1.0.0', '1.0.0', '1.0', '1', 'L', 'L.Y', 'L.Y.Y', 'L.Y.Y', 'Y.0.0', 'Y.0.0', 'Y.Y.0',
                     'L.Y.0', 'Y.Y.Y', '2.0.0', 'Y.Y.Y', '1.8.Y', '1.8.Y || 1.10.Y', 'Y.Y.0 || L.L.Y',
                     '>1.8.0 && <2.0.0', 'L.Y.Y', 'L.Y.Y-Y', 'L.Y.Y-Y', 'L.Y.Y', 'Y.Y.Y', 'Y.Y.Y-Y', 'L.L.Y-alpine',
                     'L.L.Y-alpine3.6', 'L.L.Y-L', 'L.L.Y-L', 'L.L.Y', 'L.L.Y', 'L.L.Y', 'L.L.Y', 'L.L.Y', '^1.0.0',
                     '^L.L.L', '^L.L.L', '-1.0.0', '-1.0.0', '-1.0.0', '-L.0.0', '-L.0.0', '-L.0.0', '-Y.0.0', '-Y.0.0',
                     '-Y.0.0', '-Y.0.0', '-Y.Y.0', '-Y.0.0', '>=L1.0.0', 'L1.Y.Y', 'L.L.L-L']

    for m in invalid_masks:
        assert(VersionFilter.semver_validate(m) is True)

    invalid_masks = ['-^1.1.1', 'a', '?.?.?', '', 'YY.0.0', 'LL.0.0']
    for m in invalid_masks:
        assert(VersionFilter.semver_validate(m) is False)
