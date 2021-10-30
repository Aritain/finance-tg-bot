from settings import MAX_INPUT_LEN

def validate_input(input):
    input = input.replace(',','.')
    if len(input) > MAX_INPUT_LEN:
        return False
    try:
        input = float(input)
    except (ValueError, TypeError):
        return False
        
    return format(input, '.2f')

def compile_message(data, text):
    message = f'{text}\n\n'
    for key, value in data.items():
        fomatted_value = format(value, '.2f')
        message += f'{key}: {fomatted_value}\n'
    return message
    