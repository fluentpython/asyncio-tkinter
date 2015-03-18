import tkinter as tk
import tulip
import threading

from tkevents import TkEventLoop

from HardWork import *
import concurrent.futures

def async(it, *args):
    return (yield from tulip.get_event_loop().run_in_executor(None, it, *args))

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=800, height=400)

        self.grid(sticky=tk.N+tk.S+tk.W+tk.E)
        self.grid_propagate(0)

        self.button = tk.Button(self, font='Consolas 18')
        self.button["text"] = "Count Words"
        self.button["command"] = self.do_count
        self.button.grid(column=0, row=0, sticky=tk.E+tk.W)

        self.QUIT = tk.Button(self, text="QUIT", fg="red", font='Consolas 18', command=root.destroy)
        self.QUIT.grid(column=0, row=2)

        header = tk.Label(self, font='Consolas 16')
        header["text"] = "Status"
        header.grid(column=1, row=0, sticky=tk.W)

        self.status = []
        for i in range(4):
            self.status.append(tk.Label(self, font='Consolas 14'))
            self.status[i].grid(column=1, row=1+i, sticky=tk.W)

    def painful_do_count(self):
        for label in self.status:
            label["text"] = ""

        executor = concurrent.futures.ThreadPoolExecutor(5)
        print('Loading words on ', threading.get_ident())
        future_words = executor.submit(load_words, "Holmes.txt")

        def words_loaded(future_words):
            print('Words loaded completed on thread', threading.get_ident())
            words = future_words.result()
            def words_loaded_update_ui():
                print("{0} words loaded".format(len(words)))
                self.status[0]["text"] = "{0} words loaded".format(len(words))

                print('Cleaning on ', threading.get_ident())
                self.status[1]["text"] = "Cleaning..."
                        
                def words_cleaned(future_clean_words):
                    def words_cleaned_update_ui():
                        words = future_clean_words.result()
                        print("{0} remain after cleaning".format(len(words)))
                        self.status[1]["text"] = "{0} remain after cleaning".format(len(words))

                        def words_counted(future_count):
                            def words_counted_update_ui():
                                count = future_count.result()
                                print("{0} distinct words after counting".format(len(count)))
                                self.status[2]["text"] = "{0} distinct words after counting".format(len(count))

                                def words_sorted(future_most_common):
                                    def words_sorted_update_ui():
                                        self.status[3]["text"] = "Sorting..."
                                        most_common = future_most_common.result()
                                        print("The ten most common words: {0}".format(', '.join(most_common)))
                                        self.status[3]["text"] = "The ten most common words: {0}".format(', '.join(most_common))
                                        print('Sorting on thread ', threading.get_ident())
                                    self.after(0, words_sorted_update_ui)

                                future_most_common = executor.submit(get_most_common, count, 10)
                                future_most_common.add_done_callback(words_sorted)
                            self.after(0, words_counted_update_ui)

                        future_count = executor.submit(count_words, words)
                        future_count.add_done_callback(words_counted)

                    self.after(0, words_cleaned_update_ui)

                future_clean_words = executor.submit(clean_words, words)
                future_clean_words.add_done_callback(words_cleaned)

            self.after(0, words_loaded_update_ui)
            
        future_words.add_done_callback(words_loaded)

    @tulip.task
    def do_count(self):
        for label in self.status:
            label["text"] = ""

        print('Loading words on ', threading.get_ident())
        words = yield from async(load_words, "Holmes.txt")
        print("{0} words loaded".format(len(words)))
        self.status[0]["text"] = "{0} words loaded".format(len(words))

        print('Cleaning on ', threading.get_ident())
        self.status[1]["text"] = "Cleaning..."
        words = yield from async(clean_words, words)
        print("{0} remain after cleaning".format(len(words)))
        self.status[1]["text"] = "{0} remain after cleaning".format(len(words))

        print('Counting on', threading.get_ident())
        self.status[2]["text"] = "Counting..."
        count = yield from async(count_words, words)
        print("{0} distinct words after counting".format(len(count)))
        self.status[2]["text"] = "{0} distinct words after counting".format(len(count))

        print('Sorting on thread ', threading.get_ident())
        self.status[3]["text"] = "Sorting..."
        most_common = yield from async(get_most_common, count, 10)
        print("The ten most common words: {0}".format(', '.join(most_common)))
        self.status[3]["text"] = "The ten most common words: {0}".format(', '.join(most_common))


root = tk.Tk()
app = Application(master=root)

print('Starting on thread', threading.get_ident())
#app.mainloop()
TkEventLoop(app).mainloop()
