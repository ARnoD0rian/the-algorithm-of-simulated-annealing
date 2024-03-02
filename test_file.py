import json
from algorithm.classic import Algorithm as Clas
from algorithm.classicKMethod import Algorithm as Kmethod
from algorithm.modKmethod import Algorithm as ModKmenhod
from algorithm.polupationModKmethod import Algorithm as PopModKmethod
from algorithm.modKmethodpopulation import Algorithm as modKmethodpop
from algorithm.classicAndNearestNeibhor import Algorithm as lastmodification
from algorithm.karcas import Algorithm
import os
import copy
import time


N = 100

def test_on_result(algorithm: Algorithm, filename: str):
    with open(f"results/result/{filename}.txt", "w") as file:
        for i in range(4, N + 1):
            name = f"tests/result/test_{i}.json"
            print(f"test {i}, result")
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm()
                algo.init_graph(data["num_vertex"], data["edges"])
                sum_1 = 0
                for edge in algo.search_hamilton_cycle():
                    sum_1 += edge["weight"]
                file.write(f"{sum_1}\n")
                # print(f"test,{i}, {filename}, {sum_1}")

def test_on_search(algorithm: Algorithm, filename: str):
    with open(f"results/search/{filename}.txt", "w") as file:
        k = 0
        for i in range(4, N + 1):
            name = f"tests/search/test_{i}.json"
            print(f"test {i}, search")
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm()
                algo.init_graph(data["num_vertex"], data["edges"])
                way = algo.search_hamilton_cycle()
                if len(way) != 0: k += 1 
                
        file.write(f"{k/(N - 3)}\n")
        
def test_on_time(algorithm: Algorithm, filename: str):
    with open(f"results/time/{filename}.txt", "w") as file:
        for i in range(4, N + 1):
            name = f"tests/time/test_{i}.json"
            print(f"test {i}, time")
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm()
                time_start = time.time()
                algo.init_graph(data["num_vertex"], data["edges"])
                way = algo.search_hamilton_cycle()
                time_end = time.time()
                if len(way) != 0: file.write(f"{time_end - time_start}\n")

def start_test(algorithm: Algorithm, filename: str, test):
    test(algorithm, filename)
    print(f"{filename} has completed successfully, {test.__name__}")
    
tests = {"result": test_on_result, "search": test_on_search, "time": test_on_time}

if __name__ == "__main__":
    start_test(Clas, "sumulated_annealing", tests["time"])
    start_test(lastmodification, "modification", tests["time"])
    start_test(lastmodification, "modification", tests["result"])
    start_test(Kmethod, "nearest neibhor", tests["result"])