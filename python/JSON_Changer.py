import json

input_file = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Export v2 project - Colony_Counter - 7_19_2024.ndjson'
output_file = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Export v2 project - Colony_Counter - 7_19_2024 - 복사본.json'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    data = [json.loads(line) for line in infile]
    json.dump(data, outfile, indent=4)
