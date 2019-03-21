from wagtail.wagtailcore import hooks


@hooks.register('construct_main_menu')
def show_reactionquestions(request, menu_items):
        menu_items[:] = [
            item for item in menu_items if item.name != 'reactionquestions']
