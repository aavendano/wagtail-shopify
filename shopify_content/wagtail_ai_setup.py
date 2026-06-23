from wagtail.models import Page

from wagtail_ai.panels import AITitleFieldPanel

Page.content_panels = [AITitleFieldPanel('title')]
