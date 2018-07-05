from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
#from tika import parser

import PyPDF2

ps = PorterStemmer()

pdfFileObj = open('.\\notebooks\\pdf.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pages = pdfReader.numPages
#pageObj = pdfReader.getPage(0)
text = ''
print(pdfReader.numPages)
for page in range(pages):
    pageObj = pdfReader.getPage(page)
    text += pageObj.extractText()
#text = pageObj.extractText()

print(text)
pdfFileObj.close()
# text = "Video provides a powerful way to help you prove your point. When you click Online Video, you"\
# +"can paste in the embed code for the video you want to add. You can also type a keyword to search"\
# +"online for the video that best fits your document. To make your document look professionally"\
# +"produced, Word provides header, footer, cover page, and text box designs that complement each"\
# +"other. For example, you can add a matching cover page, header, and sidebar. Click Insert and then"\
# +"choose the elements you want from the different galleries. Themes and styles also help keep your"\
# +"document coordinated. When you click Design and choose a new Theme, the pictures, charts, and"\
# +"SmartArt graphics change to match your new theme. When you apply styles, your headings"\
# +"change to match the new theme. Save time in Word with new buttons that show up where you"\
# +"need them."

stopWords = set(stopwords.words("english"))
words = word_tokenize(text)

freqTable = dict()
for word in words:
    word = word.lower()
    word = ps.stem(word)
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

sentences = sent_tokenize(text)
sentenceValue = dict()

# for sentence in sentences:
#     for wordValue in freqTable:
#         if wordValue[0] in sentence.lower():
#             if sentence[:10] in sentenceValue:
#                 print(sentence[:10], wordValue[1])
#                 sentenceValue[sentence[:10]] += wordValue[1]
#             else:
#                 sentenceValue[sentence[:10]] = wordValue[1]

for sentence in sentences:
     for index, wordValue in enumerate(freqTable, start=1):
          if wordValue in sentence.lower(): # index[0] return word
               if sentence in sentenceValue:  
                    sentenceValue[sentence] += index # index return value of occurence of that word
                    #sentenceValue.update({sentence: index})
                    #print(sentenceValue)
               else:
                   # sentenceValue[sentence] = wordValue
                    sentenceValue[sentence] = index
                    #print(sentenceValue)                

sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

average = int(sumValues / len(sentenceValue))

summary = ''
for sentence in sentences:
    # if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (1.5 * average):
    if sentence in sentenceValue and sentenceValue[sentence] > (1.5 * average):
        summary += " " + sentence
print("###########")
print(summary)

