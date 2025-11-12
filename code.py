# Python

import random

def fitness_function(x):
    """Целевая функция: f(x) = -(x - 5)**2 + 25"""
    return -(x - 5)**2 + 25

def initialize_population(pop_size, chrom_length):
    """Инициализация начальной популяции"""
    return [[random.randint(0, 1) for _ in range(chrom_length)] for _ in range(pop_size)]

def decode_chromosome(chromosome, x_min, x_max):
    """Преобразование двоичной строки в вещественное число"""
    decimal = sum(gene * (2 ** (len(chromosome) - 1 - i)) for i, gene in enumerate(chromosome))
    return x_min + (decimal / (2**len(chromosome) - 1)) * (x_max - x_min)

def select_parent(population, fitnesses):
    """Отбор родителя методом рулетки"""
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, chrom in enumerate(population):
        current += fitnesses[i]
        if current > pick:
            return chrom

def crossover(parent1, parent2, crossover_rate):
    """Одноточечный кроссовер"""
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def mutate(chromosome, mutation_rate):
    """Точечная мутация"""
    return [1 - gene if random.random() < mutation_rate else gene for gene in chromosome]

# Ввод параметров
print("Генетический алгоритм для максимизации f(x) = -(x-5)^2 + 25")
print("Диапазон x: [0, 10]")
print()

pop_size = int(input("Размер популяции: ") or "20")
generations = int(input("Количество поколений: ") or "50")
crossover_rate = float(input("Вероятность кроссовера: ") or "0.8")
mutation_rate = float(input("Вероятность мутации: ") or "0.1")
chrom_length = int(input("Длина хромосомы: ") or "10")

# Параметры задачи
x_min, x_max = 0, 10

# Инициализация
population = initialize_population(pop_size, chrom_length)
best_x, best_fitness = 0, -float('inf')

# Основной цикл ГА
for gen in range(generations):
    # Декодирование и оценка
    decoded = [decode_chromosome(chrom, x_min, x_max) for chrom in population]
    fitnesses = [fitness_function(x) for x in decoded]
    
    # Обновление лучшего решения
    for i, x in enumerate(decoded):
        if fitnesses[i] > best_fitness:
            best_fitness = fitnesses[i]
            best_x = x
    
    # Создание нового поколения
    new_population = []
    while len(new_population) < pop_size:
        parent1 = select_parent(population, fitnesses)
        parent2 = select_parent(population, fitnesses)
        child1, child2 = crossover(parent1, parent2, crossover_rate)
        new_population.append(mutate(child1, mutation_rate))
        new_population.append(mutate(child2, mutation_rate))
    
    population = new_population[:pop_size]

# Вывод результатов
print(f"\nЛучшее решение: x = {best_x:.6f}")
print(f"Максимальное значение: f(x) = {best_fitness:.6f}")
print(f"Истинный максимум: x = 5.000000, f(x) = 25.000000")
print(f"Погрешность: {abs(25.0 - best_fitness):.8f}")
