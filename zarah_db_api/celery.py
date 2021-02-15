from celery import Celery

app = Celery('zarah',
             broker='redis://localhost',
             include=['document.tasks', 'authority_list.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()