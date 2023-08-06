Changelog
=========

1.1.3 (2018-01-31)
------------------

Fixes:

- Fix packaging
  [sunew]


1.1.2 (27-11-2017)
------------------

- Added MANIFEST to include CHANGES.rst

1.1 (22-11-2017)
----------------

Features:

- add option to specify an external uri in portlet.
  External link will override reference.
  [tmog]

- add option to set timeout in portlet.
  [tmog]

- add new widgets from plone.app.widgets
  [datakurre]

Fixes:

- only do rotation if we have more
  than one item
  [tmog]

- allow picking old style Topics
  [tmog]

- add BBB for ATTopic
  [tmog]

- add Finnish localization
  [datakurre]


1.0 (30-12-2013)
----------------

Initial public release

Fixes:

- included the plone.behavior meta.zcml file,
  so that we get access to the <plone:behavior /> ZCML directive.
  [bogdangi]
- work with plone:master p.a.portlets
  [tmog]
