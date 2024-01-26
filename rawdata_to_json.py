import json


def text_to_json(input_file,output_file):

    json_output = []

    with open(input_file,encoding='utf-8') as f:

        items = f.read().split("Sentence:")
        determiner = "Some"

        for item in items:
            no_whitespaces = [item_a for item_a in item.split("\n") if item_a]
            try:
                sentence = no_whitespaces[0]
                drg_a = [item for item in no_whitespaces[1:] if not item.isspace()]
                drg = [item for item in drg_a if len(item)> 10]
                json_item = {'sentence': sentence,
                             'determiner': determiner,
                            'drg': drg}
                json_output.append(json_item)
                for item in drg_a:
                    if len(item) < 10:
                        determiner = item
            except IndexError:
                continue
    
    with open(output_file,'w',encoding='utf-8') as w:
        json.dump(json_output,w,indent=4)
            

text_to_json("testSet.txt","testSet.json")