WITH A(rowIndex, columnIndex, val) AS (SELECT * FROM matrixa),
    B(rowIndex, columnIndex, val) AS (SELECT * FROM matrixb),
    v(rowIndex, val) AS (SELECT rowIndex, val FROM vectorv)
    SELECT A.rowIndex AS rowIndex, SUM(A.val * B.val * v.val) AS val
    FROM A, B, v
    WHERE A.columnIndex = B.columnIndex AND B.rowIndex = v.rowIndex
    GROUP BY A.rowIndex
    ORDER BY A.rowIndex;