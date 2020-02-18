# use a Tkinter label as a panel/frame with a background image
# (note that Tkinter reads only GIF and PGM/PPM images)
 
import TKinter as tk
import random
import numpy as np
from PIL import ImageTk, Image


def initBoard(master, boardData, tiles, tokens):
    canvas = Canvas(master, width=600, height=600, bg='#607f99')
    canvas.wheatTile = ImageTk.PhotoImage(file="wheat.png")
    canvas.woodTile = ImageTk.PhotoImage(file="wood.png")
    canvas.brickTile = ImageTk.PhotoImage( file="brick.png")
    canvas.oreTile = ImageTk.PhotoImage(file="ore.png")
    canvas.woolTile = ImageTk.PhotoImage(file="wool.png")
    canvas.desertTile = ImageTk.PhotoImage( file="desert.png")
    # Each hex has 6 vertices of which settlements can go on
    # settlements can be upgraded to cities
    # Each hex has 6 edges of which roads can go on
    # roads and cities remain until the game is over
    # you may only build a settlement on an unoccupied intersection and only if none of the 3 adjacent intersections contains a settlement or city
    # you may only build settlements on your roads

    # begin turn by rolling dice
    # each player who has settlement on vertices of the hex that has the number which is the sum of the dice rolls will recieve 1 resource card of the hex type
    # 2 resource cards if you have a city on the verticies

    # vert -> road -> vert ->road -> vert -> road where each vert stores data for who's occupied it, is it a city?, adjacent hex number, adjacent hex resources
    # OR
    # we treat the hex as a cube, each vertex will hold a 3d vec position 
    # when player wants to add a settlement, they will click a button on the vertex, the button will return a unique value corresponding to the vertex, we call the function that
    #    will traverse the board data to update that vertex

    # 1 = wheat
    # 2 = wood
    # 3 = brick
    # 4 = ore
    # 5 = wool
    # 6 = desert
    tileWidth = canvas.wheatTile.width()
    tileHeight = canvas.wheatTile.height()
    indexOffset = 0
    yBoard = 40
    xBoard = 140
    maxID = 0
    for i in range(len(tiles)):
        if i < 3:
            j = 0
            vertOffset = 0
            horOffset = 0
        elif i < 7:
            j = 3
            vertOffset = 1
            horOffset = 1
        elif i < 12:
            j = 7
            vertOffset = 2
            horOffset = 2
        elif i < 16:
            j = 12
            vertOffset = 3
            horOffset = 1
        elif i < 19:
            j = 16
            vertOffset = 4
            horOffset = 0
        if tiles[i] == 1:
            canvas.create_image(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth, yBoard + vertOffset*3*(tileHeight/4), image = canvas.wheatTile, anchor = NW)
        elif tiles[i] == 2:
            canvas.create_image(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth, yBoard + vertOffset*3*(tileHeight/4), image = canvas.woodTile, anchor = NW)
        elif tiles[i] == 3:
            canvas.create_image(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth, yBoard + vertOffset*3*(tileHeight/4), image = canvas.brickTile, anchor = NW)
        elif tiles[i] == 4:
            canvas.create_image(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth, yBoard + vertOffset*3*(tileHeight/4), image = canvas.oreTile, anchor = NW)
        elif tiles[i] == 5:
            canvas.create_image(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth, yBoard + vertOffset*3*(tileHeight/4), image = canvas.woolTile, anchor = NW)
        else:
            canvas.create_image(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth, yBoard + vertOffset*3*(tileHeight/4), image = canvas.desertTile, anchor = NW)
            indexOffset = 1
        if i < 12:
            tileX = 0 + (i - j) - horOffset
            tileY = 2 - (i - j)
            tileZ = -2 + vertOffset
        else:
            tileX = 0 + (i - j) - 2
            tileY = - (i - j) + horOffset
            tileZ = -2 + vertOffset 
        order = [(0,1,0), (1,1,0), (1,0,0), (1,0,1), (0,0,1), (0,1,1)]
        
        for (x, y, z) in order:  
            if ((x +y+z) != 0 and (x +y+z) != 3):
                if boardData[tileX + x][tileY + y][tileZ + z] > maxID:
                    print(maxID)
                    maxID = boardData[tileX + x][tileY + y][tileZ + z]
                    button = Button(text=str(boardData[tileX + x][tileY + y][tileZ + z]), command = lambda buttonID=boardData[tileX + x][tileY + y][tileZ + z]: callback(buttonID))
                    if ((x,y,z) == (0,1,0)): #1
                        xPos = -2
                        yPos = 0
                    elif ((x,y,z) == (1,1,0)): #2
                        xPos = 1
                        yPos = -2
                    elif ((x,y,z) == (1,0,0)): #3
                        xPos = 4
                        yPos = 0
                    elif ((x,y,z) == (1,0,1)): #4
                        xPos = 4.25
                        yPos = 4
                    elif ((x,y,z) == (0,0,1)): #5
                        xPos = 1
                        yPos = 5.5
                    elif ((x,y,z) == (0,1,1)): #6
                        xPos = -2
                        yPos = 4
                    canvas.create_window(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth + xPos*15 + 25 , yBoard + vertOffset*3*(tileHeight/4) + yPos*15 + 23, anchor=NW, height = 15, width = 15, window=button)
        #print(str(boardData[tileX + x][tileY + y][tileZ + z])+ ", " + str(tileX + x) + ", " + str(tileY + y) + ", " + str(tileZ + z) )
        if tiles[i] != 6:
            canvas.create_text(xBoard - horOffset*(tileWidth/2) + (i - j)*tileWidth - 1 + (tileWidth/2), yBoard + vertOffset*3*(tileHeight/4) + 8 + 3*(tileHeight/4), fill="black",font="Times 10 bold", text=str(tokens[i-indexOffset]))
    return canvas
