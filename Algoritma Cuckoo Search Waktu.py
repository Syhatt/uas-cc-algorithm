import random
import copy

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

# Fungsi untuk melakukan pencarian Cuckoo Search
def cuckoo_search():
    population_size = 50
    best_solution = None
    best_time = float('inf')

    # Inisialisasi populasi awal
    population = [generate_initial_solution() for _ in range(population_size)]

    for _ in range(100):
        # Pilih sarang yang akan ditinggalkan oleh telur
        nest_index = random.randint(0, population_size - 1)
        nest = population[nest_index]

        # Buat solusi baru dari sarang yang dipilih
        cuckoo = generate_neighbor(nest)

        # Evaluasi fitness solusi sarang
        nest_fitness = calculate_total_time(nest)

        # Evaluasi fitness solusi cuckoo
        cuckoo_fitness = calculate_total_time(cuckoo)

        # Jika solusi cuckoo lebih baik, ganti sarang dengan cuckoo
        if cuckoo_fitness < nest_fitness:
            population[nest_index] = cuckoo

        # Jika solusi cuckoo terbaik, simpan sebagai solusi terbaik
        if cuckoo_fitness < best_time:
            best_solution = copy.deepcopy(cuckoo)
            best_time = cuckoo_fitness

        # Buang beberapa telur dengan probabilitas rendah
        p = 0.1
        for i in range(population_size):
            if random.random() < p:
                population[i] = generate_initial_solution()

    return best_solution, best_time

# Jalankan pencarian Cuckoo Search
best_solution, best_time = cuckoo_search()

# Tampilkan hasil
print("Kombinasi tugas dan perangkat mobile dengan waktu minimum (Cuckoo Search):")
for job, device in best_solution.items():
    print("Tugas", job, "-> Perangkat Mobile", device)
print("Total waktu:", best_time)
solution_list = list(best_solution.values())
print("Kombinasi terbaik:", solution_list)
print("Jumlah waktu terendah:", best_time)