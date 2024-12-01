import Code.hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        '''
            Will be storing tuples of (title, distinct words) in self.books. When counting distinct words is called, we will return the length of the distinct words list.
        '''
        super().__init__()

        self.books = []         
        for title, text in zip(book_titles, texts):
            # Sort words and remove duplicates
            sorted_words = self._merge_sort(text)
            distinct = []
            
            # Remove duplicates while maintaining order
            for word in sorted_words:
                if not distinct or word != distinct[-1]:
                    distinct.append(word)
            
            self.books.append((title,distinct))

        # Sort the books by title
        self.books = self._merge_sort(self.books, comparator=lambda x, y: x[0] < y[0])

    def _merge_sort(self, arr, comparator=None):
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid], comparator)
        right = self._merge_sort(arr[mid:], comparator)
        
        return self._merge(left, right, comparator)

    def _merge(self, left, right, comparator):
        if comparator is None:
            comparator = lambda x, y: x < y
        
        result = []
        while left and right:
            if comparator(left[0], right[0]):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        
        result.extend(left or right)
        return result
    
    def distinct_words(self, book_title):
        book = self._search_book(book_title)
        if book is not None:
            return book[1]
        return None

    def _search_book(self, book_title):
        left, right = 0, len(self.books) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.books[mid][0] == book_title:
                return self.books[mid]
            elif self.books[mid][0] < book_title:
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    def _search_word(self, arr, word):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == word:
                return arr[mid]
            elif arr[mid] < word:
                left = mid + 1
            else:
                right = mid - 1
        return None

    def count_distinct_words(self, book_title):
        book = self._search_book(book_title)
        if book is not None:
            return len(book[1])
        return None
    
    def search_keyword(self, keyword):
        book_with_keyword = []
        for book in self.books:
            find_word = self._search_word(book[1], keyword)
            if find_word is not None:
                book_with_keyword.append(book[0])
        
        return book_with_keyword
    
    def print_books(self):
        for title, words in self.books:
            words_str = " | ".join(words)
            print(f"{title}: {words_str}") 

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        if name == "Jobs":
            self.library = ht.HashMap("Chain", params)
        elif name == "Gates":
            self.library = ht.HashMap("Linear", params)
        elif name == "Bezos":
            self.library = ht.HashMap("Double", params)
           
    def add_book(self, book_title, text):
        param_for_hash_set = (self.library.z1, self.library.z2, self.library.c2, self.library.table_size) if self.name == "Bezos" else (self.library.z, self.library.table_size)
        word_set = ht.HashSet(self.library.collision_type, param_for_hash_set)
        
        for word in text:
            word_set.insert(word)
        
        self.library.insert((book_title, word_set))
    
    def distinct_words(self, book_title):
        result = self.library.find(book_title)
        if result is None:
            return None

        word_set = result  # This is the HashSet containing distinct words
        word_list = []

        if word_set.collision_type == "Chain":
            for bucket in word_set.table:
                if bucket:
                    word_list.extend(bucket)
        else:
            for word in word_set.table:
                if word is not None:
                    word_list.append(word)

        return word_list
    
    def count_distinct_words(self, book_title):
        word_set = self.library.find(book_title)
        if word_set is not None:
            return word_set.num_of_elements
        return 0
    
    def search_keyword(self, keyword):
        books_with_keyword = []
        for node in self.library.table:
            if node is not None:
                if self.name == "Jobs": 
                    for book_title, word_set in node:
                        if word_set and word_set.find(keyword):
                            books_with_keyword.append(book_title)
                else:
                    book_title, word_set = node
                    if word_set and word_set.find(keyword):
                        books_with_keyword.append(book_title)
        return books_with_keyword
        
    def print_books(self):
        if self.library.collision_type == "Chain":
            for bucket in self.library.table:
                for entry in bucket:
                    if entry is not None:
                        book_title, word_set = entry
                        print(f"{book_title}: {word_set}")
        else:
            for entry in self.library.table:
                if entry is not None:
                    book_title, word_set = entry
                    print(f"{book_title}: {word_set}")