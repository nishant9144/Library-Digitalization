from prime_generator import get_next_size
'''
-------------------------------------------------------------------------------------------------
This is the simple implementation of the hash table, hash set and hash map classes.
-------------------------------------------------------------------------------------------------
'''

class HashTable:
    def __init__(self, collision_type, params, is_map=False):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.table_size = params[-1]
        self.num_of_elements = 0
        self.is_map = is_map  # Distinguishes between HashSet and HashMap behavior

        if collision_type == "Double":
            self.z1, self.z2, self.c2 = params[0:3]
        else:
            self.z = params[0]

        if collision_type == "Chain":
            self.table = [[] for _ in range(self.table_size)]
        else:
            self.table = [None] * self.table_size
        
    def _hash_code(self, character):
        ''' 
            Returns the hash code of a character as explained.
         '''
        if character.islower():
            return ord(character) - ord('a')
        else:
            return ord(character) - ord('A') + 26
        
    def get_slot(self, key):
        value = 0
        z = self.z1 if self.collision_type == "Double" else self.z
        i = 0
        current_z = 1
        for char in key:
            value = (value % self.table_size + (self._hash_code(char) % self.table_size) * (z ** i)) % self.table_size
            i += 1
        
        return value
    
    def _get_step_size(self, key):
        '''
            In probing, we need to calculate the step size for each key.
        '''
        if self.collision_type != "Double":
            return 1
            
        value = 0
        for char in key:
            value = ((value * self.z2) % self.c2 + self._hash_code(char) % self.c2) % self.c2
            
        return self.c2 - value
    
    def insert(self, item):
        if self.num_of_elements >= self.table_size:
            if self.collision_type != "Chain":
                raise Exception("Table is full!")
            
        key, value = item if self.is_map else (item, None)

        if self.find(key):
            return
        
        # Finding initial slot for the key
        initial_slot = self.get_slot(key)
        
        # Chaining collision handling
        if self.collision_type == "Chain":
            self.table[initial_slot].append((key, value) if self.is_map else key)
            self.num_of_elements += 1
            return
            
        # Probing collision handling
        step_size = self._get_step_size(key)
        current_slot = initial_slot
        probes = 0
        
        while probes < self.table_size:
            if self.table[current_slot] is None:
                self.table[current_slot] = (key, value) if self.is_map else key
                self.num_of_elements += 1
                return
            
            current_slot = (current_slot % self.table_size + step_size % self.table_size) % self.table_size
            probes += 1

    def find(self, key):
        initial_slot = self.get_slot(key)
        
        # Chaining collision handling
        if self.collision_type == "Chain":
            for entry in self.table[initial_slot]:
                if (entry if not self.is_map else entry[0]) == key:
                    return True if not self.is_map else entry[1]
            return False if not self.is_map else None
            
        # Probing collision handling
        step_size = self._get_step_size(key)
        current_slot = initial_slot
        probes = 0
        
        while probes < self.table_size:
            if self.table[current_slot] is None:
                return False if not self.is_map else None
            if (self.table[current_slot] if not self.is_map else self.table[current_slot][0]) == key:
                return True if not self.is_map else self.table[current_slot][1]
            current_slot = (current_slot % self.table_size + step_size % self.table_size) % self.table_size
            probes += 1
            
        return False if not self.is_map else None
    
    def get_load(self):
        return self.num_of_elements / self.table_size
         
    def __str__(self):
        content = []
        
        for slot in self.table:
            if self.collision_type == "Chain":
                if not slot:
                    content.append("<EMPTY>")
                else:
                    formatted_entries = []
                    for entry in slot:
                        if self.is_map:
                            # For HashMap: (key, value)
                            formatted_entries.append(f"({entry[0]}, {entry[1]})")
                        else:
                            # For HashSet: just the keys
                            formatted_entries.append(str(entry))
                    content.append(" ; ".join(formatted_entries))
            else:
                if slot is None:
                    content.append("<EMPTY>")
                else:
                    if self.is_map:
                        # For HashMap with probing: (key, value)
                        content.append(f"({slot[0]}, {slot[1]})")
                    else:
                        # For HashSet with probing: just the key
                        content.append(str(slot))
        
        return " | ".join(content)
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass

# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE

# HashSet class inheriting HashTable
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params, is_map=False)  # HashSet does not store values

    def insert(self, key):
        super().insert(key)
    
    def find(self, key):
        return super().find(key)
    
    def get_slot(self, key):
        return super().get_slot(key)    
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()

# HashMap class inheriting HashTable
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params, is_map=True)  # HashMap stores key-value pairs

    def insert(self, key):
        super().insert(key)
    
    def find(self, key):
        return super().find(key)
    
    def get_slot(self, key):
        return super().get_slot(key)    
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()
