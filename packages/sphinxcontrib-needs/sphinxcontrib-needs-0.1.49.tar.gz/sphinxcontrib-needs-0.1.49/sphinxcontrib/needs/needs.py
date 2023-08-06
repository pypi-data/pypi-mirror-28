# -*- coding: utf-8 -*-

import os
import random
import string

from docutils import nodes
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinxcontrib.needs.builder import NeedsBuilder
from sphinxcontrib.needs.environment import install_backend_static_files
from sphinxcontrib.needs.need import Need, NeedDirective, process_need_nodes, purge_needs
from sphinxcontrib.needs.need_incoming import Need_incoming, process_need_incoming
from sphinxcontrib.needs.need_ref import Need_ref, process_need_ref
from sphinxcontrib.needs.needfilter import Needfilter, NeedfilterDirective, process_needfilters
from sphinxcontrib.needs.needimport import Needimport, NeedimportDirective
from sphinxcontrib.needs.need_outgoing import Need_outgoing, process_need_outgoing

DEFAULT_TEMPLATE = """
.. _{{id}}:

{% if hide == false -%}
.. role:: needs_tag
.. role:: needs_status
.. role:: needs_type
.. role:: needs_id
.. role:: needs_title

.. rst-class:: need
.. rst-class:: need_{{type_name}}

:needs_type:`{{type_name}}`: :needs_title:`{{title}}` :needs_id:`{{id}}`
    {%- if status and  status|upper != "NONE" and not hide_status %}
    | status: :needs_status:`{{status}}`
    {%- endif -%}
    {%- if tags and not hide_tags %}
    | tags: :needs_tag:`{{tags|join("` :needs_tag:`")}}`
    {%- endif %}
    | links incoming: :need_incoming:`{{id}}`
    | links outgoing: :need_outgoing:`{{id}}`

    {{content|indent(4) }}

{% endif -%}
"""



# Old node template
# DEFAULT_TEMPLATE = """
# .. _{{id}}:
#
# {% if hide == false -%}
# {{type_name}}: **{{title}}** ({{id}})
#
#     {{content|indent(4) }}
#
#     {% if status and not hide_status -%}
#     **status**: {{status}}
#     {% endif %}
#
#     {% if tags and not hide_tags -%}
#     **tags**: {{"; ".join(tags)}}
#     {% endif %}
#
#     **links incoming**: :need_incoming:`{{id}}`
#
#     **links outgoing**: :need_outgoing:`{{id}}`
#
# {% endif -%}
# """

DEFAULT_DIAGRAM_TEMPLATE = \
    "<size:12>{{type_name}}</size>\\n**{{title|wordwrap(15, wrapstring='**\\\\n**')}}**\\n<size:10>{{id}}</size>"


