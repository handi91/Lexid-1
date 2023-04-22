import json
import pandas
import stanza

# stanfordnlp.download('id')  # This downloads the Indonesian models for the neural pipeline
nlp = stanza.Pipeline(lang='id')  # This sets up a default neural pipeline in Indonesian
text = "Apa pertimbangan dalam membuat Peraturan Daerah Kabupaten Batang Nomor 7 Tahun 2010?"
text = "Apa asas penyelenggaraan penyuluhan pertanian, perikanan, kehutanan?"
doc = nlp(text)
# doc = nlp("rumah sakit yang didirikan oleh swasta dapat berupa rumah sakit dengan penanaman modal asing.")
# doc = nlp(
#     "pelayanan medik subspesialis sebagaimana dimaksud pada ayat (1) huruf c berupa pelayanan medik subspesialis dasar dan pelayanan medik subspesialis lain.")
relationships = []
for idx_sentence in range(len(doc.sentences)):
    for relation in doc.sentences[idx_sentence]._dependencies:
        relationship = {}
        word_source = relation[0]
        word_target = relation[2]
        relationship['sentence_id'] = idx_sentence
        relationship['source'] = {'text': word_source._text, 'word_type': word_source._upos,
                                  'word_feats': word_source._feats, 'xpos':word_source._xpos}
        relationship['target'] = {'text': word_target._text, 'word_type': word_target._upos,
                                  'word_feats': word_target._feats, 'xpos':word_target._xpos}
        relationship['rel_name'] = relation[1]
        relationships.append(relationship)

res = pandas.DataFrame(relationships)
print(json.dumps(relationships, indent=4))
print(res)
print(doc.sentences[0].print_dependencies())