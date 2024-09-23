#Trevor Eby 9/13/24 Programming Languages(304) Assignment 2
#uses an external library(rectpack) to solve a bin packing problem with different sized rectangles
#also uses tkinter to visualize the bin packing
import sys
import tkinter
from tkinter import Canvas
from rectpack import newPacker
from typing import List, Tuple

#used to create new canvas objects
class CustomCanvas:
    #constructor
    #each canvas will have a height and a width when created.
    def __init__(self, height: int, width: int, root):
        self.canvas = Canvas(root, height=height, width=width)
        self.height = height
        self.width = width

#used to create new rectangle objects
class Rectangle:
    #each rectangle will have a height, width, x, and y when created.
    def __init__(self, height: int, width: int, x: int =0, y: int =0):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.area = height * width

#finds and returns the area of a rectangle
def rectangleArea(rect):
    return rect.height * rect.width

#sorts the rectanlges by area
def sortArea(rectangles):
    return sorted(rectangles, key=rectangleArea, reverse=True)

#uses the rectPack external library to create bins and do the packing.
def pack(allRect: List[Rectangle], canvasSize: Tuple[int, int]) -> List[Rectangle]:
    
    #gets the height and the width of the canvas/bin
    canvasHeight, canvasWidth = canvasSize
    #this list will hold all the new packed rectangles
    packedRectangles = []
    #create a new packer called packer
    packer = newPacker()
    #create a new list of the sorted rectangles, biggest to smallest
    sortedRectangles = sortArea(allRect)
    #add the list of sorted rectangles to the packing queue
    for rect in sortedRectangles:
        packer.add_rect(rect.width, rect.height)
    #add a bin with the canvas size
    packer.add_bin(canvasWidth, canvasHeight)
    #pack the rectangles into the bin
    packer.pack()
    #for x in allRect:
        #print(x)
    #print(packer.rect_list())

    #create and add new rectangles to the packedRectangles list from the data of the packed bin.
    for bin in packer:
        for r in bin:
            packedRectangles.append(Rectangle(height=r.height, width=r.width, x=r.x, y=r.y))
    #return the list of rectangles so that it can be used to add rectangle shapes to the canvas with correct sizes and positions.
    return packedRectangles
    
def main():
    #get the file from the command line.
    inputFile = sys.argv[1]
    #open the file and read all the lines.
    f= open(inputFile, "r")
    lines = f.readlines()
    #get the first line and split it into 2 values, the first being the height and the second the width
    firstLine = lines[0].strip()
    canvasHeight, canvasWidth = [int(x) for x in firstLine.split(',')]

    #creates a new list for all the rectangles from the input file
    rectangles = []
    #starting at line 1, read each line and create a new rectangle with each lines data, then add it to the rectangles list.
    for line in lines[1:]:
        RecHeight, RecWidth = map(int, line.strip().split(','))
        rectangles.append(Rectangle(height=RecHeight, width=RecWidth))
    
    #create a list of the packed rectangles and all their data
    packedRectangles = pack(rectangles, (canvasWidth, canvasHeight))

    #used for testing
    #print("Packed Rectangles:")
    #for rect in packedRectangles:
        #print(rect)

    #create the window for the canvas
    root = tkinter.Tk()
    #title the canvas
    root.title('Assignment 2')
    #give the canvas a height and width
    cCanvas = CustomCanvas(height=canvasHeight, width=canvasWidth, root=root)
    #makes the canvas visible and adjusts its size
    cCanvas.canvas.pack()

    #creates new rectangles in the canvas with the each packed rectangles data.
    #count and the text were used for testing and ease of counting how many squares were correctly displayed.
    #count=1
    for rect in packedRectangles:
        cCanvas.canvas.create_rectangle(rect.x, rect.y, rect.x + rect.width, rect.y + rect.height, outline="black", fill="blue")
        #cCanvas.canvas.create_text(rect.x + 10, rect.y+10, text=count, fill="white", font='tkDefaeltFont 10')
        #count = count+1
    #keeps the window and canvas visible
    root.mainloop()

#makes sure main is only called when the code is executed and not also called when it's imported.
if __name__ == "__main__":
    main()    