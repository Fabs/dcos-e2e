"""
Tests for the Docker backend.
"""

import os
import uuid
from pathlib import Path

import pytest
from passlib.hash import sha512_crypt

from dcos_e2e.backends import AWS
from dcos_e2e.cluster import Cluster


class TestAWSBackend:
    """
    Tests for functionality specific to the AWS backend.
    """

    def test_copy_to_installer_not_supported(self) -> None:
        """
        The AWS backend does not support copying files to the installer.
        """
        with pytest.raises(NotImplementedError) as excinfo:
            Cluster(
                cluster_backend=AWS(),
                files_to_copy_to_installer={Path('/'): Path('/')},
            )

        expected_error = (
            'Copying files to the installer is currently not supported by the '
            'AWS backend.'
        )

        assert str(excinfo.value) == expected_error

    def test_install_dcos_from_path(self, oss_artifact: Path) -> None:
        """
        The AWS backend requires a build artifact URL in order to launch a
        DC/OS cluster.
        """
        with Cluster(
            cluster_backend=AWS(),
            masters=1,
            agents=0,
            public_agents=0,
        ) as cluster:
            with pytest.raises(NotImplementedError) as excinfo:
                cluster.install_dcos_from_path(build_artifact=oss_artifact)

        expected_error = (
            'The AWS backend does not support the installation of build '
            'artifacts passed via path. This is because a more efficient'
            'installation method exists in ``install_dcos_from_url``.'
        )

        assert str(excinfo.value) == expected_error

    def test_run_integration_test(self, license_key_contents: str) -> None:
        """
        It is possible to run DC/OS integration tests on AWS.
        """
        superuser_username = str(uuid.uuid4())
        superuser_password = str(uuid.uuid4())
        config = {
            'superuser_username': superuser_username,
            'superuser_password_hash': sha512_crypt.hash(superuser_password),
            'fault_domain_enabled': False,
            'license_key_contents': license_key_contents,
            'security': 'strict',
        }

        aws_backend = AWS(workspace_dir=Path('/tmp'))

        with Cluster(
            cluster_backend=aws_backend,
            masters=1,
        ) as cluster:

            (master, ) = cluster.masters

            result = master.run(
                args=['echo', '$USER'],
                shell=True,
            )

            assert result.stdout.decode() == 'centos\n'

            cluster.install_dcos_from_url(
                build_artifact=os.environ['INSTALLER_URL'],
                extra_config=config,
                log_output_live=True,
            )

            cluster.wait_for_dcos_ee(
                superuser_username=superuser_username,
                superuser_password=superuser_password,
            )

            # No error is raised with a successful command.
            cluster.run_integration_tests(
                pytest_command=['pytest', '-vvv', '-s', '-x', 'test_tls.py'],
                env={
                    'DCOS_LOGIN_UNAME': superuser_username,
                    'DCOS_LOGIN_PW': superuser_password,
                },
                log_output_live=True,
            )

            # Test running on Travis
            # Document how to run tests locally.
            # Why not self.launcher.wait?

            # Nice to have:
            # Get Bilal to use it
            # Get it to work with Windows

            # Vendoring:
            # Change DC/OS Launch as there is an error on import after
            # vendoring.
            # Idea is for it do use inspect rather than pkg_resource
            #
            # Make a script which uses ``python-vendorize``internals to remap
            # the dcos-test-utils imports.
