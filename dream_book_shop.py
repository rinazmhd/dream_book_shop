import sys
print(sys.executable)
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from typing import List, Optional
import os

class LoginSystem:
  
 
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "password123"
    MAX_ATTEMPTS = 3
    
    @staticmethod
    def authenticate() -> bool:

        print("\n" + "=" * 60)
        print("  DREAM BOOK SHOP - DATA ANALYSIS APPLICATION  ")
        print("=" * 60)
        print("  Please login to access the system             ")
        print("=" * 60)
        
        attempts = 0
        while attempts < LoginSystem.MAX_ATTEMPTS:
            print(f"\n[Login Attempt {attempts + 1}/{LoginSystem.MAX_ATTEMPTS}]")
            
            username = input("  Enter Username: ").strip()
            password = input("  Enter Password: ").strip()
            
            if username == LoginSystem.VALID_USERNAME and password == LoginSystem.VALID_PASSWORD:
                print("\n" + "=" * 60)
                print("   LOGIN SUCCESSFUL! Welcome to Dream Book Shop!  ")
                print("=" * 60)
                return True
            else:
                attempts += 1
                remaining = LoginSystem.MAX_ATTEMPTS - attempts
                if remaining > 0:
                    print(f"   Invalid credentials. {remaining} attempts remaining.")
                else:
                    print("   Too many failed attempts. Access denied.")
        
        return False




class DataLoader:

    def __init__(self):
        self.data = None
        self.file_path = None
    
    def load(self, file_path: str) -> Optional[pd.DataFrame]:

        try:
            if not os.path.exists(file_path):
                print(f"[ERROR] File '{file_path}' not found.")
                print("[INFO] Please ensure 'books.csv' is in the current directory.")
                return None
            
            self.data = pd.read_csv(file_path)
            self.file_path = file_path
            
            if self.data.empty:
                print("[WARNING] Dataset is empty!")
                return None
            
            print(f"[SUCCESS] Loaded {len(self.data)} records from {file_path}")
            print(f"[INFO] Columns: {', '.join(self.data.columns.tolist())}")
            return self.data
            
        except pd.errors.EmptyDataError:
            print("[ERROR] File is empty.")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return None
    
    def get_data(self) -> Optional[pd.DataFrame]:

        return self.data
    
    def get_record_count(self) -> int:

        if self.data is not None:
            return len(self.data)
        return 0


class DataCleaner:

    
    REQUIRED_COLUMNS = ['Title', 'Author', 'Year']
    
    def clean(self, data: pd.DataFrame) -> pd.DataFrame:

        if data is None or data.empty:
            print("[WARNING] No data to clean.")
            return data
        
 
        missing_cols = []
        for col in self.REQUIRED_COLUMNS:
            if col not in data.columns:
                missing_cols.append(col)
        
        if missing_cols:
            print(f"[ERROR] Missing required columns: {missing_cols}")
            return data
        

        original_len = len(data)
        data = data.drop_duplicates()
        duplicates_removed = original_len - len(data)
        if duplicates_removed > 0:
            print(f"[INFO] Removed {duplicates_removed} duplicate rows")
        

        data = data.dropna(subset=self.REQUIRED_COLUMNS)
        rows_removed = original_len - len(data) - duplicates_removed
        if rows_removed > 0:
            print(f"[INFO] Removed {rows_removed} rows with missing required columns")
        
        return data


class Analysis(ABC):
    
    @abstractmethod
    def perform_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_analysis_name(self) -> str:
        pass
    
    @abstractmethod
    def get_column_used(self) -> str:
        pass


class PublicationTrendStrategy(Analysis):
    
    def __init__(self):
        self.results = None
    
    def perform_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
        """Group books by year and count publications."""
        if data is None or data.empty:
            return pd.DataFrame()
        

        year_col = None
        for col in data.columns:
            if col.lower() == 'year':
                year_col = col
                break
        
        if year_col is None:
            print("[ERROR] No Year column found.")
            return pd.DataFrame()
        
        self.results = data.groupby(year_col).size().reset_index(name='Count')
        self.results = self.results.sort_values(year_col)
        return self.results
    
    def get_analysis_name(self) -> str:
        return "Publication Trends Over Time"
    
    def get_column_used(self) -> str:
        return "Year"


class TopAuthorsStrategy(Analysis):
  
    
    def __init__(self, top_n: int = 5):
        self.top_n = top_n
        self.results = None
    
    def perform_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
      
        if data is None or data.empty:
            return pd.DataFrame()
        
    
        author_col = None
        for col in data.columns:
            if col.lower() == 'author':
                author_col = col
                break
        
        if author_col is None:
            print("[ERROR] No Author column found.")
            return pd.DataFrame()
        
        self.results = data.groupby(author_col).size().reset_index(name='Book Count')
        self.results = self.results.sort_values('Book Count', ascending=False).head(self.top_n)
        self.results = self.results.reset_index(drop=True)
        return self.results
    
    def get_analysis_name(self) -> str:
        return f"Top {self.top_n} Most Prolific Authors"
    
    def get_column_used(self) -> str:
        return "Author"


