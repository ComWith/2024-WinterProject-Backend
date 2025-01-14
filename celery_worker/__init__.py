from celery import Celery
from app.config import Config

def make_celery(app):

    celery = Celery(
        app.import_name,
        backend=Config.CELERY_RESULT_BACKEND,
        broker=Config.CELERY_BROKER_URL
    )
    celery.conf.update(app.config)

    # Flask 앱 컨텍스트에서 Celery 작업을 실행할 수 있도록 설정
    class ContextTask(celery.Task):
        """Flask 앱 컨텍스트를 포함한 Celery 작업"""
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery

