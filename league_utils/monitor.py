try:
    import os

    import raven

    try:
        SENTRY_DSN = os.environ['SENTRY_DSN']
    except KeyError:
        SENTRY_DSN = open('/run/secrets/sentry_dsn_league').read().rstrip()

    SENTRY = raven.Client(dsn=SENTRY_DSN)
except (ImportError, IOError):
    class ravenClient:
        # pylint: disable=too-few-public-methods
        def captureException(self):
            pass

    SENTRY = ravenClient()
