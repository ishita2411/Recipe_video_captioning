from nltk.translate import meteor
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from evaluate import load
bertscore = load("bertscore")
import json
import nltk
nltk.download('punkt')
nltk.download('wordnet')

def get_meteor_score(data, bard_captions):
  output = {}
  for key in bard_captions:
    input_captions = ""
    k=f'v_{key}'
    for i in data[k]['sentences']:
      input_captions = input_captions + i+'. '
    output[key] = meteor([word_tokenize(input_captions)],word_tokenize(bard_captions[key]))
  return output

def get_bleu_score(data, bard_captions):
  output = {}
  for key in bard_captions:
    input_captions = ""
    k=f'v_{key}'
    for i in data[k]['sentences']:
      input_captions = input_captions + i+'. '
    output[key] = sentence_bleu([word_tokenize(input_captions)],word_tokenize(bard_captions[key]))
  return output

def get_bert_score(data, bard_captions):
  output = {}
  for key in bard_captions:
    input_captions = ""
    k=f'v_{key}'
    for i in data[k]['sentences']:
      input_captions = input_captions + i+'. '
    output[key] =bertscore.compute(predictions=[bard_captions[key]], references=[input_captions], lang="en")
  return output