# Name: Elizabeth Kacala
# OSU Email: kacalae@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/6/2024
# Description: Contains a class that creates a hashmap using a dynamic
# array and open addressing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Puts a given key value pair into the hash map. If a collision
        occurs, this method uses open addressing to find a new index.
        """
        # Compute load factor and resize table if necessary
        load_factor = self.table_load()
        if load_factor >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Compute element's bucket using the hash function
        index = self._hash_function(key) % self._capacity

        # Place key value pair in array
        if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1
        elif self._buckets[index].key == key:
            self._buckets[index].value = value
        else:
            # Probe for empty index
            count = 0
            new_index = index
            found_status = False
            while found_status is False:
                count += 1
                new_index = (index + count ** 2) % self._capacity
                if new_index > self._capacity:
                    new_index = (new_index - self._capacity)

                if self._buckets[new_index] is None:
                    found_status = True
                elif self._buckets[new_index].is_tombstone is True:
                    found_status = True
                elif self._buckets[new_index].key == key:
                    found_status = True

            # Place key value pair at new index
            if self._buckets[new_index] is None or self._buckets[new_index].is_tombstone is True:
                self._size += 1

            self._buckets.set_at_index(new_index, HashEntry(key, value))

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map to the given capacity. Does nothing if the
        capacity is less than the current size of the hash map.
        """
        if new_capacity < self._size:
            return
        elif self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Resize hash map
        new_buckets = HashMap(new_capacity, self._hash_function)

        if new_capacity == 2:
            new_buckets._capacity = 2
            new_buckets._buckets.pop()

        bucket_key_values = self.get_keys_and_values()

        for num in range(self._size):
            # Get key value pair
            key = str(bucket_key_values[num][0])
            value = bucket_key_values[num][1]

            # Insert key value
            new_buckets.put(key, value)

        self._capacity = new_buckets._capacity
        self._buckets = new_buckets._buckets

    def table_load(self) -> float:
        """
        Compute the load factor by dividing the number of elements in the
        table by the tables total capacity.
        """
        load_factor = self.get_size() / self._buckets.length()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Calculate and return the number of empty buckets in the hash map.
        """
        return self.get_capacity() - self.get_size()

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. Returns None if
        the key is not in the hash map.
        """
        if self.contains_key(key) is False:
            return None

        # Compute index
        index = self._hash_function(key) % self._capacity

        # Get value
        if self._buckets[index].key == key:
            return self._buckets[index].value
        else:
            count = 0
            new_index = index
            while self._buckets[new_index] is not None:
                count += 1
                new_index = (index + count ** 2) % self._capacity
                if new_index > self._capacity:
                    new_index = (new_index - self._capacity)

                if self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is False:
                    return self._buckets[new_index].value

    def contains_key(self, key: str) -> bool:
        """
        Checks if the given key is in the hash map. Returns True if it
        is and False if it is not.
        """
        if self._size == 0:
            return False

        # Find key index
        index = self._hash_function(key) % self._capacity

        # Check if index is in hash table
        if self._buckets[index] is None:
            return False
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is True:
            return False
        else:
            if self._buckets[index].key == key:
                return True
            else:
                count = 0
                new_index = index
                while self._buckets[new_index] is not None:
                    count += 1
                    new_index = (index + count ** 2) % self._capacity
                    if new_index > self._capacity:
                        new_index = (new_index - self._capacity)

                    if self._buckets[new_index] is None:
                        return False
                    elif self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is False:
                        return True

                return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and it's associates value from the hash
        map.
        """
        index = self._hash_function(key) % self._capacity

        # Check if key is in the calculated index
        if self.contains_key(key) is True:
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                self._buckets[index].is_tombstone = True
            else:
                # Probe for value at other indices
                count = 0
                new_index = index
                found_status = False
                while found_status is False: # self._buckets[new_index] is not None:
                    count += 1
                    new_index = (index + count ** 2) % self._capacity
                    if new_index > self._capacity:
                        new_index = (new_index - self._capacity)

                    if self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is False:
                        found_status = True

                self._buckets[new_index].is_tombstone = True
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates and returns a dynamic array containing the hash maps
        keys and values.
        """
        keys_and_values = DynamicArray()

        # Loop through array and append values to the dynamic array
        for num in range(self._capacity):
            if self._buckets[num] is not None:
                if self._buckets[num].is_tombstone is False:
                    key_value = self._buckets[num].key, self._buckets[num].value
                    keys_and_values.append(key_value)

        return keys_and_values

    def clear(self) -> None:
        """
        Empties the hash map while maintaining its capacity.
        """
        new_table = HashMap(self._capacity, self._hash_function)

        if self._capacity == 2:
            new_table._capacity = 2

        self._capacity = new_table._capacity
        self._buckets = new_table._buckets
        self._size = new_table._size

    def __iter__(self):
        """
        Create iterator for loop.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Get next value and advance iterator.
        """
        value = None
        try:
            while value is None or self._buckets[self._index].is_tombstone is True:
                self._index += 1
                value = self._buckets[self._index]
            return value
        except DynamicArrayException:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    """
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    """
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    """
    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))
    
    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    """
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())
    """
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))
    
    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())
    
    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
    
    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    """
    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
