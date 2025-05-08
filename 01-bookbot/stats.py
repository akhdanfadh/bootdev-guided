def get_num_words(text):
    return len(text.split())

def get_num_chars(text):
    text = text.lower()
    result = {}
    for char in text:
        if char in result:
            result[char] += 1
        else:
            result[char] = 1
    return result

def sort_on(dict):
    return dict["num"]

def sort_num_chars(char_dict):
    result = []
    for char, num in char_dict.items():
        result.append({"char": char, "num": num})
    result.sort(reverse=True, key=sort_on)
    return result
