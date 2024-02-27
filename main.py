from gui.gui import GUI
import tkinter as tk
import json
from algorithm.classic import Algorithm as Clas
from algorithm.classicKMethod import Algorithm as Kmethod
from algorithm.karcas import Algorithm
import os
import time

def test(algorithm: Algorithm, filename: str):
    with open(f"results/{filename}.txt", "w") as file:
        for i in range(4, 101):
            name = f"tests/test_{i}.json"
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm
                algo.init_graph(data["num_vertex"], data["edges"])
                sum_1 = 0
                for edge in algo.search_hamilton_cycle():
                    sum_1 += edge["weight"]
                file.write(f"{sum_1}\n")
                print(f"test,{i}, {filename}, {sum_1}")
    

if __name__ == "__main__":
    algoritm = Clas()
    t_start = time.time()
    test(algoritm, "classic")
    t_end = time.time()
    print(f"classic: {(t_end - t_start) / 100}")
    
    algoritm = Kmethod()
    t_start = time.time()
    test(algoritm, "kmethod")
    t_end = time.time()
    print(f"kmethod: {(t_end - t_start) / 100}")
            