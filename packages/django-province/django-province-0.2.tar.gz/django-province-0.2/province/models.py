# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.


class Province(models.Model):

    title = models.CharField(max_length=100)

    def __unicode__(self):

        return self.title

    def get_api_url(self):
        return reverse("api:province:detail", kwargs={"id": self.id})

    def get_api_url_city(self):
        return reverse("api:province:city-api:list", kwargs={"province_id": self.id})

    def get_api_url_shahrak(self):
        return reverse("api:province:shahrak-api:list", kwargs={"province_id": self.id})


class City(models.Model):

    province = models.ForeignKey(Province)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s - %s"%(self.province.title, self.title)

    def get_api_url(self):
        return reverse("api:province:city-api:detail", kwargs={"province_id": self.province.id, "id": self.id})

    def get_api_url_town(self):
        return reverse("api:province:city-api:town-api:list", kwargs={"province_id": self.province.id, "city_id": self.id})


class Shahrak(models.Model):

    province = models.ForeignKey(Province)
    title = models.TextField()

    def __unicode__(self):
        return "%s - %s"%(self.province.title, self.title)

    def get_api_url(self):
        return reverse("api:province:shahrak-api:detail", kwargs={"province_id": self.province.id, "id": self.id})


class Town(models.Model):

    city = models.ForeignKey(City)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s - %s"%(self.city.title, self.title)

    def get_api_url(self):
        return reverse("api:province:city-api:town-api:detail", kwargs={"province_id": self.city.province.id, "city_id": self.city.id, "id": self.id})