def setup(app):
    log = logging.getLogger(__name__)
    app.add_builder(NeedsBuilder)
    app.add_config_value('needs_types',
                         [dict(directive="req", title="Requirement", prefix="R_", color="#BFD8D2", style="node"),
                          dict(directive="spec", title="Specification", prefix="S_", color="#FEDCD2", style="node"),
                          dict(directive="impl", title="Implementation", prefix="I_", color="#DF744A", style="node"),
                          dict(directive="test", title="Test Case", prefix="T_", color="#DCB239", style="node"),
                          # Kept for backwards compatibility
                          dict(directive="need", title="Need", prefix="N_", color="#9856a5", style="node")
                          ],
                         'html')
    app.add_config_value('needs_template',
                         DEFAULT_TEMPLATE,
                         'html')

    app.add_config_value('needs_include_needs', True, 'html')
    app.add_config_value('needs_need_name', "Need", 'html')
    app.add_config_value('needs_spec_name', "Specification", 'html')
    app.add_config_value('needs_id_prefix_needs', "", 'html')
    app.add_config_value('needs_id_prefix_specs', "", 'html')
    app.add_config_value('needs_id_length', 5, 'html')
    app.add_config_value('needs_specs_show_needlist', False, 'html')
    app.add_config_value('needs_id_required', False, 'html')
    app.add_config_value('needs_show_link_type', False, 'html')
    app.add_config_value('needs_show_link_title', False, 'html')
    app.add_config_value('needs_file', "needs.json", 'html')

    app.add_config_value('needs_role_need_template', "{title} ({id})", 'html')

    app.add_config_value('needs_diagram_template',
                         DEFAULT_DIAGRAM_TEMPLATE,
                         'html')

    # If given, only the defined status are allowed.
    # Values needed for each status:
    # * name
    # * description
    # Example: [{"name": "open", "description": "open status"}, {...}, {...}]
    app.add_config_value('needs_statuses', False, 'html')

    # If given, only the defined tags are allowed.
    # Values needed for each tag:
    # * name
    # * description
    # Example: [{"name": "new", "description": "new needs"}, {...}, {...}]
    app.add_config_value('needs_tags', False, 'html')

    # Path of css file, which shall be used for need style
    app.add_config_value('needs_css', "modern.css", 'html')

    # Define nodes
    app.add_node(Need)
    app.add_node(Needfilter)
    app.add_node(Needimport)

    ########################################################################
    # DIRECTIVES
    ########################################################################

    # Define directives
    # As values from conf.py are not available during setup phase, we have to import and read them by our own.
    # Otherwise this "app.config.needs_types" would always return the default values only.
    try:
        import imp
        # If sphinx gets started multiple times inside a python process, the following module gets also
        # loaded several times. This has a drawback, as the config from the current build gets somehow merged
        # with the config from the previous builds.
        # So if the current config does not define a parameter, which was set in build before, the "old" value is
        # taken. This is dangerous, because a developer may simply want to use the defaults (like the predefined types)
        # and therefore does not set this specific value. But instead he would get the value from a previous build.
        # So we generate a random module name for our configuration, so that this is loaded for the first time.
        # Drawback: The old modules will still exist (but are not used).
        #
        # From https://docs.python.org/2.7/library/functions.html#reload
        # "When a module is reloaded, its dictionary (containing the module’s global variables) is retained.
        # Redefinitions of names will override the old definitions, so this is generally not a problem.
        # If the new version of a module does not define a name that was defined by the old version,
        # the old definition remains"

        # Be sure, our current working directory is the folder, which stores the conf.py.
        # Inside the conf.py there may be relatives paths, which would be incorrect, if our cwd is wrong.
        old_cwd = os.getcwd()
        os.chdir(app.confdir)
        module_name = "needs_app_conf_" + ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
        config = imp.load_source(module_name, os.path.join(app.confdir, "conf.py"))
        os.chdir(old_cwd)  # Lets switch back the cwd, otherwise other stuff may not run...
        types = getattr(config, "needs_types", app.config.needs_types)
    except FileExistsError:
        types = app.config.needs_types
    except Exception as e:
        log.error("Error during sphinxcontrib-needs setup: {0}".format(
            os.path.join(app.confdir, "conf.py")))
        types = app.config.needs_types

    for type in types:
        # Register requested types of needs
        app.add_directive(type["directive"], NeedDirective)
        app.add_directive("{0}_list".format(type["directive"]), NeedDirective)

    app.add_directive('needfilter', NeedfilterDirective)

    # Kept for backwards compatibility
    app.add_directive('needlist', NeedfilterDirective)

    app.add_directive('needimport', NeedimportDirective)

    ########################################################################
    # ROLES
    ########################################################################
    # Provides :need:`ABC_123` for inline links.
    app.add_role('need', XRefRole(nodeclass=Need_ref,
                                  innernodeclass=nodes.emphasis,
                                  warn_dangling=True))

    app.add_role('need_incoming', XRefRole(nodeclass=Need_incoming,
                                           innernodeclass=nodes.emphasis,
                                           warn_dangling=True))

    app.add_role('need_outgoing', XRefRole(nodeclass=Need_outgoing,
                                           innernodeclass=nodes.emphasis,
                                           warn_dangling=True))

    ########################################################################
    # EVENTS
    ########################################################################
    # Make connections to events
    app.connect('env-purge-doc', purge_needs)
    app.connect('doctree-resolved', process_need_nodes)
    app.connect('doctree-resolved', process_needfilters)
    app.connect('doctree-resolved', process_need_ref)
    app.connect('doctree-resolved', process_need_incoming)
    app.connect('doctree-resolved', process_need_outgoing)
    app.connect('env-updated', install_backend_static_files)

    # Removed with version 0.1.40
    # Allows jinja statements in rst files
    # app.connect("source-read", rstjinja)

    return {'version': '0.1.49'}  # identifies the version of our extension
