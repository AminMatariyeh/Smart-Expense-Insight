import matplotlib.pyplot as plt
from load_expenses import load_expenses

df= load_expenses("expenses.csv")

category_total= df.groupby("Category")["Amount"].sum().sort_values()
plt.figure(figsize=(10,6))
plt.barh(category_total.index, category_total.values)
plt.title("Total Spending by Category")
plt.xlabel("Total Amount Spent ($)")
plt.ylabel("Category")
for index, value in enumerate(category_total.values):
    plt.text(value+5, index, f"${value:.2f}",va="center", fontsize=10)
plt.tight_layout()
plt.show()