class LanguageStrategy(Analysis):

    
    def __init__(self):
        self.results = None
    
    def perform_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
       
        if data is None or data.empty:
            return pd.DataFrame()
        
    
        lang_col = None
        for col in data.columns:
            if col.lower() == 'language':
                lang_col = col
                break
        
        if lang_col is None:
            print("[ERROR] No Language column found.")
            return pd.DataFrame()
        
        self.results = data.groupby(lang_col).size().reset_index(name='Count')
        self.results = self.results.sort_values('Count', ascending=False)
        self.results = self.results.reset_index(drop=True)
        return self.results
    
    def get_analysis_name(self) -> str:
        return "Language Distribution"
    
    def get_column_used(self) -> str:
        return "Language"


class PublisherStrategy(Analysis):
  
    
    def __init__(self):
        self.results = None
    
    def perform_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
     
        if data is None or data.empty:
            return pd.DataFrame()
        
     
        pub_col = None
        for col in data.columns:
            if col.lower() == 'publisher':
                pub_col = col
                break
        
        if pub_col is None:
            print("[ERROR] No Publisher column found.")
            return pd.DataFrame()
        
        self.results = data.groupby(pub_col).size().reset_index(name='Book Count')
        self.results = self.results.sort_values('Book Count', ascending=False)
        self.results = self.results.reset_index(drop=True)
        return self.results
    
    def get_analysis_name(self) -> str:
        return "Publisher Analysis"
    
    def get_column_used(self) -> str:
        return "Publisher"


class ISBNStrategy(Analysis):
    
    
    def __init__(self):
        self.results = None
    
    def perform_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
     
        if data is None or data.empty:
            return pd.DataFrame()
        
     
        isbn_col = None
        for col in data.columns:
            if col.lower() == 'isbn':
                isbn_col = col
                break
        
        if isbn_col is None:
            print("[ERROR] No ISBN column found.")
            return pd.DataFrame()
        
        total_records = len(data)
        

        missing_isbn = data[isbn_col].isna().sum()
        empty_isbn = (data[isbn_col] == '').sum()
        total_missing = missing_isbn + empty_isbn
        percentage = (total_missing / total_records) * 100 if total_records > 0 else 0
        
        self.results = pd.DataFrame({
            'Metric': ['Total Records', 'Missing ISBN', 'Missing Percentage', 'Valid ISBN'],
            'Value': [total_records, total_missing, f'{percentage:.2f}%', total_records - total_missing]
        })
        return self.results
    
    def get_analysis_name(self) -> str:
        return "Missing ISBN Analysis"
    
    def get_column_used(self) -> str:
        return "ISBN"


class AnalysisContext:
    
    def __init__(self, strategy: Analysis):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Analysis):
        self._strategy = strategy
    
    def execute_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
        return self._strategy.perform_analysis(data)
    
    def get_analysis_name(self) -> str:
        return self._strategy.get_analysis_name()



class ChartGenerator:

    
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def generate_chart(self, data: pd.DataFrame, analysis_name: str):

        if data is None or data.empty:
            print("[WARNING] No data to chart.")
            return None
        
        if "Trends" in analysis_name or "Over Time" in analysis_name:
            return self._generate_line_chart(data, analysis_name)
        elif "Distribution" in analysis_name:
            return self._generate_pie_chart(data, analysis_name)
        elif "ISBN" in analysis_name:
            return self._generate_isbn_chart(data, analysis_name)
        elif "Author" in analysis_name or "Publisher" in analysis_name:
            return self._generate_bar_chart(data, analysis_name)
        else:
            return self._generate_bar_chart(data, analysis_name)
    
    def _generate_bar_chart(self, data: pd.DataFrame, title: str):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        columns = data.columns.tolist()
        x_col = columns[0]
        y_col = columns[1]
        

        if len(data) > 15:
            data = data.head(15)
        
        bars = ax.bar(data[x_col], data[y_col], color='skyblue', edgecolor='navy')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}' if height == int(height) else f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
    
    def _generate_line_chart(self, data: pd.DataFrame, title: str):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        columns = data.columns.tolist()
        x_col = columns[0]
        y_col = columns[1]
        
        ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, color='green')
        

        for i, row in data.iterrows():
            ax.annotate(str(row[y_col]), (row[x_col], row[y_col]),
                       textcoords="offset points", xytext=(0,10), ha='center')
        
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _generate_pie_chart(self, data: pd.DataFrame, title: str):

        fig, ax = plt.subplots(figsize=(10, 8))
        
        columns = data.columns.tolist()
        label_col = columns[0]
        value_col = columns[1]
        
    
        if len(data) > 8:
            top_data = data.head(8)
            other_sum = data[value_col][8:].sum()
            
       
            other_row = pd.DataFrame({label_col: ['Other'], value_col: [other_sum]})
            plot_data = pd.concat([top_data, other_row], ignore_index=True)
        else:
            plot_data = data
        
        colors = plt.cm.Set3(range(len(plot_data)))
        wedges, texts, autotexts = ax.pie(plot_data[value_col],
                                          labels=plot_data[label_col],
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          explode=[0.02] * len(plot_data))
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def _generate_isbn_chart(self, data: pd.DataFrame, title: str):
      
        fig, ax = plt.subplots(figsize=(8, 6))
        
        valid = int(data.loc[data['Metric'] == 'Valid ISBN', 'Value'].iloc[0])
        missing = int(data.loc[data['Metric'] == 'Missing ISBN', 'Value'].iloc[0])
        
        labels = ['Valid ISBN', 'Missing ISBN']
        values = [valid, missing]
        colors = ['green', 'red']
        
        bars = ax.bar(labels, values, color=colors, edgecolor='black')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def display(self, fig):
        if fig is not None:
            plt.show()
            plt.close(fig)


