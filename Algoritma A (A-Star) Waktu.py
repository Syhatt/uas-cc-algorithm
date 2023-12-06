import random
import heapq

# Informasi pekerjaan
jobs = {
    1: {
        "Ukuran": 30,  # dalam KB
        "Eksekusi": 40000  # dalam Hz
    },
    2: {
        "Ukuran": 100,  # dalam KB
        "Eksekusi": 500000  # dalam Hz
    },
    3: {
        "Ukuran": 10000,  # dalam KB
        "Eksekusi": 40000  # dalam Hz
    },
    4: {
        "Ukuran": 50,  # dalam KB
        "Eksekusi": 200000  # dalam Hz
    },
    5: {
        "Ukuran": 500,  # dalam KB
        "Eksekusi": 1000000  # dalam Hz
    },
    6: {
        "Ukuran": 200,  # dalam KB
        "Eksekusi": 600000  # dalam Hz
    },
    7: {
        "Ukuran": 1000,  # dalam KB
        "Eksekusi": 300000  # dalam Hz
    },
    8: {
        "Ukuran": 150,  # dalam KB
        "Eksekusi": 700000  # dalam Hz
    },
    9: {
        "Ukuran": 1000,  # dalam KB
        "Eksekusi": 200000  # dalam Hz
    },
    10: {
        "Ukuran": 2000,  # dalam KB
        "Eksekusi": 900000  # dalam Hz
    }
}

# Informasi perangkat mobile
devices = {
    i: {
        "CPU": random.uniform(1.0, 2.0),  # dalam GHz
        "Battery": random.uniform(3.0, 6.0),  # dalam AH
        "TransferRate": random.uniform(10, 50)  # dalam Mbps
    }
    for i in range(1, 51)
}

# Informasi transfer energi
transfer_energy = {
    "Fog": 0.01,  # dalam AH per KB
    "Cloud": 0.01  # dalam AH per KB
}

# Fungsi untuk menghitung waktu
def calculate_time(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]

    # Hitung waktu eksekusi pada perangkat
    execution_time = job_size / (execution_freq / cpu_freq)

    return execution_time

# Fungsi untuk menghitung waktu transfer data
def calculate_transfer_time(source, destination, data_size):
    transfer_rate = devices[source]["TransferRate"]

    # Hitung waktu transfer data
    transfer_time = data_size / transfer_rate

    return transfer_time

# Fungsi untuk menghitung total waktu
def calculate_total_time(combination):
    total_time = 0

    for job, device in combination.items():
        data_size = jobs[job]["Ukuran"]
        execution_time = calculate_time(job, device)
        transfer_time = calculate_transfer_time(device, "Fog", data_size)
        total_time += execution_time + transfer_time

    return total_time

# Fungsi untuk menghasilkan kombinasi awal
def generate_initial_solution():
    combination = {}

    for job in range(1, 11):
        devices_copy = list(devices.keys())
        random.shuffle(devices_copy)
        device = devices_copy[0]
        combination[job] = device

    return combination

# Fungsi untuk menghasilkan tetangga baru berdasarkan permutasi dua tugas
def generate_neighbor(solution):
    neighbor = solution.copy()
    jobs = list(neighbor.keys())
    random.shuffle(jobs)
    job1, job2 = jobs[:2]
    neighbor[job1], neighbor[job2] = neighbor[job2], neighbor[job1]
    return neighbor

    # Fungsi untuk menghitung estimasi heuristik
def calculate_heuristic(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]
    transfer_rate = devices[device]["TransferRate"]

    # Hitung estimasi waktu eksekusi pada perangkat
    execution_time = (job_size / transfer_rate) / cpu_freq

    # Hitung estimasi waktu transfer data
    transfer_time = job_size / transfer_rate

    # Hitung estimasi heuristik sebagai jumlah waktu eksekusi dan transfer
    heuristic = execution_time + transfer_time

    return heuristic

# Fungsi untuk melakukan pencarian Algoritma A*
def a_star_search():
    start_node = (0, generate_initial_solution())
    open_set = [start_node]
    closed_set = set()

    while open_set:
        _, current_solution = heapq.heappop(open_set)

        if frozenset(current_solution.items()) in closed_set:
            continue

        closed_set.add(frozenset(current_solution.items()))

        if len(current_solution) == len(jobs):
            total_time = calculate_total_time(current_solution)
            return current_solution, total_time

        remaining_jobs = set(jobs.keys()) - set(current_solution.keys())
        remaining_devices = set(devices.keys()) - set(current_solution.values())

        for job in remaining_jobs:
            for device in remaining_devices:
                neighbor = current_solution.copy()
                neighbor[job] = device
                g = calculate_total_time(neighbor)
                h = calculate_heuristic(job, device)
                f = g + h
                heapq.heappush(open_set, (f, neighbor))

    return None, None

# Jalankan pencarian Algoritma A*
best_solution, best_time = a_star_search()

# Tampilkan hasil
if best_solution is None:
    print("Tidak ditemukan solusi yang memenuhi")
else:
    print("Kombinasi tugas dan perangkat mobile dengan waktu minimum (A-Star):")
    for job, device in best_solution.items():
        print("Tugas", job, "-> Perangkat Mobile", device)
    print("Total waktu:", best_time)
    solution_list = list(best_solution.values())
    print("Kombinasi terbaik:", solution_list)
    print("Jumlah waktu terendah:", best_time)