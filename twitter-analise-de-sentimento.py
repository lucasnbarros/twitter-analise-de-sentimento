import tweepy # conecta o Python com a API do Twitter
import re # examina o texto e identifica as partes que casam com a especificação dada.
import pandas as pd # facilita a estruturação e análise de dados 
from textblob import TextBlob # efetua a análise de sentimento


class SentimentAnalysis:

    def __init__(self):

        self.tweets = [] # lista de tweets

    def DownloadData(self):

        # chaves adquiridas no cadastro de uma conta de desenvolvedor no Twitter
        consumerKey = "chave aqui" 
        consumerSecret = "chave aqui"

        # autenticação feita como Aplicativo(450 tweets/15 min) ao invés de usuário(180 tweets/15 min)
        auth = tweepy.AppAuthHandler(consumerKey, consumerSecret)

        api = tweepy.API(auth,
                         wait_on_rate_limit=True, # espera 15 min após atingir limite de tweets
                         wait_on_rate_limit_notify=True)# envia notificação ao chegar no limite de tweets

        searchTerm = '#TheMandalorian' # termo de busca 
        NoOfTerms = 10 # quantidade de tweets que deseja extrair

        # método que faz paginação dos tweets
        self.tweets = tweepy.Cursor(api.search, # método que faz a busca na API
                                    q=searchTerm, # termo de busca
                                    until="2019-11-30", # busca de até dez dias antes dessa data
                                    lang="en",# só extrai tweets em inglês
                                    tweet_mode='extended', # extrai o texto completo do twitter(mais de 140 caracteres)
                                    count=100 # numero máximo de tweets que retornam por página
                                    ).items(NoOfTerms) # quantidade de tweets a serem pesquisados

        # variáveis que armazenam quantidades da análise
        positive = 0
        negative = 0
        neutral = 0
        total = 0

        data = [] # lista que armazena cada dicionário de tweets

        
        for tweet in self.tweets:

            total += 1

            self.tweetDict = {} # dicionário com as colunas específicas de tweets

            # adiciona as colunas created_at, id_str, full_text ao dicionário
            self.tweetDict['created_at'] = tweet.created_at
            self.tweetDict['id_str'] = tweet.id_str
            self.tweetDict['full_text'] = self.cleanTweet(# método que faz a limpeza no texto dos tweets
                tweet.full_text).encode('utf-8')
            
            # faz a análise de sentimento usando a biblioteca Textblob
            analysis = TextBlob(tweet.full_text)

            # adiciona a coluna sentimento no dicionário
            if (analysis.sentiment.polarity == 0):
                self.tweetDict['sentiment'] = 'neutral'
                neutral += 1
            elif (analysis.sentiment.polarity > 0):
                self.tweetDict['sentiment'] = 'positive'
                positive += 1
            elif (analysis.sentiment.polarity < 0):
                self.tweetDict['sentiment'] = 'negative'
                negative += 1

            # imprime o tweet a cada iteração
            print(str(tweet.created_at) + ' id ' +
                  tweet.id_str + ' tweet ' + str(total))
            
            # adiciona os dados na lista
            data.append(self.tweetDict)

        # cria um quadro de dados
        df = pd.DataFrame(data)

        # imprime as quantidades
        print()
        print("positive " + str(positive))
        print("negative " + str(negative))
        print("positive + negative " + str(positive + negative))
        print("neutral " + str(neutral))
        print("total " + str(total))
        print()

        # faz um relatório da análise feita
        print("How people are reacting on " + searchTerm +
              " by analyzing " + str(positive + negative) + " tweets.")
        print()
        print("General Report: ")

        # imprime se a análise de sentimento foi positiva ou negativa
        if (positive > negative):
            print('Positive')
        else:
            print('Negative')

        print()

        # gera o arquivo csv
        df.to_csv('result_df.csv', header=True, index=False,
                  encoding='utf-8')
        
    # método de preprocessamento do texto
    def cleanTweet(self, tweet):

        # remove links, caracteres especias e outras coisas
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
