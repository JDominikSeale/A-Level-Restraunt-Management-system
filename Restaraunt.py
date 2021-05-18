import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import *
import RegEx
import Email_Sender


def Run():
    Root = Tk()
    Main(Root)
    Root.mainloop()


class Main():
    def __init__(self, window):
        self.window = window
        self.window.geometry('300x200')
        self.window.resizable(width=False, height=False)
        self.window.title('Restaraunt Booking System')

        Label(self.window, text='George & Dragon', font=("Comic sans MS", "24", "bold")).pack()
        Button(self.window, text='Inventory Manager', width=20, command=self.InventoryManagerWindow).pack()
        Button(self.window, text='Cash Register', width=20, command=self.CashRegisterWindow).pack()
        Button(self.window, text='Client Manager', width=20, command=self.ClientManagerWindow).pack()
        Button(self.window, text='Quit', width=22, command=self.Quit).pack(side=BOTTOM)

    def InventoryManagerWindow(self):
        Root = Toplevel(self.window)
        InventoryManagerWindow(Root)

    def CashRegisterWindow(self):
        Root = Toplevel(self.window)
        CashRegisterWindow(Root)

    def ClientManagerWindow(self):
        Root = Toplevel(self.window)
        ClientManagerWindow(Root)

    def Quit(self):
        self.window.destroy()


class InventoryManagerWindow():

    def __init__(self, window):

        self.window = window
        self.window.geometry('600x500')
        self.window.title('Inventory Manager')

        def ClearItemName(event):
            if self.ItemNameEntry.get() == 'Name':
                self.ItemNameEntry.delete(0, END)

        def ClearItemStock(event):
            if self.ItemStockEntry.get() == 'Stock':
                self.ItemStockEntry.delete(0, END)

        def ClearInvID(event):
            if self.InventoryIDEntry.get() == 'ID':
                self.InventoryIDEntry.delete(0, END)

        self.InventorySearchBarVar = StringVar()
        self.InventorySearchBar = Entry(self.window, textvariable=self.InventorySearchBarVar)
        self.InventorySearchBar.grid(column=0, row=0)

        self.InventoryShow = ttk.Treeview(self.window)
        self.InventoryShow["columns"] = ("One", "Two",)
        self.InventoryShow.heading("#0", text="ProductID")
        self.InventoryShow.heading("#1", text="Product")
        self.InventoryShow.heading("#2", text="Stock")
        self.InventoryShow.grid(column=0, row=4)

        Cursor.execute("SELECT * FROM Inventory")
        AllInventory = Cursor.fetchall()
        for row in AllInventory:
            self.InventoryShow.insert("", END, text=row[0], values=row[1:])

        EditButton = Button(self.window, text='Select', command=self.InvItemSelect)
        EditButton.grid(column=0, row=5)

        self.ItemIDVar = IntVar()
        self.InventoryIDEntry = Entry(self.window, textvariable=self.ItemIDVar)
        self.ItemIDVar.set('ID')
        self.InventoryIDEntry.bind('<Button-1>', ClearInvID)
        self.InventoryIDEntry.grid(column=0, row=6)

        self.ItemNameVar = StringVar()
        self.ItemNameEntry = Entry(self.window, textvariable=self.ItemNameVar)
        self.ItemNameVar.set('Name')
        self.ItemNameEntry.bind('<Button-1>', ClearItemName)
        self.ItemNameEntry.grid(column=0, row=7)

        self.ItemStockVar = IntVar()
        self.ItemStockEntry = Entry(self.window, textvariable=self.ItemStockVar)
        self.ItemStockVar.set('Stock')
        self.ItemStockEntry.bind('<Button-1>', ClearItemStock)
        self.ItemStockEntry.grid(column=0, row=8)

        self.MenuEdit = Button(self.window, text='Menu Edit', command=self.MenuEditFunc)
        self.MenuEdit.grid(column=0, row=10)

        ItemInvUpdateButton = Button(self.window, text='UPDATE', command=self.InvItemUpdate)
        ItemInvUpdateButton.grid(column=0, row=9)

        self.InventoryAddButton = Button(self.window, text='ADD', command=self.InvAddFunc)
        self.InventoryAddButton.grid()

        self.InventroyDelButton = Button(self.window, text='DELETE', command=self.InvDelFunc)
        self.InventroyDelButton.grid()

    def InvDelFunc(self):
        ID = self.InventoryIDEntry.get()
        Cursor.execute('DELETE FROM Inventory WHERE ProductID = %s' % (ID))
        Connection.commit()

    def InvAddFunc(self):
        Name = self.ItemNameEntry.get()
        Stock = float(self.ItemStockEntry.get())
        if Stock > 0:
            Cursor.execute('SELECT MAX(ProductID) FROM Inventory')
            maxID = Cursor.fetchall()
            print(maxID)
            print(maxID[0][0])
            if maxID[0][0] == None:
                ID = 1
            else:
                ID = int(maxID[0][0]) + 1
            print(ID)
            print(type(ID))
            Cursor.execute('INSERT INTO Inventory VALUES(%s, "%s", %s)' % (ID, Name, Stock))
            Connection.commit()
        else:
            print('Not able insert into DB')

    def MenuEditFunc(self):
        Root = Toplevel(self.window)
        MenuEditWindow(Root)

    def InvItemSelect(self):
        try:
            Item = list(self.InventoryShow.item(self.InventoryShow.focus()).values())
            self.ItemIDVar.set(Item[0])
            self.ItemNameVar.set(Item[2][0])
            self.ItemStockVar.set(Item[2][1])
            print(Item[0], Item[2][0], Item[2][1], '         Selected Items')
        except:
            Item = self.InventorySearchBar.get()
            A = Cursor.execute('SELECT * FROM Inventory WHERE Product = "%s"' % (Item))
            A = A.fetchall()
            self.ItemNameVar.set(A[0][1])
            self.ItemStockVar.set(A[0][2])
            self.InventorySearchBar.delete(0, END)

    def InvItemUpdate(self):
        ItemID = list(self.InventoryShow.item(self.InventoryShow.focus()).values())[0]
        ItemName = self.ItemNameEntry.get()
        ItemStock = self.ItemStockEntry.get()
        Cursor.execute(
            'UPDATE Inventory SET Product = "%s", Stock = "%s" WHERE ProductID = "%s"' % (ItemName, ItemStock, ItemID))
        Connection.commit()


