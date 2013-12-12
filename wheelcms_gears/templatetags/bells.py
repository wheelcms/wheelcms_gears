from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.tag(name="bell")
def bell(parser, token):
    try:
        tag_name, bellname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument"
                                           % token.contents.split()[0])

    bellname = bellname.strip("\"'")
    return BellNode(bellname)

from ..models import whistles, Whistle

class BellNode(template.Node):
    def __init__(self, bellname):
        self.name = bellname

    def render(self, context):
        instance = context['instance']
        bells_edit = context.get('bells_edit', False)

        bellcontent = []
        for b in instance.content().bells.filter(slot=self.name).order_by("position"):
            view = None
            form = None

            w = Whistle.forBell(b)
            if w:
                view = w.render_view()
                if bells_edit:
                    form = w.render_form()

                bellcontent.append(dict(view=view, form=form))

        tpl = render_to_string("bell_slot.html",
              dict(whistles=(dict(id=w.id, name=w.name) for w in whistles),
              bellcontent=bellcontent,
              slot=self.name,
              bells_edit=bells_edit))
        return tpl
