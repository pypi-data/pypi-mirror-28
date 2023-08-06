import os
import errno
import sys

from mockfs import replace_builtins, restore_builtins
from mock import Mock, MagicMock
import pytest
from yaml import load

from six.moves import builtins
from jasmine.entry_points import (
    continuous_integration,
    query,
    standalone,
    mkdir_p,
    install
)
from jasmine.ci import CIRunner
import jasmine.standalone


class FakeApp(object):
    def __init__(self, jasmine_config=None):
        FakeApp.app = self
        self.run = MagicMock(name='run')

    def run(self, host=None, port=None, blocking=False):
        pass


@pytest.fixture
def mockfs(request):
    mfs = replace_builtins()
    request.addfinalizer(lambda: restore_builtins())
    return mfs


@pytest.fixture
def mockfs_with_config(request):
    mfs = replace_builtins()
    mfs.add_entries({
        "/spec/javascripts/support/jasmine.yml": """
        src_dir: src
        spec_dir: spec
        """
    })
    request.addfinalizer(lambda: restore_builtins())
    return mfs

@pytest.fixture
def mockfs_with_config_and_custom_config(request):
    mfs = replace_builtins()
    mfs.add_entries({
        "/spec/javascripts/support/jasmine.yml": """
        src_dir: src
        spec_dir: spec
        """,
        "/custom/path/to/jasmine.yml": """
        src_dir: custom_src
        spec_dir: custom_spec
        """
    })
    request.addfinalizer(lambda: restore_builtins())
    return mfs


@pytest.fixture
def mock_CI_run(request):
    CIRunner.run = MagicMock(name='run')


def test_ci_config_check(mockfs, monkeypatch, mock_CI_run):
    monkeypatch.setattr(sys, 'argv', ['test.py'])

    continuous_integration()
    assert not CIRunner.run.called


