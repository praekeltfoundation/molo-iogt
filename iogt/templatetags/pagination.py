from django import template

register = template.Library()


def uniqify(*collections):
    sets = [set(c) for c in collections]
    remaining = set(v for s in sets for v in s)
    results = []

    for s in sets:
        results.append(list(s & remaining))
        remaining = remaining - s

    return results


@register.simple_tag()
def get_pages(page, padding=2, edge_padding=2):
    pages = list(page.paginator.page_range)
    curr = page.number - 1

    _, before_current, after_current, start, end = uniqify(
        [page.number],
        pages[curr - padding:curr],
        pages[page.number:page.number + padding],
        pages[:edge_padding],
        pages[-edge_padding:])

    ellipses_before = curr > edge_padding + padding
    ellipses_after = page.number < len(pages) - (edge_padding + padding)

    return {
        'start': start,
        'end': end,
        'before_current': before_current,
        'after_current': after_current,
        'ellipses_before': ellipses_before,
        'ellipses_after': ellipses_after
    }
