from django.db import models
from wheelcms_axle.content import Content
from django import forms

"""
Ook hier een opsplitsing naar "lean model" en "spoke achtig"
wrapper

Not sure what pattern I'm using is (and if I should care).
Keep models lean (skinny), put functionality into separate class
Do skinny models wear thick coats? 

"""
class GearBaseModel(models.Model):
    class Meta:
        abstract = True

    content = models.ForeignKey(Content, related_name="bells")
    type = models.CharField(max_length=40)
    position = models.IntegerField(default=0)
    slot = models.CharField(max_length=40)

    def save(self, *a, **b):
        self.type = self.__class__.__name__.lower()
        super(GearBaseModel, self).save(*a, **b)

class GearModel(GearBaseModel):
    pass

def gearformfactory(model):
    m = model
    class Form(forms.ModelForm):
        class Meta:
            model = m
            exclude = ["slot", "content", "position", "type"]
    return Form

class HTMLGear(GearModel):
    body = models.TextField(blank=True)

class HTMLGearForm(gearformfactory(HTMLGear)):
    pass
    # body = forms.CharField(widget=TinyMCE(), required=False)
"""
    Definieer een tag ("placeholder") met een naam (en evt. inheritance
    default). In view mode zoekt/verzamelt/toont deze bells, in edit mode
    kan je ze toevoegen/verplaatsen/verwijderen en bewerken.

    edit mode wordt (vooralsnog?) een aparte tab onder edit

"""

class TwitterGear(GearModel):
    name = models.CharField(max_length=100)

class TwitterGearForm(gearformfactory(TwitterGear)):
    pass

from django.template.loader import render_to_string

class GearBox(object):
    id = "base"
    template = ""

    def __init__(self, b=None):
        self.instance = b

    def render_view(self):
        return render_to_string(self.template, dict(bell=self.instance))

    def render_form(self, data=None):
        return self.form(data, instance=self.instance)

    @classmethod
    def forGear(cls, bell):
        bell = getattr(bell, bell.type)
        for w in boxes:
            if w.model == bell.__class__:
                return w(bell)
        return None

class TwitterGearBox(GearBox):
    id = "twitter"
    name = "Twitter fraglet"
    kaka = id
    model = TwitterGear
    form = TwitterGearForm

    template = "twitterbell.html"

class HTMLGearBox(GearBox):
    id = "html"
    name = "HTML fraglet"
    kaka = id
    model = HTMLGear
    form = HTMLGearForm

    template = "htmlbell.html"

boxes = [HTMLGearBox, TwitterGearBox]
boxes_map = dict((w.id, w) for w in boxeswhistles)
