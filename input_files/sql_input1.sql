        SELECT bc.firstname, bc.lastname "Last Name", b.title, TO_CHAR(bo.orderdate, 'MM/DD/YYYY') "Order Date", p.publishername
FROM finance_sche.book_customer bc, books b, book_order bo, publisher p
WHERE(publishername = 'PRINTING IS US') and bc.book_customer like 'KZ%';
SELECT bc.firstname, bc.lastname, b.title, 
TO_CHAR(bo.orderdate, 'MM/DD/YYYY') "Order Date", p.publishername
FROM book_customer bc, books b, book_order bo, publisher p WHERE(publishername = 'PRINTING IS US') and bc.book_customer like 'KZ%';