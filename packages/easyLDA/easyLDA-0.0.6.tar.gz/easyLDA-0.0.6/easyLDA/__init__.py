try:
    import nltk
    nltk.download("stopwords")
except:
    'stopword data downloaded already'
    
from .base import PipelineLDA, main



def main():
    print 'executing...'
    main()

