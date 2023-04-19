import matplotlib.pyplot as plt
import json
import os

def plot_yearly_clusters(img_out_dir: str, json_out_file: str, extension: str = "png") -> None:
    """
    this plots the number of movies in each year buckets

    Parameters
    ----------
    img_out_dir: str
        the directory where the image should be stored. DO NOT INCLUDE IMAGE NAME

    json_out_file: str
        the file to store the data used to make the plot
    
    extension: str [optional] default = png
        format to save image as 
    """
    with open(json_out_file, "r") as f:
        json_content = f.read()

    json_data = dict(json.loads(json_content))
    bottom_offset = 0.28
    length, width = 6, 5
    fig = plt.figure(figsize=(length, width))
    bar_width = (width - bottom_offset)/len(json_data.keys()) * 1.8
    plt.bar(json_data.keys(), json_data.values(), color="purple", width = bar_width)
    plt.xticks(rotation="vertical")
    plt.subplots_adjust(bottom=bottom_offset)
    plt.title("NUMBER OF MOVIES COLLECTED FOR A RANGE OF YEARS")
    plt.xlabel("Year Ranges")
    plt.ylabel("Number of movies")
    plt.gca()
    os.mkdir(img_out_dir) if not os.path.exists(img_out_dir) else None
    plt.savefig(f"{img_out_dir}yearly_clusters_image.{extension}")


if __name__ == "__main__":
    plot_yearly_clusters("Metacritic/Statistics/images/", "Metacritic/Statistics/json/year_clusters.json")
