class Calendar(object):
    def __init__(self):
        self.date = 0

    def get_date(self):
        return self.date

    def advance(self):
        self.date += 1
        return self.date

class Book(object):
    def __init__(self, ID, title, author):
        self.id = ID
        self.title = title
        self.author = author
        self.due_date = None

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_due_date(self):
        return self.due_date

    def check_out(self, due_date):
        self.due_date = due_date

    def check_in(self):
        self.due_date = None

    def __str__(self):
        return str(self.id) + ": " + self.title + ", by " + self.author

class Patron(object):
    def __init__(self, name, library):
        self.name = name
        self.library = library
        self.book_set = []

    def get_name(self):
        return self.name

    def check_out(self, book):
        self.book_set.append(book)

    def give_back(self, book):
        self.book_set.remove(book)

    def get_books(self):
        return self.book_set

    def get_overdue_books(self):
        over_due = []
        for i in self.get_books():
            if i.get_due_date() < self.library.calendar.get_date():
                over_due.append(i)
        return over_due

class Library(object):
    def __init__(self):
        collections = open('collection.txt', 'r', encoding='utf-8')
        booktxt = eval(collections.read().strip('\n'))
        collections.close()
        i = 1
        book_list = []
        for m in booktxt:
            book = Book(i, m[0], m[1])
            i += 1
            book_list.append(book)

        self.book_list = book_list
        self.calendar = Calendar()
        self.patron_info = {}
        self.flag = 'N'
        self.current_patron = None

    def open(self):
        if self.flag == 'Y':
            raise Exception("The library is already open!")
        self.flag = 'Y'
        date = self.calendar.advance()
        return "Today is day " + str(date)

    def find_all_overdue_books(self):
        info = ''
        for i in self.patron_info:
            books = self.patron_info[i].get_overdue_books()
            x = 0
            if books != []:
                for book in books:
                    books[x] = str(book)
                    x += 1
                info = info + self.patron_info[i].name + ':\n' + ',\n'.join(books) + '\n\n'
        if info == '':
            return "No books are overdue."
        return info

    def issue_card(self, name_of_patron):
        if self.flag == 'N':
            raise Exception("The library is not open.")
        if name_of_patron in self.patron_info:
            return name_of_patron + " already has a library card."
        self.patron_info[name_of_patron] = Patron(name_of_patron, self)
        return "Library card issued to " + name_of_patron + '.'

    def serve(self, name_of_patron):
        if self.flag == 'N':
            raise Exception("The library is not open.")
        if name_of_patron not in self.patron_info:
            return name_of_patron + " does not have a library card."
        self.current_patron = self.patron_info[name_of_patron]
        return "Now serving " + name_of_patron + '.'

    def find_overdue_books(self):
        if self.flag == 'N':
            raise Exception("The library is not open.")
        if self.current_patron == None:
            raise Exception("No patron is currently being served.")
        books = self.current_patron.get_overdue_books()              
        if books == []:
            return None
        x = 0
        for book in books:
            books[x] = str(book)
            x += 1
        return '\n'.join(books)

    def check_in(self, *book_numbers):
        if self.flag == 'N':
            raise Exception("The library is not open")
        if self.current_patron == None:
            raise Exception("No patron is currently being served.")
        books = {}
        n = 0
        for book in self.current_patron.get_books():
            books[book.get_id()] = book
        for i in book_numbers:
            if i not in books:
                raise Exception("The patron does not have book %d."%i)
        for i in book_numbers:
            books[i].check_in()
            self.current_patron.give_back(books[i])
            self.book_list.append(books[i])
            n += 1
        return self.current_patron.get_name() + " has returned %d books."%n

    def search(self, string):
        if len(string) < 4:
            return "Search string must contain at least four characters."
        books = ''
        for book in self.book_list:
            if str(book).lower().find(string.lower()) != -1:
                if str(book)[5 - len(str(book)) : -1] != books[4 - len(str(book)) : -2]:
                    books = books + str(book) + '\n'
        if books == '':
            return "No books found."
        return books

    def check_out(self, *book_ids):
        if self.flag == 'N':
            raise Exception("The library is not open")
        if self.current_patron == None:
            raise Exception("No patron is currently being served.")
        if len(self.current_patron.book_set) + len(book_ids) > 3:
            raise Exception("Patron cannot have more than three books.")
        books = {}
        for book in self.book_list:
            books[book.get_id()] = book
        for i in book_ids:
            if i not in books:
                raise Exception("The library does not have book %d."%i)
        for i in book_ids:
            books[i].check_out(self.calendar.date + 7)
            self.current_patron.check_out(books[i])
            self.book_list.remove(books[i])
        return "%d books have been checked out to " %len(book_ids) + self.current_patron.get_name()

    def renew(self, *book_ids):
        if self.flag == 'N':
            raise Exception("The library is not open")
        if self.current_patron == None:
            raise Exception("No patron is currently being served.")
        books = {}
        n = 0
        for book in self.current_patron.get_books():
            books[book.get_id()] = book
        for i in book_ids:
            if i not in books:
                raise Exception("The patron does not have book %d."%i)
            self.current_patron.give_back(books[i])
            books[i].check_out(self.calendar.date + 7)
            self.current_patron.check_out(books[i])
            n += 1
        return "%d books have been renewed for "%n + self.current_patron.get_name()

    def close(self):
        if self.flag == 'N':
            raise Exception("The library is not open")
        self.flag = 'N'
        self.current_patron = None
        return "Good night."

    def quit(self):
        return "The library is now closed for renovations."

