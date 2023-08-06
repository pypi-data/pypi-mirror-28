from atelier.invlib.ns import ns
ns.setup_from_tasks(
    globals(), "lino_amici",
    languages="en de fr et".split(),
    tolerate_sphinx_warnings=False,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_amici/lib/amici/locale',
    demo_projects=[
        'lino_amici/projects/herman'],
)