class MenuEditWindow():
    def __init__(self, window):
        self.window = window
        self.window.geometry('1000x600')
        self.window.title('Menu Edit')

        def ClearItemName(event):
            if self.MenuNameEntry.get() == 'Item Name':
                self.MenuNameEntry.delete(0, END)

        def ClearItemPrice(event):
            if self.MenuPriceEntry.get() == 'Price':
                self.MenuPriceEntry.delete(0, END)

        def ClearProductID(event):
            if self.productIDEntry.get() == 'Product IDs':
                self.productIDEntry.delete(0, END)

        def ClearStockTake(event):
            if self.stockTakeEntry.get() == 'Stock Take':
                self.stockTakeEntry.delete(0, END)

        def TreeView():
            Cursor.execute('SELECT * FROM Meals')
            mAll = Cursor.fetchall()
            self.MenuShow = ttk.Treeview(self.window)
            self.MenuShow["columns"] = ("One", 'Two', 'Three')
            self.MenuShow.heading("#0", text="Meal", anchor=tk.W)
            self.MenuShow.heading("One", text="Price", anchor=tk.W)
            self.MenuShow.heading('Two', text='Product ID', anchor=tk.W)
            self.MenuShow.heading('Three', text='Stock Take', anchor=tk.W)
            for row in mAll:
                self.MenuShow.insert("", END, text=row[0], values=row[1:])
            self.MenuShow.grid()

        TreeView()

        self.MenuNameVar = StringVar()
        self.MenuNameEntry = Entry(self.window, textvariable=self.MenuNameVar)
        self.MenuNameVar.set('Item Name')
        self.MenuNameEntry.bind('<Button-1>', ClearItemName)
        self.MenuNameEntry.grid()

        self.MenuPriceVar = IntVar()
        self.MenuPriceEntry = Entry(self.window, textvariable=self.MenuPriceVar)
        self.MenuPriceVar.set('Price')
        self.MenuPriceEntry.bind('<Button-1>', ClearItemPrice)
        self.MenuPriceEntry.grid()

        self.productIDVar = StringVar()
        self.productIDEntry = Entry(self.window, textvariable=self.productIDVar)
        self.productIDVar.set('Product IDs')
        self.productIDEntry.bind('<Button-1>', ClearProductID)
        self.productIDEntry.grid()

        self.stockTakeVar = StringVar()
        self.stockTakeEntry = Entry(self.window, textvariable=self.stockTakeVar)
        self.stockTakeVar.set('Stock Take')
        self.stockTakeEntry.bind('<Button-1>', ClearStockTake)
        self.stockTakeEntry.grid()

        menuSelect = Button(self.window, text='Select', command=self.menuSelectFunc)
        menuSelect.grid()

        menuAdd = Button(self.window, text='Add', command=self.addItemFunc)
        menuAdd.grid()

        deleteButton = Button(self.window, text='Delete', command=self.deleteItemFunc)
        deleteButton.grid()

    def addItemFunc(self):
        def listMake(String):
            checkAgainst = [',', ' ', '[', ']', '(', ')']
            output = []
            second = list(String)
            if len(second) > 1:
                second.append(',')
                for i in range(len(String)):
                    value = []
                    for k in range(len(second)):
                        if second[0].isnumeric() == True or second[0] == '.':
                            value.append(second[0])
                            second.pop(0)
                        else:
                            second.pop(0)
                            break
                    blank = ''
                    spaceCount = output.count(blank)
                    if blank in output:
                        for i in range(spaceCount):
                            output.pop(output.index(blank))
                    numValue = "".join(value)
                    output.append(numValue)
                output.pop(-1)
                trueOutput = []
                for i in output:
                    trueOutput.append(float(i))
            else:
                print(second)
                trueOutput = [float(second[0])]
            return trueOutput

        def listMakeProduct(String):
            checkAgainst = [',', ' ', '[', ']', '(', ')']
            output = []
            second = list(String)
            if len(second) > 1:
                second.append(',')
                for i in range(len(String)):
                    value = []
                    for k in range(len(second)):
                        if second[0].isnumeric() == True or second[0] == '.':
                            value.append(second[0])
                            second.pop(0)
                        else:
                            second.pop(0)
                            break
                    blank = ''
                    spaceCount = output.count(blank)
                    if blank in output:
                        for i in range(spaceCount):
                            output.pop(output.index(blank))
                    numValue = "".join(value)
                    output.append(numValue)
                output.pop(-1)
                trueOutput = []
                for i in output:
                    trueOutput.append(int(i))
            else:
                print(second)
                trueOutput = [int(second[0])]
            return trueOutput

        Name = self.MenuNameEntry.get()
        Price = self.MenuPriceEntry.get()
        productID = listMakeProduct(self.productIDEntry.get())
        stockTake = listMake(self.stockTakeEntry.get())

        Cursor.execute('SELECT MAX(MealID) FROM Meals')
        menuID = Cursor.fetchall()
        menuID = menuID[0][0]
        if menuID == None:
            menuID = 1
        else:
            menuID += 1

        Cursor.execute(
            'INSERT INTO Meals VALUES("%s", "%s", "%s", "%s", "%s")' % (Name, Price, productID, stockTake, menuID))
        Connection.commit()

    def deleteItemFunc(self):
        self.Item = list(self.MenuShow.item(self.MenuShow.focus()).values())
        itemName = self.Item[0]
        itemPrice = self.Item[2][0]
        productIDs = self.Item[2][1]
        stockTakes = self.Item[2][2]
        Cursor.execute(
            'DELETE FROM Meals WHERE Meal = "%s" AND Price = %s AND ProductID = "%s" AND StockTake = "%s"' % (
                itemName, itemPrice, productIDs, stockTakes))
        Connection.commit()

    def menuSelectFunc(self):
        self.Item = list(self.MenuShow.item(self.MenuShow.focus()).values())
        self.itemName = self.Item[0]
        self.itemPrice = self.Item[2][0]
        self.productIDs = self.Item[2][1]
        self.stockTakes = self.Item[2][2]

        ##################################


