import sqlite3

class Post():

    def __init__(self,img_id,title,writer,post_info,link):
        self.img_id = img_id
        self.title = title
        self.writer = writer
        self.post_info = post_info
        self.link = link


    def text_of_mail(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title></title>
        </head>
        <body>

        <a href='""" + self.link + """'><img src='""" + 'https://oyungezer.com.tr/' + self.img_id + """' width="300px" height="155px" alt="Image Poster"><a/>

        <a href='""" + self.link + """' style="text-decoration: none;"><h1 style="color: orange; max-height: 67px!important; font: 20px/22px 'Contentia Bold', Tahoma, sans-serif; margin-top: 5px; width: 300px;">""" + self.title +"""</h1></a>

        <div style="font-size: 12px; margin-top: 5px; width: 300px;">
            <span>
                """ + self.writer + ' tarafından' + """
            </span>
        </div>

        <p style="font: 14px/1.5 'Ubuntu', Arial, sans-serif; text-align: justify; width: 300px; word-wrap:break-word;">""" + self.post_info + """</p> 

        </body>
        </html>
        """


class Database_Post():

    def __init__(self):

        self.connect_database()

    def connect_database(self):

        self.connection = sqlite3.connect("Oyungezer.db")
        self.cursor = self.connection.cursor()

        query = "create table if not exists " \
                "Tbl_Posts (" \
                "ID text," \
                "Title text," \
                "Writer text," \
                "Info text," \
                "Link text)"
        self.cursor.execute(query)
        self.connection.commit()

    def check_if_post_exists(self, img_id = '', link = ''):

        #query = "select * from tbl_posts where link = @p1"
        #self.cursor.execute(query,(link,))

        query_search = ""
        value = ""

        if (len(img_id) != 0):
            query_search = 'ID'
            value = img_id
        elif (len(link) != 0):
            query_search = 'link'
            value = link

        query = "select * from tbl_posts where " + query_search + " = '" + value + "'"
        self.cursor.execute(query)
        posts = self.cursor.fetchall()

        if (len(posts) == 0):
            return 1

        else:
            return 0

    def add_post(self,Post):

        query = "insert into tbl_posts values (@p1,@p2,@p3,@p4,@p5)"
        self.cursor.execute(query,(Post.img_id,Post.title,Post.writer,Post.post_info,Post.link))
        self.connection.commit()
