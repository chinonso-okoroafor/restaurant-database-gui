import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class updateManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Manager")

        self.root.geometry("500x500")
        self.root.protocol("WM_DELETE_WINDOW", self.closeApplication)

        self.createMenu()
        self.showRestaurant()

    def createMenu(self):
        menuBar = tk.Menu(self.root)

        startMenu = tk.Menu(menuBar, tearoff=0)
        startMenu.add_command(label="Update Manager", command=self.showRestaurant)
        startMenu.add_command(label="Calculate Mean", command=self.showMean)
        startMenu.add_command(label="Plot Histogram", command=self.draw_histogram)
        startMenu.add_command(label="Quit", command=self.closeApplication)
        
        menuBar.add_cascade(label="Start", menu=startMenu)

        self.root.config(menu=menuBar)

    def closeApplication(self):
        response = messagebox.askquestion("Close Application", "Are you sure you want to close the application?")
        
        if response == 'yes':
            print("Closing the application...")
            self.root.destroy()
        else:
            print("Application not closed.")

    def showRestaurant(self):
        for widget in self.root.winfo_children():
            if widget.winfo_class() != 'Menu':
               widget.destroy()
        
        self.selectRestaurant = tk.Label(root, text="Pick Restaurant: ")
        self.restaurantVariable = tk.StringVar()
        self.restaurantDropdown = ttk.Combobox(root, textvariable=self.restaurantVariable,state="readonly")

        self.managerName = tk.Label(root, text="Manager Name: ")
        self.managerNameVariable = tk.StringVar()
        self.managerNameInfo = tk.Label(root, textvariable=self.managerNameVariable)

        self.managerEmail = tk.Label(root, text="Manager Email: ")
        self.managerEmailVariable = tk.StringVar()
        self.managerEmailInfo = tk.Label(root, textvariable=self.managerEmailVariable)

        self.yearsOfExperience = tk.Label(root, text="Years of Experience: ")
        self.yearsOfExperienceVariable = tk.StringVar()
        self.yearsOfExperienceInfo = tk.Label(root, textvariable=self.yearsOfExperienceVariable)

        self.newManagerEmailLabel = tk.Label(root, text="New Manager Email:")
        self.newManagerEmail = tk.Entry(root)

        self.updateManagerButton = tk.Button(root, text="Update Manager Details", command=self.updateManager)

        ## Setting up the layout
        self.selectRestaurant.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.restaurantDropdown.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.managerName.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.managerNameInfo.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.managerEmail.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.managerEmailInfo.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.yearsOfExperience.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.yearsOfExperienceInfo.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.newManagerEmailLabel.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.newManagerEmail.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.updateManagerButton.grid(row=5, column=0, pady=10, columnspan=2)

        self.getAllRestaurants()

        self.restaurantDropdown.bind("<<ComboboxSelected>>", self.getManagerInfo)
    
    def updateManager(self):
        selectedRestaurant = self.restaurantVariable.get()
        newManagerEmail = self.newManagerEmail.get().strip()

        if not self.isValidEmail(newManagerEmail):
            messagebox.showerror("Error", "Invalid Email format")
            return
        
        try:
            conn = sqlite3.connect("Coursework.db")
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Manager Set Email = ? Where ID = (
                           select ManagerID from Restaurant where RestaurantName = ?
                )
            """, (newManagerEmail, selectedRestaurant,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Manager updated successfully")
            self.getManagerInfo(None)

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
    
    def plotHistogram(self):
       # Remove existing widgets
        for widget in self.root.winfo_children():
            if widget.winfo_class() != 'Menu':
               widget.destroy()

        self.selectRestaurant = tk.Label(root, text="Pick Something Else")
        self.restaurantVariable = tk.StringVar()
        self.restaurantDropdown = ttk.Combobox(root, textvariable=self.restaurantVariable,state="readonly")

    @staticmethod
    def isValidEmail(emailAddress):
        # Simple email format validation
        import re
        emailRegExp = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.match(emailRegExp, emailAddress))
    
    def showMean(self):
       # Remove existing widgets
        for widget in self.root.winfo_children():
            if widget.winfo_class() != 'Menu':
               widget.destroy()

        self.selectRestaurant = tk.Label(root, text="Restautant Name: ")
        self.restaurantVariable = tk.StringVar()
        self.restaurantDropdown = ttk.Combobox(root, textvariable=self.restaurantVariable,state="readonly")

        self.foodRatingLabel = tk.Label(root, text="Food Rating Mean:")
        self.foodRatingVariable = tk.StringVar()
        self.foodRatingInfo = tk.Label(root, textvariable=self.foodRatingVariable)

        self.selectRestaurant.grid(row=0,column=0, padx=10, pady=5, sticky=tk.E)
        self.restaurantDropdown.grid(row=0,column=1, padx=10, pady=5, sticky=tk.W)

        self.foodRatingLabel.grid(row=1,column=0, padx=10, pady=5, sticky=tk.E)
        self.foodRatingInfo.grid(row=1,column=1, padx=10, pady=5, sticky=tk.W)

        self.calculateMeanButton = tk.Button(root, text='Calculate Mean', command=self.calculateMean)

        self.getAllRestaurants()

        self.calculateMeanButton.grid(row=2,column=0, columnspan=3, pady=10)


    def calculateMean(self):
        selectedRestaurant = self.restaurantDropdown.get()

        try:
            conn = sqlite3.connect("Coursework.db")
            cursor = conn.cursor()

            cursor.execute('''
                Select AVG(CustomerRatingFood)
                FROM Orders
                Join Restaurant
                ON Orders.RestaurantID = Restaurant.RestaurantID
                WHERE Restaurant.RestaurantName = ?
            ''', (selectedRestaurant,))

            mean = cursor.fetchall()

            if(mean):
                self.foodRatingVariable.set(round(mean[0][0], 2))
            else:
                print("No mean found")

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error calculating mean", str(e))

    def getAllRestaurants(self):
        try:
            conn = sqlite3.connect("Coursework.db")
            cursor = conn.cursor()

            cursor.execute("Select RestaurantName from Restaurant")
            allRestaurants = [row[0] for row in cursor.fetchall()]

            self.restaurantDropdown['values'] = allRestaurants

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error loading restaurants", str(e))

    def getManagerInfo(self, event):
        selectedRestaurant = self.restaurantVariable.get()

        try:
            conn = sqlite3.connect("Coursework.db")
            cursor = conn.cursor()

            cursor.execute('''
                SELECT Manager.ManagerName, Manager.Email, Manager.YearsAsManager from Restaurant Join Manager on Restaurant.ManagerID = Manager.ID where Restaurant.RestaurantName = ?
            ''', (selectedRestaurant,))

            managerInformation = cursor.fetchone()

            if(managerInformation):
                self.managerNameVariable.set(f"{managerInformation[0]}")
                # self.managerEmailVariable.config(width= (len(managerInformation[1]) + 5))
                # self.managerEmailVariable.update_idletasks()
                # self.managerEmailVariable.delete(0, tk.END)
                # self.managerEmailVariable.insert(0, f"{managerInformation[1]}")
                self.managerEmailVariable.set(f"{managerInformation[1]}")
                self.yearsOfExperienceVariable.set(f"{managerInformation[2]}")
            else:
                self.managerNameVariable.set("No Manager Assigned")
            
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error loading Manager Information", str(e))
            
    def draw_histogram(self):
        conn = sqlite3.connect("Coursework.db")
        cursor = conn.cursor()
        # Perform SQL query to retrieve Delivery Time Taken data
        # Replace 'your_table' with the actual table name
        query = "SELECT DeliveryTimeTaken FROM Orders"
        cursor.execute(query)
        delivery_times = [record[0] for record in cursor.fetchall()]
        print(len(delivery_times))
        # Draw histogram using a plotting library (e.g., matplotlib)
        plt.hist(delivery_times, bins=30, edgecolor='black')
        plt.xlabel("Delivery Time Taken (mins)")
        plt.ylabel("Frequency")
        plt.title("Histogram of Delivery Time Taken for All Orders")
        plt.show()

root = tk.Tk()
app = updateManager(root)
root.mainloop()
