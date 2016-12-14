from django.db import models

# Create your models here.


class Food(models.Model):
    """食品"""
    name = models.CharField('食品名', max_length=255, blank=False)
    url = models.CharField('URL', max_length=255, default="")
    price = models.IntegerField('価格', default=0)
    energy = models.FloatField ('エネルギー', default=0)
    carbohydrates = models.FloatField('炭水化物', default=0)
    protein = models.FloatField('タンパク質', default=0)
    fat = models.FloatField('脂肪', default=0)
    calcium = models.FloatField('カルシウム', default=0)
    iron = models.FloatField('鉄', default=0)
    vitaminA = models.FloatField('ビタミンA', default=0)
    vitaminB1 = models.FloatField('ビタミンB1', default=0)
    vitaminB2 = models.FloatField('ビタミンB2', default=0)
    vitaminC = models.FloatField('ビタミンC', default=0)

    def __str__(self):
        return self.name
