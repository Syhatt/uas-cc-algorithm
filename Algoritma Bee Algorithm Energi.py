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

# Fungsi untuk menghitung energi
def calculate_energy(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]
    battery = devices[device]["Battery"]
    transfer_rate = devices[device]["TransferRate"]

    # Hitung energi eksekusi pada perangkat
    execution_energy = (execution_freq / cpu_freq) * (job_size / transfer_rate) * battery

    return execution_energy

# Fungsi untuk menghitung energi transfer data
def calculate_transfer_energy(source, destination, data_size):
    transfer_rate = devices[source]["TransferRate"]
    transfer_energy_per_kb = transfer_energy[destination]

    # Hitung energi transfer data
    transfer_energy_value = (data_size / transfer_rate) * transfer_energy_per_kb

    return transfer_energy_value

# Fungsi untuk menghitung total energi
def calculate_total_energy(combination):
    total_energy = 0

    for job, device in combination.items():
        data_size = jobs[job]["Ukuran"]
        execution_energy = calculate_energy(job, device)
        transfer_energy = calculate_transfer_energy(device, "Fog", data_size)
        total_energy += execution_energy + transfer_energy

    return total_energy

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

# Fungsi untuk menghitung total energi
def calculate_total_energy(solution):
    total_energy = 0
    for job, device in solution.items():
        job_size = jobs[job]["Ukuran"]
        cpu_freq = devices[device]["CPU"]
        transfer_rate = devices[device]["TransferRate"]
        execution_time = job_size / transfer_rate
        energy = execution_time * cpu_freq
        total_energy += energy
    return total_energy

# Fungsi untuk menghitung fitness
def calculate_fitness(solution):
    total_energy = calculate_total_energy(solution)
    return 1 / total_energy

# Fungsi untuk menghasilkan tetangga baru berdasarkan permutasi dua tugas
def generate_neighbor(solution):
    neighbor = solution.copy()
    jobs = list(neighbor.keys())
    random.shuffle(jobs)
    job1, job2 = jobs[:2]
    neighbor[job1], neighbor[job2] = neighbor[job2], neighbor[job1]
    return neighbor

# Fungsi untuk melakukan pencarian Bee Algorithm
def bee_algorithm_search():
    population_size = 50
    elite_bees = 10
    best_solution = None
    best_fitness = 0

    # Inisialisasi populasi awal
    population = [generate_initial_solution() for _ in range(population_size)]

    # Evaluasi fitness populasi awal
    fitness_values = [calculate_fitness(solution) for solution in population]

    for _ in range(100):
        # Pekerja lebah elit
        elite_solutions = [population[i] for i in range(elite_bees)]
        elite_fitness = [fitness_values[i] for i in range(elite_bees)]

        # Pekerja lebah penjelajah
        scout_solutions = [generate_initial_solution() for _ in range(population_size - elite_bees)]
        scout_fitness = [calculate_fitness(solution) for solution in scout_solutions]

        # Pekerja lebah pengikut
        follower_solutions = []

        for i in range(population_size - elite_bees):
            follower_solution = copy.deepcopy(scout_solutions[i])

            for _ in range(5):
                neighbor_solution = generate_neighbor(follower_solution)
                neighbor_fitness = calculate_fitness(neighbor_solution)

                if neighbor_fitness > calculate_fitness(follower_solution):
                    follower_solution = neighbor_solution

            follower_solutions.append(follower_solution)

        # Menggabungkan semua solusi
        all_solutions = elite_solutions + scout_solutions + follower_solutions
        all_fitness = elite_fitness + scout_fitness + [calculate_fitness(solution) for solution in follower_solutions]

        # Memilih solusi terbaik
        best_index = all_fitness.index(max(all_fitness))
        best_solution = all_solutions[best_index]
        best_fitness = all_fitness[best_index]

        # Menyimpan solusi terbaik
        if best_fitness > calculate_fitness(best_solution):
            best_solution = copy.deepcopy(best_solution)

        # Memperbarui populasi
        population = elite_solutions + follower_solutions
        fitness_values = elite_fitness + [calculate_fitness(solution) for solution in follower_solutions]

    return best_solution, calculate_total_energy(best_solution)

# Jalankan pencarian Bee Algorithm
best_solution, best_energy = bee_algorithm_search()

# Tampilkan hasil
print("Kombinasi tugas dan perangkat mobile dengan energi minimum (Bee Algorithm):")
for job, device in best_solution.items():
    print("Tugas", job, "-> Perangkat Mobile", device)
print("Total energi:", best_energy)
solution_list = list(best_solution.values())
print("Kombinasi terbaik:", solution_list)
print("Total energi terendah:", best_energy)