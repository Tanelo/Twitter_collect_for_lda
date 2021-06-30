import json
dict_twittos = json.load(open('list.json'))
our_list = list(dict_twittos.keys())
print(len(our_list))
