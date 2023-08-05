################
djangocms-search
################

A Search plugin for django CMS. Could be inserted with a form itself into CMS placeholders.
Uses Aldryn-search (Django-Haystack) for indexing of titles and pages.


Installation
~~~~~~~~~~~~


This plugin requires :code:`django CMS` 3.0 or higher to be properly installed and
configured. 

* In your projects :code:`virtualenv`, run :code:`pip install djangocms-search`.
* Add :code:`djangocms_search'` to your :code:`INSTALLED_APPS` setting.
* If using Django 1.7 add :code:`'djangocms_search': 'djangocms_search.migrations_django',`
  to :code:`MIGRATION_MODULES`  (or define `:code:`MIGRATION_MODULES`` if it does not exists);
  when django CMS 3.1 will be released, migrations for Django 1.7 will be moved
  to the standard location and the south-style ones to :code:`south_migrations`.
* Run ``manage.py migrate djangocms_search``.


Settings
~~~~~~~~

Setting you could define in your main project settings.py is:

 :code:`COMMON_PAGINATOR_PAGINATE_BY = [Paginate your search results by this number of entries]`

Example (default setting):

 :code:`COMMON_PAGINATOR_PAGINATE_BY = 10` 

Requirements
~~~~~~~~~~~~

This plugin depends on forked version of `aldryn-search <https://github.com/garmoncheg/aldryn-search>` it is updated to 0.2.8 and should be installed in order to be comartible with django-cms 3.x
Follow haystack configuration of the Aldryn-search.
Mine looks like (settings.py):

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(PROJECT_PATH, 'whoosh_index'),
        },
    }
    HAYSTACK_ROUTERS = ['aldryn_search.router.LanguageRouter', ]
    ALDRYN_SEARCH_REGISTER_APPHOOK = False

This should help register indexing properly. It is also modified to index pages along with titles. So installing this modified version will be required in order for pluin to work propery.

Children
~~~~~~~~

This plugin does not support child plugins.

Translations
~~~~~~~~~~~~

Not Yet...