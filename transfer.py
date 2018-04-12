import json
import codecs

def transfer(fpath_in="./examples/chatito_output.json",
             fpath_out="./examples/chatito_output_chn.json"):

    fin = codecs.open(fpath_in, 'r', 'utf8').read()
    if fin.startswith(u'\ufeff'):
        fin = fin.encode('utf8')[3:].decode('utf8')
    inp_data = json.loads(fin)

    rasa_nlu_data = inp_data['rasa_nlu_data']
    regex_features = rasa_nlu_data['regex_features']
    entity_synonyms = rasa_nlu_data['entity_synonyms']
    common_examples = rasa_nlu_data['common_examples']

    new_common_examples = list()

    for exmp in common_examples:
        exmp_text = "".join(exmp['text'].split(" "))
        exmp_intent = exmp['intent']
        exmp_entities = exmp['entities']

        new_exmp_entities = list()

        start_with_entity = 0

        for idx, entity in enumerate(exmp_entities):
            if idx == 0:
                if entity['start'] > 0:
                    start_with_entity = 1

            new_exmp_entities.append({"start": (entity['start'] - (2 * idx + start_with_entity)),
                                      "end": (entity['end'] - (2 * idx + start_with_entity)),
                                      "value": entity['value'],
                                      "entity": entity['entity']})


        new_common_examples.append({
            "text": exmp_text,
            "intent": exmp_intent,
            "entities": new_exmp_entities
        })

    new_rasa_nlu_data = {"regex_features": regex_features,
                         "entity_synonyms": entity_synonyms,
                         "common_examples": new_common_examples}

    json.dump({"rasa_nlu_data": new_rasa_nlu_data}, open(fpath_out, 'w'), ensure_ascii=False, indent=4)


if __name__ == "__main__":
    transfer("./examples/chatito_output_chn.json", "./examples/chatito_output_chn2.json")