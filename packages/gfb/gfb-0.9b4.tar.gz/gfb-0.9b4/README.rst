gfb - Find Branches in Github
=============================

``gfb`` is a command line utility that  allows the user to search for
branches in a remote github repository. Branches are specified as a 
standard Python regular expression pattern. If the search is started
from within a directory that's part of a local ``git`` repository, the
user is presented with the option to check out the matching branch. 

Installation
------------

::

    pip install gfb

Depending on your local python environment, you may need to specify the 
python3 version of pip: 

::

    pip3 install gfb


Basic Usage
-----------

::

    gfb [-h] [--repo REPO] [--config CONFIG_FILE] [--setup] regex                 

    positional arguments:                     
      regex                 branch regular expression                                    

      optional arguments:  
        -h, --help            show this help message and exit                              
       --repo REPO           name of github repository to search                          
       --config CONFIG_FILE  gfb configuration file                                       
       --setup               create a new default configuration file

For example::

    gfb feature/

Will find all the braches that  contain the text ``feature/`` in their name.

If the ``gfb`` command is executed from within a directory in a local repository
(and a specific repository is omitted), the user will be given the option to fetch
and checkout the desired branch, for example::

   1. feature/a
   2. feature/b
   3. feature/c
   4. feature/d
   5. feature/e
         
   Enter the branch number to checkout or 'X' to exit: 

Selecting ``2`` will fetch and checkout the branch named 
``feature/b``. Any uncommitted changes that exist will be stashed
and named something like ``gfb-<timestamp>`` where  ``<timestamp>``
is the current date and time in iso8601 format.

You can specify any remote repository for which you have access to view
by providing the ``--repo`` option and providing the repostory name
in addition to the branch pattern::

    gfb --repo apple/swift '^stdlib-'

Returns all the branches in Apple's swift repository that start with the
text ``stdlib-``. 

``gfb`` requires that you have proper Github credentials. These credential
are read from a configuration file. The default file is named ``.gfbrc`` and
is located in the user's home directory. by specifying the ``--setup`` flag, 
``gfb`` will guide the user through creating a new configuration. You can 
provide either an Github api key, or a valid Github username and password. The
preferred method is to use an api key. You can create an api key or
personal access token from the *Developer Settings*  in  your Github account.
The configuratioon fill wll be created with owner read/write access and will
warn you and refuse to run if group or world read access is enabled.

The source for this project is available here
https://github.com/barnardn/gfb.git.

Troubleshooting
---------------

If you've installed ``gfb`` on macOS sierra or greater and are running Python 3.6,
you'll need to install the SSL certificates for the SSL libraries that are
baked into python. To do so:: 

    cd /Applications/Python\ 3.6/
    ./Install\ Certificates.command

Change into the Python 3.6 directory in Applications and run the 
``Install Certficiates.command`` script.
