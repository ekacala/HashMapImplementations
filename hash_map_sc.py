# Author: Elizabeth Kacala
# Description: Contains a class that creates a hashmap using a dynamic
# array and linked lists.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Put given key value pair into the hash map. Resize table if
        necessary.
        """
        # Find load factor and check if table needs to be resized
        load_factor = self.table_load()
        if load_factor >= 1.0:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Compute element's bucket using the hash function
        index = self._hash_function(key) % self._capacity
        # index = hash % self._capacity

        # Search that bucket for the given key
        searched_key = self._buckets[index].contains(key)
        if searched_key is not None and searched_key.key == key:
            # Replace old value with new value
            searched_key.value = value
        else:
            # Place new key value pair in hash map
            self._buckets[index].insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash map to the given capacity. Does nothing if
        the given capacity is less than 1.
        """
        # Check new_capacity is greater than one and a prime number
        if new_capacity < 1:
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
        Calculate and return the number of empty buckets in the hash map
        """
        empty_buckets = 0
        for num in range(self.get_capacity()):
            if self._buckets[num].length() == 0:
                empty_buckets += 1
        return empty_buckets

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        """
        # Compute index
        index = self._hash_function(key) % self._capacity

        # Search bucket for given key
        if self._buckets[index] is None:
            return None
        else:
            found_key = self._buckets[index].contains(key)

        if found_key is not None:
            return found_key.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the given key is in the hash map. Returns True if it
        is and False if it is not.
        """
        # Find key index
        index = self._hash_function(key) % self._capacity

        if self._buckets[index].contains(key) is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and it's associates value from the hash
        map.
        """
        index = self._hash_function(key) % self._capacity

        # Check if key is in the calculated index
        if self.contains_key(key) is True:
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates and returns a dynamic array containing the hash maps
        keys and values.
        """
        keys_and_values = DynamicArray()

        # Loop through array and append values to the dynamic array
        for num in range(self._capacity):
           # if self._buckets[num] is not None:
            for node in self._buckets[num]:
                key_value = node.key, node.value
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


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the mode of the given dynamic array. Places each value into a hash
    map with the key being the string in the array and the value being the
    number of times it appears. Then loops through the hash map to find the
    key value pair(s) with the highest value.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mode_values = DynamicArray()
    frequency = 0

    # Place items from dynamic array into hash map. Key is the object
    # in the dynamic array and value is the number of times it appears.
    for num in range(da.length()):
        value = map.get(da[num])
        if value is None:
            map.put(da[num], 1)
        else:
            map.put(da[num], value + 1)

    map_keys_and_values = map.get_keys_and_values()

    # Compare values in the new array and update the mode_values array
    # and frequency as needed
    for num in range(map_keys_and_values.length()):
        key = map_keys_and_values[num][0]
        value = map_keys_and_values[num][1]

        if value > frequency:
            if mode_values.length() > 0:  # Reset array if a higher value is found
                mode_values = DynamicArray()
            mode_values.append(key)
            frequency = value
        elif value == frequency:
            mode_values.append(key)

    return mode_values, frequency

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 3")
    print("-------------------")
    m = HashMap(11, hash_function_2)
    m.put('key111', 935)
    m.put('key784', 196)
    m.put('key431', 875)
    m.put('key990', -416)
    m.put('key186', -68)
    m.put('key587', 912)
    m.put('key458', -670)
    m.put('key401', 765)
    m.put('key947', -221)
    m.put('key566', 498)
    m.put('key547', -404)
   # print(m.table_load(), m.get_capacity(), m.get_size())
    m.put('key174', 999)
    print(m)
    print(m.table_load())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    

    print("\nPDF - resize example 3")
    print("----------------------")
    m = HashMap(97, hash_function_1)
    m.put("key346", -536)
    m.put("key653", -809)
    m.put("key915", -111)
    m.put("key348", 218)
    m.put("key564", -745)
    m.put("key907", -357)
    m.put("key628", 606)
    m.put("key556", -326)
    m.put("key971", 643)
    m.put("key935", 448)
    m.put("key648", -470)
    m.put("key549", -908)
    m.put("key865", 662)
    m.put("key757", -841)
    m.put("key929", -759)
    m.put("key996", 686)
    m.put("key41", -533)
    m.put("key19", -308)
    m.put("key87", 129)
    m.put("key88", 813)
    m.put("key421", 722)
    m.put("key6", -670)
    m.put("key810", 201)
    m.put("key900", 489)
    m.put("key722", 715)
    m.resize_table(2)
#    m = HashMap()
    print(m)
    print(m.get_capacity(), m.get_size())

    print("\nPDF - resize example 4")
    print("----------------------")
    m = HashMap(37, hash_function_1)
    m.resize_table(2)
    print(m)

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
    m = HashMap(53, hash_function_1)
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
    
    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")


