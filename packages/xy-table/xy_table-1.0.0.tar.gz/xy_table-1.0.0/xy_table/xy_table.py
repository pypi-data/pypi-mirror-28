import terminaltables as tt

''' 返回Ascii Table'''
def table(data,type='single'):
    if type == 'ascii':
        t = tt.AsciiTable(data)
    elif type == 'single':
        t = tt.SingleTable(data)
    elif type == 'double':
        t = tt.DoubleTable(data)
    elif type == 'github':
        t = tt.GithubFlavoredMarkdownTable(data)

    return t.table
