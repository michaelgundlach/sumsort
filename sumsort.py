"""
Python implementation of Nathan's sum-sorting problem, using a priority
queue to track our progress through the N-dimensional landscape.
"""

# Note to Nathan re implementation of algorithm: We do NOT need a separate set
# of seen_items in order to guarantee correctness when picking up from where we
# left off earlier.  Because: a seen item is either in the queue, or has been
# popped from the queue.  If it's in the queue, we know about it.  If it has
# been popped from our queue, then the queue will never contain items that
# small ever again, because you can only put items in the queue by popping
# something, then putting that something's larger descendants into the queue.
# So it is sufficient to just make the queue discard duplicates upon insertion.
# However, it may be more efficient to keep a set.


def sorted_sums(lists, pq):
    """
    Yields the sorted sums of items from each list in |lists|.
    |lists| is a list of sorted lists.
    |pq| is a priority queue that discards duplicates.  It will be modified as
    the algorithm runs.  If it is non-empty, the algorithm starts from where it
    earlier left off.
    """
    def itemAt(coords):
        """Return (s, |coords|), where s is the sum of the list values at
        those coordinates."""
        the_sum = sum(L[c] for L, c in zip(lists, coords))
        return (the_sum, coords)
    def next_steps_from(coords):
        """Starting at |coords| in an N-dimensional landscape, yield the
        coords of each single step you can take forward from there.
        For example, (2,4,0) yields (3,4,0), (2,5,0), and (2,4,1).
        """
        coords = list(coords) # convert from (immutable) tuple
        for i in range(len(coords)):
            if len(lists[i]) == coords[i]+1:
                continue # We walked off the map
            coords[i] += 1
            yield tuple(coords)
            coords[i] -= 1

    # If we were handed a non-empty priority queue, pick up from where we
    # left off.  Otherwise, we start at the "entry point" in the landscape.
    if pq.empty():
        root_coords = tuple(0 for L in lists)
        pq.push( itemAt(root_coords) )
    while not pq.empty():
        total, coords = pq.pop()
        #print "Debug: yielding %s at coords %s." % (total, coords)
        #print "Debug: pq is %s" % pq.items
        #print
        yield (total, coords)
        for next_step in next_steps_from(coords):
            pq.push(itemAt(next_step))


class MinPriorityQueue(object):
    """Stub priority queue to implement sorted_sums.  Works, but is
    inefficient for insertion."""
    def __init__(self):
        self.items = []
    def empty(self):
        return not bool(self.items)
    def pop(self):
        return self.items.pop() # from end of list
    def push(self, value):
        for i, x in enumerate(self.items):
            if value > x:
                self.items.insert(i, value)
                break
            if value == x:
                return
        else:
            self.items.append(value)


def tests():
    def test(name, lists, answer, pq=None):
        print "RUNNING TEST: %s" % name
        if pq is None:
            pq = MinPriorityQueue()
        print "INPUTS:"
        for l in lists:
            print l
        print "PRIORITY QUEUE:"
        print pq.items
        print "SUMS:"
        result = list(sorted_sums(lists, pq))
        print [total for total, coords in result]
        print "COORDS:"
        print [coords for total, coords in result]
        if answer != [total for total, coords in result]:
            print "** FAILED TEST '%s': EXPECTED ANSWER WAS: **" % name
            print answer
            print
            import sys
            sys.exit(1)
        print
    test("One list", [ range(10) ], answer=range(10) )
    test("Two simple lists", [ [1,2,3], [100,200,300] ],
         answer=[101,102,103,201,202,203,301,302,303])
    test("Three simple lists", [ [1,2,3], [1,2,3], [1,2,3] ],
         answer=[3,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,9])

    test("Two different-length lists", [ [1,5,10], [2,8,9,40,50] ],
         answer=[3,7,9,10,12,13,14,18,19,41,45,50,51,55,60])

    pq = MinPriorityQueue()
    # This is how the previous test's pq looked after yielding 12.
    # So the following test should yield everything after 12.
    pq.items = [ (41, (0,3)), (14, (1,2)), (13, (1,1)) ]
    test("Picking up where we left off", [ [1,5,10], [2,8,9,40,50] ],
         answer=[13,14,18,19,41,45,50,51,55,60],
         pq=pq)

    test("5 complicated lists", [ [1,2], [3,4], [1,5,10], [2,10], [1,3,6] ],
         answer=[8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 13, 14, 14, 14,
             14, 15, 15, 15, 16, 16, 17, 17, 17, 17, 18, 18, 18, 18, 18,
             18, 19, 19, 19, 19, 19, 20, 20, 20, 20, 21, 21, 21, 21, 22,
             22, 22, 22, 22, 23, 23, 23, 23, 23, 24, 24, 25, 25, 26, 26,
             26, 26, 27, 27, 27, 28, 28, 29, 30, 31, 31, 32])

    # Test using a timeout
    lists =[ [1,2], [3,4], [1,5,10], [2,10], [1,3,6] ]
    import time
    pq = MinPriorityQueue()
    print "Watch me run in half-second bursts!"
    try:
        while True:
            generator = sorted_sums(lists, pq)
            start = time.time()
            while time.time() - start < .5:
                print generator.next()
                time.sleep(0.02)
            print "Pausing..."
            time.sleep(0.3)
            print "Now picking up from where I left off."
    except StopIteration:
        pass


if __name__ == '__main__':
    tests()
