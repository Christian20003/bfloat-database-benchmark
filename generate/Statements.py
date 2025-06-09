STATEMENT = '''
    WITH data(val) AS (SELECT 0.5::{}) SELECT * FROM data, generate_series({});
'''