import logging

from mercury.common.configuration import MercuryConfiguration
from mercury.common.task_managers.base.manager import Manager
from mercury.common.task_managers.redis.task import RedisTask
from mercury.common.transport import SimpleRouterReqClient

from mercury.backend.rpc_client import RPCClient
from mercury.backend.configuration import (
    add_common_options, BACKEND_CONFIG_FILE
)


log = logging.getLogger(__name__)


def options():
    configuration = MercuryConfiguration(
        'mercury-rpc-worker',
        BACKEND_CONFIG_FILE,
        description='Manager process for RPC workers'
    )

    add_common_options(configuration)

    configuration.add_option('backend.redis.host',
                             default='localhost',
                             help_string='Redis server address')

    configuration.add_option('backend.redis.port',
                             default=6379,
                             special_type=int,
                             help_string='Redis server port')

    configuration.add_option('backend.redis.queue',
                             default='rpc_task_queue',
                             help_string='The queue to use for RPC tasks')

    configuration.add_option('backend.workers.threads',
                             special_type=int,
                             default=4)

    configuration.add_option('backend.workers.max_requests_per_thread',
                             special_type=int,
                             default=100)

    configuration.add_option('backend.rpc_router',
                             required=True,
                             help_string='The RPC service router')

    return configuration.scan_options()


class RPCTask(RedisTask):
    def __init__(self, rpc_router, redis_host, redis_port, redis_queue):
        """

        :param rpc_router:
        :param redis_host:
        :param redis_port:
        :param redis_queue:
        """
        self.rpc_router = rpc_router
        super(RPCTask, self).__init__(redis_host, redis_port, redis_queue)

    def do(self):
        url = 'tcp://{host}:{port}'.format(**self.task)
        client = SimpleRouterReqClient(url, linger=10, response_timeout=10)
        _payload = {
            'category': 'rpc',
            'method': self.task['method'],
            'args': self.task['args'],
            'kwargs': self.task['kwargs'],
            'task_id': self.task['task_id'],
            'job_id': self.task['job_id']
        }
        log.info('Dispatching task: %s' % self.task)
        try:
            response = client.transceiver(_payload)
        except OSError as os_error:
            log.error(f'Agent at {url} has gone away while handling '
                      f'{self.task["task_id"]}')
            self.rpc_router.complete_task({
                'task_id': self.task['task_id'],
                'status': 'ERROR',
                'response': f'Dispatch Error: {os_error}'
            })
        else:
            if response['status'] != 0:
                self.rpc_router.complete_task({
                    'task_id': self.task['task_id'],
                    'status': 'ERROR', 'response': 'Dispatch Error: %s' % response})

            # Clean up the session
        finally:
            client.close()


def configure_logging(config):
    logging.basicConfig(level=logging.getLevelName(config.logging.level),
                        format=config.logging.format)


def main():
    config = options()

    configure_logging(config)

    # Set this up for access from our threads

    rpc_router_client = RPCClient(config.backend.rpc_router)

    manager = Manager(RPCTask, config.backend.workers.threads,
                      config.backend.workers.max_requests_per_thread,
                      handler_args=(rpc_router_client,
                                    config.backend.redis.host,
                                    config.backend.redis.port,
                                    config.backend.redis.queue))
    manager.manage()


if __name__ == '__main__':
    main()
