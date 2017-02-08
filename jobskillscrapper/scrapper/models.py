from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=250)


class Skill(models.Model):
    name = models.CharField(max_length=250)


class JobSkill(models.Model):
    job = models.ForeignKey(Job)
    skill = models.ForeignKey(Skill)


class ParsedProfile(models.Model):
    url = models.URLField(max_length=250)


class ProfilToParse(models.Model):
    url = models.URLField(max_length=250)
    site = models.CharField(max_length=250, null=True)
