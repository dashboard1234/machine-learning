from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import urllib.request
from bs4 import BeautifulSoup
import PyPDF2

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in list(freq.keys()):
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)

def get_only_text(url):
    page = urllib.request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page)
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text

#pdfFile = urllib.request.urlopen('http://localhost:48224/product/pdf/RL44955', 'rb')
pdfFile = urllib.request.urlopen('https://www.usatoday.com/story/news/nation/2018/06/29/capital-gazette-shooting/744864002/').read()
# pdfReader = PyPDF2.PdfFileReader(pdfFile)
# pages = pdfReader.numPages

feed = BeautifulSoup(pdfFile.decode('utf8'))
to_summarize = map(lambda p: p.text, feed.find_all('guid'))

fs = FrequencySummarizer()
# for article_url in to_summarize[:5]:
#     title, text = get_only_text(article_url)
#     print('----------------------------------')
#     print(title)
#     for s in fs.summarize(text, 2):
#         print('*',s)  

#title, text = get_only_text('http://www.businessinsider.com/trump-leave-world-trade-organization-wto-2018-6')
title, text = get_only_text('https://www.politico.com/story/2018/06/29/white-house-prank-call-bob-menendez-687897')
print('----------------------------------')
print(title)
#print(text)
print("############################ Summary ###############################")
for s in fs.summarize(text, 2):
    print('*',s)  