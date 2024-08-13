import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
import json
import os


class ResultPresenter():
    
  
    def __init__(self):
      script_dir = os.path.dirname(os.path.abspath(__file__))
      project_root = os.path.dirname(script_dir)
      results_path = os.path.join(project_root, 'outputs', 'results.json')
      self._results: Dict[str, List[str]] = self.__read_json(results_path)
      self._inbailwick_result = self._results["inbailwick_result"]
      self._inbailwick_partial_result = self._results['inbailwick_partial_percent']
      self._companies = [self.clean_name(item[0]) for item in self._results.get("top_unreachable_percents", [])]
      self._top_unreachable_percents = [item[1] for item in self._results.get("top_unreachable_percents", [])]
      self._top_unreachable_numbers = [item[1] for item in self._results.get("top_unreachable_numbers", [])]
      self._top_affected_percents = [item[1] for item in self._results.get("top_affected_percents", [])]
      self._top_affected_numbers = [item[1] for item in self._results.get("top_affected_numbers", [])]
    
    
    def clean_name(self, item):
      '''
      Converts names into human readable format
        
      Keyword arguments:
      item(str): word to clean
      '''
      length = len(item)
      for i in range(length):
          if item[i] in '- ,':
              return item[:i]
      return item
   
    def __read_json(self, file_name: str) -> Dict:
        '''
        Private function to read json
        
        @Keyword arguments:
        file_name(str): Name of requested file to unpack
        '''
        with open(file_name, 'r') as jsonfile:
            data = json.load(jsonfile)
        return data

    
    def save_image(self, filename):
        '''
        saves the image in the proper folder, even when calling from this script directly
        
        Keyword arguments:
        filename(str): desired file export name
        '''
        script_dir = os.path.dirname(__file__)
        graphics_dir = os.path.join(script_dir, '..', 'graphics')
        file_path = os.path.join(graphics_dir, f'{filename}')
        plt.savefig(file_path)
    
    
    def create_bar_chart(self):
        '''Creates the bar chart for top unreachable and affected company numbers'''
        x, y_1, y_2 = self._companies, self._top_unreachable_numbers, self._top_affected_numbers
        plt.grid(True)
        plt.gca().set_axisbelow(True)
        plt.bar(x, y_1, label = "Unreachable")
        y_2 = [b-a for a, b in zip(y_1,y_2)]
        plt.bar(x, y_2, bottom = y_1, label = "Affected")
        plt.xlabel('Categories')
        plt.ylabel('Number of Domains')
        plt.xticks(rotation = 45, fontsize = 7, ha = 'right')
        plt.legend()
        plt.tight_layout()
        self.save_image("bar_chart.png")
    
    
    def create_table(self):
        '''Creates the table for top unreachable and affected company percentages'''
        data = list(zip(self._companies, self._top_unreachable_percents, self._top_affected_percents))
        total_unreachable = round(sum(self._top_unreachable_percents), 2)
        total_affected = round(sum(self._top_affected_percents), 2)
        data.append(["Total", total_unreachable, total_affected])
        columns = ('', '% Unreachable', "% Affected")
        fig, ax = plt.subplots()
        ax.axis('tight')
        ax.axis('off')
        colors = [["#f2f2f2", "#f2f2f2", "#f2f2f2"] if i % 2 == 0 else ["#ffffff", "#ffffff", "#ffffff"] for i in range(len(data))]
        table = ax.table(cellText=data, colLabels=columns, loc='center', cellColours = colors, colColours =['#ffffff'] *3)
        total_rows = len(data)
        for key, cell in table.get_celld().items():
            if key[0] != total_rows:
                cell.set_edgecolor('none')
        self.save_image("result_table.png")


    
    def create_inbailwick_table(self):
        '''Creates the full/partial inbailwick percentage table'''
        data = [
            ["Full Inbailwick Domain %", self._inbailwick_result],
            ["Partial Inbailwick Domain %", self._inbailwick_partial_result]
        ]
        fig, ax = plt.subplots()
        ax.axis('tight')
        ax.axis('off')
        colors = [["#f2f2f2", "#f2f2f2"], ["#ffffff", "#ffffff"]]
        table = ax.table(cellText=data, loc='center', cellColours=colors)
        for key, cell in table.get_celld().items():
            cell.set_text_props(horizontalalignment='center')
            if key[1] == 0:
                cell.set_text_props(fontweight='bold')
            cell.set_edgecolor('none')
        table.scale(1, 1.5)
        self.save_image('inbailwick_table.png')
