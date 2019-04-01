from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.app.config['CELERY_RESULT_BACKEND'],
        broker=app.app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
