from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from wagtailschemaorg.models import PageLDMixin
from wagtailschemaorg.utils import extend, image_ld

from molo.core.blocks import MarkDownBlock
from molo.core.models import MoloMediaBlock, ArticlePage, SectionPage


class ExtendedArticlePage(PageLDMixin, ArticlePage):
    structured_data = StreamField(
        blocks.StreamBlock([
            ('faq', blocks.StructBlock([
                ('title_for_faq', blocks.CharBlock(required=False)),
                ('question_and_answer', blocks.ListBlock(blocks.StructBlock([
                    ('question', blocks.CharBlock()),
                    ('answer', blocks.CharBlock()),
                ]))),
            ], icon='help', max_num=1)),

            ('how_to', blocks.StructBlock([
                ('title_for_how_to', blocks.CharBlock(required=False)),
                ('image_when_finished', ImageChooserBlock(required=False)),
                ('description', MarkDownBlock(required=False)),
                ('estimated_cost', blocks.CharBlock(required=False)),
                ('materials_required', blocks.ListBlock(
                    blocks.CharBlock(label='material'), default=[])),
                ('tools_required', blocks.ListBlock(
                    blocks.CharBlock(label='tool'), default=[])),
                ('steps', blocks.ListBlock(blocks.StructBlock([
                    ('step_name', blocks.CharBlock()),
                    ('step_image', ImageChooserBlock(required=False)),
                    ('step_parts', blocks.StreamBlock([
                        ('instruction', blocks.CharBlock()),
                        ('suggestion', blocks.CharBlock()),
                    ], required=False)),
                ]))),
            ], icon='list-ul', max_num=1)),

        ], max_num=1),
        null=True,
        blank=True,
    )

    # Replace ArticlePage.body with iogt_body
    # (e.g. below Title, Subtitle and Image)
    content_panels = \
        ArticlePage.content_panels[:4] \
        + [StreamFieldPanel('structured_data')] \
        + ArticlePage.content_panels[4:]


SectionPage.subpage_types += ['schemapages.ExtendedArticlePage']
ArticlePage.subpage_types += ['schemapages.ExtendedArticlePage']
