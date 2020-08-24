import inline
from flask import Flask, make_response
import pandas as pd
import fileProcessing
import dataProcessing
from flask import Flask, render_template, request
import csv
import io
from flask import Flask, stream_with_context
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import os
from matplotlib import pyplot as plt
from datetime import datetime


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1



# to able refresh the output of our result.. especially for the plot figure
#https://stackoverflow.com/questions/23112316/using-flask-how-do-i-modify-the-cache-control-header-for-all-output

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/')
def Home():
 return render_template("Home.html")

@app.route('/info')
def info():
 return render_template("information.html")

@app.route('/textSearch')
def textSearch():
 return render_template("TextSearch.html")

@app.route('/uploadFile')
def uploadFile():
 return render_template("uploadFile.html")

@app.route('/about')
def about():
    befor = 'static/images/Before_Prediceted_manual.png'
    beforReport = 'static/images/beforPredicet_manual.png'
    after = 'static/images/Before_Prediceted_withKaggle.png'
    afterReport = 'static/images/after_predicted_withkaggle.png'
    return render_template("about.html" , befor=befor , after=after , beforReport=beforReport, afterReport=afterReport)

# a Decision Tree Classifier by typing test
@app.route('/process', methods= ['POST','GET'])
def process():
        text = request.form['message']
        data = dataProcessing.DecsionTree(text)
        return render_template("resultOfSearch.html", data = data)

@app.route('/processUpload', methods= ['POST','GET'])
def processUpload():
    #https://www.tutorialspoint.com/flask/flask_file_uploading.htm
    theFile = request.files['file']
    if not theFile:
        return "No file"
    stream = io.StringIO(theFile.stream.read().decode("ISO-8859-1"), newline=None)
    csv_input = csv.reader(stream)

    data = fileProcessing.readingAndPredicting(csv_input)
    counter = 0
    for  d in data:
        if counter == 0:
            counter = counter + 1
            continue
        d[0] = datetime.strptime(d[0], "%d/%m/%y %H:%M")

    # print data after analysizing to the panda
    toCsvFile = pd.DataFrame.from_records(data, index='created_at', columns=['created_at','id','text','source','label2','newlabel'])
    #https://stackoverflow.com/questions/31328861/python-pandas-replacing-header-with-top-row
    toCsvFile = toCsvFile[1:]  # 'take the data less the header row'

    #calling function of ploting data

    sl=imageSourceAndLabel(toCsvFile)
    cl=imageCreatedAndLabel(toCsvFile)
    tl=imageTimeAndLabel(toCsvFile)


    #https://datascienceplus.com/twitter-analysis-with-python/
    return render_template("tableOfResult.html", data =data , sl='static/images/sourceLabel1.png', cl='static/images/createdAndLabel1.png', tl='static/images/timeAndLabel1.png')

# to download new file prediction
def downloadLabledFile():
    data = io.StringIO()
    yield data.getvalue()
    data.seek(0)
    data.truncate(0)
    writer = csv.writer(data)
    predectedFile = []
    with open('newPrediction.csv', 'r') as File:
        Read = csv.reader(File)
        predectedFile.append(list(Read))
    # write each log item

    for row in predectedFile :
        for row in row:
            writer.writerow(row)
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)


@app.route('/download', methods=['POST', 'GET'])
def download():
    # add a filename
    H = Headers()
    H.set('Content-Disposition', 'attachment', filename='LABELEDDATA.csv')
    return Response(
        stream_with_context(downloadLabledFile()),
        mimetype = 'text/csv', headers = H
    )

# three function to ploting data beside bully that asign by the Desicion Tree classifer
# this will be a newlabel in new dataset after upload.

def imageSourceAndLabel(toCsvFile):
    # to give ability to us just count with bully text we remove each row that have a value of '0' which means that is not bully
    newCsv = toCsvFile[toCsvFile.newlabel != '0']

    #here we plot our data...for each pie chart and bar for the rest of imageCreated def line 147 and line 162
    # https://datascienceplus.com/twitter-analysis-with-python/
    tweets_source = newCsv.groupby(['source'])['newlabel'].count()
    tweets_source.rename("", inplace=True)
    explode = (1, 0, 0)
    colors = ['#EC7063', '#F5B7B1', '#E5E7E9', '#D98880','#F2D7D5','#F6DDCC','#CD6155']
    tweets_source.plot(kind='pie', figsize=(40, 40), autopct='%1.1f%%', shadow=True, explode=None, colors=colors , textprops={'fontsize': 40})
    plt.legend(bbox_to_anchor=(.2, .2), loc='left', borderaxespad=0. , prop={'size': 40})
    plt.title('Source and New Label', bbox={'facecolor': '0.8', 'pad': 0}, fontsize=70)
    plt.savefig('static/images/sourceLabel1.png')
    plt.clf()
    plt.cla()
    plt.close()

def imageCreatedAndLabel(toCsvFile):
    newCsv = toCsvFile[toCsvFile.newlabel != '0']
    tweets_time = newCsv.groupby(['created_at'])['newlabel'].count()
    tweets_time.rename("", inplace=True)
    explode = (1, 0, 0)
    colors = ['#E5E7E9', '#AED6F1', '#D98880', '#EAEDED','#F1948A','#FDEBD0']
    tweets_time.plot(kind='pie', figsize=(40, 40), autopct='%1.1f%%', shadow=True, explode=None , colors=colors, textprops={'fontsize': 40})
    plt.legend(bbox_to_anchor=(.2, .2), loc='left',prop={'size': 40})
    plt.title('created_at and New Label', bbox={'facecolor': '0.8', 'pad': 0} ,fontsize=70)
    plt.savefig('static/images/createdAndLabel1.png')
    plt.clf()
    plt.cla()
    plt.close()


def imageTimeAndLabel(toCsvFile):
    newCsv = toCsvFile[toCsvFile.newlabel != '0']
    tweets_sentiment_time = newCsv.groupby(newCsv.index.map(lambda t: t.minute))['newlabel'].count()

    for timegroup in tweets_sentiment_time:
        print(timegroup)
    tweets_sentiment_time.plot(kind='barh', figsize=(20, 20))
    plt.legend(bbox_to_anchor=(1, 1), loc=3, borderaxespad=0.)
    plt.title('Time and Label New ', bbox={'facecolor': '0.8', 'pad': 0})
    plt.savefig('static/images/timeAndLabel1.png')
    plt.clf()
    plt.cla()
    plt.close()


if __name__ == '__main__':
    SESSION_TYPE = 'filesystem'
    app.secret_key = os.urandom(12)
    app.run(debug=True)

