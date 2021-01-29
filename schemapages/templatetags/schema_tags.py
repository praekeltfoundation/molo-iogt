import json

from django.utils.safestring import mark_safe
from django import template


register = template.Library()


LD_TAGS = '<script type="application/ld+json">{}</script>' 


@register.simple_tag()
def faq_ld(faq_data):
    #  faq_data['title_for_faq']
    ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [],
    }

    for block in faq_data['question_and_answer']:
        ld['mainEntity'].append({
            "@type": "Question",
            "name": block['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": block['answer'],
            }
        })

    return mark_safe(LD_TAGS.format(json.dumps(ld, indent=4)))


@register.simple_tag()
def howto_ld(how_to_data):
    ld = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "description": how_to_data['description'],
    }

    if how_to_data['title_for_how_to']:
        ld["name"] = how_to_data['title_for_how_to']

    if how_to_data['estimated_cost']:
        ld["estimatedCost"] = {
            "@type": "MonetaryAmount",
            #"currency": "USD",
            "value": how_to_data.get('estimated_cost', ""),
        },

    if how_to_data['materials_required']:
        ld['supply'] = []
        for item in how_to_data['materials_required']:
            ld['supply'].append({
                "@type": "HowToSupply",
                "name": item,
        })
        
    if how_to_data['tools_required']:
        ld['tool'] = []
        for item in how_to_data['tools_required']:
            ld['tool'].append({
                "@type": "HowToTool",
                "name": item,
        })

    if how_to_data['steps']:
        ld['step'] = []
        for item in how_to_data['steps']:
            ld['step'].append({
                "@type": "HowToStep",
                "name": item['step_name'],
                "itemListElement": [
                    {
                        "@type": "HowToTip" \
                            if block.block_type == 'suggestion' \
                            else "HowToDirection",
                        "text": block.value,
                    } for block in item['step_parts']
                ],
            })

    return mark_safe(LD_TAGS.format(json.dumps(ld, indent=4)))

