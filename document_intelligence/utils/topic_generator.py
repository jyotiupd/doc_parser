from nltk.tokenize import sent_tokenize
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

class Topic_gen:
    def __init__(self):
        self.wordnet=WordNetLemmatizer()
        self.tfidf=TfidfVectorizer()
        self.svd = TruncatedSVD(n_components=10,random_state=30)

    def clean_text(self,text):
        no_punc=[char for char in text if char not in string.punctuation]
        no_punc="".join(no_punc)
        no_num=re.sub(r'\d+','',no_punc)
        clean=[self.wordnet.lemmatize(word.lower()) for word in no_num.split() if word.lower() not in stopwords.words('english')]
        clean=' '.join(clean)
        return clean

    def  create_topic(self,text):
        cleaned_tokens = self.clean_text(text)
        vectors=self.tfidf.fit_transform([cleaned_tokens]).toarray()
        corpus_svd = self.svd.fit(vectors)
        feature_scores = dict(
                zip(
                    self.tfidf.get_feature_names(),
                    corpus_svd.components_[0]
                )
            )
        topic_output = sorted(
                feature_scores, key=feature_scores.get, reverse=True
                )
        return topic_output


if __name__ == "__main__":
    text = """Rate Code Explanations
    RS
    Residential service for a single family dwelling
    Residential service for a single family dwelling with electric water heating
    RH Residential service for a single family dwelling with electric heat
    CW
    Controlled electric water heating
    SS
    Secondary service small (General Service)
    SH Secondary service for electric heat (May have electric water heating and electric air conditioning combined with electric heat)
    UW Uncontrolled electric water heating only
    For Large Commercial & Industrial rate information, please visit aesindiana.com. If you have questions concerning your rate classification, please call 317-261-8222.
    Meter Use Explanations
    P
    kWh Delivered Register (Permanent Service)
    """
    s = Topic_gen()
    topics = s.create_topic(text)