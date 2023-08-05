#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import shutil
import zipfile

def lookup(keyword):
    tmp_file = "/tmp/ichigojam-%s.txt" % (keyword)
    ichihgo_docs = os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs/ichigojam.zip")
    with zipfile.ZipFile(ichihgo_docs) as z:
        try:
            with z.open("%s.txt" % (keyword)) as zf, open(tmp_file, 'wb') as f:
                shutil.copyfileobj(zf, f)
            os.system("less %s" % (tmp_file))
        except KeyError:
            print("'%s': No such command" % (keyword))
