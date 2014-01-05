#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import urllib2
import zipfile


__url__ = 'https://www.ars.usda.gov/SP2UserFiles/Place/12354500/Data/SR26/dnload/sr26.zip'

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


def unzip(fname):
    with zipfile.ZipFile(fname, 'r') as z:
        z.extractall('./')

if __name__ == '__main__':
    fname = retrieve_database()
    #unzip(fname)
