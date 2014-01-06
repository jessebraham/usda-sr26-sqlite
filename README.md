usda-sr26-sqlite
================

This is a simple utility I wrote as part of a few other projects I'm working
on.  I wanted access to the SR26 database as provided by the USDA, but
was disappointed to find the only available formats were ASCII, and
Microsoft Access.  Neither of these worked for me, so I wrote this to
download the ASCII version, unzip it, and parse the data into a sqlite3
database.  

I don't do any cleaning up of data or any fancy business here.  I'm simply
parsing the text files and inserting each row into the database.  It's not
exactly the prettiest.  If you need it cleaned up, you're responsible.  

This script uses the following modules, all of which should be included
within a standard Python installation:
- os
- shutil
- sqlite3
- urllib2
- zipfile

### License
THE BEER-WARE LICENSE" (Revision 42):  
[Jesse Braham](https://github.com/jessebraham) wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return - Jesse Braham
