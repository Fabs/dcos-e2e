# First experiment will happen with:
# * DC/OS OSS - Simpler, later we need Enterprise
# * CentOS on Vagrant
# , with one master node

from pathlib import Path

from dcos_e2e.backends import Vagrant


def test_selinux(oss_artifact: Path) -> None:
    cluster_backend = Vagrant()
    with Cluster(
        masters=1,
        agents=0,
        public_agents=0,
        cluster_backend=cluster_backend,
    ) as cluster:
        (master, ) = cluster.masters
        import pdb; pdb.set_trace()
        # TODO enable SELinux here
        cluster.install_dcos_from_path(
            build_artifact=oss_artifact,
            dcos_config=cluster.base_config,
            log_output_live=True,
        )

        cluster.wait_for_dcos_oss()
