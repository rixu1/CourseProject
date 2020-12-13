import spacy
import os,codecs

nlp = spacy.load('en_core_web_md')


def num_there(s):
    return any(i.isdigit() for i in s)


def apply_name_rule(name):
    if "Ave" in name:
        return False
    if num_there(name):
        return False
    return True


def main(bio_dir, name_path):
    names = []
    for i in range(6525):
        with codecs.open(os.path.join(bio_dir, str(i) + '.txt'), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            sents = nlp(text)
            name = ''
            for ee in sents.ents:
                if ee.label_ == 'PERSON':
                    is_name = apply_name_rule(str(ee))
                    if is_name:
                        name = str(ee)
            name = name.strip()
            names.append(name)
            print (i, name)
    with open(name_path, 'w') as f:
        for name in names[:-1]:
            f.write(name)
            f.write('\n')
        f.write(names[-1])

# def expand_person_entities(doc):
#     new_ents = []
#     for ent in doc.ents:
#         # Only check for title if it's a person and not the first token
#         if ent.label_ == "PERSON":
#             if ent.start != 0:
#                 # if person preceded by title, include title in entity
#                 prev_token = doc[ent.start - 1]
#                 if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
#                     new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
#                     new_ents.append(new_ent)
#                 else:
#                     # if entity can be parsed as a date, it's not a person
#                     if dateparser.parse(ent.text) is None:
#                         new_ents.append(ent)
#         else:
#             new_ents.append(ent)
#     doc.ents = new_ents
#     return doc


if __name__ == '__main__':
    bio_dir = '../data/compiled_bios/'
    name_path = '../data/names_secondary.txt'
    main(bio_dir, name_path)
