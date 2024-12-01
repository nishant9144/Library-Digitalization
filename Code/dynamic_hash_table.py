from Code.hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.table
        old_size = self.table_size

        new_size = get_next_size()
        
        # Get new size and reinitialize table
        self.table_size = new_size
        self.num_of_elements = 0
        
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(self.table_size)]
            # Rehash all elements from all chains
            for chain in old_table:
                for key in chain:
                    self.insert(key)
        else:
            self.table = [None] * self.table_size
            # Rehash all elements from old table
            for i in range(old_size):
                if old_table[i] is not None:
                    self.insert(old_table[i])
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()

    def __str__(self):
        return super().__str__()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.table
        old_size = self.table_size

        new_size = get_next_size()
        
        # Get new size and reinitialize table
        self.table_size = new_size
        self.num_of_elements = 0
        
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(self.table_size)]
            # Rehash all elements from all chains
            for chain in old_table:
                for key, value in chain:
                    self.insert((key, value))
        else:
            self.table = [None] * self.table_size
            # Rehash all elements from old table
            for i in range(old_size):
                if old_table[i] is not None:
                    self.insert(old_table[i])
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()

    def __str__(self):
        return super().__str__()