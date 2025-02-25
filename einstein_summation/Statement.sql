WITH A(rowIndex, columnIndex, val) AS (SELECT * FROM MatrixA),
    B(rowIndex, columnIndex, val) AS (SELECT * FROM MatrixB),
    v(rowIndex, val) AS (SELECT rowIndex, val FROM VectorV)
    SELECT A.rowIndex AS rowIndex, SUM(A.val * B.val * v.val) AS val
    FROM A, B, v
    WHERE A.columnIndex = B.columnIndex AND B.rowIndex = v.rowIndex
    GROUP BY A.rowIndex
    ORDER BY A.rowIndex;