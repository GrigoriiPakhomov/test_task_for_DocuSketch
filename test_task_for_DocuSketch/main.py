import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import requests



# Загрузка .json файла
df = pd.read_json('https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json')


class PlotGenerator:
    def __init__(self):
        self.output_folder = 'charts'
        os.makedirs(self.output_folder, exist_ok=True)

    def draw_plots(self, json_url):
        # Загрузка JSON-данных с веб-ресурса
        try:
            response = requests.get(json_url)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            return f"Ошибка при загрузке JSON-файла: {str(e)}"

        # Создание графиков для сравнения разных столбцов
        plot_paths = []
        for column in df.columns:
            if df[column].dtype == 'int64' or df[column].dtype == 'float64':
                plt.figure(figsize=(8, 6))
                plt.plot(df[column])
                plt.title(f'График для столбца "{column}"')
                plt.xlabel('Индекс')
                plt.ylabel('Значение')
                plot_file_path = os.path.join(self.output_folder, f'{column}_plot.png')
                plt.savefig(plot_file_path)
                plot_paths.append(plot_file_path)
                plt.close()

        return plot_paths

# Пример использования
if __name__ == "__main__":
    plot_generator = PlotGenerator()
    json_file_url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    plot_paths = plot_generator.draw_plots(json_file_url)

    if plot_paths:
        print("Созданные графики сохранены в папке 'charts'. Пути к файлам:")
        for path in plot_paths:
            print(path)
    else:
        print("Не удалось создать графики.")

