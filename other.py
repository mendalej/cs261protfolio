# if self._buckets[quad] is None:
#     self._buckets.set_at_index(quad, HashEntry(key, value))
#     self._size += 1
# else:
#     inital = 1
#     quad_restated = quad
#     while self._buckets[quad_restated]:
#         if self._buckets[quad_restated].key == key:
#             if self._buckets[quad_restated].is_tombstone:
#                 self._buckets.set_at_index(quad, HashEntry(key, value))
#                 self._size += 1
#                 self._buckets[quad_restated].is_tombstone = False
#             else:
#                 self._buckets.set_at_index(quad, HashEntry(key, value))
#                 break
#         quad_restated = (quad + inital ** 2) % self._capacity
#         inital += 1
# self._buckets.set_at_index(quad, HashEntry(key, value))
# self._size += 1

# hash_1 = quad
# bucket_quad = self._buckets[quad]
# while bucket_quad:
#     # for when the key is in the map
#     if bucket_quad.key == key:
#         self._buckets.set_at_index(quad, HashEntry(key, value))
#         self._size += 1
#         bucket_quad.is_tombstone = False
#     # if you dont find it keep searching
#     elif bucket_quad.is_tombstone is True or key is None:
#         quad = hash_1 + starter**2
#         starter += 1
#     # if you reach the end and it doesnt exist
#     else:
#         self._buckets.set_at_index(quad, HashEntry(key, value))

# uses the quad probing equations
# quad = (quad + starter ** 2) % self._capacity
# starter += 1
# self._buckets.set_at_index(quad, HashEntry(key, value))
# self._size += 1


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
        # a nested for loop
        for elem in range(self._capacity):
            for element in self._buckets[elem]:
                # uses the put method
                new_hash_map.put(element.key, element.value)
        # updates the original items to the new items in the new hash map
        self._buckets, self._capacity, self._size = new_hash_map._buckets, new_hash_map._capacity, new_hash_map._size





set_capacity = new_capacity
        old_buckets = DynamicArray()
        self._buckets = DynamicArray()
        if set_capacity < 1:
            return
        # since it will automatically do nothing if it is less than one, the >= 1 is not restated
        # makes sure that new_capacity is prime and if not it changes it to the next highest prime number
        if self._is_prime(set_capacity) is False:
            set_capacity = self._next_prime(set_capacity)
        for items in range(set_capacity):
            self._buckets.append(LinkedList())
        for element in range(self._capacity):
            for item in self._buckets[element]:
                self._buckets[element].put(item.key, item.value)
        # updates the original items to the new items in the new hash map
        self._buckets = old_buckets
        self._capacity = new_capacity
)