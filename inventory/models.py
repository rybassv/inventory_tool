from django.db import models


class Blueprint(models.Model):
    blueprint_name = models.CharField('Blueprint name', max_length=200, unique=True)

    def __str__(self):
        return self.blueprint_name

    class Meta:
        verbose_name = 'Blueprint'
        verbose_name_plural = 'Blueprints'


class Device(models.Model):
    production_date = models.DateTimeField('Production date', auto_now_add=True)
    parts_price = models.FloatField('Total parts price', default=0)
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)

    def __str__(self):
        return 'Assembled ' + self.blueprint.blueprint_name

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'


class Part(models.Model):
    part_name = models.CharField('Part name', max_length=200, unique=True)
    measure_unit = models.CharField('Measure unit', max_length=20)
    url = models.CharField('Shop URL', max_length=200)

    def __str__(self):
        return self.part_name

    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'


class BOM(models.Model):
    qty = models.IntegerField('Part quantity')
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def __str__(self):
        return self.part.part_name + ' in ' + self.blueprint.blueprint_name

    class Meta:
        verbose_name = 'BOM'
        verbose_name_plural = 'BOMs'


class Inventory(models.Model):
    income = models.IntegerField('Part income', default=0)
    usage = models.IntegerField('Part usage', default=0)
    price_per_unit = models.FloatField('Unit price', default=0)
    transaction_date = models.DateTimeField('Transaction date', auto_now_add=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.part.part_name

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'


