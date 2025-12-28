import pandas as pd

def extract_clients(csv_path: str) -> pd.DataFrame:
    '''
    Docstring for extract_clients
    
    :param csv_path: Description
    :type csv_path: str
    :return: Description
    :rtype: DataFrame
    '''
    df = pd.read_csv(csv_path) 
    return df

