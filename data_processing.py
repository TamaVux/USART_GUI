# Data recive form USART will byte a time


# Turn a list of 1 character in to list of useable data
def data_processing(rawdata):
    sep_char = '-'   

    string = ''.join([str(elem) for elem in rawdata])
    try:
        format_data = list(string.split(sep_char))
    except:
        pass

    return format_data[:-1]    # lastest data is ignore

def string_to_float(data):
    return [float(x) for x in data]