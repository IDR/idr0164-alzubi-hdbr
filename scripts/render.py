import omero
from omero.cli import cli_login
from omero.gateway import BlitzGateway
import pandas
import re
import os
import yaml

"""
Create rendering settings yml files from the rendering.csv file
"""

def get_settings(dataset_name, image_name):
    image_name_c = clean_image_name(image_name)
    df = pandas.read_csv("../rendering.csv", dtype=str)
    for index, row in df.iterrows():
        ds_name = row["Dataset Name"]
        img_name = row["Image Name"]
        img_name_c = clean_image_name(img_name)
        if ds_name != dataset_name:
            continue
        if img_name_c in image_name_c:
            return (row)
    return None


def clean_image_name(img_name):
    img_name = os.path.splitext(img_name)[0]  # Remove file extension
    return re.sub(r'[^\w\d]', '', img_name)


def save_yml(dataset_name, image_name, row):
    result = {"channels": {}}
    for index in range(1, 5):
        channel = get_channel_yml(row, index)
        if channel:
            result["channels"][index] = channel
    result["greyscale"] = False
    result["version"] = 2

    os.makedirs(dataset_name, exist_ok=True)
    if '||' in image_name:
        print("WARNING: Image name contains ||: ", image_name)
    image_name_escaped = image_name.replace('/', '||')
    yml_path = f"{dataset_name}/{image_name_escaped}.yml"
    with open(yml_path, "w") as f:
        yaml.dump(result, f)
    

def get_channel_yml(row, index):
    color_key = f"channel{index}_color"
    if color_key not in row or pandas.isna(row[color_key]):
        return None
    channel_info = {
        "color": row[f"channel{index}_color"],
        "start": row[f"channel{index}_min"],
        "end": row[f"channel{index}_max"],
        "active": True
        }
    res = {index: channel_info}
    return channel_info


with omero.cli.cli_login() as c:
    conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
    project = conn.getObject("Project", attributes={'name': 'idr0164-alzubi-hdbr/experimentA'})
    for dataset in project.listChildren():
        for image in dataset.listChildren():
            from_csv = get_settings(dataset.getName(), image.getName())
            if from_csv is not None:
                save_yml(dataset.getName(), image.getName(), from_csv)