class GameInit():
    def __init__(self):
        self.tiles = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6]
        self.tokens = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        random.shuffle(self.tiles)
        random.shuffle(self.tokens)

        self.boardData = np.zeros((6, 6,6), dtype=int)

        indexOffset = 0
        vertID = 0
        for i in range(len(self.tiles)):
            if i < 3:
                j = 0
                vertOffset = 0
                horOffset = 0
            elif i < 7:
                j = 3
                vertOffset = 1
                horOffset = 1
            elif i < 12:
                j = 7
                vertOffset = 2
                horOffset = 2
            elif i < 16:
                j = 12
                vertOffset = 3
                horOffset = 1
            elif i < 19:
                j = 16
                vertOffset = 4
                horOffset = 0
            if self.tiles[i] == 6:
                indexOffset = 1
            if i < 12:
                tileX = 0 + (i - j) - horOffset
                tileY = 2 - (i - j)
                tileZ = -2 + vertOffset
            else:
                tileX = 0 + (i - j) - 2
                tileY = - (i - j) + horOffset
                tileZ = -2 + vertOffset 
            # set the front vertex of the "cube" to be the token value, and the back vertex to be the resource value
            self.boardData[tileX][tileY][tileZ] = self.tiles[i]
            self.boardData[tileX + 1][tileY + 1][tileZ + 1] = self.tokens[i-indexOffset]
            # set the values around the cube to be values that settlements can be placed on
            order = [(0,1,0), (1,1,0), (1,0,0), (1,0,1), (0,0,1), (0,1,1)]
            for (x, y, z) in order:  
                if self.boardData[tileX + x][tileY + y][tileZ + z] == 0:
                    vertID += 1
                    self.boardData[tileX + x][tileY + y][tileZ + z] = vertID



def callback(number):
    print (str(number))

class CatanApp(Frame):
    def __init__(self):
        super().__init__()
        self.board = GameInit()
        self.initUI()

    def initUI(self):
        self.configure(background='#edebd4')
        self.master.title("Windows")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        # create the canvas, size in pixels
        board = initBoard(self, self.board.boardData, self.board.tiles, self.board.tokens)
        board.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
        # pack the canvas into a frame/form
       # canvas.pack(expand=YES, fill=BOTH)
       # area = Text(self)
        logo = ImageTk.PhotoImage(file="CATAN_logo.png")
        logoLabel = Label(self, bg='#edebd4', image=logo)
        logoLabel.photo = logo
        logoLabel.grid(row=1, column=3, columnspan=2, stick=N)

        player="Player 1"
        cbtn = Label(self, bg='#edebd4', font = 'Times 20', text=player+"'s Turn")
        cbtn.grid(row=2, column=3, pady=30, stick=W)

        hbtn = Button(self,  font = 'Times 20', text="Roll Dice")
        hbtn.grid(row=2, column=4, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=3, column=3)

def main():
   
    root = tk.Tk()
    root.wm_attributes('-transparentcolor','white')
    app = CatanApp()
    root.mainloop()


if __name__ == '__main__':
    main()
 









