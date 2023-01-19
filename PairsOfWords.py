"""
@author Sanji Albert
I assumed you could use the same word twice in a pair, so I didn't check for that.
@using pypy 3.11 or python 3.11
"""
import os
import pickle
import time
from math import floor
from multiprocessing import Pool
from queue import Queue

LETTERS = set('abcdefghijklmnopqrstuvwxyz'.upper())


def get_set_from_dict_file(pathtofile):
    with open(pathtofile) as data:
        return {line.strip().upper() for line in data}


def getPairs(words):
    """
    :param words: list of all words
    :return: set of all pairs of 3 letter words with a letter in between them that can be found in the library
    """
    seven_let_words = {x for x in words if len(x) == 7}
    return {word for word in seven_let_words if
            word[:3] in words and word[4:] in words and word[3] in LETTERS}


def main(print_results=True):
    results = Queue()
    start_time = time.time()

    words = get_set_from_dict_file("usa.txt")
    results.put(f"Total words read: {len(words)}")
    results.put(f"Total time taken to read the file: {round((time.time() - start_time) * 1000)} ms")
    start_time_2 = time.time()
    pairs = getPairs(words)
    results.put(f"Number of words that can be built with 3 letter word + letter + 3 letter word: {len(pairs)}")

    results.put(f"Total time taken to find the pairs: {round((time.time() - start_time_2) * 1000)} ms")

    results.put(f"Time taken: {round((time.time() - start_time) * 1000)}ms")
    if print_results:
        [print(x) for x in results.queue]
    return (time.time() - start_time_2) * 1000


def benchmark(n=1000):
    # start number of threads equal to 90% of cores running main() using multiprocessing, continue until n runs complete
    process_num = floor(os.cpu_count() * 0.9) if n >= os.cpu_count() else n
    with Pool(process_num) as pool:
        results = pool.map_async(main, [False] * n)

        # Save best run time and its code as a pickle file in format (time, code)
        try:
            with open('best_run.pickle', 'rb') as f:
                best_run = pickle.load(f)
        except FileNotFoundError:
            best_run = (float('inf'), None)

        results = results.get()
    avg_time_ms = round(sum(results) / len(results))
    run = (avg_time_ms, open(__file__).read())
    if run[0] < best_run[0]:
        best_run = run
        with open('best_run.pickle', 'wb') as f:
            pickle.dump(best_run, f)

    return run[0], best_run[0]


if __name__ == "__main__":
    print("Do you want to benchmark? (y/n)")
    if input().upper() == "Y":
        print("Benchmark n times: (int)")
        n = input()
        n = int(n) if (n.isdigit() and 0 < int(n) <= 1000) else 200
        start = time.time()
        bench = benchmark(n)
        end = time.time()
        print("\n----------Multi-Thread Benchmark----------")
        print(f"Average time taken: {bench[0]} ms")
        print(f"Best time taken yet: {bench[1]} ms")
        print(f"Total bench time: {end - start:0.5} s")

        # start = time.time()
        # non_t_results = [main(False) for _ in range(n)]
        # end = time.time()
        # print("\n----------Single-Thread Benchmark----------")
        # print(f"Average time taken: {round(sum(non_t_results) / len(non_t_results))} ms")
        # print(f"Total bench time: {end - start:0.5} s")

    else:
        main()
