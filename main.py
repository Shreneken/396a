import typer
import os 
import json

app = typer.Typer()
SRC_PATH = "./MergedData/merged_movie_jsons"


@app.command()
def vibes(title: str, release_year: str):
    for movie in os.listdir(f'{SRC_PATH}/{release_year}'):
        with open(f'{SRC_PATH}/{release_year}/{movie}', 'r') as get_movie:
            curr = json.load(get_movie)
        if curr['title'] == title:
            print(curr['vibes'])
            return
    print("Couldn't find given movie")

@app.command()     
def all(title:str, release_year: str):
    for movie in os.listdir(f'{SRC_PATH}/{release_year}'):
        with open(f'{SRC_PATH}/{release_year}/{movie}', 'r') as get_movie:
            curr = json.load(get_movie)
        if curr['title'] == title:
            print(f"Title: {curr['title']}")
            print(f"Rating: {curr['rating']}")
            print(f"Release date: {curr['release_date']}")
            print(f"Reviews count: {curr['num_reviews']}")
            if len(curr['summary']) > 0: print(f"Summary: {curr['summary']}")
            print(f"Vibes: {curr['vibes']}")
            return 
    print("Couldn't find given movie")
    

if __name__ == "__main__":
    app()