class CashRegisterWindow():
    def __init__(self, window):
        self.window = window
        self.window.geometry('900x500')
        self.window.title('Cash Register')

        Label(self.window, text='Menu').grid(column=0, row=0)
        Label(self.window, text='Customer Order').grid(column=1, row=0)

        self.MenuListing = ttk.Treeview(self.window)
        self.MenuListing["columns"] = ("One")
        self.MenuListing.heading("#0", text="Item", anchor=tk.W)
        self.MenuListing.heading("One", text="Price", anchor=tk.W)
        self.MenuListing.grid(column=0, row=1)

        Cursor.execute('SELECT * FROM Meals')
        self.AllMenu = Cursor.fetchall()
        for row in self.AllMenu:
            self.MenuListing.insert("", END, text=row[0], values=row[1:])

        self.CustomerOrderListing = ttk.Treeview(self.window)
        self.CustomerOrderListing["columns"] = ("One")
        self.CustomerOrderListing.heading("#0", text="Item", anchor=tk.W)
        self.CustomerOrderListing.heading("One", text="Price", anchor=tk.W)
        self.CustomerOrderListing.grid(column=1, row=1)

        self.CustomerItems = []
        self.customerItemsList = []
        AddItem = Button(self.window, text='Add Item', command=self.AddItem)
        AddItem.grid(column=0, row=3)

        RemoveItem = Button(self.window, text='Remove Item', command=self.RemoveItem)
        RemoveItem.grid(column=0, row=4)

        self.FinalPriceSum = DoubleVar()
        self.FinalPriceSum.set(0.0)
        FinalPrice = Label(self.window, text='£%s' % self.FinalPriceSum.get())
        FinalPrice.grid(column=0, row=5)

        def ClearCustomerIDEntry(event):
            self.CustomerIDSetEntry.delete(0, END)

        self.CustomerIDSetVar = IntVar()
        self.CustomerIDSetEntry = Entry(self.window, textvariable=self.CustomerIDSetVar)
        self.CustomerIDSetVar.set('Customer ID')
        self.CustomerIDSetEntry.bind('<Button-1>', ClearCustomerIDEntry)
        self.CustomerIDSetEntry.grid(column=1, row=4)

        CustomerIDSearch = Button(self.window, text='Search Customr')
        CustomerIDSearch.grid(column=1, row=3)

        SaveButton = Button(self.window, text='Save', command=self.SaveFunc)
        SaveButton.grid(column=1, row=6)

        MakeSale = Button(self.window, text='Make Sale', command=self.MakeSaleButton)
        MakeSale.grid(column=1, row=5)

        self.NonClientCheckVar = IntVar()
        NonClientCheck = Checkbutton(self.window, text="Non Client", variable=self.NonClientCheckVar)
        NonClientCheck.grid(column=2, row=4)

    def SaveFunc(self):
        CheckBox = self.NonClientCheckVar.get()
        if CheckBox == 1:
            Cursor.execute('UPDATE Receipt SET Request = "%s" WHERE CustomerID = %s' % (self.CustomerItems, CheckBox))
            Connection.commit()
        else:
            print('Unable to save due to Customer not existing')

    def MakeSaleButton(self):
        def listMake(String):
            checkAgainst = [',', ' ', '[', ']', '(', ')']
            output = []
            second = list(String)
            if len(second) > 1:
                second.append(',')
                for i in range(len(String)):
                    value = []
                    for k in range(len(second)):
                        if second[0].isnumeric() == True or second[0] == '.':
                            value.append(second[0])
                            second.pop(0)
                        else:
                            second.pop(0)
                            break
                    blank = ''
                    spaceCount = output.count(blank)
                    if blank in output:
                        for i in range(spaceCount):
                            output.pop(output.index(blank))
                    numValue = "".join(value)
                    output.append(numValue)
                output.pop(-1)
                trueOutput = []
                for i in output:
                    trueOutput.append(int(i))
            else:
                print(second)
                trueOutput = [int(second[0])]
            return trueOutput

        def listMakeStock(String):
            checkAgainst = [',', ' ', '[', ']', '(', ')']
            output = []
            second = list(String)
            if len(second) > 1:
                second.append(',')
                for i in range(len(String)):
                    value = []
                    for k in range(len(second)):
                        if second[0].isnumeric() == True or second[0] == '.':
                            value.append(second[0])
                            second.pop(0)
                        else:
                            second.pop(0)
                            break
                    blank = ''
                    spaceCount = output.count(blank)
                    if blank in output:
                        for i in range(spaceCount):
                            output.pop(output.index(blank))
                    numValue = "".join(value)
                    output.append(numValue)
                output.pop(-1)
                trueOutput = []
                for i in output:
                    trueOutput.append(float(i))
            else:
                print(second)
                trueOutput = [float(second[0])]
            return trueOutput

        def databaseProcess(customerItems):
            output = []
            for i in range(0, Len):
                productID = listMake(customerItems[i][2])
                stockTake = listMakeStock(customerItems[i][3])
                for k in range(0, len(productID)):
                    name = customerItems[i][k]
                    Cursor.execute('SELECT Stock FROM Inventory WHERE productID = "%s"' % (productID[k]))
                    stock = Cursor.fetchall()[0][0]
                    stock -= stockTake[k]
                    Cursor.execute('UPDATE Inventory SET Stock = "%s" WHERE ProductID = "%s"' % (stock, productID[k]))
                    Connection.commit()
                    output.append(name)
            return output

        CheckBox = self.NonClientCheckVar.get()
        customerItems = self.customerItemsList
        print(customerItems)
        Len = len(customerItems)

        if CheckBox == 0:
            Cursor.execute('SELECT MAX(ReceiptNumber) FROM Receipt')
            ReceiptNumber = Cursor.fetchall()
            ReceiptNumber = ReceiptNumber[0][0]

            try:
                ReceiptNumber += 1
            except:
                ReceiptNumber = 1
            CustomerList = databaseProcess(customerItems)
            finalPrice = self.FinalPriceSum.get()
            customerID = self.CustomerIDSetEntry.get()
            Cursor.execute('SELECT Email FROM Customer WHERE CustomerID = "%s"' % customerID)
            customerEmail = Cursor.fetchall()[0][0]
            Email_Sender.emailSend(customerEmail, customerItems, finalPrice, ReceiptNumber)
        else:
            databaseProcess(customerItems)

    def AddItem(self):
        MenuItemInfo = self.MenuListing.focus()
        MenuItemInfo = self.MenuListing.item(MenuItemInfo)
        MenuItemInfo = MenuItemInfo.values()
        MenuItemInfo = list(MenuItemInfo)
        MenuItem = MenuItemInfo[0]
        MenuItemPrice = float(MenuItemInfo[2][0])
        menuItemProductID = MenuItemInfo[2][1]
        menuItemStockTake = MenuItemInfo[2][2]
        menuItemID = MenuItemInfo[2][3]
        print(MenuItemPrice)

        currentPrice = self.FinalPriceSum.get()
        newPrice = currentPrice + MenuItemPrice
        print(newPrice)
        self.FinalPriceSum.set(newPrice)

        self.CustomerOrderListing.insert("", END, text=MenuItem, values=MenuItemPrice)

        self.CustomerItems.append(MenuItem)
        self.customerItemsList.append([MenuItem, MenuItemPrice, menuItemProductID, menuItemStockTake, menuItemID])

        FinalPriceAdd = Label(self.window, text='£%s' % self.FinalPriceSum.get())
        FinalPriceAdd.grid(column=0, row=5)

    def RemoveItem(self):
        FocusedItem = self.CustomerOrderListing.focus()

        CustomerItemInfo = self.CustomerOrderListing.item(FocusedItem)
        CustomerItemInfo = CustomerItemInfo.values()
        CustomerItemInfo = list(CustomerItemInfo)
        CustomerItemPrice = float(CustomerItemInfo[2][0])
        FinalPrice = self.FinalPriceSum.get()
        self.FinalPriceSum.set(FinalPrice - CustomerItemPrice)
        print(self.FinalPriceSum.get(), 'AFTER REMOVED ITEM')
        CustomerItem = CustomerItemInfo[0]

        self.CustomerOrderListing.delete(FocusedItem)

        self.CustomerItems.remove(CustomerItem)

        FinalPriceRemove = Label(self.window, text='£%s' % self.FinalPriceSum.get())
        FinalPriceRemove.grid(column=0, row=5)


