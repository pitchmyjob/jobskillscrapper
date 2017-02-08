from django.contrib import admin

from .models import Job, Skill, ParsedProfile, ProfilToParse


class NameScrapperAdmin(object):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


class URLScrapperAdmin(object):
    fields = ('url',)
    list_display = ('url',)
    search_fields = ('url',)


@admin.register(Job)
class JobAdmin(NameScrapperAdmin, admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(NameScrapperAdmin, admin.ModelAdmin):
    pass


@admin.register(ParsedProfile)
class ParsedProfileAdmin(URLScrapperAdmin, admin.ModelAdmin):
    pass


@admin.register(ProfilToParse)
class ProfilToParseAdmin(URLScrapperAdmin, admin.ModelAdmin):
    pass
