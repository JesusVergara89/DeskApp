import pandas as pd

def calculate_statistics(column_data):
    stats = {}
    
    # Convertir la columna a un DataFrame si no lo es ya
    if not isinstance(column_data, pd.Series):
        column_data = pd.Series(column_data)
    
    stats['Mean'] = column_data.mean()
    stats['Variance'] = column_data.var()
    stats['Std Dev'] = column_data.std()
    stats['25th Percentile'] = column_data.quantile(0.25)
    stats['50th Percentile (Median)'] = column_data.quantile(0.50)
    stats['75th Percentile'] = column_data.quantile(0.75)
    
    return stats
