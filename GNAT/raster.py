import csv

class SpikeRaster:
    def __init__(self, n_cells):
        self.n_cells = n_cells
        self.sp_lists = [[] for _ in range(n_cells)]
        self.t_min = 0
        self.t_max = 0
        self.n_spikes = 0

    def head_append(self, sp):
        if sp.n_id >= self.n_cells:
            print("FATAL: Attempting to add spike from neuron outside of raster population")
            exit(-1)

        self.sp_lists[sp.n_id].insert(0, sp)
        
        # Update t_max and t_min
        if self.n_spikes == 0:
            self.t_min = sp.ts
            self.t_max = sp.ts
        else:
            self.t_min = min(self.t_min, sp.ts)
            self.t_max = max(self.t_max, sp.ts)

        self.n_spikes += 1


class Spike:
    def __init__(self):  # Other attributes
        self.next = None
        # Initialize other attributes

def SpikeListReverse(list_head):
    prev = None
    cur = list_head
    next = None

    while cur:
        next = cur.next
        cur.next = prev
        prev = cur
        cur = next

    return prev  # New list head

def RasterReverse(sr):
    for idx in range(sr.n_cells):
        new_head = SpikeListReverse(sr.sp_lists[idx])
        sr.sp_lists[idx] = new_head


def RasterReadFile(sr, fname):
    try:
        with open(fname, 'r') as sp_file:
            csv_reader = csv.reader(sp_file, delimiter=',')
            next(csv_reader)  # Skip the header row

            for row in csv_reader:
                if len(row) != 3:
                    print("FATAL: Invalid row format")
                    exit(-1)

                _sp_type, _ts, _n_id = row

                try:
                    _ts = int(_ts, 16)  # Assuming timestamp is in hexadecimal
                    _n_id = int(_n_id)
                    _sp_type = int(_sp_type)
                except ValueError:
                    print("FATAL: Unable to parse spike data")
                    exit(-1)

                sp = create_spike(_n_id, _ts)
                RasterHeadAppend(sr, sp)

            RasterReverse(sr)

    except IOError:
        print(f"FATAL: Could not open spike file {fname}")
        exit(-1)

def RasterPrint(sr):
    if not sr:
        return

    print("------ Spike Raster ------")
    for idx, spike_list in enumerate(sr.sp_lists):
        print(f"Cell {idx}")
        for sp in spike_list:
            print_spike(sp)
            print()
    print("------ End Spike Raster ------")
