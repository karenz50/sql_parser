SELECT bc.firstname "First Name", bc.lastname, b.title, TO_CHAR(bo.orderdate, 'MM/DD/YYYY') "Order Date", p.publishername FROM finance_sche.book_customer bc, books b, book_order bo, publisher p WHERE firstname in ('tom', 'sarah', 'karen');
SELECT bc.firstname "First Name", bc.lastname, b.title, TO_CHAR(bo.orderdate, 'MM/DD/YYYY') "Order Date", p.publishername FROM finance_sche.book_customer bc, books b, book_order bo, publisher p WHERE bc like 'KZ%' or book_customer = "Yay";
SELECT bc.firstname "First Name", bc.lastname, b.title, TO_CHAR(bo.orderdate, 'MM/DD/YYYY') "Order Date", p.publishername FROM finance_sche.book_customer bc, books b, book_order bo, publisher p WHERE(firstname in ('tom', 'sarah', 'karen')) and (bc like 'KZ%' or book_customer = "Yay");