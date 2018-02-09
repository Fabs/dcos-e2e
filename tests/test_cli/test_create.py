"""
XXX
"""

from textwrap import dedent

from click.testing import CliRunner

from cli import dcos_docker


class TestHelp:
    def test_help(self) -> None:
        """
        Help test is shown with `dcos_docker create --help`.
        """
        runner = CliRunner()
        result = runner.invoke(dcos_docker, ['create', '--help'])
        assert result.exit_code == 0
        # yapf breaks multiline noqa
        # yapf: disable
        expected_help = dedent(
            """\
            Usage: dcos_docker create [OPTIONS] ARTIFACT

              Create a DC/OS cluster.

            Options:
              --linux-distribution [centos-7|ubuntu-16.04|coreos|fedora-23|debian-8]
              --help                          Show this message and exit.
            """# noqa: E501,E261
        )
        # yapf: enable
        assert result.output == expected_help


class TestNoOptions:
    """
    Tests for using `dcos_docker create`
    """

    def test_invalid_artifact_path(self) -> None:
        """
        An error is shown if an invalid artifact path is given.
        """
        runner = CliRunner()
        result = runner.invoke(dcos_docker, ['create', '/not/a/path'])
        assert result.exit_code == 2
        expected_error = (
            'Error: Invalid value for "artifact": '
            'Path "/not/a/path" does not exist.'
        )
        assert expected_error in result.output

    # def test_create(oss_artifact: Path) -> None:
    #     """
    #     XXX
    #     """
    #     runner = CliRunner()
    #     result = runner.invoke(dcos_docker, ['create', str(oss_artifact)])
    #     assert result.exit_code == 0
    #     assert result.output == ''
    #     'create --masters=3'
    #     assert num_masters=3
