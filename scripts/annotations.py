import csv
import os

def read_csv_to_dict(input_file):
    """Read CSV file and return list of dictionaries."""
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def process_ndpi_rows(data):
    """Duplicate rows where Image Name ends with ndpi."""
    processed_data = []
    for row in data:
        if row['Image Name'].endswith('.ndpi'):
            main = row.copy()
            main['Image Name'] = row['Image Name'].replace('.ndpi', '.ndpi [0]')
            processed_data.append(main)
            macro = row.copy()
            macro['Image Name'] = row['Image Name'].replace('.ndpi', '.ndpi [macro image]')
            processed_data.append(macro)
            mask = row.copy()
            mask['Image Name'] = row['Image Name'].replace('.ndpi', '.ndpi [macro mask image]')
            processed_data.append(mask)
        else:
            processed_data.append(row)
    return processed_data

def write_dict_to_csv(data, output_file):
    """Write list of dictionaries to CSV file."""
    if not data:
        return
    
    fieldnames = data[0].keys()
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    # Define input and output paths
    input_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                             'experimentA', 'idr0164-experimentA-annotation.csv')
    output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              'experimentA', 'idr0164-experimentA-annotation-2.csv')
    
    # Read CSV as dictionary
    data = read_csv_to_dict(input_file)
    
    # Duplicate rows where Image Name ends with ndpi
    processed_data = process_ndpi_rows(data)
    
    # Write processed data to new CSV
    write_dict_to_csv(processed_data, output_file)

if __name__ == "__main__":
    main()