class Spike:
    def __init__(self, n_id, ts):
        self.n_id = n_id
        self.ts = ts
        self.next = None

    def equals(self, other):
        if not isinstance(other, Spike):
            return False
        return self.n_id == other.n_id and self.ts == other.ts

    def print_spike(self):
        print(f"Spike: n_id={self.n_id}, ts={self.ts}")

    def __str__(self):
        return f"Spike[{self.n_id}, {self.ts}]"

class SpikePair:
    def __init__(self, sp1, sp2):
        if sp1.n_id != sp2.n_id:
            print("WARNING: Creating spike pair from spikes from two different cells!")

        if sp1.ts == sp2.ts:
            print("WARNING: Creating spike pair from identical spikes!")

        self.sp1 = sp1
        self.sp2 = sp2
        self.next = None  # Only needed if you're using a linked list structure
        self.prev = None  # Only needed if you're using a linked list structure

    def print_spike_pair(self):
        sp1_str = self.sp1.print_spike() if self.sp1 else "[NULL SPIKE]"
        sp2_str = self.sp2.print_spike() if self.sp2 else "[NULL SPIKE]"
        print(f"{sp1_str} <---> {sp2_str}")


class QuadTree:
    def __init__(self, bbox):
        self.capacity = 0
        self.bdry = bbox
        self.pairs = []  # Python list to store SpikePairs, replaces the NULL pointer in C
        self.NW = None
        self.SW = None
        self.NE = None
        self.SE = None

    def insert(self, spp):
        # Implement logic to insert a SpikePair into the QuadTree
        pass

    def map_query_range(self, r, func):
        # Implement logic for range query
        pass

    def print_qtree(self):
        # Implement logic to print the QuadTree
        pass
    
    def subdivide(self):
        d2 = self.bdry.w2 / 2
        cx, cy = self.bdry.c_x, self.bdry.c_y

        # Creating new bounding boxes for each quadrant
        bbNW = BoundingBox(cx - d2, cy + d2, d2)
        bbNE = BoundingBox(cx + d2, cy + d2, d2)
        bbSW = BoundingBox(cx - d2, cy - d2, d2)
        bbSE = BoundingBox(cx + d2, cy - d2, d2)

        # Creating new QuadTree nodes for each quadrant
        self.NW = QuadTree(bdry=bbNW)
        self.NE = QuadTree(bdry=bbNE)
        self.SW = QuadTree(bdry=bbSW)
        self.SE = QuadTree(bdry=bbSE)

        # Redistributing SpikePairs to the appropriate child nodes
        pairs_to_redistribute = self.pairs
        self.pairs = []

        for spp in pairs_to_redistribute:
            if self.NW.insert(spp):
                continue
            if self.NE.insert(spp):
                continue
            if self.SW.insert(spp):
                continue
            if self.SE.insert(spp):
                continue
            
    def insert(self, spike_pair):
        # Check if spike pair is in our bounding box
        if not self.bdry.contains_point(spike_pair):
            return False

        # If we are not full, add spike pair to list
        if len(self.pairs) < QT_MAX_CAP and self.NW is None:
            self.pairs.append(spike_pair)
            return True

        # If we haven't been subdivided yet, do subdivision
        if self.NW is None:
            self.subdivide()

        # Insert new spike pair into the appropriate quadrant
        if self.NW.insert(spike_pair):
            return True
        if self.SW.insert(spike_pair):
            return True
        if self.NE.insert(spike_pair):
            return True
        if self.SE.insert(spike_pair):
            return True

        # Shouldn't reach here
        return False
    
    def map_query_range(self, r, func):
        """
        Maps the function func to all elements in the QuadTree that fall within the bounding box r.
        """
        # If the region does not intersect our BBox, return
        if not self.bdry.intersects(r):
            return

        # Apply func to all SpikePairs in the current node
        for spp in self.pairs:
            func(spp)

        # Recursively call map_query_range on child nodes if they exist
        if self.NW:
            self.NW.map_query_range(r, func)
            self.SW.map_query_range(r, func)
            self.NE.map_query_range(r, func)
            self.SE.map_query_range(r, func)
    
    def print_tree(self):
        """
        Print the elements of the QuadTree in a depth-first traversal manner.
        """
        if self.capacity > 0:
            for spp in self.pairs:
                print_spike_pair(spp)

        if self.NW:
            self.NW.print_tree()
            self.SW.print_tree()
            self.NE.print_tree()
            self.SE.print_tree()



