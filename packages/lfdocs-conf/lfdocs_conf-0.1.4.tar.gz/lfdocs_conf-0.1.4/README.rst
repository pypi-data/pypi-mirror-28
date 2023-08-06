LF Docs Config
==============

The purpose of this project is to allow LF projects a centralized location for
storing common project configuration.

To use this a project should create a conf.yaml file in the same
directory as their conf.py. Conf.py should contain at minimum::

    from docs_conf import *

The conf.yaml file should contain at minimum::

    ---
    project_cfg=myproject

If defaults for 'myproject' exist, they will be loaded from this
package, otherwise the basic Sphinx defaults will be set.

Configuration precedence for configuration is as follows:

#. project/conf.py
#. project/conf.yaml
#. docs_conf/defaults/{project_cfg}.yaml
#. docs_conf/defaults/default.yaml
#. docs_conf/__init__.py

conf.py structure and documentation:
  http://www.sphinx-doc.org/en/stable/config.html

TODO
----

- [ ] Define the minimum set of config values to release initial version.
      These can probably come from ODL/OPNFV site conf.py files.

- [ ] Use sane defaults, and don't error out if something is not set.
      Each config needs to be imported gracefully (if it doesn't
      exist, set None or something; similar to dict.get

- [ ] Create own documentation for project detailing use of 'conf.cfg'
      file as some values will require subkeys given that they're
      dictionaries or expect a list of tuples.

- [ ] Setup and document section. The documentation already is organized
      by section, so the config should also contain these section and look
      for their values under them.

      Sections:

        - general (aka sphinx)
        - project
        - i18n
        - html_output
        - apple_help
        - epub_output
        - latex_output
        - text_output
        - manpage_output
        - texinfo_output
        - linkcheck
        - xml
        - cplusplus

- [ ] Configure pre-plugin sections, and reference by plugin listing.
