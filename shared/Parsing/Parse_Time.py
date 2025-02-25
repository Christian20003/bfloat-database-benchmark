import json

def parse_time_metrics(output: str) -> dict:
    '''
    This function parses the output of the database into a python processible structure
    by extracting the produced json object containing all necessary time metrics.

    :param output: The output string from the database executable.

    :return: A dictionary which contains every time metric.
    '''
    print('Parse the output into correct format')
    output = output.decode('utf-8')
    start = output.index('{')
    json_str = output[start:]
    json_str = json_str.replace('\t', ' ').replace('\n', ' ').replace(' ', '')
    json_obj = json.loads(json_str)
    return json_obj