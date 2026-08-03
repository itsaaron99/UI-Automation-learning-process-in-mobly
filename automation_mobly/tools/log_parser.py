"""
LogParser

This parser will be activated after executing the GitHub action workflow (CI).
Which will provide a dash board that shows the test details and figues.

Args:
    File: The test_summary.yaml file, which will automatically created by Mobly on Github actions 

Dependencies:

Core Functions:

"""

import yaml
import pandas as pd

class LogParser:
    def __init__(self, file: str):
        self.file = file

    def parse_mobly_summary(self) -> list:
        parsed_data = []

        with open(self.file, 'r', encoding='utf-8') as f:
            records = yaml.safe_load_all(f)
            for item in records:
                if item.get('Type') == 'Record':
                    test_name = item.get('Test Name')
                    test_result = item.get('Result')
                    begin_time = item.get('Begin Time')
                    end_time = item.get('End Time')
                    duration = (end_time - begin_time) / 1000 # seconds
                    extra_errors = item.get('Extra Errors')

                    parsed_data.append({
                        'test_name': test_name,
                        'test_result': test_result,
                        'begin_time': begin_time,
                        'end_time': end_time,
                        'duration': duration,
                        'extra_errors': extra_errors,
                    })

        return parsed_data

    def to_dataframe(self) -> pd.DataFrame:
        data = self.parse_mobly_summary()
        return pd.DataFrame(data)

    def export_csv(self, output_path: str) -> str:
        df = self.to_dataframe()
        df.to_csv(output_path, index=False)
        return output_path

if __name__ == '__main__':
    # test for the dashboard
    parser = LogParser("C:/Users/pata2/OneDrive/Desktop/mobly/Google_Mobly_TestBed/latest/test_summary.yaml")
    
    # 1. Test dataframe transfer
    df = parser.to_dataframe()
    print("--- DataFrame preview ---")
    print(df)
    
    # 2. Test the count fuctions
    print("\n--- Sum of test result ---")
    print(df['test_result'].value_counts())
    
    # 3. Test csv output
    csv_path = parser.export_csv("summary_report.csv")
    print(f"\noutput CSV to: {csv_path}")