def test_continuous_integration__set_browser(monkeypatch, mockfs_with_config, mock_CI_run):
    monkeypatch.setattr(sys, 'argv', ["test.py", "--browser", "firefox"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    continuous_integration()

    CIRunner.run.assert_called_once_with(browser='firefox', show_logs=False, seed=None, app=FakeApp.app)


def test_continuous_integration__browser_default(monkeypatch, mockfs_with_config, mock_CI_run):
    monkeypatch.setattr(sys, 'argv', ["test.py"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    continuous_integration()

    CIRunner.run.assert_called_once_with(browser=None, show_logs=False, seed=None, app=FakeApp.app)


def test_continuous_integration__show_logs(monkeypatch, mockfs_with_config, mock_CI_run):
    monkeypatch.setattr(sys, 'argv', ["test.py", "--logs"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    continuous_integration()

    CIRunner.run.assert_called_once_with(show_logs=True, browser=None, seed=None, app=FakeApp.app)


def test_continuous_integration__set_seed(monkeypatch, mockfs_with_config, mock_CI_run):
    monkeypatch.setattr(sys, 'argv', ["test.py", "--seed", "1234"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    continuous_integration()

    CIRunner.run.assert_called_once_with(seed="1234", show_logs=False, browser=None, app=FakeApp.app)

def test_continuous_integration__custom_config__from_argv(monkeypatch, mockfs_with_config_and_custom_config):
    monkeypatch.setattr(sys, 'argv', ["test.py", "-c", "/custom/path/to/jasmine.yml"])
    fake_standalone = Mock()
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', fake_standalone)

    continuous_integration()

    fake_standalone.assert_called_once()
    standalone_construction_kwargs = fake_standalone.call_args[1]
    called_with_config = standalone_construction_kwargs['jasmine_config'].yaml_file
    assert called_with_config == "/custom/path/to/jasmine.yml"


def test_standalone__set_host(monkeypatch, mockfs_with_config):
    monkeypatch.setattr(sys, 'argv', ["test.py", "-o", "127.0.0.2"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    standalone()

    FakeApp.app.run.assert_called_once_with(host="127.0.0.2", port=8888, blocking=True)


def test_standalone__set_port(monkeypatch, mockfs_with_config):
    monkeypatch.setattr(sys, 'argv', ["test.py", "-p", "1337"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    standalone()

    FakeApp.app.run.assert_called_once_with(host="127.0.0.1", port=1337, blocking=True)


def test_standalone__port_default(monkeypatch, mockfs_with_config):
    monkeypatch.setattr(sys, 'argv', ["test.py"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    standalone()

    FakeApp.app.run.assert_called_once_with(host="127.0.0.1", port=8888, blocking=True)


def test_standalone__port_invalid(monkeypatch, mockfs_with_config):
    FakeApp.app = None
    monkeypatch.setattr(sys, 'argv', ["test.py", "-p", "pants"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    with pytest.raises(SystemExit):
        standalone()

    assert "invalid int value: 'pants'"
    assert FakeApp.app == None

def test_standalone__missing_config(monkeypatch, mockfs):
    FakeApp.app = None
    monkeypatch.setattr(sys, 'argv', ["test.py"])
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

    standalone()

    assert FakeApp.app == None

def test_standalone__custom_config__from_argv(monkeypatch, mockfs_with_config_and_custom_config):
    monkeypatch.setattr(sys, 'argv', ["test.py", "-c", "/custom/path/to/jasmine.yml"])
    fake_standalone = Mock()
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', fake_standalone)

    standalone()

    fake_standalone.assert_called_once()
    standalone_construction_kwargs = fake_standalone.call_args[1]
    called_with_config = standalone_construction_kwargs['jasmine_config'].yaml_file
    assert called_with_config == "/custom/path/to/jasmine.yml"

def test_standalone__custom_config__when_environment_variable_set(monkeypatch, mockfs_with_config_and_custom_config):
    monkeypatch.setattr(sys, 'argv', ["test.py"])
    env_vars = {'JASMINE_CONFIG_PATH': "/custom/path/to/jasmine.yml"}
    monkeypatch.setattr(os, 'environ', env_vars)
    fake_standalone = Mock()
    monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', fake_standalone)

    standalone()

    fake_standalone.assert_called_once()
    standalone_construction_kwargs = fake_standalone.call_args[1]
    called_with_config = standalone_construction_kwargs['jasmine_config'].yaml_file
    assert called_with_config == "/custom/path/to/jasmine.yml"


def test__query__yes(capsys, monkeypatch):
    input_string(monkeypatch, "Y")

    choice = query("Would you like to play a game?")

    out, err = capsys.readouterr()

    assert out == "Would you like to play a game? [Y/n] "
    assert True == choice


def test__query__no(capsys, monkeypatch):
    input_string(monkeypatch, "N")

    choice = query("Would you like to hear some cat facts?")

    out, err = capsys.readouterr()

    assert out == "Would you like to hear some cat facts? [Y/n] "
    assert False == choice


def test__query__default(capsys, monkeypatch):
    input_string(monkeypatch, "")

    choice = query("Would you like to blindly accept my defaults?")

    out, err = capsys.readouterr()

    assert out == "Would you like to blindly accept my defaults? [Y/n] "
    assert True == choice


def test__mkdir_p(mockfs):
    mkdir_p("/pants/a/b/c")

    assert os.path.isdir("/pants")
    assert os.path.isdir("/pants/a")
    assert os.path.isdir("/pants/a/b")
    assert os.path.isdir("/pants/a/b/c")


def test__mkdir_p_error(mockfs, monkeypatch):
    def raise_error(path):
        o = OSError()
        o.errno = errno.EEXIST
        raise o

    monkeypatch.setattr(os, 'makedirs', raise_error)
    mockfs.add_entries({
        '/pants/a/b/c': {}
    })
    mkdir_p("/pants/a/b/c")


def input_string(monkeypatch, string=""):
    try:
        monkeypatch.setattr(builtins, 'raw_input', lambda: string)
    except AttributeError:
        monkeypatch.setattr(builtins, 'input', lambda: string)


def test_install__yes(mockfs, monkeypatch):
    # Should create spec/javascripts/support
    # Should create a spec/javascripts/support/jasmine.yml
    spec_dir = "spec/javascripts/support"
    yaml_file = os.path.join(spec_dir, "jasmine.yml")

    input_string(monkeypatch, "Y")

    install()

    assert os.path.isdir(spec_dir)
    assert os.path.isfile(yaml_file)

    yaml = load(open(yaml_file))

    assert yaml['spec_files'] == ["**/*[Ss]pec.js"]


def test_install__yes__existing_yaml(mockfs, monkeypatch):
    # Should create spec/javascripts/support
    # Should NOT overwrite spec/javascripts/support/jasmine.yml
    spec_dir = "spec/javascripts/support"
    yaml_file = os.path.join(spec_dir, "jasmine.yml")

    mockfs.add_entries({
        '/spec/javascripts/support/jasmine.yml': """
        spec_files:
            - "**/pants.*"
        """
    })

    input_string(monkeypatch, "Y")

    install()

    assert os.path.isdir(spec_dir)
    assert os.path.isfile(yaml_file)

    yaml = load(open(yaml_file))

    assert yaml['spec_files'] == ["**/pants.*"]


def test_install__no(mockfs, monkeypatch):
    # Should NOT create spec/javascripts/support
    # Should NOT create a spec/javascripts/support/jasmine.yml
    spec_dir = "spec/javascripts/support"
    yaml_file = os.path.join(spec_dir, "jasmine.yml")

    input_string(monkeypatch, "N")

    install()

    assert not os.path.isdir(spec_dir)
    assert not os.path.isfile(yaml_file)
