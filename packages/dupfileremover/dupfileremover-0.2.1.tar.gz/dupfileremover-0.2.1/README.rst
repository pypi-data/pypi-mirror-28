dupfileremover
==============

dupfileremover is a python command line utility that takes in files from folders,
or individual file names, and hashes the files found to see if there are any matches.
This can be useful to see if you have any duplicates files that you may want to clean up.

Basic Usage
===========

dupfileremover [OPTIONS] [FOLDERS]...

Options:
  -n, --number INTEGER  The maximum number of each file that should be found
                        (default is 1)
  --help                Show this message and exit.


Examples
========

``dupfileremover myPicsFolder/``

This command will hash every file within the ``myPicsFolder/`` and all sub folders
then look for duplicates. The default is set to 1. As in there should be only 1 unique
file in the directory.

``dupfileremover -n 2 desktopWallpapers/videoGames/ desktopWallpapers/cars/``

This command looks in two different directories (videoGames and cars) that are both
within a directory called ``desktopWallpapers``. Each files in both directories will be
hashed then compared to see if any matching files are found either in the same directory
or in the opposite directory. This command however uses the ``-n`` flag followed by the
number 2. This means that you know for a fact, or a fine if there is at least
one duplicate file found. If there are more than 2 duplicates found then it will be displayed
in the results.

``dupfileremover cat.jpeg picsOfCats/``

This command will hash the individual ``cat.jpeg`` file and all the files within the
``picsOfCats/`` directory and compare all files for matches. This means you will be quickly
able to see if ``cat.jpeg`` already exists within ``picsOfCats/`` with the same, or different, name.

Prerequisites
=============

dupfileremover requires ``Click``. ``Click`` is what manages all arguments and options that are
passed to the program. It can be installed with ``pip install Click``.

License
=======

This project is licensed under the MIT License - See the LICENSE.md file for more details