class AnalysisEngine:
    
    def __init__(self):
        self.data = None
        self.loader = DataLoader()
        self.cleaner = DataCleaner()
        self.chart_generator = ChartGenerator()
        self.results = {}
    
    def load_dataset(self, file_path: str) -> bool:
        print("\n" + "=" * 60)
        print("LOADING DATASET")
        print("=" * 60)
        
        data = self.loader.load(file_path)
        if data is None:
            return False
        
        self.data = self.cleaner.clean(data)
        if self.data is None or self.data.empty:
            print("[ERROR] Dataset cleaning failed.")
            return False
        
        print(f"[SUCCESS] Dataset ready: {len(self.data)} records, {len(self.data.columns)} columns")
        return True
    
    def _execute_strategy(self, strategy: Analysis) -> Optional[pd.DataFrame]:
        if self.data is None or self.data.empty:
            print("[ERROR] No data loaded. Please load dataset first.")
            return None
        
        try:
            print(f"\n[INFO] Executing: {strategy.get_analysis_name()}")
            context = AnalysisContext(strategy)
            results = context.execute_analysis(self.data)
            
            if results is not None and not results.empty:
                self.results[strategy.get_analysis_name()] = results
                return results
            else:
                print(f"[WARNING] No results from {strategy.get_analysis_name()}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")
            return None
    
    def run_publication_trends(self) -> Optional[pd.DataFrame]:
        strategy = PublicationTrendStrategy()
        results = self._execute_strategy(strategy)
        if results is not None:
            self._display_results("Publication Trends Over Time", results)
            self._show_chart(results, strategy.get_analysis_name())
        return results
    
    def run_top_authors(self) -> Optional[pd.DataFrame]:
        strategy = TopAuthorsStrategy()
        results = self._execute_strategy(strategy)
        if results is not None:
            self._display_results("Top 5 Most Prolific Authors", results)
            self._show_chart(results, strategy.get_analysis_name())
        return results
    
    def run_language_distribution(self) -> Optional[pd.DataFrame]:
        strategy = LanguageStrategy()
        results = self._execute_strategy(strategy)
        if results is not None:
            self._display_results("Language Distribution", results)
            self._show_chart(results, strategy.get_analysis_name())
        return results
    
    def run_publisher_analysis(self) -> Optional[pd.DataFrame]:
        strategy = PublisherStrategy()
        results = self._execute_strategy(strategy)
        if results is not None:
            self._display_results("Publisher Analysis", results)
            self._show_chart(results, strategy.get_analysis_name())
        return results
    
    def run_isbn_analysis(self) -> Optional[pd.DataFrame]:
        strategy = ISBNStrategy()
        results = self._execute_strategy(strategy)
        if results is not None:
            self._display_results("Missing ISBN Analysis", results)
            self._show_chart(results, strategy.get_analysis_name())
        return results
    
    def _display_results(self, title: str, results: pd.DataFrame):
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
        print("\n[SUMMARY]")
        if len(results.columns) == 2:
      
            for _, row in results.iterrows():
                print(f"  {row[results.columns[0]]}: {row[results.columns[1]]}")
        else:
            print(results.to_string(index=False))
    
    def _show_chart(self, results: pd.DataFrame, analysis_name: str):
        try:
            fig = self.chart_generator.generate_chart(results, analysis_name)
            if fig:
                print("\n[CHART] Displaying visualization...")
                self.chart_generator.display(fig)
        except Exception as e:
            print(f"[WARNING] Could not generate chart: {e}")
    
    def get_data_info(self) -> str:
        if self.data is None:
            return "No dataset loaded."
        return f"Dataset: {len(self.data)} records, {len(self.data.columns)} columns"


