from django.db import models

# Create your models here.


class ContentModel(models.Model):
    STATUS_CHOICES = (
        ("terms", "Terms"),
        ("pp", "PP"),
        ("aout", "About")
    )
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='terms')
    title = models.CharField(max_length=250)
    text = models.TextField()

    def __str__(self):
        return self.title




