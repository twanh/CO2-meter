from celery import Celery

def create_celery(app):
    celery = Celery(
        app.name,
        backend=app.config["result_backend"],
        broker=app.config["CELERY_BROKER_URL"],
        include=['app.tasks'],
        ack_late=True
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    celery.conf.beat_schedule = {
        'update-all-sensors-every-10-min': {
            'task': 'app.tasks.update_all_sensors',
            'schedule': 10*60 # 10 minutes 
        }
    }

    return celery
