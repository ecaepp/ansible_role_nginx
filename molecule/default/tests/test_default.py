import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


NGINX_FILES = ['nginx.conf', 'general.conf', 'nginx_repo.list']


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pkg_installed(host):
    p = host.package('nginx')

    assert p.is_installed


def test_file_exists(host):
    f = host.file("/etc/apt/sources.list.d/nginx_repo.list")

    assert f.exists


# Example test code
# def test_myvar_using_get_variables(host):
#     all_variables = host.ansible.get_variables()
#     assert 'myvar' in all_variables
#     assert all_variables['myvar'] == 'myvalue'


# def test_myvar_using_debug_var(host):
#     result = host.ansible("debug", "var=myvar")
#     assert 'myvar' in result
#     assert result['myvar'] == 'myvalue'


# def test_myvar_using_debug_msg(host):
#     result = host.ansible("debug", "msg={{ myvar }}")
#     assert 'msg' in result
#     assert result['msg'] == 'myvalue'
