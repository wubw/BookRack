import unittest
import localbook_search


class TestStringMethods(unittest.TestCase):

    def test_process_string(self):
        s = "红楼梦 [脂砚斋重批]"
        self.assertEqual(localbook_search.process_string(s), '红楼梦')

        s = "納蘭詞箋注"
        self.assertEqual(localbook_search.process_string2(s), '纳兰词笺注')

    def test_search_book_fromdb(self):
        douban_books = [{"_id": {"$oid": "5ec116c6647ff9b6f3dd609b"}, "title": "历史深处的忧虑", "info": "更新图书信息或封面||作者:||林达||出版社:||生活·读书·新知三联书店||副标题:||近距离看美国之一||出版年:||1997-5||页数:||320||定价:||19.00元||装帧:||平装||丛书:||林达作品系列||ISBN:||9787108010186", "img": "https://img9.doubanio.com/view/subject/s/public/s1768916.jpg",
                         "rating": "9.0", "ratingpeople": "35889", "reading_status": "have_read", "my_rating": "5", "timestamp": "2012-10-02", "tags": "标签: 文学 历史", "file_create_time": 1589116688.7198398, "author": "林达", "publisher": "生活·读书·新知三联书店", "sub-title": "近距离看美国之一", "publish-time": "1997-5", "pages": "320"}]
        self.assertIsNotNone("近距离看美国2", douban_books)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
