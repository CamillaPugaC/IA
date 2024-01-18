import tkinter as tk
from queue import Queue
from collections import deque

class Node:
    def __init__(self, board, moves):
        self.board = board
        self.moves = moves

class FichaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de las Fichas")
        self.goal_board = [1, 2, 3, 0]  # Estado objetivo
        self.moves_queue = Queue()
        self.moves_stack = []
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Estado inicial
        self.label_initial = tk.Label(self.frame, text="Estado inicial:")
        self.label_initial.grid(row=0, column=0)

        self.initial_table = tk.Frame(self.frame)
        self.initial_table.grid(row=1, column=0)
        self.initial_board = [1, 2, 3, 0]
        self.initial_cells = self.create_table(self.initial_table, self.initial_board, True)

        # Estado final
        self.label_goal = tk.Label(self.frame, text="Estado final:")
        self.label_goal.grid(row=0, column=1)

        self.goal_table = tk.Frame(self.frame)
        self.goal_table.grid(row=1, column=1)
        self.goal_cells = self.create_table(self.goal_table, self.goal_board, False)

        # Movimientos usando colas
        self.label_queue = tk.Label(self.frame, text="Movimientos (cola):")
        self.label_queue.grid(row=2, column=0)

        self.queue_display = tk.Text(self.frame, width=25, height=5)
        self.queue_display.grid(row=3, column=0)

        # Movimientos usando pilas
        self.label_stack = tk.Label(self.frame, text="Movimientos (pila):")
        self.label_stack.grid(row=2, column=1)

        self.stack_display = tk.Text(self.frame, width=25, height=5)
        self.stack_display.grid(row=3, column=1)

        # Botones
        self.btn_play = tk.Button(self.root, text="Jugar", command=self.play_game)
        self.btn_play.pack()

        self.btn_clear = tk.Button(self.root, text="Limpiar", command=self.clear_game)
        self.btn_clear.pack()

    def create_table(self, parent, board, enable_move):
        cells = []
        cell_width = 50
        cell_height = 50

        for i in range(2):
            for j in range(2):
                index = i * 2 + j
                cell_value = board[index]
                x1, y1 = j * cell_width, i * cell_height
                x2, y2 = x1 + cell_width, y1 + cell_height

                if cell_value != 0:
                    cell = tk.Canvas(parent, width=cell_width, height=cell_height)
                    cell.create_rectangle(0, 0, cell_width, cell_height, fill="lightblue")
                    cell.create_text(cell_width // 2, cell_height // 2, text=str(cell_value), font=("Arial", 24))
                    cell.grid(row=i, column=j)
                else:
                    cell = tk.Canvas(parent, width=cell_width, height=cell_height, bg="white")
                    cell.grid(row=i, column=j)

                if enable_move and cell_value != 0:
                    cell.bind("<Button-1>", lambda event, index=index: self.on_cell_click(index))

                cells.append(cell)

        return cells

    def on_cell_click(self, index):
        row, col = index // 2, index % 2
        empty_index = self.initial_board.index(0)
        empty_row, empty_col = empty_index // 2, empty_index % 2

        if (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row):
            self.initial_board[empty_index], self.initial_board[index] = self.initial_board[index], self.initial_board[empty_index]
            self.update_table(self.initial_cells, self.initial_board)

    def update_table(self, cells, board):
        for i in range(len(cells)):
            cell = cells[i]
            cell_value = board[i]
            cell.delete("all")

            if cell_value != 0:
                cell.create_rectangle(0, 0, 50, 50, fill="lightblue")
                cell.create_text(25, 25, text=str(cell_value), font=("Arial", 24))

    def play_game(self):
        self.queue_display.delete("1.0", tk.END)
        self.stack_display.delete("1.0", tk.END)

        initial_state = self.initial_board
        self.moves_queue.queue.clear()
        self.moves_stack = []
        initial_node = Node(initial_state, [])
        self.moves_queue.put(initial_node)
        self.solve_puzzle(self.moves_queue, self.queue_display)

        initial_state = self.initial_board
        self.moves_stack = []
        initial_node = Node(initial_state, [])
        stack = [initial_node]
        self.solve_puzzle(stack, self.stack_display)

    def solve_puzzle(self, structure, display):
        visited = set()
        while structure:
            current_node = structure.get() if isinstance(structure, Queue) else structure.pop()
            current_board, current_moves = current_node.board, current_node.moves

            if tuple(current_board) in visited:
                continue

            visited.add(tuple(current_board))

            if current_board == self.goal_board:
                for move in current_moves:
                    display.insert(tk.END, f"{move}\n")
                break

            for i in range(4):
                new_board = current_board[:]
                empty_index = new_board.index(0)
                if self.can_move(empty_index, i):
                    new_board[empty_index], new_board[i] = new_board[i], new_board[empty_index]
                    new_moves = current_moves + [f"Mover {new_board[i]}"]
                    new_node = Node(new_board, new_moves)

                    if isinstance(structure, list):
                        structure.append(new_node)
                    else:
                        structure.put(new_node)

    def can_move(self, empty_index, target_index):
        moves = {
            0: [1, 2],
            1: [-2, 1],
            2: [-1, 1],
            3: [-2, -1]
        }
        possible_moves = moves.get(empty_index, [])

        return target_index == empty_index + possible_moves[0] or target_index == empty_index + possible_moves[1]

    def clear_game(self):
        self.queue_display.delete("1.0", tk.END)
        self.stack_display.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = FichaGame(root)
    root.mainloop()





