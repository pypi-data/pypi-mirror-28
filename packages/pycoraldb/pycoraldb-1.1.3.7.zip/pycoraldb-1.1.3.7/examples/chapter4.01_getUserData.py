#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pycoraldb

if __name__ == '__main__':
    client = pycoraldb.CoralDBClient('coraldb://127.0.0.1:5166')
    client.login("test", "123456")
    rs = client.getUserData("test.test", password="123456")
    print rs
    import pandas as pd
    df = pd.DataFrame(rs)
    print df
