#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sqlite3
import urllib2
import zipfile

__url__ = 'https://www.ars.usda.gov/SP2UserFiles/Place/12354500/Data/SR26/dnload/sr26.zip'


def get_file_list(dirname):
     return [f for f in os.listdir(dirname)
            if os.path.isfile(os.path.join(dirname, f))
            and f.split('.')[-1] == 'txt']


def retrieve_database(url=__url__):
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
            status = r"%10d  [%3.2f%%]" % (downloaded, downloaded * 100. / fsize)
            status = status + chr(8)*(len(status)+1)
            print status,

    return fname


def unzip(fname, dirname='.tmp'):
    if not os.path.exists(dirname):
        print 'Creating temporary directory "' + dirname + '"'
        os.makedirs(dirname);
    else:
        print 'Directory "' + dirname + '" already exists, using directory'

    print 'Extracting zipfile "' + fname + '" into directory "' + dirname  + '"'
    with zipfile.ZipFile(fname, 'r') as z:
        z.extractall(dirname)


def cleanup_data_files(dirname='.tmp'):
    files = get_file_list(dirname)

    for fname in files:
        print 'Cleaning up ' + fname + '...'
        with open(os.path.join(dirname, fname), 'r') as f:
            data = f.read()
        with open(os.path.join(dirname, fname), 'w') as f:
            f.write(data.replace('~', ''))


def init_database(fname_db='sr26.db', fname_schema='sr26.schema'):
    if not os.path.exists(fname_schema):
        print 'Schema file not found, terminating'
        return

    with open(fname_schema, 'r') as f:
        data = f.read()

    conn = sqlite3.connect(fname_db)
    conn.executescript(data)
    conn.commit()
    conn.close()


f __name__ == '__main__':
    fname = retrieve_database()
    unzip(fname)
    cleanup_data_files()

    if not os.path.exists('sr26.db'):
        init_database()
    else:
        print 'Database already exists'
