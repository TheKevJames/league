try:
    import os

    import raven

    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SENTRY = raven.Client(dsn=SENTRY_DSN)
except ImportError:
    class ravenClient:
        def captureException(self):
            pass

    SENTRY = ravenClient()
