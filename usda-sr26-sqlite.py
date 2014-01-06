#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import shutil
import sqlite3
import urllib2
import zipfile

__url__ = 'https://www.ars.usda.gov/SP2UserFiles/Place/12354500/Data/' \
          'SR26/dnload/sr26.zip'


def get_file_list(dirname):
    """
    Iterate through all files in the directory (provided as an argument),
    and append the filename to a list if the extension is of type *.txt.
    Return said list.

    Parameters
    ----------
    dirname : str
            A string representing the path of the directory you wish
            to retrieve files from.

    Returns
    -------
    list
            A list of all files of type *.txt in the specified directory.
    """
    return [f for f in os.listdir(dirname)
            if os.path.isfile(os.path.join(dirname, f))
            and f.split('.')[-1] == 'txt']


def retrieve_database(url=__url__):
    """
    Initially determine the filename in which we're downloading uses the
    provided URL, and check to see if that file already exists in the
    current directory.  If the file exists, do not bother re-downloading it.
    If the file does not exist, download it.  A pleansant little download
    status bar has been provided for your entertainment.  Return the name
    of the file, regardless of whether it was downloaded or it already
    existed.

    Parameters
    ----------
    url : str, optional
            The url in which to download the database from.  Defaults to the
            USDA SR26 download link stored in __url__.

    Returns
    -------
    str
            The name of the file which has been downloaded.
    """
    fname = url.split('/')[-1]
    if os.path.isfile(fname):
        print 'Zipfile already exists, terminating download'
        return fname

    print 'Reading from: ' + url
    u = urllib2.urlopen(url)

    meta = u.info()
    fsize = int(meta.getheaders('Content-Length')[0])
    print 'Downloading: %s Bytes: %s' % (fname, fsize)

    downloaded = 0
    blocksize = 8192

    with open(fname, 'wb') as f:
        while True:
            buffer = u.read(blocksize)
            if not buffer:
                break

            downloaded += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (downloaded,
                                           downloaded * 100.0 / fsize)
            status = status + chr(8) * (len(status) + 1)
            print status,

    return fname


def unzip(fname, dirname='.tmp'):
    """
    Check if the directory already exists.  If it does not, create it.  If it
    does, we'll use it!  Unzip the downloaded archive into the specified
    directory.

    Parameters
    ----------
    fname : str
            The name of the zip archive in which to unzip.
    dirname : str, optional
            The temporary directory in which to store the unzipped files.
            Defaults to '.tmp'.
    """
    if not os.path.exists(dirname):
        print 'Creating temporary directory "' + dirname + '"'
        os.makedirs(dirname)
    else:
        print 'Directory "' + dirname + '" already exists, using directory'

    print 'Extracting zipfile "' + fname + '" into directory "' + dirname + '"'
    with zipfile.ZipFile(fname, 'r') as z:
        z.extractall(dirname)


def cleanup_data_files(dirname='.tmp'):
    """
    For each file that was unzipped from the downloaded archive, open said
    file and remove all tildas ( '~' ) surrounding data, and write the
    changes back.

    Parameters
    ----------
    dirname : str, optional
            The temporary directory in which temp data is stored.
            Defaults to '.tmp'.
    """
    files = get_file_list(dirname)

    for fname in files:
        print 'Cleaning up ' + fname + '...'
        with open(os.path.join(dirname, fname), 'r') as f:
            data = f.read()
        with open(os.path.join(dirname, fname), 'w') as f:
            f.write(data.replace('~', ''))


def init_database(fname_db='sr26.db', fname_schema='sr26.schema'):
    """
    Begin by ensuring the schema file does indeed exist.  If it does not,
    we can't initiate the database, so return False to indicate such.  If it
    exists, open and read the schema file.  Create a connection to the
    database, and execute the script.  Commit changes, and close the
    connection.

    Parameters
    ----------
    fname_db : str, optional
            The name of the database file in which to create.
            Defaults to 'sr26.db'.
    fname_schema : str, optional
            The name of the schema file in which to read from.
            Defaults to 'sr26.schema'.

    Returns
    -------
    bool
            Return whether or not the database was successfully initiated.
    """
    if not os.path.exists(fname_schema):
        print 'Schema file not found, terminating'
        return False

    with open(fname_schema, 'r') as f:
        data = f.read()

    conn = sqlite3.connect(fname_db)
    conn.executescript(data)
    conn.commit()
    conn.close()

    return True


def populate_db(fname_db='sr26.db', dirname='.tmp'):
    """
    Create a connection to the database.  For each file in the tempoarary
    directory, read each row and insert the parsed data into the appropriate
    table.  Commit all changes, and close the connection.

    Parameters
    ----------
    fname_db : str, optional
            The name of the database file in which to populate.
            Defaults to 'sr26.db'.
    dirname : str, optional
            The name of the directory in which the temporary data is stored.
            Defaults to '.tmp'.
    """
    print 'Preparing to populate database...'
    conn = sqlite3.connect(fname_db)
    conn.text_factory = str
    cur = conn.cursor()

    files = get_file_list(dirname)
    for fname in files:
        table_name = fname.split('.')[-2]

        with open(os.path.join(dirname, fname), 'r') as f:
            tmp = f.readline()

        query = 'INSERT INTO ' \
                + table_name \
                + ' VALUES (' \
                + str('?,' * len(tmp.split('^'))).rstrip(',') \
                + ')'

        with open(os.path.join(dirname, fname), 'r') as f:
            print 'Populating table ' + table_name + '...'
            for line in f:
                cur.execute(query, line.split('^'))

    conn.commit()
    conn.close()


def cleanup(fname=__url__.split('/')[-1], dirname='.tmp'):
    """
    Remove the downloaded archive and the temporary directory along with its
    contents.

    Parameters
    ----------
    fname : str, optional
            The name of the downloaded archive file.
            Defaults to the name as determined by the __url__ variable.
    dirname : str, optional
            The name of the directory containing the temporary data.
            Defaults to '.tmp'.

    """
    print "Cleaning up..."
    os.remove(fname)
    shutil.rmtree(dirname)


if __name__ == '__main__':
    fname = retrieve_database()
    unzip(fname)
    cleanup_data_files()

    ret = False
    if not os.path.exists('sr26.db'):
        ret = init_database()
    else:
        print 'Database already exists'

    if ret is True:
        populate_db()

    cleanup()
    print 'Done!'
