import logging
import subprocess

LOG = logging.getLogger(__name__)


def run(*cmd, **kwargs):
    """Log and run a command."""
    cwd = kwargs.get('cwd')
    capture = kwargs.get('capture')
    capture_stderr = kwargs.get('capture_stderr')
    env = kwargs.get('env')

    LOG.info('%s', ' '.join(cmd))

    if capture or capture_stderr:
        stderr = subprocess.STDOUT if capture_stderr else None
        return subprocess.check_output(cmd, stderr=stderr, cwd=cwd)

    subprocess.check_call(cmd, cwd=cwd, env=env)
