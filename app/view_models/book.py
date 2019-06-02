# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 4:58 AM
# @Author  : Hopen

# 单个的情况，集合交给 Collection


class BookViewModel:
    def __init__(self, book):
        """
        创建这个视图函数是为了处理显示的逻辑，接受一个 YushuBook 类进行构建
        :param book: YushuBook 类
        """
        self.title = book['title']
        self.author = '、'.join(book['author'])
        self.binding = book['binding']
        self.publisher = book['publisher']
        self.image = book['image']
        self.price = '￥' + book['price'] if book['price'] else book['price']
        self.pubdate = book['pubdate']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.pages = book['pages']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.keyword = keyword


class BookViewModelOld:
    @classmethod
    def from_api(cls, keyword, data):
        '''
            为什么不在spider里做成viewmodel？
            从豆瓣获取的数据可能是单本，也可能是多本集合
            data 有三种情况：
            1. 单本
            2. 空对象
            3. 有对象
        '''
        # if not data:

        yushu_books = data.get('books', 'null')
        if yushu_books == 'null':
            total = 1
            temp_books = [data]
        else:
            if len(yushu_books) > 0:
                total = data['total']
                temp_books = yushu_books
            else:
                total = 0
                temp_books = []

        books = []
        for book in temp_books:
            book = cls.get_detail(book, 'from_api')
            books.append(book)
        # douban_books = result['books'] if result.get('books') else [result]
        view_model = {
            'total': total,
            'keyword': keyword,
            'books': books
        }
        return view_model

    @classmethod
    def single_book_from_mysql(cls, keyword, data):
        count = 1
        if not data:
            count = 0
        returned = {
            'total': count,
            'keyword': keyword,
            'books': [cls.get_detail(data)]
        }
        return returned

    @classmethod
    def get_detail(cls, data, from_where='from_mysql'):
        if from_where == 'from_api':
            book = {
                'title': data['title'],
                'author': '、'.join(data['author']),
                'binding': data['binding'],
                'publisher': data['publisher'],
                'image': data['images']['large'],
                'price': data['price'],
                'isbn': data['isbn'],
                'pubdate': data['pubdate'],
                'summary': data['summary'],
                'pages': data['pages']
            }
        else:
            book = {
                'title': data['title'],
                'author': '、'.join(data['author']),
                'binding': data['binding'],
                'publisher': data['publisher'],
                'image': data.image,
                'price': data['price'],
                'isbn': data.isbn,
                'pubdate': data['pubdate'],
                'summary': data['summary'],
                'pages': data['pages']
            }
        return book

        # @classmethod
        # def get_isbn(cls, book):
        #     isbn13 = book.get('isbn13', None)
        #     isbn10 = book.get('isbn10', None)
        #     return isbn13 if isbn13 else (isbn10 if isbn10 else '')
