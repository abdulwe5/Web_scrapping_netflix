import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    """Fetch and parse the web page content."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "lxml")
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
        return None

def scrape_movie_data(soup):
    """Scrape movie names and rankings."""
    movie_list = []
    ranking_list = []

    # Select and extract movie names
    movie_elements = soup.select("td.pb-2.tbl-cell.tbl-cell-name")
    for element in movie_elements:
        movie_list.append(element.text.strip())

    # Select and extract rankings
    ranking_elements = soup.select("td.pb-2.tbl-cell.tbl-cell-rank")
    for element in ranking_elements:
        ranking_list.append(element.text.strip())

    return movie_list, ranking_list

def create_recommendations(movie_list, ranking_list, top_n=5):
    """Create a list of movie recommendations with name and ranking."""
    recommendations = []
    for i in range(min(top_n, len(movie_list), len(ranking_list))):
        recommendations.append({"name": movie_list[i], "ranking": ranking_list[i]})
    return recommendations

def show_recommendations():
    """Function to display the movie recommendations on the GUI."""
    url = "https://www.netflix.com/tudum/top10/tv"
    soup = fetch_page_content(url)

    if soup:
        # Scrape movie data
        movie_list, ranking_list = scrape_movie_data(soup)

        # Create recommendations
        recommendations = create_recommendations(movie_list, ranking_list, top_n=5)

        # Clear the output area
        result_text.delete(1.0, tk.END)

        # Display recommendations
        for movie in recommendations:
            result_text.insert(tk.END, f"{movie['ranking']}. {movie['name']}\n")

# Create the main window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("400x400")

# Add a title label
title_label = ttk.Label(root, text="Top Netflix TV Show Recommendations", font=("Helvetica", 14))
title_label.pack(pady=10)

# Add a button to fetch and display movie recommendations
recommend_button = ttk.Button(root, text="Get Top 5 Recommendations", command=show_recommendations)
recommend_button.pack(pady=20)

# Text widget to display results
result_label = ttk.Label(root, text="Recommended Movies:", font=("Helvetica", 12))
result_label.pack(pady=5)
result_text = tk.Text(root, height=10, width=40)
result_text.pack()

# Run the Tkinter event loop
root.mainloop()