# Name: Alejandra Mendez
# OSU Email: mendalej@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Portfolio assignment
# Due Date: June 9th, 2023
# Description: Completion of the Hashmap implementation using either open addressing or collision resolution

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
        Updates the key/value pair in the hash map
        """
        # to resize and uses table load
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hashed_key = self._hash_function(key) % self._capacity
        bucket_key = self._buckets[hashed_key]
        dupe = bucket_key.contains(key)
        # for when there is no hashmap key
        if bucket_key.length() == 0:
            bucket_key.insert(key, value)
            self._size += 1
        # to check if there is a duplicate of the key and replacement of that value
        elif dupe is not None:
            dupe.value = value
        # otherwise just insert new key/value pair
        else:
            bucket_key.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # counter
        counter = 0
        for elem in range(self._capacity):
            # looks at a specific index and the length
            if self._buckets[elem].length() == 0:
                # increase the counter by 1
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Returns the current hash table factor
        """
        # the equation for table load is n/m (m is the number of buckets and n is the total number of elements)
        return self._size / self._capacity

    def clear(self) -> None:
        """
        clears the contents of the hash map
        """
        self._buckets = DynamicArray()
        self._size = 0
        # appends the LinkedList into the Dynamic array
        for items in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map
        """
        # checks if the new capacity is not less than 1
        # checks if the new capacity is not less than 1
        set_capacity = new_capacity
        if set_capacity < 1:
            return
        # since it will automatically do nothing if it is less than one, the >= 1 is not restated
        # makes sure that new_capacity is prime and if not it changes it to the next highest prime number
        if self._is_prime(set_capacity) is False:
            set_capacity = self._next_prime(set_capacity)
        # the new created hash map
        new_hash_map = HashMap(set_capacity, self._hash_function)
        # for when it is 2 and doesn't know that 2 is a prime number
        if set_capacity == 2:
            new_hash_map._capacity = 2
            new_hash_map._size = 2
        # a nested for loop
        for elem in range(self._capacity):
            for element in self._buckets[elem]:
                # uses the put method
                new_hash_map.put(element.key, element.value)
        # updates the original items to the new items in the new hash map
        self._buckets, self._capacity, self._size = new_hash_map._buckets, new_hash_map._capacity, new_hash_map._size



    def get(self, key: str):
        """
        Returns the value associated with the given key and returns None if the key is not in the hash map
        """
        hashed_key = self._hash_function(key) % self._capacity
        bucket_key = self._buckets[hashed_key]
        # for when it is empty
        if bucket_key.length() == 0:
            return None
        for element in bucket_key:
            # checking if the key is equal to the key
            if element.key == key:
                return element.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        # basically did the same thing from get except instead of returning the element I am returning true or False
        hashed_key = self._hash_function(key) % self._capacity
        bucket_key = self._buckets[hashed_key]
        for elem in bucket_key:
            if elem.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        # a for loop to iterate through the range of the capacity
        for element in range(self._capacity):
            # the second for loop is needed to iterate through self._bucket
            for elem in self._buckets[element]:
                # compares the elem key to the given key
                if elem.key == key:
                    # removes the key by using remove from a6 include
                    self._buckets[element].remove(key)
                    # decreases the size
                    self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a dynamic array where each index contains a tuple of key/value pair stored in the hash map
        """
        # creates the dynamic array
        array = DynamicArray()
        # for loop to go iterate through the capacity
        for element in range(self._capacity):
            # the second for loop is needed to iterate through self._bucket
            # return the tuples
            for elem in self._buckets[element]:
                array.append((elem.key, elem.value))
        return array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A standalone function that receives a dynamic array and returns a tuple containing, a dynamic array comprising the
    mode value and an integer that represents the highest frequency
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mod = DynamicArray()
    # goes through the hashmap
    for item in range(da.length()):
        if not map.contains_key(da[item]):
            map.put(da[item], 1)
        else:
            map.put(da[item], map.get(da[item]) + 1)
    visitation = map.get_keys_and_values()
    # tries to find the frequency and the mode
    highest_frequency = visitation[0][1]
    for element in range(visitation.length()):
        if highest_frequency < visitation[element][1]:
            highest_frequency = visitation[element][1]
    for element in range(visitation.length()):
        if visitation[element][1] == highest_frequency:
            mod.append(visitation[element][0])
    return mod, highest_frequency

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
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