class DreamBookShopApp:
    
    def __init__(self):
        self.engine = AnalysisEngine()
        self.is_loaded = False
        self.running = True
    
    def display_welcome(self):
        print("\n" + "=" * 70)
        print("   DREAM BOOK SHOP - DATA ANALYSIS APPLICATION  ")
        print("=" * 70)
        print("   Analyse bibliographic data with ease          ")
        print("   Generate charts and textual summaries        ")
        print("   Make data-driven business decisions          ")
        print("=" * 70)
    
    def display_menu(self):
        print("\n" + "=" * 60)
        print("  MAIN MENU")
        print("=" * 60)
        print("  1.  Load Dataset")
        print("  2.  Publication Trends Over Time")
        print("  3.  Top 5 Most Prolific Authors")
        print("  4.  Language Distribution")
        print("  5.  Publisher Analysis")
        print("  6.  Missing ISBN Analysis")
        print("  7.  Run All Analyses")
        print("  8.  Dataset Info")
        print("  9.  Exit")
        print("=" * 60)
        
        status = " Loaded" if self.is_loaded else " Not Loaded"
        print(f"  Dataset Status: {status}")
        print("=" * 60)
    
    def get_user_choice(self) -> int:
        while True:
            try:
                choice = int(input("\n  Enter your choice: "))
                if 1 <= choice <= 9:
                    return choice
                print("  ️ Please enter a number between 1 and 9")
            except ValueError:
                print("   Please enter a valid number")
    
    def run(self):
        self.display_welcome()
        
    
        if not LoginSystem.authenticate():
            print("\n[ERROR] Authentication failed. Exiting...")
            return
        
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == 1:
                self.load_dataset()
            elif choice == 2:
                self.engine.run_publication_trends()
            elif choice == 3:
                self.engine.run_top_authors()
            elif choice == 4:
                self.engine.run_language_distribution()
            elif choice == 5:
                self.engine.run_publisher_analysis()
            elif choice == 6:
                self.engine.run_isbn_analysis()
            elif choice == 7:
                self.run_all_analyses()
            elif choice == 8:
                self.show_dataset_info()
            elif choice == 9:
                self.exit_app()
    
    def load_dataset(self):
        print("\n" + "=" * 60)
        print("  LOAD DATASET")
        print("=" * 60)
        
    
        default_file = "books.csv"
        file_path = input(f"  Enter CSV file path (default: {default_file}): ").strip()
        
        if not file_path:
            file_path = default_file
        
        if self.engine.load_dataset(file_path):
            self.is_loaded = True
            print("\n   Dataset loaded successfully!")
        else:
            print("\n   Failed to load dataset.")
    
    def run_all_analyses(self):
     
        if not self.is_loaded:
            print("\n  ️ Please load a dataset first!")
            return
        
        print("\n" + "=" * 60)
        print("  RUNNING ALL ANALYSES")
        print("=" * 60)
        
        analyses = [
            ("Publication Trends", self.engine.run_publication_trends),
            ("Top Authors", self.engine.run_top_authors),
            ("Language Distribution", self.engine.run_language_distribution),
            ("Publisher Analysis", self.engine.run_publisher_analysis),
            ("ISBN Analysis", self.engine.run_isbn_analysis)
        ]
        
        for name, func in analyses:
            print(f"\n[INFO] Running: {name}")
            func()
        
        print("\n   All analyses completed!")
    
    def show_dataset_info(self):
   
        print("\n" + "=" * 60)
        print("  DATASET INFORMATION")
        print("=" * 60)
        
        if not self.is_loaded:
            print("  No dataset loaded.")
            return
        
        data = self.engine.data
        print(f"  Total Records: {len(data)}")
        print(f"  Total Columns: {len(data.columns)}")
        print(f"\n  Columns:")
        for col in data.columns:
            print(f"    • {col}")
        
        print(f"\n  Data Types:")
        for col, dtype in data.dtypes.items():
            print(f"    • {col}: {dtype}")
        
        print(f"\n  Preview (first 3 rows):")
        print(data.head(3).to_string(index=False))
    
    def exit_app(self):
     
        print("\n" + "=" * 60)
        print("   Thank you for using Dream Book Shop Analysis!")
        print("   Goodbye!")
        print("=" * 60)
        self.running = False


def main():
  
    try:
        app = DreamBookShopApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n   Application terminated by user.")
        print("  Thank you for using Dream Book Shop Analysis!")
    except Exception as e:
        print(f"\n   An unexpected error occurred: {e}")
        print("  Please restart the application.")


if __name__ == "__main__":
    main()
