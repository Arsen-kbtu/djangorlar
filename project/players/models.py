from django.db import models

# placeholder model for players app

class Player(models.Model):
    nickname = models.CharField(max_length=100)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
