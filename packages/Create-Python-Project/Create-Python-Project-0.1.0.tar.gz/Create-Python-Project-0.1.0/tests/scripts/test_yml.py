"""
    tests.scripts.test_yml
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for .yml scripts manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""
import os

from create_python_project.scripts import YmlScript


def test_yml_script(repo_path):
    yml_script = YmlScript()
    for filename in ['.travis.yml', '.gitlab-ci.yml']:
        yml_script.set_source(os.path.join(repo_path, filename))
        assert yml_script.source.source_path == os.path.join(repo_path, filename)
        assert yml_script.publish() is not None


def test_yml_script_change():
    source = \
        'sudo: false\n' \
        'language: python # language python\n' \
        '\n' \
        'cache: pip\n' \
        '\n' \
        'matrix:\n' \
        '  include:\n' \
        '    - os: linux\n' \
        '      python: 3.5\n' \
        '      env: TOXENV=py,codecov\n' \
        '    - python: 3.6\n' \
        '\n' \
        'install:\n' \
        '  - git config --global user.email "runner@travis.org"\n' \
        '\n'

    yml_script = YmlScript(source=source)

    updated_source = \
        'sudo: false\n' \
        'language: python # language python\n' \
        '\n' \
        'cache: pip\n' \
        '\n' \
        'matrix:\n' \
        '  include:\n' \
        '    - os: linux\n' \
        '      python: 3.5\n' \
        '      env: TOXENV=py,codecov\n' \
        '    - python: 3.6\n' \
        '\n' \
        'install:\n' \
        '  - git config --global user.email "new-runner@travis.org"\n' \
        '\n'
    assert yml_script.publish(old_value='runner@travis.org',
                              new_value='new-runner@travis.org') == updated_source

    updated_source = \
        'sudo: false\n' \
        'language: java # language java\n' \
        '\n' \
        'cache: pip\n' \
        '\n' \
        'matrix:\n' \
        '  include:\n' \
        '    - os: linux\n' \
        '      python: 3.5\n' \
        '      env: TOXENV=py,codecov\n' \
        '    - python: 3.6\n' \
        '\n' \
        'install:\n' \
        '  - git config --global user.email "new-runner@travis.org"\n' \
        '\n'
    assert yml_script.publish(old_value='python', new_value='java') == updated_source
