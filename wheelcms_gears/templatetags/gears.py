from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.tag(name="gear")
def gear(parser, token):
    try:
        tag_name, gearname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument"
                                           % token.contents.split()[0])

    gearname = gearname.strip("\"'")
    return GearNode(gearname)

from ..models import whistles, Whistle

class GearNode(template.Node):
    def __init__(self, gearname):
        self.name = gearname

    def render(self, context):
        instance = context['instance']
        gears_edit = context.get('gears_edit', False)

        gearcontent = []
        for b in instance.content().gears.filter(slot=self.name).order_by("position"):
            view = None
            form = None

            w = Whistle.forGear(b)
            if w:
                view = w.render_view()
                if gears_edit:
                    form = w.render_form()

                gearcontent.append(dict(view=view, form=form))

        tpl = render_to_string("gear_slot.html",
              dict(whistles=(dict(id=w.id, name=w.name) for w in whistles),
              gearcontent=gearcontent,
              slot=self.name,
              gears_edit=gears_edit))
        return tpl
