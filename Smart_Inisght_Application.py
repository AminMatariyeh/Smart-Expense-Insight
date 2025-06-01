import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from load_expenses import load_expenses
from Abnormal_activity_detection import detect_abnormalities





class ExpenseApp:



    def file_dialog(self):
        self.filepath =filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.filepath:

            try:
                self.df= load_expenses(self.filepath)

                self.btn_show.config(state="normal")  

                self.text_area.delete('1.0',tk.END)
                self.text_area.insert(tk.END, f"Loaded file: {self.filepath}\n")
            except Exception as e:
                messagebox.showerror("Error, Failed to load file")
    
    
    def __init__(self, root):
        self.root =root
        root.title("Smart Expense Analyzer")

        self.filepath = None
        self.df=None

        self.btn_select = tk.Button(root,text="Select CSV File", command=self.file_dialog)
        
        self.btn_select.pack(pady=10)

        self.option_var= tk.StringVar(value="all_expenses")
        options_frame =tk.Frame(root)
        options_frame.pack(pady=10)


        tk.Radiobutton(options_frame, text="List All Expenses", variable=self.option_var, value="all_expenses").pack(anchor="w")
        tk.Radiobutton(options_frame, text="Summary by Category", variable=self.option_var, value="summary").pack(anchor="w")

        tk.Radiobutton(options_frame, text="Show Abnormal Transactions", variable=self.option_var, value="abnormal").pack(anchor="w")
        self.btn_show = tk.Button(root,text="Show Results", command=self.show_results, state="disabled")
        self.btn_show.pack(pady=10)


        self.text_area= scrolledtext.ScrolledText(root, width=100, height=25)
        self.text_area.pack(pady=10)

    def show_all_expenses(self):
        self.text_area.insert(tk.END, "Expenses: \n")
        for _, row in self.df.iterrows():

            line=f"{row['Date']} | ${row['Amount']:.2f} | {row['Category']} | {row['Description']}/n"

            self.text_area.insert(tk.END,line)
    def show_summary(self):
        summary =self.df.groupby('Category')['Amount'].agg(['count', 'sum']).sort_values(by='sum', ascending=False)
        self.text_area.insert(tk.END,"Summary by Category:\n\n")
        
        
        for cat, row in summary.iterrows():

            line = f"{cat}: {row['count']} transactions, Total Spent: ${row['sum']:.2f}\n"
          
            self.text_area.insert(tk.END, line)
    def show_abnormalities(self):
        
        
        abnormal = detect_abnormalities(self.df)

        self.text_area.delete(1.0, tk.END)

        if abnormal.empty:
            self.text_area.insert(tk.END,"No abnormal activity detected.\n")
       
        else:
            self.text_area.insert(tk.END, f"{len(abnormal)} abnormal transactions found:\n\n")
            for _, row in abnormal.iterrows():


                line = f"{row['Date']} | ${row['Amount']:.2f} | {row['Category']} | {row['Description']}\n"
                
                self.text_area.insert(tk.END, line)

    
    def show_results(self):
        if self.df is None:
            messagebox.showwarning("Please load a CSV file first.")
            return
        choice=self.option_var.get()

        self.text_area.delete('1.0',tk.END)

        if choice == "all_expenses":
            self.show_all_expenses()
       
        elif choice =="summary":
            self.show_summary()
        
        elif choice=="abnormal":
            self.show_abnormalities()
    


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