class ClientManagerWindow():
    def __init__(self, window):
        self.window = window
        self.window.geometry('300x400')
        self.window.title('Client Manager')

        def ClearFirstName(event):
            if self.FirstNameEntry.get() == 'First Name':
                self.FirstNameEntry.delete(0, END)

        def ClearLastName(event):
            if self.LastNameEntry.get() == 'Last Name':
                self.LastNameEntry.delete(0, END)

        def ClearPhoneNo(event):
            if self.PhoneNoEntry.get() == 'Phone No':
                self.PhoneNoEntry.delete(0, END)

        def ClearEmail(event):
            if self.EmailEntry.get() == 'Email':
                self.EmailEntry.delete(0, END)

        def ClearCustomerSearch(event):
            if self.CustomerSearchEntry.get() == 'Customer Search':
                self.CustomerSearchEntry.delete(0, END)

        self.FirstNameVar = StringVar()
        self.FirstNameEntry = Entry(self.window, textvariable=self.FirstNameVar)
        self.FirstNameVar.set('First Name')
        self.FirstNameEntry.bind('<Button-1>', ClearFirstName)
        self.FirstNameEntry.grid(column=0, row=0)

        self.LastNameVar = StringVar()
        self.LastNameEntry = Entry(self.window, textvariable=self.LastNameVar)
        self.LastNameVar.set('Last Name')
        self.LastNameEntry.bind('<Button-1>', ClearLastName)
        self.LastNameEntry.grid(column=0, row=1)

        self.PhoneNoVar = StringVar()
        self.PhoneNoEntry = Entry(self.window, textvariable=self.PhoneNoVar)
        self.PhoneNoVar.set('Phone No')
        self.PhoneNoEntry.bind('<Button-1>', ClearPhoneNo)
        self.PhoneNoEntry.grid(column=0, row=2)

        self.EmailVar = StringVar()
        self.EmailEntry = Entry(self.window, textvariable=self.EmailVar)
        self.EmailVar.set('Email')
        self.EmailEntry.bind('<Button-1>', ClearEmail)
        self.EmailEntry.grid(column=0, row=3)

        self.CustomerSearchVar = IntVar()
        self.CustomerSearchEntry = Entry(self.window, textvariable=self.CustomerSearchVar)
        self.CustomerSearchVar.set('Customer Search')
        self.CustomerSearchEntry.bind('<Button-1>', ClearCustomerSearch)
        self.CustomerSearchEntry.grid(column=0, row=4)

        CustomerInput = Button(self.window, text='Customer Input', command=self.ClientInput)
        CustomerInput.grid(column=0, row=5)

        CustomerEdit = Button(self.window, text='Customer Search', command=self.ClientEdit)
        CustomerEdit.grid(column=1, row=5)

        CustomerShow = Button(self.window, text='Show Customers', command=self.CustomerShow)
        CustomerShow.grid(column=2, row=5)

        BookMake = Button(self.window, text='Book Make', command=self.BookMakeFunc)
        BookMake.grid(column=0, row=6)

    def BookMakeFunc(self):
        Root = Toplevel(self.window)
        BookMakingWindow(Root)

    def CustomerShow(self):
        Root = Toplevel(self.window)
        CustomerShowWindow(Root)

    def ClientInput(self):
        Cursor.execute('SELECT MAX(CustomerID) FROM Customer')
        CustomerID = Cursor.fetchall()
        CustomerID = CustomerID[0][0]
        AlreadyCustomer = False

        try:
            CustomerID += 1
        except:
            CustomerID = 1

        SearchedCustomerID = self.CustomerSearchEntry.get()
        try:
            SearchedCustomerID = int(SearchedCustomerID)
        except:
            pass

        if isinstance(SearchedCustomerID, int):
            CustomerID = SearchedCustomerID
            AlreadyCustomer = True

        FirstName = self.FirstNameEntry.get()
        LastName = self.LastNameEntry.get()
        PhoneNo = self.PhoneNoEntry.get()
        Email = self.EmailEntry.get()
        if RegEx.regEmail(Email) != 'None' and RegEx.regEmail(PhoneNo) != None:

            if AlreadyCustomer == False:
                Cursor.execute('INSERT INTO Customer VALUES(%s, "%s", "%s", "%s", "%s")' % (CustomerID, FirstName, LastName, PhoneNo, Email))
            else:
                    Cursor.execute('UPDATE Customer SET FirstName = "%s", LastName = "%s", PhoneNo = "%s", Email = "%s" WHERE CustomerID = %s' % (FirstName, LastName, PhoneNo, Email, CustomerID))

            Connection.commit()

    def ClientEdit(self):
        try:
            CustomerID = self.CustomerSearchEntry.get()

            Cursor.execute('SELECT * FROM Customer WHERE CustomerID = %s' % (CustomerID))
            CustomerInfo = Cursor.fetchall()
            CustomerInfo = CustomerInfo[0]

            FirstName = CustomerInfo[1]
            LastName = CustomerInfo[2]
            PhoneNo = CustomerInfo[3]
            Email = CustomerInfo[4]

            self.FirstNameVar.set(FirstName)
            self.LastNameVar.set(LastName)
            self.PhoneNoVar.set(PhoneNo)
            self.EmailVar.set(Email)
        except:
            print('Error Messege')


