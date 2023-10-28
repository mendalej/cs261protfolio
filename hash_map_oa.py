# Name: Alejandra Mendez
# OSU Email: mendalej@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Portfolio assignment
# Due Date: June 9th, 2023
# Description: Completion of the Hashmap implementation using either open addressing or collision resolution

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
        Updates the key/value pair in the hash map
        """
        # the table resize
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        quad = self._hash_function(key) % self._capacity
        b_quad = self._buckets[quad]
        j = 1
        # if the key is not equal to the key and tomb is false
        probing = quad
        # the section that does the probing
        while b_quad is not None and (b_quad.is_tombstone is False and b_quad.key != key):
            probing = (quad + j ** 2) % self._capacity
            j += 1
            b_quad = self._buckets[probing]
        new = HashEntry(key, value)
        if b_quad is None or (b_quad.key != key and b_quad.is_tombstone is True) or b_quad.key == key:
            self._buckets[probing] = new
        if b_quad is None or b_quad.is_tombstone is True:
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # the equation for table load is n/m (m is the number of buckets and n is the total number of elements)
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the Hash Table
        """
        # check to see if this is correct
        # m is total slots and n is filled slots therefore m-n gives the open or empty slots
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table
        """
        set_capacity = new_capacity
        # checks that it is not less than the current number of elements
        if set_capacity < self._size:
            return
        # checks if it is valid and if it is a prime number, if not it goes to the next prime number
        if self._is_prime(set_capacity) is False:
            set_capacity = self._next_prime(set_capacity)
        new_hash_map = HashMap(set_capacity, self._hash_function)
        # for when it is 2 and doesn't know that 2 is a prime number
        for index in range(self._capacity):
            element = self._buckets[index]
            if element is not None:
                # uses the put method
                new_hash_map.put(element.key, element.value)
        # updates the original items to the new items in the new hash map
        self._buckets = new_hash_map._buckets
        self._capacity = new_hash_map._capacity
        self._size = new_hash_map._size
        #
    def quadratic_helper(self, key):
        """
        helper function for quadratic probing
        """

        j = 1
        quad = self._hash_function(key) % self._capacity
        b_quad = self._buckets[quad]
        # if the key is not equal to the key and tomb is false
        probing = quad
        while b_quad is not None:
            if b_quad.key == key:
                return probing
            else:
                probing = (quad + j ** 2) % self._capacity
                j += 1
            b_quad = self._buckets[probing]
        return probing

    def get(self, key: str) -> object:
        """
        Returns the value associated with the give key.
        """
        index = self.quadratic_helper(key)
        bucket = self._buckets[index]
        # uses the helper method and uses the same idea as put
        if bucket is not None and bucket.key == key and not bucket.is_tombstone:
            return bucket.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        # uses the quadratic helper method
        index = self.quadratic_helper(key)
        bucket = self._buckets[index]
        # uses the same idea as get and put in checking if key = key and sets tombstone to false
        return bucket is not None and bucket.key == key and not bucket.is_tombstone

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map
        """
        # uses the helper method
        quad = self.quadratic_helper(key)
        bucket = self._buckets[quad]
        # uses the same idea as get and put in checking if key = key and sets tombstone to false
        if bucket is not None and bucket.key == key and not bucket.is_tombstone:
            # decreases the size
            self._size -= 1
            # sets is_tombstone to True
            bucket.is_tombstone = True

    def clear(self) -> None:
        """
        Clears the contents of the hashmap
        """
        # uses append to help clear the contents
        self._buckets = DynamicArray()
        for items in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a dynamic array where each index contains a tuple of key/value pair stored in the hash map
        """

        # creates the dynamic array
        array = DynamicArray()
        # for loop to go iterate through the capacity
        for index in range(self._capacity):
            element = self._buckets[index]
            if element and element.is_tombstone is False:
                # uses append to add the key and value to the array
                array.append((element.key, element.value))
        return array


    def __iter__(self):
        """
        Enables the hash map to iterate across itself.
        """
        # basically the same thing I did in the previous assignment
        self._index = 0
        # adapted from the example in the exploration
        # the recommended tracker
        tracker = 0
        tracker += 1

        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of the iterator.
        """
        # implemented in the same way as from assignment 2 with some modifications since it only needs to iterate over
        # active items only
        try:
            # adapted from the example in the exploration
            # a loop so that it only iterates over active items
            value = None
            # use is.tombstone bc it is set to True when a value is deleted
            while value is None or value.is_tombstone:
                value = self._buckets[self._index]
                self._index += 1
        except DynamicArrayException:
            raise StopIteration
        return value


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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1', )
    m.resize_table(12)
    print(m.get_keys_and_values())

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
