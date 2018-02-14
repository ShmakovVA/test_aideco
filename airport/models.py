from django.db import models


# catalogues

class City(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    code = models.CharField(max_length=4, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.code)

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.code)


class Status(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return u'{}'.format(self.name)


class Gate(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return u'{}'.format(self.name)


class Type_fly(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return u'{}'.format(self.name)


# Flights

class Flight(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False, unique=True)
    direction_from = models.ForeignKey(City, verbose_name=u'Из', related_name='from_city')
    direction_to = models.ForeignKey(City, verbose_name=u'В', related_name='to_city')
    arr_dep = models.PositiveSmallIntegerField()
    counter = models.IntegerField(default=0)

    def increment(self):
        self.counter += 1
        self.save()

    def __str__(self):
        return '[{}]_________[{} - {}]______________{}'.format(self.name, self.direction_from, self.direction_to, self.counter)

    def __unicode__(self):
        return u'[{}]_________[{} - {}]______________{}'.format(self.name, self.direction_from,
                                                self.direction_to, self.counter)


# Fly

class Fly(models.Model):
    flight = models.ForeignKey(Flight, verbose_name=u'Рейс')
    gate = models.ForeignKey(Gate, verbose_name=u'Выход', blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name=u'Статус', blank=True, null=True)
    fly_type = models.ForeignKey(Type_fly, verbose_name=u'Тип ВС', blank=True, null=True)
    time_from = models.DateTimeField(verbose_name=u'Время')
    time_to = models.DateTimeField(verbose_name=u'Время (фактическое)', blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Комментарий')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_closed = False
        if self.status:
            self.was_closed = self.status.name == u'Завершен'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Fly, self).save()
        if not self.was_closed and self.status.name == u'Завершен':
            self.flight.increment()

    def __str__(self):
        return '{}  |  {}  |  {}  |  {}  |  {}  |  {}'.format(self.flight, self.time_from, self.time_to, self.gate,
                                                              self.status,
                                                              self.comment)

    def __unicode__(self):
        return u'{}  |  {}  |  {}  |  {}  |  {}  |  {}'.format(self.flight, self.time_from, self.time_to, self.gate,
                                                               self.status,
                                                               self.comment)
