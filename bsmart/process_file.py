# csv_handler.py
import pandas as pd
import matplotlib.pyplot as plt
from .models import CsvData

def process_csv(file):
    pdf = pd.read_csv('media/'+file)
    # Save data to CsvData model
    avg_price_by_year = pdf.groupby('year')['price'].mean()

    # Create a line chart to visualize the average price by year
    plt.figure(figsize=(8, 6))
    plt.plot(avg_price_by_year.index, avg_price_by_year.values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    plt.title('Average Price by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Price')
    plt.title('Price by Year')
    chart_path = 'media/sample_chart.png'  # Save the chart as an image
    plt.savefig(chart_path)
    plt.close()
    return chart_path
