from __future__ import print_function
from newsapi import NewsApiClient
import MySQLdb
from dateutil import parser
import json

api = NewsApiClient(api_key='e6702efb133e48418f78ea26f4620e20')

HOST = "localhost"
USER = "root"
PASSWD = "za786001"
DATABASE = "usenews"


def store_data(articles, source, author, title, description, url, timestamp, content):
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = MySQLdb.escape_string("INSERT INTO usa_news (articles, source, author, title, description, url, timestamp, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(insert_query, (articles, source, author, title, description, url, timestamp, content,))
    db.commit()
    cursor.close()
    db.close()
    return

def get_data():
    data = api.get_everything(q='dominican republic AND dead')
    return data

    
def on_data(data):
     #This is the meat of the script...it connects to your mongoDB and stores the tweet
     try:
     # Decode the JSON from Twitter
         d1 = json.dumps(data)
         datajson = json.loads(d1)
         articles = datajson['articles'][0]['source']['id']
         source = datajson['articles'][0]['source']['name']
         author = datajson['articles'][0]['author']
         title = datajson['articles'][0]['title']
         description = datajson['articles'][0]['description']
         url = datajson['articles'][0]['url']
         timestamp = parser.parse(datajson['articles'][0]['publishedAt'])
         content = datajson['articles'][0]['content']
         store_data(articles, source, author, title, description, url, timestamp, content)
         print('done')
     except Exception as e:
             print(e)


def main():
    on_data(get_data())

main()
