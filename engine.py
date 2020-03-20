from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import re

client = MongoClient("mongodb://karansawant:jeTX5ydaYRM3UwJE@covid-shard-00-00-1dr8b.mongodb.net:27017,covid-shard-00-01-1dr8b.mongodb.net:27017,covid-shard-00-02-1dr8b.mongodb.net:27017/test?ssl=true&replicaSet=covid-shard-0&authSource=admin&retryWrites=true&w=majority")
dbData = client['dataManager']
dbPheremones = dbData.pheremones
dbraw = dbData.raw

pheremone = dbPheremones.find({"site": "equishell"})
pheremone = pheremone.next()
pheremone = pheremone["data"]
raw = dbraw.find({"site": "equishell"})
raw = raw.next()
raw = raw["data"]

function = __import__("functions")

def cosineScore(questions):
    vectorizer = CountVectorizer().fit_transform(questions)
    vectors = vectorizer.toarray()
    csim = cosine_similarity(vectors)
    m = (csim * csim.T)[-1][:-1]
    return (m, csim[-1][:-1])

def tfidfScore(msg):
    questions = raw["Question"][:]
    questions.append(msg)
    vect = TfidfVectorizer(analyzer='char', ngram_range=(1,2), min_df = 0)
    tfidf = vect.fit_transform(questions)
    m = (tfidf * tfidf.T).A[-1][:-1]
    similarity = dict(enumerate(m))
    sindices = []
    csim_data = []
    for k in sorted(similarity, key=similarity.get,  reverse=True):
        if similarity[k] < 0.5 or len(sindices)>10:
            break
        sindices.append({"key": k, "score": similarity[k]})
        csim_data.append(questions[k])
    csim_data.append(msg)
    (csimt, csim) = cosineScore(csim_data)
    score = []
    for i,s in enumerate(csim):
        socre_ = (s+sindices[i]["score"])/2
        score.append({"key": sindices[i]["key"], "score": socre_})
    return sorted(score, key = lambda i: i['score'],reverse=True) 

def tokenize(data):
    rgx = re.compile(r"[#\w']+")
    word_list = rgx.findall(data)
    word_list = [w for w in word_list]
    return word_list

def equishellEngine(msg):
    token = tokenize(msg)
    score = tfidfScore(msg)
    if len(score) != 0:
        answer = raw["Answer"][score[0]["key"]]
        print(answer)
        if "function:" in answer:
            fun_ = {}
            for ans in answer.split(","):
                ans_ = ans.split(":")
                fun_[ans_[0]] = ans_[1]
            print(fun_)
            answer = getattr(function, fun_["function"])(fun_["value"].lower())
            return answer
        else:
            return answer
    else:
        # use skip fill
        pass
    return "We are unable to process you query due to high traffic."