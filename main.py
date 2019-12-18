import os

from dotenv import load_dotenv
load_dotenv('.env')
RESULT_DIR = os.environ.get('RESULT_DIR')

from api_utils import APIConnector
from model_builder import ModelBuilder


def run_generation(
    api_connector,
    model_builder,
    i_generation,
):
    population = api_connector.get_population(i_generation)
    model_builder.update_population(population)
    model_builder.learn_mpm()

    mpm_path = os.path.join(RESULT_DIR, f'mpm{i_generation:03d}.txt')
    model_builder.save_mpm(mpm_path)
    ret = api_connector.post_mpm(filename=mpm_path, i_generation=i_generation)

    should_end = (ret['max_fitness'] == 100)
    if should_end:
        with open(os.path.join(RESULT_DIR, 'optimum.txt'), 'w') as f:
            f.write(f"{ret['best_chromosome']}\n")
    print(f'mpm size: {len(model_builder.registered_bbs)}')
    print(ret)
    return should_end


if __name__ == '__main__':
    STUDENT_ID = os.environ.get('STUDENT_ID')
    print(f'Running student_id: {STUDENT_ID}')
    if not os.path.isdir(RESULT_DIR):
        print(f'Making folder for results: {RESULT_DIR}')
        os.mkdir(RESULT_DIR)
    else:
        print(f'Result folder already exists, abort. {RESULT_DIR}')
        exit()

    should_end = False
    i_generation = 0
    api_connector = APIConnector(
        api_url=os.environ.get('API_URL'),
        student_id=STUDENT_ID,
    )
    model_builder = ModelBuilder()

    while not should_end:
        if i_generation > 50:
            print('Too many generations, abort.')
            exit()
        print(f'Running generation {i_generation}...')
        should_end = run_generation(api_connector, model_builder, i_generation)
        i_generation += 1
