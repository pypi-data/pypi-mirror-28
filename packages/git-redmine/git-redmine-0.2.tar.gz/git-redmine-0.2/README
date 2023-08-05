git-redmine
===========

Redmine integration to git.

Configuration
-------------

Add the following snippet to your .config/git/config file.::

   [redmine]
   url = https://redmine.mycompany.org/
   key = apikey

      OR

   username = username
   password = password

Usage
-----

project
.......

Show the current default project.

project set
...........

Set the current default project for this repository, useful for creating new
issues.::

   git redmine project set myproject-id

issue new
.........

Given a default project, create a new issue, an editor is launched to define
subject and description of the issue.::

  git redmine issue new

issue take
..........

Handle the given issue by creating or switching to a branch named
`wip/<issue-number>-<slugified-issue-subject>` forking from `master`.::

  git redmine issue take 123

issue submit
............

Use `git format-patch` to create the patch serie from `master` and attach it to
the current issue. An editor is launched to add a commment.::

  git redmine issue submit
