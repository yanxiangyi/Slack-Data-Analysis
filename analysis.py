from flask import Flask
from six.moves import urllib
import json
import networkx as nx
from community import community_louvain
import time
import datetime
from QcloudApi.qcloudapi import QcloudApi
import ast
from collections import Counter
import re
app = Flask(__name__)

'''
Methods
'''


def load_json(url):
    # load json dict from response
    response = urllib.request.urlopen(url)
    result = json.loads(response.read().decode('utf-8'))
    return result


# Get all available channels of a team: /api/channel?team={TEAM_ID}
def load_channels(team_id):
    return load_json(path+'channel?team=' + team_id)['data']


def load_channel_mention(team_id, channel_id, from_time, to_time):
    # Get the statistics of mentions within a date range: /api/mention?team={TEAM_ID}&channel={CHANNEL_ID}&from={FROM_TIME}&to={TO_TIME}
    result = load_json(path+ 'mention?team=' + str(team_id) + '&channel=' + str(channel_id) + '&from=' + str(from_time) + '&to=' +str(to_time))
    return result['data']


def load_team_mention(team_id, from_time, to_time):
    # Get the statistics of mentions within a date range: /api/mention?team={TEAM_ID}&channel={CHANNEL_ID}&from={FROM_TIME}&to={TO_TIME}
    result = load_json(path+ 'mention?team=' + str(team_id)  + '&from=' + str(from_time) + '&to=' +str(to_time))
    return result['data']


def load_team_count(team_id, from_time, to_time):
    result = load_json(path+ 'message/count?team=' + str(team_id)  + '&from=' + str(from_time) + '&to=' +str(to_time))
    return result['data']


def load_channel_count(team_id, channel_id, from_time, to_time):
    # Get count of messages by all participants.
    result = load_json(path+ 'message/count?team=' + str(team_id) + '&channel=' + str(channel_id) + '&from=' + str(from_time) + '&to=' +str(to_time))
    return result['data']


def cluster(G):
    # http://cjauvin.blogspot.com/2014/03/k-means-vs-louvain.html
    partition = community_louvain.best_partition(G)
    return partition


def show_channel_history(team_id, channel_id, from_time, to_time, length, offset):
    response = urllib.request.urlopen(path+ 'message?team=' + str(team_id) + '&channel=' + str(channel_id) + '&from=' + str(from_time) + '&to=' +str(to_time) + '&length=' + str(length) + '&offset=' + str(offset))
    result = json.loads(response.read().decode('utf-8'))
    return result['data']


def text_sentiment_json(input):
    module = 'wenzhi'
    action = 'TextSentiment'
    config = {
        'Region': 'sz',
        'secretId': 'AKIDvhHhu7CD9vVt45JYr4A92nRt8AzdtIXh',
        'secretKey': 'KURFrIahcDfx7NTQsMhqmDUecOxVUO6e',
        'method': 'GET',
        'SignatureMethod': 'HmacSHA1'
    }

    action_params = {
        'content': input,
    }

    try:
        service = QcloudApi(module, config)
        secretId = 'AKIDvhHhu7CD9vVt45JYr4A92nRt8AzdtIXh'
        service.setSecretId(secretId)
        secretKey = 'KURFrIahcDfx7NTQsMhqmDUecOxVUO6e'
        service.setSecretKey(secretKey)
        region = 'gz'
        service.setRegion(region)
        method = 'GET'
        service.setRequestMethod(method)
        SignatureMethod = 'HmacSHA1'
        service.setSignatureMethod(SignatureMethod)
        dict = ast.literal_eval(service.call(action, action_params).decode())
        return dict

    except Exception as e:
        import traceback
        print('traceback.format_exc():\n%s' % traceback.format_exc())


def add_one_day(from_time):
    orig = datetime.datetime.fromtimestamp(int(from_time))
    new = orig + datetime.timedelta(days=1)
    next_time = int(time.mktime(new.timetuple()))
    return next_time

def find_all_word(team_id, channel_id, from_time, to_time, length, offset):
    histories = show_channel_history(team_id, channel_id, from_time, to_time, length, offset)
    all_history = ''
    for history in histories['message']:
        all_history += str(history['text']) + ' '
    return all_history


'''
app
'''

path = 'http://slack.imxieyi.com/api/'


@app.route('/team_account_num/<team_id>')
def output_account_num_team(team_id):
    channels = load_channels(team_id)
    count = 0
    for channel in channels:
        count += channel['num_members']
    return str(count)


@app.route('/channel_account_num/<team_id>/<channel_id>')
def output_account_num_channel(team_id, channel_id):
    channels = load_channels(team_id)
    for channel in channels:
        if channel['id'] == channel_id:
            return str(channel['num_members'])
        else:
            return '0'


@app.route('/team_message_num/<team_id>/<from_time>/<to_time>')
def output_team_message_count(team_id, from_time, to_time):
    counts = load_team_count(team_id, from_time, to_time)
    total = 0
    for count in counts:
        total += count['count']
    return str(total)


@app.route('/channel_message_num/<team_id>/<channel_id>/<from_time>/<to_time>')
def output_channel_message_count(team_id, channel_id, from_time, to_time):
    counts = load_channel_count(team_id, channel_id, from_time, to_time)
    total = 0
    for count in counts:
        total += count['count']
    return str(total)


@app.route('/team_mention_num/<team_id>/<from_time>/<to_time>')
def output_team_mention_count(team_id, from_time, to_time):
    counts = load_team_mention(team_id, from_time, to_time)
    total = 0
    for count in counts:
        total += count['count']
    return str(total)


