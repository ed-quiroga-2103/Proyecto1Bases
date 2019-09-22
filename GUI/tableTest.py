from tkinter import *

class Window:
    def __init__(self):
        self.infoList1 = ["Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre","Nombre"]
        self.infoList2 = ["Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1","Apellido1"]
        self.infoList3 = ["Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2","Apellido2"]
        
        self.master = Tk()

        self.infoBox1 = Listbox(self.master, yscrollcommand=self.yscroll1)
        self.infoBox2 = Listbox(self.master, yscrollcommand=self.yscroll2)
        self.infoBox3 = Listbox(self.master, yscrollcommand=self.yscroll3)

        self.scrollbar = Scrollbar(self.master, orient="vertical")

        self.createInfoWindow()
    
    def insertTuple(self, info1, info2, info3):

        for i in range(len(self.infoList1)):
            info1.insert(END, self.infoList1[i])
            info2.insert(END, self.infoList2[i])
            info3.insert(END, self.infoList3[i])

            if i%2 == 0:
                info1.itemconfig(i, {'bg':'lightblue'})
                info2.itemconfig(i, {'bg':'lightblue'})
                info3.itemconfig(i, {'bg':'lightblue'})


        return

    def scrollAll(self, list1, list2, list3):
        list1.yview()
        list2.yview()
        list3.yview()

    def createInfoWindow(self):
        
        

        self.master.title("Info")
        

        self.insertTuple(self.infoBox1, self.infoBox2, self.infoBox3)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar.config(command=self.yview)

        self.infoBox1.pack(side="left",fill="both", expand=True)
        self.infoBox2.pack(side="left",fill="both", expand=True)
        self.infoBox3.pack(side="left",fill="both", expand=True)

    

        self.master.mainloop()

    def yscroll1(self, *args):
        if self.infoBox2.yview() != self.infoBox1.yview():
            self.infoBox2.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll2(self, *args):
        if self.infoBox3.yview() != self.infoBox2.yview():
            self.infoBox3.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll3(self, *args):
        if self.infoBox1.yview() != self.infoBox3.yview():
            self.infoBox1.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yview(self, *args):
        self.infoBox1.yview(*args)
        self.infoBox2.yview(*args)
        self.infoBox3.yview(*args)
        
window = Window()     

print("Done")