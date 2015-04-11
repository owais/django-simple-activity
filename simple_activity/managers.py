from django.db import models


class ActionManager(models.Manager):
    def for_clients(self):
        return self.exclude(visibility=self.model.VENDORS)

    def for_vendors(self):
        return self.exclude(visibility=self.model.CLIENTS)
