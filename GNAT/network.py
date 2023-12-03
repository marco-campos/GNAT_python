import math
import csv

class Synapse:
    def __init__(self, src_id, tgt_id, rel_w, delay):
        self.src_id = src_id
        self.tgt_id = tgt_id
        self.rel_w = rel_w
        self.neg_log_rel_w = -math.log(rel_w)
        self.delay = delay
        self.next = None

    def print_synapse(self):
        print(f"{self.src_id} --> {self.tgt_id} [{self.rel_w:.2f}, {self.delay:.2f}]")

    def __str__(self):
        return f"Synapse(src_id={self.src_id}, tgt_id={self.tgt_id}, rel_w={self.rel_w}, delay={self.delay})"

class PhysNetwork:
    def __init__(self, n_cells):
        self.n_cells = n_cells
        self.presyns = [[] for _ in range(n_cells)]

    def add_synapse(self, synapse):
        if synapse.tgt_id >= self.n_cells:
            raise Exception("Trying to add synapse onto a cell outside of the network population.")
        
        self.presyns[synapse.tgt_id].insert(0, synapse)

    def read_file(self, fname):
        pass

    def print_network(self):
        for synapse_list in self.presyns:
            for synapse in synapse_list:
                synapse.print_synapse()
    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                next(reader)  # Skip the header row
                for row in reader:
                    if len(row) != 4:
                        raise ValueError("Incorrect number of fields in row")

                    src_id, tgt_id = map(int, row[:2])
                    rel_w, delay = map(float, row[2:])
                    synapse = Synapse(src_id, tgt_id, rel_w, delay)

                    self.add_synapse(synapse)

        except IOError:
            raise Exception(f"Unable to open synapse file {filename}")
        except ValueError as e:
            raise Exception(f"File parsing error: {str(e)}")

def create_synapse(src, tgt, rel_w, delay):
    return Synapse(src, tgt, rel_w, delay)