class BookMakingWindow():
    def __init__(self, window):
        self.window = window
        self.window.geometry('600x400')
        self.window.title('Booking Maker')

        def ClearCustomerID(event):
            if self.CustomerIDEntry.get() == 'Customer ID':
                self.CustomerIDEntry.delete(0, END)

        def ClearPartySize(event):
            if self.PartySizeEntry.get() == 'Party Size':
                self.PartySizeEntry.delete(0, END)

        def ClearDay(event):
            if self.DayEntry.get() == 'Day':
                self.DayEntry.delete(0, END)

        def ClearMonth(event):
            if self.MonthEntry.get() == 'Month':
                self.MonthEntry.delete(0, END)

        def ClearYear(event):
            if self.YearEntry.get() == 'Year':
                self.YearEntry.delete(0, END)

        def ClearTime(event):
            if self.TimeEntry.get() == 'Time':
                self.TimeEntry.delete(0, END)

        CustomerIDVar = IntVar()
        CustomerIDVar.set('Customer ID')
        self.CustomerIDEntry = Entry(self.window, textvariable=CustomerIDVar)
        self.CustomerIDEntry.bind('<Button-1>', ClearCustomerID)
        self.CustomerIDEntry.grid(column=0, row=0)

        PartySizeVar = IntVar()
        PartySizeVar.set('Party Size')
        self.PartySizeEntry = Entry(self.window, textvariable=PartySizeVar)
        self.PartySizeEntry.bind('<Button-1>', ClearPartySize)
        self.PartySizeEntry.grid(column=0, row=1)

        DayVar = StringVar()
        DayVar.set('Day')
        self.DayEntry = Entry(self.window, textvariable=DayVar)
        self.DayEntry.bind('<Button-1>', ClearDay)
        self.DayEntry.grid(column=0, row=2)

        DashLabel = Label(self.window, text='-')
        DashLabel.grid(column=1, row=2)

        MonthVar = StringVar()
        MonthVar.set('Month')
        self.MonthEntry = Entry(self.window, textvariable=MonthVar)
        self.MonthEntry.bind('<Button-1>', ClearMonth)
        self.MonthEntry.grid(column=2, row=2)

        DashLabel = Label(self.window, text='-')
        DashLabel.grid(column=3, row=2)

        YearVar = StringVar()
        YearVar.set('Year')
        self.YearEntry = Entry(self.window, textvariable=YearVar)
        self.YearEntry.bind('<Button-1>', ClearYear)
        self.YearEntry.grid(column=4, row=2)

        DashLabel = Label(self.window, text='-')
        DashLabel.grid(column=5, row=2)

        TimeVar = StringVar()
        TimeVar.set('Time')
        self.TimeEntry = Entry(self.window, textvariable=TimeVar)
        self.TimeEntry.bind('<Button-1>', ClearTime)
        self.TimeEntry.grid(column=6, row=2)

        SaveButton = Button(self.window, text='Save', command=self.Save)
        SaveButton.grid(column=0, row=6)

        self.tableAddVar = IntVar()
        self.tableAddVar.set('Seat Count')
        self.addTableEntry = Entry(self.window, textvariable=self.tableAddVar)
        self.addTableEntry.grid()

        self.tableNameVar = StringVar()
        self.tableNameVar.set('Table Name')
        self.tableNameEntry = Entry(self.window, textvariable=self.tableNameVar)
        self.tableNameEntry.grid()

        addTableButton = Button(self.window, text='Add Table', command=self.addTableFunc)
        addTableButton.grid()

    def addTableFunc(self):
        tableAdding = self.addTableEntry.get()
        tableName = self.tableNameEntry.get()

        Cursor.execute('SELECT MAX(SeatID) FROM Seats')
        SeatID = Cursor.fetchall()[0][0]
        try:
            SeatID += 1
        except:
            SeatID = 1

        Cursor.execute('INSERT INTO Seats VALUES("%s", "%s", "%s")' % (SeatID, tableName, tableAdding))
        Connection.commit()

    def Save(self):
        def HourMinCal(listedTime):
            colonIndex = listedTime.index(':')
            hour = []
            for i in range(0, colonIndex):
                hour.append(listedTime[i])
            Min = []
            for i in range(colonIndex + 1, len(Time)):
                Min.append(listedTime[i])

            hour = int("".join(hour))
            Min = int("".join(Min))
            savedTime = (hour * 60) + Min
            return savedTime

        CustomerID = self.CustomerIDEntry.get()
        PartySize = self.PartySizeEntry.get()
        Day = self.DayEntry.get()
        Month = self.MonthEntry.get()
        Year = self.YearEntry.get()
        Time = self.TimeEntry.get()
        fullDate = Day + '-' + Month + '-' + Year + '-' + Time
        if RegEx.regDateTime(fullDate) != 'None':
            Cursor.execute('SELECT * FROM Seats WHERE Chairs = "%s"' % (PartySize))
            Checking = Cursor.fetchall()

            if Checking != []:

                Cursor.execute('SELECT MAX(ReceiptNumber) FROM Receipt')
                ReceiptID = Cursor.fetchall()
                ReceiptID = ReceiptID[0][0]

                Table = Checking[0][0]

                try:
                    ReceiptID += 1
                except:
                    ReceiptID = 1

                Cursor.execute('SELECT Date FROM Receipt')
                AlreadyDates = Cursor.fetchall()

                BookTime = str(Day) + '-' + str(Month) + '-' + str(Year) + '-' + str(Time)

                print(AlreadyDates)
                ConfirmCount = 0
                for i in range(0, len(AlreadyDates)):
                    backCheck = list(AlreadyDates[0][i])
                    print(backCheck)
                    bTime = []
                    for i in range(11, 16):
                        bTime.append(backCheck[i])

                    bDate = []
                    for i in range(0, 2):
                        bDate.append(backCheck[i])
                    savedDate = int("".join(bDate))

                    bMonth = []
                    for i in range(3, 5):
                        bMonth.append(backCheck[i])
                    savedMonth = int("".join(bMonth))

                    bYear = []
                    for i in range(6, 10):
                        bYear.append(backCheck[i])
                    savedYear = int("".join(bYear))

                    savedTime = HourMinCal(bTime)
                    Time = HourMinCal(Time)

                    print(Time, savedTime)

                    if Time == savedTime and savedDate == Day and Month == savedMonth and Year != savedYear:
                        ConfirmCount += 1
                    elif Time == savedTime and savedDate == Day and Month != savedMonth and Year == savedYear:
                        ConfirmCount += 1
                    elif Time == savedTime and savedDate != Day and Month == savedMonth and Year == savedYear:
                        ConfirmCount += 1
                    elif Time != savedTime and savedDate == Day and Month == savedMonth and Year == savedYear:
                        ConfirmCount += 1
                    else:
                        ConfirmCount += 0

                if ConfirmCount == len(AlreadyDates):
                    TableID = Cursor.execute('SELECT * FROM Seats WHERE Chairs = %s' % (PartySize))
                    TableID = TableID
                    Cursor.execute('INSERT INTO Receipt VALUES("%s", "%s", "%s", "%s", "%s")' % (
                        ReceiptID, CustomerID, "#", BookTime, Table))
                    print('TABEL MADE')

                    Connection.commit()
        else:
            print('Date Time not format correctly')


