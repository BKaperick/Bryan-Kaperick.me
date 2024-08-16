months = {
'Jan': 0,
'Feb': 1,
'Mar': 2,
'Apr': 3,
'May': 4,
'Jun': 5,
'Jul': 6,
'Aug': 7,
'Sep': 8,
'Oct': 9,
'Nov': 10,
'Dec': 11
}

invalid_key_chars = [r"<", r">", ",", ".", r"&rsquo;", "'", "-"]
def clean_key(w):
    for c in invalid_key_chars:
        w = w.replace(c,"")
    return w

def ordering(x):
    '''
    Only assumes that `year` exists.  After that, will further order on month,
    and `order_in_month` and `order_in_year` additional keys, if present.
    '''
    if 'month' in x[1] and x[1]['month'] in months:
        month = months[x[1]['month']]/1000
        if 'order_in_month' in x[1]:
            month += x[1]['order_in_month']/10000
    else:
        month = 0

    year = int(x[1]['year'])
    if 'order_in_year' in x[1]:
        year += x[1]['order_in_year']/100

    return -(year + month)

def order_photos(x):
    if 'month' in x[1] and x[1]['month'] in months:
        month = months[x[1]['month']]/1000
        if 'order_in_month' in x[1]:
            month += x[1]['order_in_month']/10000
    else:
        month = 0
    if 'order_in_year' in x[1]:
        year = int(x[1]['year']) + x[1]['order_in_year']/100
    else:
        year = 0
    return -(year + month)

