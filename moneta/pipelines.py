import sqlite3


class MonetaPipeline:

    # Database setup
    conn = sqlite3.connect('moneta.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute("""CREATE TABLE IF NOT EXISTS `moneta`
                         (category text, title text, link text, content text)""")

    def process_item(self, item, spider):
        self.c.execute("""SELECT * FROM moneta WHERE title = ? """,
                       (item.get('title'), ))
        duplicate = self.c.fetchall()
        if len(duplicate):
            return item
        print(f"New entry added at {item['link']}")

        # Insert values
        self.c.execute("INSERT INTO moneta (category, title, link, content)"
                       "VALUES (?,?,?,?)", (item.get('category'), item.get('title'), item.get('link'), item.get('content')))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

