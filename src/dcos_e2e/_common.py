"""
Common utilities for end to end tests.
"""

import logging
from subprocess import (
    PIPE,
    STDOUT,
    CalledProcessError,
    CompletedProcess,
    Popen,
)
from typing import Dict, List, Optional, Union

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def run_subprocess(
    args: List[str],
    log_output_live: bool,
    cwd: Optional[Union[bytes, str]] = None,
    env: Optional[Dict[str, str]] = None,
) -> CompletedProcess:
    """
    Run a command in a subprocess.

    Args:
        args: See :py:func:`subprocess.run`.
        log_output_live: If `True`, log output live. If `True`, stderr is
            merged into stdout in the return value.
        cwd: See :py:func:`subprocess.run`.
        env: See :py:func:`subprocess.run`.

    Returns:
        See :py:func:`subprocess.run`.

    Raises:
        subprocess.CalledProcessError: See :py:func:`subprocess.run`.
    """
    # It is hard to log output of both stdout and stderr live unless we
    # combine them.
    # See http://stackoverflow.com/a/18423003.
    if log_output_live:
        process_stderr = STDOUT
    else:
        process_stderr = PIPE

    with Popen(
        args=args,
        cwd=cwd,
        stdout=PIPE,
        stderr=process_stderr,
        env=env,
    ) as process:
        try:
            if log_output_live:
                stdout = b''
                stderr = b''
                for line in process.stdout:
                    LOGGER.debug(
                        line.rstrip().decode('ascii', 'backslashreplace')
                    )
                    stdout += line
                # stderr/stdout are not readable anymore which usually means
                # that the child process has exited. However, the child
                # process has not been wait()ed for yet, i.e. it has not yet
                # been reaped. That is, its exit status is unknown. Read its
                # exit status.
                process.wait()
            else:
                stdout, stderr = process.communicate()
        except:  # noqa: B001 pragma: no cover
            # We clean up if there is an error while getting the output.
            # This may not happen while running tests so we ignore coverage.
            process.kill()
            process.wait()
            raise
        if stderr:
            if process.returncode == 0:
                log = LOGGER.warning
                log(repr(args))
            else:
                log = LOGGER.error
            for line in stderr.rstrip().split(b'\n'):
                log(line.rstrip().decode('ascii', 'backslashreplace'))
        if process.returncode != 0:
            raise CalledProcessError(
                process.returncode,
                args,
                output=stdout,
                stderr=stderr,
            )
    return CompletedProcess(args, process.returncode, stdout, stderr)
