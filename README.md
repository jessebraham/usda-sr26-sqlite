usda-sr26-sqlite
================

This is a simple utility I wrote as part of a few other projects I'm working
on.  I wanted access to the SR26 database as provided by the USDA, but
was disappointed to find the only available formats were ASCII, and
Microsoft Access.  Neither of these worked for me, so I wrote this to
download the ASCII version, unzip it, and parse the data into a sqlite3
database.  

### To Do:
- Implement code to populate tables with data from appropriate files
- Documentation
