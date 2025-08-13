def STATEMENT_2_PARAM(db_name: str):
  if db_name == 'postgres':
    return '''
      WITH RECURSIVE gd (idx, a, b) AS (
      SELECT * FROM gd_start
      UNION ALL
      (WITH current_gd (idx, a, b) AS (
          SELECT * FROM gd
          ), subresult (idx, a, b) AS (
          SELECT idx, a - {} * {}(2 * x1 * (a * x1 + b - y)), b - {} * {}(2 * (a * x1 + b - y))
          FROM current_gd, points 
          GROUP BY idx, a, b
        )
        SELECT idx + 1, a{}, b{}
        FROM subresult
        WHERE idx < {}
        )
      )
      SELECT * FROM gd;'''
  else:
    return '''
      WITH RECURSIVE gd (idx, a, b) AS (
      SELECT * FROM gd_start
      UNION ALL
      SELECT idx+1, a - {} * {}(2 * x2 * (a * x2 + b * x1 - y)), b - {} * {}(2 * x1 * (a * x2 + b * x1 - y))
      FROM gd, points
      WHERE idx < {}
      GROUP BY idx, a, b
      )
      SELECT * FROM gd;
    '''

def STATEMENT_4_PARAM(db_name: str):
  if db_name == 'postgres':
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d) AS (
      SELECT * FROM gd_start
      UNION ALL
      (WITH current_gd (idx, a, b, c, d) AS (
          SELECT * FROM gd
          ), subresult (idx, a, b, c, d) AS (
          SELECT idx, 
                  a - {} * {}(2 * x3 * (a * x3 + b * x2 + c * x1 + d - y)), 
                  b - {} * {}(2 * x2 * (a * x3 + b * x2 + c * x1 + d - y)), 
                  c - {} * {}(2 * x1 * (a * x3 + b * x2 + c * x1 + d - y)), 
                  d - {} * {}(2 * (a * x3 + b * x2 + c * x1 + d - y))
          FROM current_gd, points 
          GROUP BY idx, a, b, c, d
        )
        SELECT idx + 1, a{}, b{}, c{}, d{}
        FROM subresult
        WHERE idx < {}
        )
      )
      SELECT * FROM gd;'''
  else:
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d) AS (
      SELECT * FROM gd_start
      UNION ALL
      SELECT idx+1,
              a - {} * {}(2 * x3 * (a * x3 + b * x2 + c * x1 + d - y)), 
              b - {} * {}(2 * x2 * (a * x3 + b * x2 + c * x1 + d - y)), 
              c - {} * {}(2 * x1 * (a * x3 + b * x2 + c * x1 + d - y)), 
              d - {} * {}(2 * (a * x3 + b * x2 + c * x1 + d - y))
      FROM gd, points
      WHERE idx < {}
      GROUP BY idx, a, b, c, d
      )
      SELECT * FROM gd;'''

def STATEMENT_6_PARAM(db_name: str):
  if db_name == 'postgres':
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d, e, f) AS (
      SELECT * FROM gd_start
      UNION ALL
      (WITH current_gd (idx, a, b, c, d, e, f) AS (
          SELECT * FROM gd
          ), subresult (idx, a, b, c, d, e, f) AS (
          SELECT idx, 
                 a - {} * {}(2 * x5 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
                 b - {} * {}(2 * x4 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
                 c - {} * {}(2 * x3 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
                 d - {} * {}(2 * x2 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
                 e - {} * {}(2 * x1 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
                 f - {} * {}(2 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y))
          FROM current_gd, points 
          GROUP BY idx, a, b, c, d, e, f
        )
        SELECT idx + 1, a{}, b{}, c{}, d{}, e{}, f{}
        FROM subresult
        WHERE idx < {}
        )
      )
      SELECT * FROM gd;'''
  else:
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d, e, f) AS (
      SELECT * FROM gd_start
      UNION ALL
      SELECT idx+1,
              a - {} * {}(2 * x5 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
              b - {} * {}(2 * x4 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
              c - {} * {}(2 * x3 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
              d - {} * {}(2 * x2 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
              e - {} * {}(2 * x1 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
              f - {} * {}(2 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y))
      FROM gd, points
      WHERE idx < {}
      GROUP BY idx, a, b, c, d, e, f
      )
      SELECT * FROM gd;'''

def STATEMENT_8_PARAM(db_name: str):
  if db_name == 'postgres':
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h) AS (
      SELECT * FROM gd_start
      UNION ALL
      (WITH current_gd (idx, a, b, c, d, e, f, g, h) AS (
          SELECT * FROM gd
          ), subresult (idx, a, b, c, d, e, f, g, h) AS (
          SELECT idx, 
                 a - {} * {}(2 * x7 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
                 b - {} * {}(2 * x6 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
                 c - {} * {}(2 * x5 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
                 d - {} * {}(2 * x4 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
                 e - {} * {}(2 * x3 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
                 f - {} * {}(2 * x2 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
                 g - {} * {}(2 * x1 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)),
                 h - {} * {}(2 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y))
          FROM current_gd, points
          GROUP BY idx, a, b, c, d, e, f, g, h
        )
        SELECT idx + 1, a{}, b{}, c{}, d{}, e{}, f{}, g{}, h{}
        FROM subresult
        WHERE idx < {}
        )
      )
      SELECT * FROM gd;'''
  else:
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h) AS (
      SELECT * FROM gd_start
      UNION ALL
      SELECT idx+1,
              a - {} * {}(2 * x7 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
              b - {} * {}(2 * x6 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
              c - {} * {}(2 * x5 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
              d - {} * {}(2 * x4 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
              e - {} * {}(2 * x3 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
              f - {} * {}(2 * x2 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
              g - {} * {}(2 * x1 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)),
              h - {} * {}(2 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y))
      FROM gd, points
      WHERE idx < {}
      GROUP BY idx, a, b, c, d, e, f, g, h
      )
      SELECT * FROM gd;'''

def STATEMENT_10_PARAM(db_name: str):
  if db_name == 'postgres':
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
      SELECT * FROM gd_start
      UNION ALL
      (WITH current_gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
          SELECT * FROM gd
          ), subresult (idx, a, b, c, d, e, f, g, h, i, j) AS (
          SELECT idx, 
                 a - {} * {}(2 * x9 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 b - {} * {}(2 * x8 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 c - {} * {}(2 * x7 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 d - {} * {}(2 * x6 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 e - {} * {}(2 * x5 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 f - {} * {}(2 * x4 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 g - {} * {}(2 * x3 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 h - {} * {}(2 * x2 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
                 i - {} * {}(2 * x1 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)),
                 j - {} * {}(2 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y))
          FROM current_gd, points
          GROUP BY idx, a, b, c, d, e, f, g, h, i, j
        )
        SELECT idx + 1, a{}, b{}, c{}, d{}, e{}, f{}, g{}, h{}, i{}, j{}
        FROM subresult
        WHERE idx < {}
        )
      )
      SELECT * FROM gd;'''
  else:
    return '''
      WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
      SELECT * FROM gd_start
      UNION ALL
      SELECT idx+1,
              a - {} * {}(2 * x9 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              b - {} * {}(2 * x8 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              c - {} * {}(2 * x7 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              d - {} * {}(2 * x6 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              e - {} * {}(2 * x5 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              f - {} * {}(2 * x4 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              g - {} * {}(2 * x3 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              h - {} * {}(2 * x2 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
              i - {} * {}(2 * x1 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)),
              j - {} * {}(2 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y))
      FROM gd, points
      WHERE idx < {}
      GROUP BY idx, a, b, c, d, e, f, g, h, i, j
      )
      SELECT * FROM gd;'''