class ReportDataKeys:
    red = "red"
    green = "green"
    blue = "blue"
    amount = "amount"
    avg = "avg"
    sum = "sum"
    min = "min"
    max = "max"
    rabbit_consumed = "rabbit_consumed"
    mysql_red = "mysql_red"
    mysql_green = "mysql_green"
    mysql_blue = "mysql_blue"
    mysql_total = "mysql_total"


select_report_data_query = "select(select count(order_id) from order_records as w where (select count(order_id) from order_records as q where q.order_id=w.order_id group by order_id)=1 and status in(3,4,5)) as red1,(select count(order_id) from order_records as w where (select count(order_id) from order_records as q where q.order_id=w.order_id group by order_id)=2 and (select count(order_id) from order_records as r where r.order_id=w.order_id and status=1)=0) as red2,(select count(order_id) from order_records as w where (select count(order_id) from order_records as q where q.order_id=w.order_id group by order_id)=1 and status=1) as blue1,(select count(order_id) from order_records as w where (select count(order_id) from order_records as q where q.order_id=w.order_id group by order_id)=2 and (select count(order_id) from order_records as r where r.order_id=w.order_id and status in(3,4,5))=0) as blue2,(select count(order_id) from order_records as w where (select count(order_id) from order_records as q where q.order_id=w.order_id group by order_id)=3) as green,(select count(order_id) from order_records) as total;"
