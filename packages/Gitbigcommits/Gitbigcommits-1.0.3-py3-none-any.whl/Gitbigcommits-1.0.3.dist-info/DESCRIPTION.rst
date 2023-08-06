
**Functionality:**

This module is useful for three purpose:

    1) You want to find the big commits happened in your git repo and who has
       committed that at what time.

    2) You want to find the dormant branches in your git repo and who is the
       author of the branch

    3) You want to prevent large commits in your local repo.

*NOTE:* All you need to do is give your repositry location as input to this
module. It does not need your git credentials.
Also, It will find large commits across all branches present in the repo

  ``pip install Gitbigcommits``

Once you install, the following below commands will be available to you in your
 terminal.

 1) bigcommits - prints big commits to stdout
 2) bigcommits-html - creates a html file and writes the report to that.
 3) dbranch-html - find the dormant branch in your repo and writes into a html
 4) bigcommits-prevent - once you execute this, your local repo will prevent
    large commits to be happened in your repo

**Supported Outputs:**

    1) Reports can be generated as HTML file.
    2) Console output

**Usage:**

bigcommits <git_location_in_your_machine> <size_in_kb>

*Eg:*

            .. code-block:: bash

              $bigcommits "usr/home/myrepo/" "1024"

Your git directory is in the "usr/home/myrepo" folder. git directory denotes
where your ".git" folder is present.

Similarly,

  .. code-block:: bash

   $ bigcommits-html "usr/home/myrepo/" "1024"

   $ dbranch-html "usr/home/myrepo/"

   $ bigcommits-prevent "usr/home/myrepo/"


