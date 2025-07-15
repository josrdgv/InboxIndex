import nltk

# Force download + verify access path
nltk.download('punkt')
nltk.data.path.append(r"C:\Users\Jotten Ben John\AppData\Roaming\nltk_data")

from nltk.tokenize import sent_tokenize

sample = "Enron was once a giant. Now it's a scandal."
print(sent_tokenize(sample))
