from django.db import models

# Create your models here.


class Food(models.Model):
    """食品"""
    name = models.CharField('食品名', max_length=255, blank=False)
    url = models.CharField('URL', max_length=255, default="")
    price = models.IntegerField('価格', default=0)
    gram = models.IntegerField('グラム', default=0)

    energy = models.FloatField ('エネルギー', default=0)
    """三大栄養素"""
    protein = models.FloatField('たんぱく質', default=0)
    fat = models.FloatField('脂質', default=0)
    carbohydrates = models.FloatField('炭水化物', default=0)
    """ビタミン"""
    vitaminA = models.FloatField('ビタミンA', default=0)
    vitaminD = models.FloatField('ビタミンD', default=0)
    vitaminE = models.FloatField('ビタミンE', default=0)
    vitaminK = models.FloatField('ビタミンK', default=0)
    vitaminB1 = models.FloatField('ビタミンB1', default=0)
    vitaminB2 = models.FloatField('ビタミンB2', default=0)
    niacin = models.FloatField('ナイアシン', default=0)
    vitaminB6 = models.FloatField('ビタミンB6', default=0)
    vitaminB12 = models.FloatField('ビタミンB12', default=0)
    folate = models.FloatField('葉酸', default=0)
    pantothenic = models.FloatField('パントテン酸', default=0)
    biotin = models.FloatField('ビオチン', default=0)
    vitaminC = models.FloatField('ビタミンC', default=0)
    """ミネラル"""
    sodium = models.FloatField('ナトリウム', default=0)
    potassium = models.FloatField('カリウム', default=0)
    calcium = models.FloatField('カルシウム', default=0)
    magnesium = models.FloatField('マグネシウム', default=0)
    phosphorus = models.FloatField('リン', default=0)
    iron = models.FloatField('鉄', default=0)
    zinc = models.FloatField('亜鉛', default=0)
    copper = models.FloatField('銅', default=0)
    manganese = models.FloatField('マンガン', default=0)
    iodine = models.FloatField('ヨウ素', default=0)
    selenium = models.FloatField('セレン', default=0)
    chromium = models.FloatField('クロム', default=0)
    molybdenum = models.FloatField('モリブデン', default=0)

    def __str__(self):
        return self.name
