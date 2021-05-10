import pymysql.cursors
from datetime import datetime, date, timedelta

"""
データベースの変数
"""   
user = ''          # DBのユーザ(適宜変更)
passwd = ''        # DBのパスワード(適宜変更)
host = 'localhost' # DBが稼働するホスト名(適宜変更)
db = 'wordpress'   # WordPressが利用しているデータベース名(適宜変更)

"""
投稿した記事のタイトルとIDを取得する関数
"""
def get_data_from_db(_user, _passwd, _host, _db):

  blog_data = {} # key:id, value:title

  conn = pymysql.connect(
        user = _user,
        passwd = _passwd,
        host = _host,
        db = _db
  )

  c = conn.cursor()
  c.execute("select * from wp_posts")
  for data in c.fetchall():
    id = data[0]
    title = data[5]
    blog_data[id] = title

  conn.close()

  return blog_data


"""
投稿した記事のpvに関するデータを取得する関数
"""
def get_pv_data_from_db(_user, _passwd, _host, _db):

  pv_data = {} # key:date, value: {post_id, count}

  conn = pymysql.connect(
        user = _user,
        passwd = _passwd,
        host = _host,
        db = _db
  )

  c = conn.cursor()
  c.execute("select * from wp_cocoon_accesses")
  for data in c.fetchall():
    post_id = data[1]
    date = data[3]
    count = data[4]
    
    tmp_dict = {}
    if date in pv_data.keys():
      tmp_dict = pv_data[date]

    tmp_dict[post_id] = count
    pv_data[date] = tmp_dict
    
  conn.close()

  return pv_data

"""
メイン文開始
"""
today = datetime.today()
yesterday = today - timedelta(days=1)
yesterday_str = datetime.strftime(yesterday, '%Y-%m-%d')
print("分析する日付:" + yesterday_str)

"""
情報取得
"""
blog_data = get_data_from_db(user, passwd, host, db)
pv_data = get_pv_data_from_db(user, passwd, host, db)

"""
PV数を表示
"""
show_num = 5
index = 0
if yesterday_str in pv_data.keys():
  for tmp_list in sorted(pv_data[yesterday_str].items(), key=lambda x:x[1], reverse=True):
    blog_id = tmp_list[0]
    count = tmp_list[1]
    print("-------------")
    print("タイトル：" + blog_data[blog_id] + " pv数:" + str(count) )
    index += 1
    if index == show_num:
      break
