"""
Tools for syncing code to a cluster.
"""

from pathlib import Path

import click

from cli.common.arguments import dcos_checkout_dir_argument
from cli.common.sync import sync_code_to_masters

from ._common import ClusterVMs
from ._options import existing_cluster_id_option


@click.command('sync')
@existing_cluster_id_option
@dcos_checkout_dir_argument
def sync_code(
    cluster_id: str,
    dcos_checkout_dir: str,
) -> None:
    """
    Sync files from a DC/OS checkout to master nodes.

    This syncs integration test files and bootstrap files.

    ``DCOS_CHECKOUT_DIR`` should be set to the path of clone of an open source
    DC/OS or DC/OS Enterprise repository.

    By default the ``DCOS_CHECKOUT_DIR`` argument is set to the value of the
    ``DCOS_CHECKOUT_DIR`` environment variable.

    If no ``DCOS_CHECKOUT_DIR`` is given, the current working directory is
    used.
    """
    cluster_containers = ClusterVMs(cluster_id=cluster_id)
    cluster = cluster_containers.cluster
    sync_code_to_masters(
        cluster=cluster,
        dcos_checkout_dir=Path(dcos_checkout_dir),
    )
