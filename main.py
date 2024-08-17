# Algorytm Johnsona dla 2 maszyn

# klasa reprezentujaca poszczegolne maszyny (da sie dodac tylko 2) -> pozniej ulepszenie na x maszyn
class Elem:
    def __init__(self, l1, value=None):
        self.l1 = [value] * len(l1) if value is not None else l1
        self.value = value

    def __repr__(self):
        return str(self.l1)

# klasa reprezentujaca cale zbiorowisko
class Work:
    def __init__(self):
        self.tab = []
        self.result = []

        self.time = []

    def add_machine(self, mach):
        self.tab.append(mach)

    def filling_result(self):
        """Inicjalizacja samymi zerami warotsci wynikowej"""
        for row in self.tab:
                self.result.append([0] * len(row.l1))

    def filling_time(self):
        """Inicjalizacja samymi zerami tabelki zakonczenia zadan"""
        for row in self.tab:
                self.time.append([0] * len(row.l1))

    def indexing(self):
        """Przypisuje wszystkie elementy i nadaje im konkretne indeksy"""
        tab_together = []
        for mach_idx, elem in enumerate(self.tab):
            for index, value in enumerate(elem.l1):
                tab_together.append((value, (mach_idx, index)))
        
        return tab_together

    def sorting(self):
        """Sortuje od najmniejszej do najwiekszej wartosci"""
        indexed_array = self.indexing()                
        return sorted(indexed_array)
    
    
    def finish(self):
        """Czarna robota"""
        self.filling_result()
        sorted_array = self.sorting()
        copy = sorted_array.copy()
        
        i = 0
        j = len(self.result[1]) - 1
        idx_top = []
        idx_bottom = []
        q = -1
        p = 0

        for value, (row, idx) in sorted_array:
            # sprawdzamy czy indeks z gory moze sie normalnie wstawic, 
            # czy ten z dolu mu nakazuje co innego
            if row == 0 and idx not in idx_bottom:
                self.result[row][i] = value
                idx_top.append(idx)
                copy.remove((value, (row, idx)))
                i += 1
            # sprawdzamy czy indeks z dolu moze sie normalnie wstawic, 
            # czy indeks z gory go ogranicza i kaze mu byc pod nim
            elif row == 1 and idx not in idx_top:
                self.result[row][j] = value
                idx_bottom.append(idx)
                copy.remove((value, (row, idx)))
                j -= 1

        # bez tej czesci kodu tablica wynikowa uzupelnia sie do polowy
        for m in idx_bottom:
            for value_, (row_, idx_) in copy:
                if m == idx_:
                    self.result[0][q] = value_
                    copy.remove((value_, (row_, idx_)))
                    q -= 1

        for n in idx_top:
            for value_, (row_, idx_) in copy:
                if n == idx_:
                    self.result[1][p] = value_
                    copy.remove((value_, (row_, idx_)))
                    p += 1
    
    def calculate_timing(self):
        """Obliczanie czasu zakonczenia zadan (finalne rozwiazanie)"""
        self.filling_time() 
        temp = 0
        # uzupelnienie wartosci w gornym wierszu
        for i in range(len(self.time[0])):
            value = self.result[0][i]
            self.time[0][i] += value
            self.time[0][i] += temp
            temp += value
        
        # pierwsza wartosc w dolnym wierszu
        self.time[1][0] = self.result[0][0] + self.result[1][0]  

        # trzeba porownywac self.time[1][x] vs self.time[0][x+1] 
        # i wybierac wieksza wartosc do dodania
        for i in range(1, len(self.time[1])): 
            if self.time[1][i-1] > self.time[0][i]:
                self.time[1][i] = self.time[1][i-1] + self.result[1][i] 
            elif self.time[1][i-1] <= self.time[0][i]:
                self.time[1][i] = self.time[0][i] + self.result[1][i]


    def printer(self):
        print(f"Uszeregowanie poczatkowe: \n{self.result}\n")
        print(f"Uszeregowanie koncowe: \n{self.time}")
        print(f"Laczny czas pracy maszyn z zadaniami wynosi: {self.time[1][-1]} jednostek.")

# m - maszyny = 2
# n - ludzie = 10


if __name__ == '__main__':
    praca = Work()
    maszyna1 = Elem([9, 6, 8, 7, 12, 3])
    maszyna2 = Elem([7, 3, 5, 10, 4, 7])
    # maszyna1 = Elem([5, 6, 11, 10, 4, 14, 9, 1, 12, 8])
    # maszyna2 = Elem([7, 3, 4, 9, 10, 2, 6, 16, 7, 1])
    praca.add_machine(maszyna1)
    praca.add_machine(maszyna2)
    praca.finish()
    praca.calculate_timing()
    praca.printer()

    # [(3, (0, 5)), (3, (1, 1)), (4, (1, 4)), (5, (1, 2)), (6, (0, 1)), (7, (0, 3)), (7, (1, 0)),
    # (7, (1, 5)), (8, (0, 2)), (9, (0, 0)), (10, (1, 3)), (12, (0, 4))]

    # [[3, 7, 9, 8, 12, 6], [7, 10, 7, 5, 4, 3]]