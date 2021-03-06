# importing the Dataset

import pandas as pd
import pickle

messages = pd.read_csv('spam.csv', encoding='ISO-8859-1')

#Data cleaning and preprocessing
import re
import nltk
nltk.download()
nltk.data.path.append('C:/Users/Sazid/Desktop/yati/Projects/NLP/NLP-Deployment-Heroku-master/NLP-Deployment-Heroku-master/flask\nltk_data')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
corpus = []
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['message'][i])
    review = review.lower()
    review = review.split()
    
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)
    
    
# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2500)
X = cv.fit_transform(corpus).toarray()

pickle.dump(cv, open('transform.pkl','wb'))


y=pd.get_dummies(messages['class'])
y=y.iloc[:,1].values


# Train Test Split

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Training model using Naive bayes classifier

from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(X_train, y_train)

y_pred=spam_detect_model.predict(X_test)


#pickle file
file = 'nlp.model.pkl'
pickle.dump(spam_detect_model, open(file, 'wb'))