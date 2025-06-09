STATEMENT_1 = '''
    WITH data(val) AS (SELECT 0.5::{}) SELECT * FROM data, generate_series(0, {});
'''

STATEMENT_2_D = '''
    SELECT repeat([0.5::{}], {});
'''

STATEMENT_2_U = '''
    SELECT array_fill(0.5::{}, array[{}]);
'''