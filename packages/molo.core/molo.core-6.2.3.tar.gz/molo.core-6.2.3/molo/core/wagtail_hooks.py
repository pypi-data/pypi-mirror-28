from django.conf.urls import url

from molo.core.admin import (
    ReactionQuestionsModelAdmin, ReactionQuestionsSummaryModelAdmin,
    AdminViewGroup
)
from molo.core.admin_views import ReactionQuestionResultsAdminView, \
    ReactionQuestionSummaryAdminView
from molo.core.models import Languages
from molo.core.utils import create_new_article_relations


from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailadmin.site_summary import SummaryItem
from wagtail.wagtailadmin.widgets import Button, ButtonWithDropdownFromHook
from wagtail.contrib.modeladmin.options import modeladmin_register
from wagtail.wagtailadmin.wagtail_hooks import page_listing_more_buttons

from molo.core.api import urls as molo_api_urls
from molo.core import views
from molo.core.utils import copy_translation_pages


@hooks.register('register_admin_urls')
def urlconf_translations():
    return [
        url(
            r'^translations/add/(?P<page_id>\d+)/(?P<locale>[\w\-\_]+)/$',
            views.add_translation,
            name='add_translation'),
    ]


@hooks.register('register_admin_urls')
def register_question_results_admin_view_url():
    return [
        url(r'reactionquestion/(?P<parent>\d+)/results/$',
            ReactionQuestionResultsAdminView.as_view(),
            name='reaction-question-results-admin'),
    ]


modeladmin_register(ReactionQuestionsModelAdmin)


@hooks.register('register_admin_urls')
def register_article_question_results_admin_view_url():
    return [
        url(r'reactionquestion/(?P<article>\d+)/results/summary/$',
            ReactionQuestionSummaryAdminView.as_view(),
            name='reaction-question-article-results-admin'),
    ]


modeladmin_register(ReactionQuestionsSummaryModelAdmin)
modeladmin_register(AdminViewGroup)


@hooks.register('construct_explorer_page_queryset')
def show_main_language_only(parent_page, pages, request):
    main_language = Languages.for_site(request.site).languages.filter(
        is_main_language=True).first()
    if main_language and parent_page.depth > 2:
        return pages.filter(languages__language__locale=main_language.locale)
    return pages


@hooks.register('after_copy_page')
def add_new_tag_article_relations(request, page, new_page):
    create_new_article_relations(page, new_page)


@hooks.register('after_copy_page')
def copy_translation_pages_hook(request, page, new_page):
    copy_translation_pages(page, new_page)


# API admin
@hooks.register("register_admin_urls")
def add_import_view():
    return molo_api_urls.urlpatterns


@hooks.register('register_admin_menu_item')
def register_api_menu_item():
    return MenuItem(
        _('API'),
        urlresolvers.reverse('site-import'),
        classnames='icon icon-download',
    )


class LanguageSummaryItem(SummaryItem):
    order = 500
    template = 'wagtail/site_languages_summary.html'

    def get_context(self):
        languages = Languages.for_site(self.request.site).languages.all()
        return {
            'summaries': [{
                'language': l.get_locale_display(),
                'total': Page.objects.filter(
                    languages__language__id=l.id).count()
            }for l in languages],
        }


@hooks.register('construct_homepage_summary_items')
def add_languages_summary_item(request, items):
    items.append(LanguageSummaryItem(request))


class LanguageErrorMessage(SummaryItem):
    order = 100
    template = 'wagtail/language_error_message.html'


@hooks.register('construct_homepage_panels')
def add_language_error_message_panel(request, panels):
    if not Languages.for_site(request.site).languages.all().exists():
        panels[:] = [LanguageErrorMessage(request)]


@hooks.register('construct_main_menu')
def hide_menu_items_if_no_language(request, menu_items):
    if not Languages.for_site(request.site).languages.all().exists():
        menu_items[:] = [
            item for item in menu_items if (
                item.name == 'settings' or
                item.name == 'api')]


@hooks.register('construct_main_menu')
def hide_site_import_if_not_in_importer_group(request, menu_items):
    if not User.objects.filter(
            pk=request.user.pk,
            groups__name='Site Importers').exists():
        menu_items[:] = [
            item for item in menu_items if item.name != 'api']


@hooks.register('construct_main_menu')
def show_explorer_only_to_users_have_access(request, menu_items):
    if (request.user.is_superuser or
        User.objects.filter(pk=request.user.pk, groups__name__in=[
            'Moderator', 'Editor']).exists()):
        return menu_items
    if User.objects.filter(pk=request.user.pk, groups__name__in=[
            'Comment Moderator', 'Expert', 'Wagtail Login Only']).exists():
        menu_items[:] = [
            item for item in menu_items if item.name != 'explorer']


@hooks.register('register_page_listing_buttons')
def page_custom_listing_buttons(page, page_perms, is_parent=False):
    yield ButtonWithDropdownFromHook(
        'More',
        hook_name='my_button_dropdown_hook',
        page=page,
        page_perms=page_perms,
        is_parent=is_parent,
        priority=50
    )


@hooks.register('register_page_listing_more_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    """
    This removes the standard wagtail dropdown menu.

    This supresses the original 'More' dropdown menu because it breaks
    the expected behaviour of the yeild functionality used to add
    additional buttons in wagtail_hooks.
    """
    if page_perms.can_move():
        return None


@hooks.register('my_button_dropdown_hook')
def new_page_listing_buttons(page, page_perms, is_parent=False):
    """
    This inherits the buttons from wagtail's page_listing_more_buttons
    https://github.com/wagtail/wagtail/blob/stable/1.8.x/wagtail/wagtailadmin/wagtail_hooks.py#L94
    (i.e. the buttons that are put in the original drop down menu)
    This is done to avoid breakages should their hooks change in the future


    It iterates through the buttons and prevents the delete button
    from being added if the Page should not be deleteable from the admin UI
    """
    original_buttons = list(page_listing_more_buttons(page,
                                                      page_perms,
                                                      is_parent))
    if not hasattr(page.specific, 'hide_delete_button'):
        for b in original_buttons:
            yield b
    else:
        for b in original_buttons:
            if (hasattr(b, 'attrs') and
                    'delete' not in b.attrs.get('title').lower()):
                    yield b

    if not page_perms.can_unpublish():
        yield Button(
            _('Publish'),
            urlresolvers.reverse('publish', args=(page.id,)),
            attrs={'title': _("Publish page '{title}'").format(
                title=page.get_admin_display_title()
            )},
            priority=40
        )


@hooks.register('my_button_dropdown_hook')
def add_copy_to_all_action_button(page, page_perms, is_parent=False):
    """
    This inherits the buttons from wagtail's page_listing_more_buttons
    https://github.com/wagtail/wagtail/blob/stable/1.8.x/wagtail/wagtailadmin/wagtail_hooks.py#L94
    (i.e. the buttons that are put in the original drop down menu)
    This is done to avoid breakages should their hooks change in the future


    It adds a copy to all action button
    """

    yield Button(
        _('Copy to All Countries'),
        urlresolvers.reverse('copy-to-all-confirm', args=(page.id,)),
        attrs={'copy_to_all_confirm': _("Copy page '{title}'").format(
            title=page.get_admin_display_title()
        )},
        priority=40
    )


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static('css/wagtail-admin.css'))
