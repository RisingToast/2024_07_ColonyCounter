import json

def read_ndjson(file_path):
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
    return data

def convert_to_coco_format(ndjson_data, output_file):
    # Your conversion logic here
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Example code for conversion (you will need to adapt this)
    for item in ndjson_data:
        image_info = {
            "id": item["data_row"]["id"],
            "file_name": item["data_row"]["external_id"],
            "height": item["media_attributes"]["height"],
            "width": item["media_attributes"]["width"]
        }
        coco_data["images"].append(image_info)

        for label in item["projects"]["clynqj52408k707zxhge54g8q"]["labels"]:
            for obj in label["annotations"]["objects"]:
                annotation = {
                    "id": obj["feature_id"],
                    "image_id": item["data_row"]["id"],
                    "category_id": 1,  # Update based on your category mapping
                    "bbox": [
                        obj["bounding_box"]["left"],
                        obj["bounding_box"]["top"],
                        obj["bounding_box"]["width"],
                        obj["bounding_box"]["height"]
                    ],
                    "area": obj["bounding_box"]["width"] * obj["bounding_box"]["height"],
                    "iscrowd": 0
                }
                coco_data["annotations"].append(annotation)

    with open(output_file, 'w') as f:
        json.dump(coco_data, f, indent=4)

if __name__ == "__main__":
    ndjson_data = read_ndjson('C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson')
    convert_to_coco_format(ndjson_data, 'C:/kkt/2024_07_ColonyCounter/JSON_File/output_file.json')
