import terminaltables as tt

''' 返回Ascii Table'''
def table(data,type='ascii'):
    type_dict = {
        'ascii':'AsciiTable',
        'single':'SingleTable',
        'double':'DoubleTable',
        'github':'GithubFlavoredMarkdownTable'
    }
    if type not in type_dict:
        type = 'ascii'
    func = type_dict[type]
    t = tt.func(data)
    # if type == 'ascii':
    #     t = tt.AsciiTable(data)
    # elif type == 'single':
    #     t = tt.SingleTable(data)
    # elif type == 'double':
    #     t = tt.DoubleTable(data)
    # elif type == 'github':
    #     t = tt.GithubFlavoredMarkdownTable(data)

    return t.table
