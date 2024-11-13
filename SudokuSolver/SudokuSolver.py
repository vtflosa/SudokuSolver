import solver
import tkinter
import tkinter.messagebox


class Window:
    """create the window and grid to display the sudoku"""
    def __init__(self, window):
        self.window = window
        self.window.title("Sudoku Solver ... by Flo")
        self.window.withdraw()
        self.main_frame = tkinter.Frame(self.window, relief="sunken", background="grey30")
        self.main_frame.grid(row=0, column=0, sticky="news")
        self.board_frame = None
        self.board = None
        self.board_text_entry = None
        self.font = ("Helvetica", "38", "bold")
        self.solve_button = None
        self.build_buttons()
        self.new_board()


    def build_buttons(self):
        new_board_button = tkinter.Button(self.main_frame, text="Nouvelle grille", bd=6, padx=40, pady=10,
                                          background="navajo white", command=self.new_board)
        new_board_button.grid(row=1, column=0)
        quit_button = tkinter.Button(self.main_frame, text="Quitter", bd=6, padx=40, pady=10,
                                     background="navajo white", command=self.quit_game)
        quit_button.grid(row=1, column=2, pady=15)
        self.build_solve_button()

    def build_solve_button(self):
        self.solve_button = tkinter.Button(self.main_frame, text="Solution", bd=6, padx=40, pady=10,
                                           background="lightblue", command=self.check_entry)
        self.solve_button.grid(row=1, column=1)

    def center_window(self):
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.update()
        w = self.window.winfo_reqwidth()
        h = self.window.winfo_reqheight()
        self.window.geometry("{}x{}+{}+{}".format(w, h, int((width - w) / 2), int((height-h) / 4)))
        self.window.minsize(w, h)
        self.window.maxsize(w, h)
        self.window.deiconify()



    def new_board(self, activate_solve_button=True):

        # reactivate solve button after new_grid is selected
        if activate_solve_button:
            self.solve_button.configure(state="normal")
        # build board frame
        if self.board_frame:
            self.board_frame.destroy()
        self.board_frame = tkinter.Frame(self.main_frame, relief="sunken")
        self.board_frame.grid(row=0, column=0, columnspan=3, sticky="news")
        region = Grid(self.board_frame)

        # create the subregion frames
        subregion = [[None for i in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                subregion[i][j] = Grid(region.subframe[i][j])

        # create an empty board
        self.board_text_entry = [[None for i in range(9)] for j in range(9)]

        # create all the entry zones
        for i in range(9):
            for j in range(9):
                (k, l), (m, n) = self.coord(i, j)
                self.board_text_entry[i][j] = tkinter.Text(region.subframe[k][l], width=1, height=1,
                                                           font=self.font,
                                                           padx=20,
                                                           relief="sunken")
                self.board_text_entry[i][j].grid(row=m, column=n, sticky="news")
                self.board_text_entry[i][j].tag_configure("center", justify="center")
                self.board_text_entry[i][j].insert("end", "", "center")
                self.board_text_entry[i][j].bind("<Enter>", self.on_mouse_over)

        # Then Center the window
        self.center_window()

    @staticmethod
    def on_mouse_over(event):
        event.widget.insert("end", "", "center")
        event.widget.focus_set()

    @staticmethod
    def coord(x, y):
        """ for a given coor in the 9x9 matrix return :
            - the region coord as 3x3 matrix in the 9x9 matrix
            - the subregion coord as 3x3 matrix in the region coord"""
        region = [[0 for i in range(9)] for i in range(9)]
        region_list = [[(i, j) for j in range(3)] for i in range(3)]
        m, n = 0, 0
        for i in range(9):
            for j in range(9):
                region[i][j] = (region_list[m][n])
                if j in [2, 5, 8]:
                    n += 1
                    if n == 3:
                        n = 0
            if i in [2, 5, 8]:
                m += 1
                if m == 3:
                    m = 0

        subregion = [[0 for i in range(9)] for i in range(9)]
        m, n = 0, 0
        for i in range(9):
            for j in range(9):
                subregion[i][j] = (region_list[m][n])
                n += 1
                if n == 3:
                    n = 0
            m += 1
            if m == 3:
                m = 0

        return region[x][y], subregion[x][y]

    def quit_game(self):
        self.window.destroy()

    def check_entry(self):
        board = [[None for i in range(9)] for j in range(9)]
        # collect the user entry
        for i in range(9):
            for j in range(9):
                board[i][j] = self.board_text_entry[i][j].get("1.0", "end")
                board[i][j] = board[i][j].replace("\n", "")
                board[i][j] = board[i][j].replace(" ", "")

        # check if entry are valid
        invalid_entry = False
        for i in range(9):
            for j in range(9):

                # not valid entry in coord i,j
                if board[i][j] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", ""]:
                    invalid_entry = True
                    board[i][j] = 0
                    self.board_text_entry[i][j].configure(bg="orange")  # change color of the invalid entry
                    self.board_text_entry[i][j].delete("1.0", "end")  # delete invalid entry
                    self.board_text_entry[i][j].insert("end", "", "center")
                    continue
                if board[i][j]:  # it's a valid entry
                    board[i][j] = int(board[i][j])
                    self.board_text_entry[i][j].configure(bg="green")
                if not board[i][j]:
                    board[i][j] = 0
                    self.board_text_entry[i][j].configure(bg="white")

        if invalid_entry:
            tkinter.messagebox.showwarning("Saisie invalide !", "Une ou plusieurs saisies sont invalides\n\n"
                                                                "Merci de ne saisir qu'un seul chiffre par case\n"
                                                                "dans les cases oranges.")

        # check if grid is valid = not impossible board due to wrong user entry
        duplicate_entry = solver.grid_not_valid(board)

        if duplicate_entry:
            for i, j in duplicate_entry:
                self.board_text_entry[i][j].configure(bg="red")  # change color of the invalid entry

            tkinter.messagebox.showwarning("Grille Invalide !", "Une ou plusieurs saisies sont invalides\n\n"
                                                                "Certains chiffres sont en double dans la même\n"
                                                                "ligne/colomne/région\n"
                                                                "Il sont colorés en rouge")

        if not invalid_entry and not duplicate_entry:
            self.solve(board)  # no more problem, now it's time to solve the sudoku
            # then color user entry

    def solve(self, board):
        # copy the board before solving
        user_board = [[0 for i in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                user_board[i][j] = board[i][j]

        solver.calc(board)  # return the modified board

        self.display_solution(board, user_board)

    def display_solution(self, solved_board, user_board):
        self.new_board()
        for i in range(9):
            for j in range(9):
                self.board_text_entry[i][j].insert("end", solved_board[i][j], "center")
                if user_board[i][j] != 0:
                    self.board_text_entry[i][j].configure(bg="lightgreen")
                else:
                    self.board_text_entry[i][j].configure(bg="lightblue")
        self.solve_button.configure(state="disabled")

        # check if there is a solution to the sudoku
        no_solution = False
        for i in range(9):
            for j in range(9):
                if solved_board[i][j] == 0:
                    no_solution = True

        if no_solution:
            tkinter.messagebox.showwarning("PAS DE SOLUTION !",
                                           "Il n'y a pas de solution à ce SUDOKU!", icon="warning")


class Grid:
    """ build a grid of 3x3 inside a tkinter frame"""
    def __init__(self, masterframe):
        self.masterframe = masterframe
        self.subframe = [[None for i in range(3)] for i in range(3)]
        self.config()

    def config(self):
        for i in range(3):
            for j in range(3):
                self.masterframe.rowconfigure(i, weight=1)
                self.masterframe.columnconfigure(j, weight=1)

                self.subframe[i][j] = tkinter.Frame(self.masterframe, bd=2,
                                                    relief="raised", bg="grey")
                self.subframe[i][j].grid(row=i, column=j, sticky="news")


def main():
    mainwindow = tkinter.Tk()
    Window(mainwindow)
    mainwindow.mainloop()

if __name__ == "__main__":
    main()
