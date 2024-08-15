from tkinter import Tk, Button, Label, Entry, Listbox, Canvas
from warframeAPI import warframeApi as api
import math
# initialize bot used to interact with API
chrome_path = "/home/shadarien/Downloads/chrome-linux64/chromedriver" 
warframe = api(chrome_path)

appWindow = Tk()
appWindow.title('Warframe Scanner')
appWindow.geometry('600x800')

packageList = []


scanLabel = Label(text = 'Enter Item to Scan')
packageList.append(scanLabel)


scanTypeLabel = Label(text = 'Select type of scan: ')
scanOptions = api.getScanOptions()

scanOptionDropdown = Listbox(
                  height = len(scanOptions), 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow")
for index,value in enumerate(scanOptions):
    scanOptionDropdown.insert(index+1, value)

scanItemEntry = Entry(
    width = 50,
    bg = 'white',
    fg = 'black'
)
packageList.append(scanItemEntry)
packageList.append(scanOptionDropdown)


def grab():
    outputWindow.delete('all')
    scanItem = scanItemEntry.get()
    chosenOption = str(scanItemEntry.selection_get()).lower()
    if chosenOption == 'market':
        scan = warframe.scan_warframe(scanItem)
        extraction =  f"{scanItem}\n\t Orders: {warframe.market_extraction['Lowest Price']}\n\t Highest Price: {warframe.market_extraction['Highest Price']}\n\t Average Price: {math.floor(warframe.market_extraction['Average Price'])}"
    if chosenOption == 'wiki':
        # TODO: Fix output for wiki 
        scan = warframe.how_to_get_item(scanItem)
        extraction=  warframe.acquisition

    
    
    
    outputWindow.create_text(300, 50, text=str(extraction), fill="black", font=('Helvetica 15 bold'))

SubmitButton = Button(
    text = 'Submit',
    width = 20,
    height = 1,
    bg = 'blue',
    fg = 'white',
    command=grab
)
packageList.append(SubmitButton)


outputWindow = Canvas(appWindow, height = 200, width=500,background='white', bd=1)


for item in packageList:
    item.pack()




outputWindow.pack()
appWindow.mainloop()


