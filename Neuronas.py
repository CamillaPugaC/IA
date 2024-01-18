## PRÁCTICA 3 - 9CM11

# Puga Carbajal Camilla
# Ramírez Luna Gloria Karina


import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *

def variations(n1, n2):
    return n1 ** n2

def create_table(n1, n2, variations):
    listx = []
    variables = n2
    integers = []
    permutations = n1 ** n2
    permutations2 = permutations
    while permutations2 > 1:   
        permutations2 //= n1
        integers.append(int(permutations2))
        
    for B_1 in range(0, permutations):
        listx.append([])

    I_integers = iter(integers)
    integers_reverse = reversed(integers)
    I_integers_reverse = iter(list(integers_reverse))

    for i in range(variables):
        A = next(I_integers)
        B = next(I_integers_reverse) 

        X = "".join(list(map(lambda num: num * A , variations)))
        X2 = X * B
        I_X2 = iter(X2)
        Y = list(map(lambda listx: listx.append(next(I_X2)), listx))
    
    return listx

class Table:       
    def __init__(self, root, rows, columns): 
        self.entries = []
        self.valuesForNeuron = []
        for i in range(rows): 
            self.entries.append(Entry(root, width=5, font=('Arial', 16, 'bold'), justify=tk.CENTER))
            self.entries[i].grid(row=i, column=0) 

    def generateNeuron(self, root, rows, cols, threshold):
        self.combinations = create_table(2, cols, "01")
        self.assignValues(rows)
        for i in range(rows):
            aux = []
            for j in range(cols+1):
                aux.append(self.combinations[i][j])
                if j == cols:
                    aux.pop()
                    result = self.calcNeuron(aux, self.valuesForNeuron, threshold)
                    self.combinations[i][j] = result
                print(self.combinations[i][j], "\t", end="")
            print('')
        self.paintNeuron(rows, cols+1, root)

    def paintNeuron(self, rows, cols, root):
        for j in range(cols): 
            if j == cols-1:
                self.e = Entry(root, width=5, fg='blue', font=('Arial', 16, 'bold')) 
                self.e.grid(row=0, column=j+1) 
                self.e.insert(END, 'Y') 
                self.e.config(state=DISABLED)
            else:
                self.e = Entry(root, width=5, fg='blue', font=('Arial', 16, 'bold')) 
                self.e.grid(row=0, column=j+1) 
                self.e.insert(END, "X"+str(j)) 
                self.e.config(state=DISABLED)
            
        for i in range(rows): 
            for j in range(cols): 
                self.e = Entry(root, width=5, fg='blue', font=('Arial', 16, 'bold')) 
                self.e.grid(row=i+1, column=j+1) 
                self.e.insert(END, self.combinations[i][j]) 
                self.e.config(state=DISABLED)

    def calcNeuron(self, xi, wi, threshold):
        acum = 0
        for i in range(len(xi)):
            acum = acum + (float(xi[i]) * float(wi[i]))
        if acum > threshold:
            return 1
        else:
            return 0

    def assignValues(self, rows):
        for i in range(len(self.entries)):
            self.valuesForNeuron.append(self.entries[i].get())
        for i in range(rows):
            self.combinations[i].append('x')

    def doCombinations(self, cols):
        variations = "01"  
        return create_table(2, cols, variations)

def genTable():
    def reset():
        frame.destroy()
        btnReset.destroy()
    rows = int(entriesNumberValue.get())
    frame = Frame(mainScreen, width=100, height=100)
    frame.grid(row=1, column=1)
    frame.config(bg="thistle")
    frame.config(bd=10)
    btnReset = ttk.Button(mainScreen, text="Limpia", command=reset)
    btnReset.grid(row=2, column=1, padx=10, pady=10)
    global data
    data = Table(frame, rows, 1)

def neuronStart():
    neuron = tk.Tk()
    cols = int(entriesNumberValue.get())
    rows = 2**cols
    threshold = float(entriesThreshold.get())
    data.generateNeuron(neuron, rows, cols, threshold)
    neuron.mainloop()

mainScreen = tk.Tk()
mainScreen.title('Neurona')
mainScreen.geometry('300x300')

mainScreen.rowconfigure(0, weight=1)
mainScreen.rowconfigure(1, weight=3)
mainScreen.rowconfigure(2, weight=1)
mainScreen.columnconfigure(0, weight=1)
mainScreen.columnconfigure(1, weight=3)
mainScreen.columnconfigure(2, weight=1)

lbl1 = tk.Label(mainScreen, text="Entradas", justify=tk.CENTER)
lbl1.grid(row=0, column=0)
entriesNumberValue = tk.StringVar(value="")
entriesNumber = ttk.Entry(mainScreen, font="Helvetica 18 bold", width=2, justify=tk.CENTER, textvariable=entriesNumberValue)
entriesNumber.grid(row=1, column=0)
btnGen = ttk.Button(mainScreen, text="Generar tabla", command=genTable)
btnGen.grid(row=2, column=0, padx=15, pady=15)

lbl2 = tk.Label(mainScreen, text="Umbral", justify=tk.CENTER)
lbl2.grid(row=0, column=2)
entriesThreshold = tk.StringVar(value="")
entryThreshold = ttk.Entry(mainScreen, font="Helvetica 18 bold", width=3, justify=tk.CENTER, textvariable=entriesThreshold)
entryThreshold.grid(row=1, column=2)
btnNeuron = ttk.Button(mainScreen, text="Neurona", command=neuronStart)
btnNeuron.grid(row=2, column=2, padx=15, pady=15)

lbl3 = tk.Label(mainScreen, text="Pesos", justify=tk.CENTER)
lbl3.grid(row=0, column=1)

mainScreen.mainloop()
