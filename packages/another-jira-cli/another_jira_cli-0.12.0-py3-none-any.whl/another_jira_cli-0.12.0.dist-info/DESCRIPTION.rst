README
======

Tool for quick JIRA logging.

See README.md for details.

CHANGELOG
=========

0.12.0
------

Date: 2018-02-01

- [FEATURE] made 'today' an alias for 'm0' in date strings
- [CHANGE] renamed command "log-time" to "log-work"
- [CHANGE] greatly simplified (and changed) cli semantics for log-work
- [CHANGE] greatly simplified (and changed) cli semantics for fill-day
- [BUGFIX] cleanup-day working again
- [BUGFIX] fill-day working again


0.11.2
------

- [BUGFIX] search: fix bug when switching back to .format() strings


0.11.1
------

- [BUGFIX] bulk-create: fix creation of tickets with labels from yaml & json


0.11.0
------

Date: 2017-10-30

- [BUGFIX] most commands: fix a bug in error handling code
- [BUGFIX] lookup: fixed errors in prime use cases, updated docs


0.10.0
------

Date: 2017-10-23

- [FEATURE] bulk-create: add --set parameter for manual field overrides
- [FEATURE] bulk-create: add -p/--print parameter


0.9.2
-----

Date: 2017-10-23

- [CHANGE] go back to python 3.5 compatibility by removing f"" strings


0.9.1
-----

Date: 2017-10-20

- [CHANGE] bulk-create command: nicer output for --dry-run


0.9.0
-----

Date: 2017-10-20

- [FEATURE] bulk-create command: Add --filter
- [FEATURE] bulk-create command: Add --dry-run
- [FEATURE] bulk-create command: Add --start-at
- [FEATURE] bulk-create command: Add handling of epic_name and epic_link fields
- [BUGFIX] bulk-create command: Fixed index calculation for log files
- [CHANGE] bulk-create command: Switched to YAML output format for logs
- [DOCS] bulk-create-command: updated --help docs with unsupported info
- NOTE: Still an experimental release.


0.8.0
-----

Date: 2017-10-19

- [FEATURE] Add 'bulk-create' command from CSV, YAML and JSON files
- [INTERNAL] Restructured internal file layout
- NOTE: This is an experimental release, it might be that things broke since there is no test coverage.


0.7.0
-----

Date: 2017-06-01

- [FEATURE] Combine search queries in the lookup command
- [BUGFIX] Remove typo which introduced a syntax error
- [DOCS] Updated README.md in the repo


0.6.0
-----

Date: 2017-06-01

- [FEATURE] Add command clear-searches
- [FEATURE] Fix command cleanup-day
- [DOCS] Many documentation updates


0.5.0
-----

Date: 2017-05-31

- [FEATURE] Add command fill-day
- [FEATURE] Add command list-worklogs
- [FEATURE] Add command list-work
- [FEATURE] Add 'jira' alias in parallel to 'jira-cli'


0.4.0
-----

Date: 2017-05-31

- [FEATURE] Add searches and saved searches


0.3.0 - 0.3.2
-------------

Date: 2017-05-31

- 0.3.2 - another name change, this time to "another-jira-cli"
- 0.3.1 - Update this file with correct version nr :)
- 0.3.0 - Update project metadata
- 0.3.0 - Change project name to "jiracli" (jira-cli did exist on pypi before)


0.2.0
-----

Date: 2017-05-31

- Add ticket aliases


0.1.0
-----

Date: 2017-04-07

- Initial release


