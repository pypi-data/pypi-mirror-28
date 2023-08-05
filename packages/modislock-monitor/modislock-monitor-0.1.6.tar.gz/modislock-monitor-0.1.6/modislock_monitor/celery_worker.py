from modislock_monitor.tasks import app
from modislock_monitor.config import load_config

config = load_config()


def main():
    log_level = 'INFO' if config.get('DEBUG') is False else 'DEBUG'

    argv = [
        'worker',
        '--loglevel=' + log_level
    ]
    app.worker_main(argv)


if __name__ == '__main__':
    main()

