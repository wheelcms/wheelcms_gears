from django.db import models
from wheelcms_axle.content import Content
from django import forms

class BellBase(models.Model):
    class Meta:
        abstract = True

    content = models.ForeignKey(Content, related_name="bells")
    type = models.CharField(max_length=40)
    position = models.IntegerField(default=0)
    slot = models.CharField(max_length=40)

    def save(self, *a, **b):
        self.type = self.__class__.__name__.lower()
        super(BellBase, self).save(*a, **b)

class Bell(BellBase):
    pass

def bellformfactory(model):
    m= model
    class Form(forms.ModelForm):
        class Meta:
            model = m
            exclude = ["slot", "content", "position", "type"]
    return Form

class HTMLBell(Bell):
    body = models.TextField(blank=True)

class HTMLBellForm(bellformfactory(HTMLBell)):
    pass
    # body = forms.CharField(widget=TinyMCE(), required=False)
"""
    Definieer een tag ("placeholder") met een naam (en evt. inheritance
    default). In view mode zoekt/verzamelt/toont deze bells, in edit mode
    kan je ze toevoegen/verplaatsen/verwijderen en bewerken.

    edit mode wordt (vooralsnog?) een aparte tab onder edit

"""

class TwitterBell(Bell):
    name = models.CharField(max_length=100)

class TwitterBellForm(bellformfactory(TwitterBell)):
    pass


## Whistles are the "spokes"

from django.template.loader import render_to_string

class Whistle(object):
    id = "base"
    template = ""

    def __init__(self, b=None):
        self.instance = b

    def render_view(self):
        return render_to_string(self.template, dict(bell=self.instance))

    def render_form(self, data=None):
        return self.form(data, instance=self.instance)

    @classmethod
    def forBell(cls, bell):
        bell = getattr(bell, bell.type)
        for w in whistles:
            if w.model == bell.__class__:
                return w(bell)
        return None

class TwitterWhistle(Whistle):
    id = "twitter"
    name = "Twitter fraglet"
    kaka = id
    model = TwitterBell
    form = TwitterBellForm

    template = "twitterbell.html"

class HTMLWhistle(Whistle):
    id = "html"
    name = "HTML fraglet"
    kaka = id
    model = HTMLBell
    form = HTMLBellForm

    template = "htmlbell.html"

whistles = [HTMLWhistle, TwitterWhistle]
whistle_map = dict((w.id, w) for w in whistles)
