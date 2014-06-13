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

### Usage
Usage is very straight forward.  Either clone the repo to the location
desired, or manually download the files.  Run as usual.

    $ git clone https://github.com/jessebraham/usda-sr26-sqlite.git
    $ # Or...
    $ wget https://raw.github.com/jessebraham/usda-sr26-sqlite/master/usda-sr26-sqlite.py
    $ wget https://raw.github.com/jessebraham/usda-sr26-sqlite/master/sr26.schema
    $ # Run the utility...
    $ python usda-sr26-sqlite.py

### License
"THE BEER-WARE LICENSE" (Revision 42):  
[Jesse Braham](https://github.com/jessebraham) wrote these files. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return - Jesse Braham

### Database table descriptions

The created database contains 12 tables. Here is a description of the more interesting ones.
Detailed descriptions are also available in the official [source data documentation (PDF)](https://www.ars.usda.gov/SP2UserFiles/Place/12354500/Data/SR26/sr26_doc.pdf).

**FOOD_DES**

Food description.

**NUT_DATA**

Nutrient data. Contains 632894 records with actual nutritient measurement data.

**WEIGHT**

Gram weights. Contains translation of various measures like "cup", "stick", "tbsp" into gram.

**FOOTNOTE**

Footnote.

**FD_GROUP**

Food group description, contains 25 categories like "Dairy and Egg Products", "Breakfast Cereals".

**LANGUAL**

LanguaL Factor.

**LANGDESC**

LanguaL factor description.

**NUTR_DEF**

Nutrient definition. Contains 150 nutritient records including name, unit of measure etc.

**SRC_CD**

Source code. Contains 10 unique codes for data sources like "Calculated or imputed".

**DERIV_CD**

Data derivation description.

**DATA_SRC**

Sources of data.

**DATASRCLN**

Sources of data - link table.

### Sample query

```sql
SELECT * FROM FOOD_DES fd
LEFT JOIN FD_GROUP fg ON (fg.FdGrp_Cd=fd.FdGrp_Cd)
LEFT JOIN NUT_DATA nd ON (fd.NDB_No=nd.NDB_No)
WHERE nd.Nutr_No IN (203, 204, 205, 255, 291)
ORDER BY NDB_No ASC
```
