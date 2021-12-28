from sqlalchemy import *
from app.db import engine


conn = engine.connect()

# res = conn.execute(text("select * from user"))
res = conn.execute(text("select * from user where token='wdUZxFXT'"))
    # ダブルクォーテーションの文字列の中に文字列を入れたいときはシングルクォーテーションでくくる。
    # `token`='wdUZxFXT'のように。（wdUZxFXTは文字列として扱いたい。）

rows = res.fetchall()

print(rows[0])
# (1, 'ほのか', 'RKMxBGuK', 42)
    # schema.sqlで示しているようなラブライブのテーブルを既に作成していれば。
print(rows[0][1])
# ほのか
    # schema.sqlで示しているようなラブライブのテーブルを既に作成していれば。
print(rows[0]["name"])
# ほのか
    # schema.sqlで示しているようなラブライブのテーブルを既に作成していれば。


# 実習（スライドp53）のメモ

# (gameserver) @magonotegaeru ➜ /workspaces/gameserver (main ✗) $ ipython
# Python 3.10.0 (default, Oct 13 2021, 08:45:17) [GCC 10.2.1 20210110]
# Type 'copyright', 'credits' or 'license' for more information
# IPython 7.30.1 -- An enhanced Interactive Python. Type '?' for help.

# In [1]: from sqlalchemy import *

# In [2]: from app.db import engine

# In [3]: conn = engine.connect()
# 2021-12-27 07:05:25,204 INFO sqlalchemy.engine.Engine SHOW VARIABLES LIKE 'sql_mode'
# 2021-12-27 07:05:25,204 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2021-12-27 07:05:25,257 INFO sqlalchemy.engine.Engine SHOW VARIABLES LIKE 'lower_case_table_names'
# 2021-12-27 07:05:25,257 INFO sqlalchemy.engine.Engine [generated in 0.00021s] ()
# 2021-12-27 07:05:25,260 INFO sqlalchemy.engine.Engine SELECT DATABASE()
# 2021-12-27 07:05:25,260 INFO sqlalchemy.engine.Engine [raw sql] ()

# In [5]: res = conn.execute(text("select * from user"))
# 2021-12-27 07:06:44,014 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2021-12-27 07:06:44,014 INFO sqlalchemy.engine.Engine select * from user
# 2021-12-27 07:06:44,014 INFO sqlalchemy.engine.Engine [generated in 0.00075s] ()

# In [6]: rows = res.fetchall()

# In [7]: rows[0].id
# Out[7]: 1

# In [8]: rows[0]["name"]
# Out[8]: 'ほのか'

# In [9]: 
