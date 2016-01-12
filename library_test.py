import unittest
from library import *

class TestLibrary(unittest.TestCase):

    def test_Calendar(self):
        date = Calendar()
        self.assertEqual(date.date, 0)
        self.assertEqual(date.advance(), 1)
        self.assertEqual(date.advance(), 2)
        self.assertEqual(date.get_date(), 2)

    def test_book(self):
        book = Book(11, 'A Bend in the River', "V. S. Naipaul")
        self.assertEqual(book.get_id(), 11)
        self.assertEqual(book.get_title(), 'A Bend in the River')
        self.assertEqual(book.get_author(), "V. S. Naipaul")
        self.assertEqual(book.get_due_date(), None)
        book.check_out(15)
        self.assertEqual(book.get_due_date(), 15)
        book.check_in()
        self.assertEqual(book.get_due_date(), None)
        self.assertEqual(str(book), '11: A Bend in the River, by V. S. Naipaul')

    def test_patron(self):
        vanpelt = Library()
        book = vanpelt.book_list[1]
        Lily = Patron('Lily Wen', vanpelt)
        self.assertEqual(Lily.get_name(), 'Lily Wen')
        self.assertEqual(Lily.get_books(), [])
        Lily.check_out(book)
        self.assertEqual(Lily.get_books(), [book])
        Lily.give_back(book)
        self.assertEqual(Lily.get_books(), [])
        self.assertEqual(Lily.get_overdue_books(), [])
        
        book2 = vanpelt.book_list[2]
        book2.check_out(15)
        vanpelt.calendar.date = 18
        Lily.check_out(book2)
        self.assertEqual(Lily.get_books(), [book2])
        self.assertEqual(Lily.get_overdue_books(), [book2])
        
        book.check_out(20)
        Lily.check_out(book)
        self.assertEqual(Lily.get_books(), [book2, book])
        self.assertEqual(Lily.get_overdue_books(), [book2])

    def test_library(self):
        vanpelt = Library()
        self.assertEqual(vanpelt.calendar.date, 0)
        self.assertEqual(vanpelt.patron_info, {})
        self.assertEqual(vanpelt.flag, 'N')
        self.assertEqual(vanpelt.current_patron, None)
        self.assertEqual(str(vanpelt.book_list[0]), str(Book(1, "20,000 Leagues Under the Seas", "Jules Verne")))
        self.assertEqual(str(vanpelt.book_list[2]), str(Book(3, "20,000 Leagues Under the Seas", "Jules Verne")))
        self.assertEqual(str(vanpelt.book_list[5]), str(Book(6, "A Canticle for Leibowitz", "Walter M Miller Jr")))

        vanpelt.open()
        self.assertEqual(vanpelt.flag, 'Y')
        self.assertRaises(Exception, vanpelt.open)
        vanpelt.close()
        vanpelt.open()
        vanpelt.close()
        self.assertEqual(vanpelt.flag, 'N')
        vanpelt.open()
        vanpelt.close()
        self.assertEqual(vanpelt.open(), 'Today is day 4')

        self.assertEqual(vanpelt.find_all_overdue_books(), "No books are overdue." )
        Lily = Patron('Lily Wen', vanpelt)
        vanpelt.patron_info = {'Lily Wen':Lily}
        book = vanpelt.book_list[1]
        book2 = vanpelt.book_list[2]
        vanpelt.calendar.date = 18
        book.due_date = 12
        book2.due_date = 11
        Lily.check_out(book)
        Lily.check_out(book2)
        self.assertEqual(vanpelt.find_all_overdue_books(),
                         "Lily Wen:\n2: 20,000 Leagues Under the Seas, by Jules Verne,\n" +
                         "3: 20,000 Leagues Under the Seas, by Jules Verne\n\n")

        self.assertEqual(vanpelt.issue_card('Lily Wen'), 'Lily Wen already has a library card.')
        self.assertEqual(vanpelt.issue_card('Didi She'), 'Library card issued to Didi She.')
        vanpelt.close()
        self.assertRaises(Exception, vanpelt.issue_card)

        self.assertRaises(Exception, vanpelt.find_overdue_books)
        vanpelt.open()
        self.assertRaises(Exception, vanpelt.find_overdue_books)

        vanpelt.close()
        self.assertRaises(Exception, vanpelt.serve)
        vanpelt.open()
        self.assertEqual(vanpelt.serve('M. Li'), "M. Li does not have a library card.")
        self.assertEqual(vanpelt.serve('Didi She'), "Now serving Didi She.")
        self.assertEqual(vanpelt.current_patron, vanpelt.patron_info['Didi She'])

        self.assertEqual(vanpelt.find_overdue_books(), None)
        vanpelt.serve('Lily Wen')
        self.assertEqual(vanpelt.find_overdue_books(),
                         "2: 20,000 Leagues Under the Seas, by Jules Verne\n" +
                         "3: 20,000 Leagues Under the Seas, by Jules Verne")
        

        self.assertEqual(vanpelt.search('abcdedfg'), "No books found.")
        self.assertEqual(vanpelt.search('abd'), "Search string must contain at least four characters.")
        self.assertEqual(vanpelt.search('Leagues'),
                         "1: 20,000 Leagues Under the Seas, by Jules Verne\n")

        self.assertEqual(vanpelt.search('Sybi'),
                         "31: A Legacy, by Sybille Bedford\n" +
                         "601: Sybil or The Two Nations, by Benjamin Disraeli\n")
                         
        vanpelt.serve('Didi She')
        self.assertEqual(vanpelt.check_out(1, 2), "2 books have been checked out to Didi She")
        self.assertEqual(vanpelt.search('Leagues'),
                         "3: 20,000 Leagues Under the Seas, by Jules Verne\n")
        self.assertEqual(vanpelt.check_out(3), "1 books have been checked out to Didi She")
        self.assertEqual(vanpelt.search('Leagues'), "No books found.")
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[0].due_date, 27)
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[1].due_date, 27)
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[2].due_date, 27)

        vanpelt.close()
        vanpelt.open()
        self.assertRaises(Exception, vanpelt.check_out)
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[0].due_date, 27)
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[1].due_date, 27)
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[2].due_date, 27)

        vanpelt.serve('Didi She')
        self.assertEqual(vanpelt.check_in(1, 3), "Didi She has returned 2 books.")
        self.assertEqual(vanpelt.search('Leagues'),
                         "1: 20,000 Leagues Under the Seas, by Jules Verne\n")
        self.assertEqual(len(vanpelt.patron_info['Didi She'].book_set), 1)

        self.assertEqual(vanpelt.renew(2), '1 books have been renewed for Didi She')
        self.assertEqual(vanpelt.patron_info['Didi She'].book_set[0].due_date, 28)


unittest.main()