def main():
    vanpelt = Library()
    commands_one = {'open':vanpelt.open, 'overdue':vanpelt.find_all_overdue_books, 'close':vanpelt.close, 'quit':vanpelt.quit}
    commands_two = {'card':vanpelt.issue_card, 'serve':vanpelt.serve, 'search':vanpelt.search}
    commands_three = {'checkin':vanpelt.check_in, 'checkout':vanpelt.check_out, 'renew':vanpelt.renew,}
    print('Brief description:\n')
    print('open -- Opens the library. \n')
    print('overdue -- Prints a list of overdue books. \n')
    print("card Person's name -- Issues a library card to the named person. \n")
    print("serve Person's name -- Makes a note of which Patron we are serving. \n")
    print('checkin id numbers -- Returns books to the library. \n')
    print('checkout id numbers -- Gives books to the patron currently being served.  \n')
    print('renew id numbers -- Extends the period of time that the patron currently being served can keep the books. \n')
    print('search string -- Searches for books containing the given string.  \n')
    print('close -- Closes the library for the day. \n')
    print('quit -- Closes the library permanently and quits the program. \n')
    
    while True:
        command = input("\n>>>").split()
        try:
            if command[0].lower() in commands_one:
                print(commands_one[command[0].lower()]())
            if command[0].lower() in commands_two:
                print(commands_two[command[0].lower()](' '.join(command[1:])))
            if command[0].lower() in commands_three:
                if type(eval(''.join(command[1:]))) != int and type(eval(''.join(command[1:]))) != tuple:
                    raise Exception('Book ids should be seperated by spaces or ","')
                if type(eval(''.join(command[1:]))) == tuple:
                    x = eval(''.join(command[1:]))
                else:
                    x = eval(', '.join(command[1:]))
                if type(x) == int:
                    print(commands_three[command[0].lower()](x))
                elif len(x) == 2:
                    print(commands_three[command[0].lower()](x[0], x[1]))
                elif len(x) == 3:
                    print(commands_three[command[0].lower()](x[0], x[1], x[3]))
                elif len(x) > 3:
                    raise Exception("Patron cannot have more than three books.")
            if command[0].lower() == 'serve':
                if vanpelt.current_patron != None and vanpelt.find_overdue_books() != None:
                    print(vanpelt.find_overdue_books())
            if command[0].lower() == 'quit':
                break
        except Exception as msg:
            print(msg)
                
if __name__ == "__main__":
    main()
