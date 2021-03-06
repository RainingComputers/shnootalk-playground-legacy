import socket
import time
import logging

from shnootalk_cc_server.template import fill_template
from shnootalk_cc_server.kube_apply import kube_apply
from shnootalk_cc_server.config import COMPILE_JOB_NAMESPACE

from shnootalk_cc_server.messages import Messages


logger = logging.getLogger(__name__)


def gen_heartbeat_id() -> str:
    timestamp_now = int(time.time())
    hostname_trimmed = socket.gethostname().split('-')[-1]
    return f'{hostname_trimmed}-{timestamp_now}'


def send_heartbeat() -> None:
    program = 'fn main() -> int { println("Hello world") return 0 }'

    job_name = f'heartbeat-{gen_heartbeat_id()}'
    job_definition = fill_template(job_name, {'main.shtk': program}, heartbeat=True)

    try:
        kube_apply(job_definition, COMPILE_JOB_NAMESPACE)
    except Exception:
        logger.exception(Messages.UNABLE_TO_SPAWN_HEARTBEAT, job_name)