@app.route('/channel_mention_num/<team_id>/<channel_id>/<from_time>/<to_time>')
def output_channel_mention_count(team_id, channel_id, from_time, to_time):
    counts = load_channel_mention(team_id, channel_id, from_time, to_time)
    total = 0
    for count in counts:
        total += count['count']
    return str(total)


@app.route('/sentiment/<team_id>/<channel_id>/<from_time>/<to_time>/<length>/<offset>')
def analyze_history_all(team_id, channel_id, from_time, to_time, length, offset):
    histories = show_channel_history(team_id, channel_id, from_time, to_time, length, offset)
    all_history = ''
    for history in histories['message']:
        all_history += str(history) + ' '

    sentiment = text_sentiment_json(all_history)
    positive = sentiment['positive']
    negative = sentiment['negative']
    result = json.dumps({'sentiment': {"positive": positive, "negative": negative}, 'history': histories})
    return result


@app.route('/force_directed/<team_id>/<from_time>/<to_time>')
def output_force_directed(team_id, from_time, to_time):
    result = load_json(path + 'channel?team=' + team_id)
    channels = result['data']
    G = nx.Graph()
    G = nx.Graph(G)
    for channel in channels:
        for edge in load_channel_mention(team_id, channel['id'], from_time, to_time):
            if not G.has_edge(edge['from_user'], edge['to_user']):
                G.add_edge(edge['from_user'], edge['to_user'], weight=1 / float(edge['count']))
            else:
                G[edge['from_user']][edge['to_user']]['weight'] = 1 / (1 / G[edge['from_user']][edge['to_user']]['weight'] + edge['count'])
    nodes = []
    links = []
    for key, value in cluster(G).items():
        nodes.append({"id": key, "group": value})
    for e in G.edges:
        links.append({"source": e[0], "target": e[1], 'weight': G[e[0]][e[1]]['weight']})
    relationships = {'nodes': nodes, 'links': links}
    return json.dumps(relationships)


@app.route('/channel-frequency/<team_id>/<channel_id>/<from_time>/<to_time>')
def output_frequency_channel(team_id, channel_id, from_time, to_time):
    results = load_json(path+ 'message/count?team=' + str(team_id) + '&channel=' + str(channel_id) + '&from=' + str(from_time) + '&to=' +str(to_time))
    total = 0
    output = []
    user_num = 0
    for result in results['data']:
        total += result['count']
        user_num += 1
    for result in results['data']:
        output.append({'user': result['user'], 'count': result['count']/total*user_num})
    return json.dumps(output)


@app.route('/team-frequency/<team_id>/<from_time>/<to_time>')
def output_frequency_team(team_id, from_time, to_time):
    results = load_json(path+ 'message/count?team=' + str(team_id)  + '&from=' + str(from_time) + '&to=' +str(to_time))
    total = 0
    output = []
    user_num = 0
    for result in results['data']:
        total += result['count']
        user_num += 1
    for result in results['data']:
        output.append({'user': result['user'], 'count': result['count']/total*user_num})
    return json.dumps(output)


@app.route('/user-frequency/<team_id>/<channel_id>/<user_id>/<from_time>/<to_time>')
def output_frequency_user(team_id, channel_id, user_id, from_time, to_time):
    output = []
    current_time = int(from_time)
    time_range = []
    while True:
        time_range.append(current_time)
        current_time = add_one_day(current_time)
        if current_time > int(to_time):
            break
    frequencies = []
    for i in range(len(time_range) - 1):
        user_counts = load_channel_count(team_id, channel_id, time_range[i], time_range[i+1])
        if user_counts != []:
            user = list(filter(lambda person: person['user'] == user_id, user_counts))
            if user != []:
                count = user[0]['count']
            else:
                count = 0
        else:
            count = 0
        frequencies.append(count)
    # Remove the last timestamp
    time_range.pop()
    for i in range(len(time_range)):
        output.append({'time': str(time.strftime('%d-%b-%y', time.localtime(time_range[i]))), 'count': frequencies[i]})
    return json.dumps(output)


@app.route('/channel-activity/<team_id>/<from_time>/<to_time>')
def output_channel_activity(team_id, from_time, to_time):
    channel_counts = []
    channel_names = []
    for i, channel in enumerate(load_channels(team_id)):
        channel_counts.append(0)
        channel_names.append(channel['name'])
        counts = load_channel_count(team_id, channel['id'], from_time, to_time)
        for count in counts:
            channel_counts[i] += count['count']
    results = []
    for i, channel_count in enumerate(channel_counts):
        result = {'text': channel_names[i], 'count': channel_count}
        results.append(result)
    return json.dumps(results)

@app.route('/channel-word-frequency/<team_id>/<channel_id>')
def find_most_frequent_word(team_id, channel_id):
    from_time = '946684800'
    to_time = '1514937600'
    length = 500
    offset = 0
    all_history = find_all_word(team_id, channel_id, from_time, to_time, length, offset)
    words = re.findall(r'\w+', all_history)
    cap_words = [word.upper() for word in words]
    word_counts = Counter(cap_words)
    word_counts = dict(word_counts)
    common_words = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once']
    common_words = [common_word.upper() for common_word in common_words]
    defaultWords = []
    for word, frequency in word_counts.items():
        if word not in common_words and not word.isdigit():
            defaultWords.append({"name": word, "value": frequency})
    return json.dumps(defaultWords)
