# First experiment will happen with:
# * DC/OS OSS - Simpler, later we need Enterprise
# * CentOS on Vagrant
# , with one master node

from pathlib import Path
from textwrap import dedent

from dcos_e2e.cluster import Cluster
from dcos_e2e.backends import Vagrant


def test_selinux(oss_artifact: Path) -> None:
    cluster_backend = Vagrant()
    with Cluster(
        masters=1,
        agents=0,
        public_agents=0,
        cluster_backend=cluster_backend,
    ) as cluster:
        # This shows that we are in 'permissive' mode, not 'enforcing' mode.
        # A next step is to change this mode.
        expected_sestatus = dedent(
            """
            SELinux status:                 enabled
            SELinuxfs mount:                /sys/fs/selinux
            SELinux root directory:         /etc/selinux
            Loaded policy name:             targeted
            Current mode:                   permissive
            Mode from config file:          permissive
            Policy MLS status:              enabled
            Policy deny_unknown status:     allowed
            Max kernel policy version:      28
            """
        )
        (master, ) = cluster.masters
        sestatus_result = master.run(
            args=['sestatus'],
            sudo=True,
        )

        sestatus_output = sestatus_result.stdout.decode().strip()
        assert sestatus_output == expected_sestatus.strip()
        return

        cluster.install_dcos_from_path(
            build_artifact=oss_artifact,
            dcos_config=cluster.base_config,
            log_output_live=True,
        )

        cluster.wait_for_dcos_oss()
