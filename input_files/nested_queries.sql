select 
    a.val1,
    a.val2,
    (
        select 
            * 
        from 
        (
            select 
                b.val1
            from 
                tb2 b
            where 
                b.val2 < a.val3 and b.val3 = a.val4
            order by 
                b.val2 desc 
        ) 
        where rownum = 1
    ) as someName
from
    tb1 a;