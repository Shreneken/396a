import os 
import json
import shutil

imdb_src_path = './imdb/imdb_movie_jsons'
rt_src_path = './RottenTomatoes/rt_movie_jsons'
metacritic_src_path = './Metacritic/metacritic_movies_json'
merged_src_path = './MergedData/merged_movie_jsons'


def copy_from_imdb():
    shutil.copytree(imdb_src_path, merged_src_path)

def get_from_meta():
    for date_dir in os.listdir(metacritic_src_path):
        if date_dir not in os.listdir(merged_src_path):
            shutil.copytree(f'{metacritic_src_path}/{date_dir}', f'{merged_src_path}/{date_dir}')
def get_from_rt():
    for date_dir in os.listdir(rt_src_path):
        if date_dir not in os.listdir(merged_src_path):
            shutil.copytree(f'{rt_src_path}/{date_dir}', f'{merged_src_path}/{date_dir}')

def merge_only_meta_and_rt():
    for date_dir in os.listdir(merged_src_path):
        if date_dir not in os.listdir(imdb_src_path):
            if date_dir in os.listdir(rt_src_path) and date_dir in os.listdir(metacritic_src_path):
                for movie_file in os.listdir(f'{merged_src_path}/{date_dir}'):
                    with open(f'{merged_src_path}/{date_dir}/{movie_file}', 'r') as curr1:
                        print(f'{merged_src_path}/{date_dir}/{movie_file}')
                        curr_data = json.load(curr1)
                    try:
                        with open(f'{rt_src_path}/{date_dir}/{movie_file}', 'r') as curr2:
                            src_data = json.load(curr2)
                        curr_data[f'rt_rating'] = src_data['rating']
                        curr_data['num_reviews'] += src_data['num_reviews']
                        # Avoiding for RT due to languages considered in genre: 
                        curr_data[f'rt_summary'] = src_data['summary']
                        curr_data['reviews'].extend(src_data['reviews'])
                        with open(f'{merged_src_path}/{date_dir}/{movie_file}', 'w') as curr3:
                            json.dump(curr_data, curr3, indent=4)
                    except:
                        continue


def add_from_src(src):
    src_path = rt_src_path if src=='rt' else metacritic_src_path if src =='meta' else 'INVALID'
    if src_path == 'INVALID': return print('INVALID')
    for date_dir in os.listdir(merged_src_path):  
        for movie_file in os.listdir(f'{merged_src_path}/{date_dir}'):
            with open(f'{merged_src_path}/{date_dir}/{movie_file}', 'r') as curr1:
                print(f'{merged_src_path}/{date_dir}/{movie_file}')
                curr_data = json.load(curr1)
            try:
                with open(f'{src_path}/{date_dir}/{movie_file}', 'r') as curr2:
                    src_data = json.load(curr2)
                curr_data[f'{src}_rating'] = src_data['rating']
                curr_data['num_reviews'] += src_data['num_reviews']
                # Avoiding for RT due to languages considered in genre: 
                if src != 'rt':
                    curr_data['genres'].extend([genre for genre in src_data['genres'] if genre not in curr_data['genres']])
                curr_data[f'{src}_summary'] = src_data['summary']
                curr_data['reviews'].extend(src_data['reviews'])
                with open(f'{merged_src_path}/{date_dir}/{movie_file}', 'w') as curr3:
                    json.dump(curr_data, curr3, indent=4)
            except:
                continue
                

if __name__ == '__main__':
    # copy_from_imdb()
    # add_from_src('rt')
    # add_from_src('meta')
    # get_from_rt()
    # merge_only_meta_and_rt()
    print('Already Merged Successfully!')

