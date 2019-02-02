import tkinter as tk
from threading import *


class perpetualTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


window = tk.Tk()
window.resizable(False, False)
window.minsize(1000, 800)
window.title("Biscuit Clicker!")

multiplierList = [1, 10, 100, 1000, 10000, 100000, 1000000]
curMult = 1

inThread = False


def to_log(text, col):
    global inThread
    logLabel["text"] = text
    logLabel["fg"] = col
    if inThread == False:
        inThread = True
        Timer(3.0, lambda: clear_log(text)).start()


def clear_log(text):
    if logLabel["text"] == text:
        logLabel["text"] = ""
    global inThread
    inThread = False


def cycle():
    global curMult
    curMult = multiplierList[(multiplierList.index(curMult) + 1) % len(multiplierList)]


def change_mult():
    cycle()
    multiplierButton["text"] = "Multiplier: " + str(curMult) + "x"


cheats = tk.IntVar()
cheats.set(0)
bpc = 1
bps = 0
biscuits = 0
negativeBiscuits = tk.IntVar()
negativeBiscuits.set(0)

secondly_biscuits = perpetualTimer(1.0, lambda: add_biscuits(bps))


def add_biscuits(count):
    global biscuits
    biscuits += count
    global biscuitCounter
    biscuitCounter["text"] = "You have " + str(biscuits) + " biscuits"


def upgrade_bpc(count, cost):
    global biscuits
    if (biscuits < cost) and (negativeBiscuits.get() == 0):
        to_log("Not Enough Biscuits!", "red")
        return
    to_log("Successfully Upgraded BPC", "green2")
    global bpc
    bpc += count
    biscuits -= cost
    biscuitCounter["text"] = "You have " + str(biscuits) + " biscuits"
    bpcCounter["text"] = "Your BPC is " + str(bpc)


def upgrade_bps(count, cost):
    global biscuits
    if biscuits < cost and negativeBiscuits.get() == 0:
        to_log("Not Enough Biscuits!", "red")
        return
    to_log("Successfully Upgraded BPS", "green2")
    global bps
    bps += count
    biscuits -= cost
    biscuitCounter["text"] = "You have " + str(biscuits) + " biscuits"
    bpsCounter["text"] = "Your BPS is " + str(bps)


def toggle_cheats():
    if cheats.get() == 0:
        allowNegative["state"] = "disabled"
    else:
        allowNegative["state"] = "normal"


biscuitCounter = tk.Label(window, text="You have " + str(biscuits) + " biscuits")
biscuitButton = tk.Button(window, text="Biscuit!", command=lambda: add_biscuits(bpc))
biscuitCounter.config(font=("Courier", 44))
biscuitButton.config(font=("Courier", 30))
bpsCounter = tk.Label(window, text="Your BPS is " + str(bps))
bpcCounter = tk.Label(window, text="Your BPC is " + str(bpc))
upgradeBPCbutton = tk.Button(window, text="""Upgrade your BPC,
                                          Price: 10""",
                             command=lambda: upgrade_bpc(1 * curMult, 10 * curMult))
upgradeBPSbutton = tk.Button(window, text="""Upgrade your BPS,
                                          Price: 10""",
                             command=lambda: upgrade_bps(1 * curMult, 10 * curMult))
multiplierButton = tk.Button(window, text="Multiplier: " + str(curMult) + "x", command=change_mult)
logLabel = tk.Label(window, text="", fg="grey")
cheatLabel = tk.Label(window, text="Cheats:")
cheatOff = tk.Radiobutton(window, text="Off", variable=cheats, value=0, command=toggle_cheats)
cheatOn = tk.Radiobutton(window, text="On", variable=cheats, value=1, command=toggle_cheats)
allowNegative = tk.Checkbutton(window, text="Allow Negative Biscuits", variable=negativeBiscuits, state="disabled")

secondly_biscuits.start()
biscuitCounter.pack()
biscuitButton.pack()
bpcCounter.pack()
bpsCounter.pack()
upgradeBPCbutton.pack()
upgradeBPSbutton.pack()
multiplierButton.pack()
logLabel.pack()
cheatLabel.pack()
cheatOff.pack()
cheatOn.pack()
allowNegative.pack()
window.mainloop()
