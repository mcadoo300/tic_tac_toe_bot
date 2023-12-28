from tkinter import *
from tkinter import messagebox
from game import *

root = Tk()
root.title('Tic Tac Toe')

game_state = GameState()
game_state.Set_player_turn('x')

a_b = Alpha_Beta(game_state)


human_turn = True
game_over = False



def b_click(b):
    global human_turn, game_grid, game_state, a_b

    if human_turn:
        if game_grid[b[0]][b[1]]["text"] == " ":
            game_grid[b[0]][b[1]]["text"] = "X"
            human_turn = False
            game_state.Place_move(b,'x')
            game_state.Set_player_turn('o')
            a_b.Update_state(game_state)
            bot_move = a_b.Gen_next_move()
            if game_state.Get_game_over() is False:
                b_click(bot_move)
        else:
            messagebox.showerror("Tic Tac Toe", "Invalid move.")
    else:
        if game_grid[b[0]][b[1]]["text"] == " ":
            game_grid[b[0]][b[1]]["text"] = "O"
            human_turn = True
            game_state.Place_move(b,'o')
            game_state.Set_player_turn('x')

# buttons/board pieces
b_0_0 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([0,0]) )
b_0_1 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([0,1]) )
b_0_2 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([0,2]) )

b_1_0 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([1,0]) )
b_1_1 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([1,1]) )
b_1_2 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([1,2]) )

b_2_0 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([2,0]) )
b_2_1 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([2,1]) )
b_2_2 = Button(root, text = " ", font = ("Helvetica", 20), height=3,width=6, bg="SystemButtonFace",command=lambda: b_click([2,2]) )


game_grid = [[b_0_0,b_0_1,b_0_2], [b_1_0,b_1_1,b_1_2] , [b_2_0,b_2_1,b_2_2]]

# Grid
b_0_0.grid(row=0,column=0)
b_0_1.grid(row=0,column=1)
b_0_2.grid(row=0,column=2)

b_1_0.grid(row=1,column=0)
b_1_1.grid(row=1,column=1)
b_1_2.grid(row=1,column=2)

b_2_0.grid(row=2,column=0)
b_2_1.grid(row=2,column=1)
b_2_2.grid(row=2,column=2)

root.mainloop()