class CustomerShowWindow():
    def __init__(self, window):
        self.window = window
        self.window.geometry('1000x400')
        self.window.title('Customers')

        CustomerShow = ttk.Treeview(self.window)
        CustomerShow["columns"] = ("One", "Two", "Three", "Four")
        CustomerShow.heading("#0", text="Customer ID", anchor=tk.W)
        CustomerShow.heading("One", text="First Name", anchor=tk.W)
        CustomerShow.heading("Two", text="Last Name", anchor=tk.W)
        CustomerShow.heading("Three", text="Phone No", anchor=tk.W)
        CustomerShow.heading("Four", text="Email", anchor=tk.W)
        CustomerShow.pack(expand=True, fill="both")

        Cursor.execute("SELECT * FROM Customer")
        AllCustomer = Cursor.fetchall()
        for row in AllCustomer:
            CustomerShow.insert("", END, text=row[0], values=row[1:])


global Connection, Cursor, Today
Connection = sqlite3.connect('Restaraunt_Master_Database.db')
Cursor = Connection.cursor()
Today = date.today()
try:
    Cursor.execute('CREATE TABLE Inventory(ProductID integer UNIQUE, Product text, Stock float)')
    Cursor.execute('CREATE TABLE Meals(Meal text, Price float, ProductID text, StockTake text, MealID integer UNIQUE)')
    Cursor.execute('CREATE TABLE Seats(SeatID integer UNIQUE, SeatName text, Chairs integer)')
    Cursor.execute('CREATE TABLE Receipt(ReceiptNumber integer UNIQUE, CustomerID integer, Request text, Date datetime, SeatID integer)')
    Cursor.execute('CREATE TABLE Customer(CustomerID integer UNIQUE, FirstName text, LastName text, PhoneNo text, Email text)')
except:
    pass

Run()
