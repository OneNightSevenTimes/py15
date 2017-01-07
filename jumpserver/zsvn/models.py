from django.db import models


# Create your models here.
class SVNLog(models.Model):
    manager = models.CharField(max_length=50)
    actionlog = models.TextField()
    type = models.CharField(max_length=50)
    addtime = models.CharField(max_length=50)
    bakfile = models.CharField(max_length=200)

    def __unicode__(self):
        return self.manager


class SVNCommitLog(models.Model):
    ctime = models.DateTimeField()
    user = models.CharField(max_length=50)
    files = models.TextField()
    project = models.CharField(max_length=50)
    commitlog = models.CharField(max_length=500)

    def __unicode__(self):
        return self.user


