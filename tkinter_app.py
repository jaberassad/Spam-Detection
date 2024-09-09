import tkinter as tk
from tkinter import ttk
import json
import math
import pandas as pd
import random



# Load the probabilities from the JSON file
with open('probabilities.json', 'r') as file:
    prob_dict = json.load(file)

with open('word_set.json', 'r') as file:
    word_set = json.load(file)

# Load the dataset from the CSV file
df = pd.read_csv('spam.csv', encoding= "latin-1")

ham_df = df[df['v1'] == 'ham']
rows_to_remove = ham_df.head(4078)
df = df[~df.index.isin(rows_to_remove.index)]

# Define the check_spam2 function
def check_spam(message):
    global word_set
    spam = math.log(0.4)
    ham = math.log(0.6)

    for i in message.split():
        if i not in prob_dict or prob_dict[i][1] == 0 or prob_dict[i][0] == 0 or not i in word_set:
            continue
        spam += math.log(prob_dict[i][1])
        ham += math.log(prob_dict[i][0])

    return spam > ham

# Create the Tkinter application
def create_app():
    root = tk.Tk()
    root.title("Spam Checker")

    # Set the window size and background color
    root.geometry("600x400")
    root.configure(bg='#f0f8ff')

    # Create and place the title label
    title_label = tk.Label(root, text="Spam Email Checker", bg='#f0f8ff', font=("Arial", 16, 'bold'))
    title_label.pack(pady=10)

    # Create and place the text input
    input_label = tk.Label(root, text="Enter your message below:", bg='#f0f8ff', font=("Arial", 12))
    input_label.pack(pady=5)

    input_text = tk.Text(root, height=6, width=60, wrap=tk.WORD)
    input_text.pack(pady=5)

    # Create and place the result label
    result_label = tk.Label(root, text="", bg='#f0f8ff', font=("Arial", 12, 'italic'))
    result_label.pack(pady=10)

    # Create and place the button for checking spam
    def on_check_spam():
        message = input_text.get("1.0", tk.END).strip()
        if check_spam(message):
            result_label.config(text="Result: This message is classified as SPAM.", fg='red')
        else:
            result_label.config(text="Result: This message is classified as NOT SPAM.", fg='green')

    check_button = tk.Button(root, text="Check if Message is SPAM", command=on_check_spam, bg='#4CAF50', fg='black', font=("Arial", 12))
    check_button.pack(pady=10)

    # Function to display a random email from the dataset
    def show_random_email():
        random_row = df.sample(n=1).iloc[0]
        email_type = random_row['v1']
        email_message = random_row['v2']
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, email_message)
        result_label.config(text=f"Random Email Type: {email_type}", fg='blue')

    # Create and place the button for generating random email
    random_email_button = tk.Button(root, text="Generate Random Email", command=show_random_email, bg='#008CBA', fg='black', font=("Arial", 12))
    random_email_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_app()
