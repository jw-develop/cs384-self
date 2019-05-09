
import re
import random

def testReplace(test, replace):
    return lambda str: replace(str) if test(str) else None

def replacement(reSearch, reReplace) :
    return testReplace(lambda str: re.search(reSearch, str),
                       lambda str: re.sub(reSearch, reReplace, str))

def response(reSearch, response) :
    return testReplace(lambda str: re.search(reSearch, str),
                       lambda str: response)

def patternResponse(reSearch, response):
    def ff(str):
        match = re.search(reSearch, str)
        if match :
            return re.sub(r'xxx', match.group(1), response)
        else :
            return None
    return ff

def multiPatternResponse(reSearch, response_orig) :
    def ff(str):
        match = re.search(reSearch, str)
        if match :
            replacements = match.groupdict()
            response = response_orig
            for x in replacements :
                response = re.sub(x, replacements[x], response)
            return response
        else :
            return None
    return ff
                       
basicSubList = [(r'\bme\b', "you"), (r'\bmy\b', "your"), (r'\bmine\b', "yours"), (r'\bi\b', "you"), (r'\bam\b', "are"), ("I\'m", "you are"),
                (r'\byou\b', "me"), (r'\byours\b', "mine"), (r'\byour\b', "my"), (r'\bare\b', "to be"), (r'\W$', "")]                       
                       
basicSubs = [replacement(basicSubList[i][0], "X%sX" % i) for i in range(len(basicSubList))] + [replacement("X%sX" % i, basicSubList[i][1]) for i in range(len(basicSubList))]

opportunistic = [response(r'[pP]ython', "Do you mean the snake, the language, or the Monty?"),
                response(r'(egg|pancake|waffle|cereal|bacon|toast)', "I enjoy a good breakfast."),
                response(r'\bVan ?(([d|D]en ?)|([d|D]er ?))?[a-zA-Z]+\b', 
                         "The space after the Van might be authentic, but it mucks up official documentation. Gotta love internal capitalization, though"),
                response(r'Eliza', "I'm not as good as Eliza"),
                response(r'(you kiss(ed|ing)?)|(kiss(ed|ing)? you)', "Was that your first kiss?")]

standardList = [(r'you are (depressed|sad|hungry|tired|angry)', r'I am sorry to hear you are xxx'),
                (r'you are (tired|exhausted|worn out)', r'What is making you so xxx?'),
                (r'me to be a (computer|program|bot|agent)', "Can\'t we xxxs get any respect?"),
                (r'\b(always|everyone|everybody|every time|all)\b', r'You say, "xxx", but can you think of a specific example?'),
                (r'(father|dad|mother|mom|brother|sister|friend|roommate|chapel buddy)', r'Do you get along with your xxx?'),
                (r'dreamed (.*$)', r'Do you wish xxx?')]

standard = [patternResponse(p, q) for (p, q) in standardList]

fancyList = [('(?P<aaa>father|dad|mother|mom|brother|sister|friend|roommate|chapel buddy)\'s (?P<bbb>\w+)', "Do you consider your aaa\'s bbb to be your own?"),
             (r'you (?P<aaa>love|like|prefer|adore|hate|dislike|loath) (?P<bbb>.*$)', r'Does bbb aaa you?')]

fancy = [multiPatternResponse(p, q) for (p, q) in fancyList]

lastResort = [lambda str : 'Is it really true that ' + str + '?',
              lambda str : str + ', so you say.',
              lambda str : "I don't understand that " + str + ".",
              lambda str : 'Perhaps we can talk about something else.']


print "Please chat with me."

while True :
    given = raw_input()
    given = given[0].lower() + given[1:]
    for sub in basicSubs :
        revised = sub(given)
        if revised :
            given = revised
    random.shuffle(opportunistic)
    random.shuffle(standard)
    random.shuffle(fancy)
    responseAttempts = opportunistic + fancy + standard
    response = None
    for attempt in responseAttempts :
        if response == None :
            response = attempt(given)
    if response == None :
        random.shuffle(lastResort)
        response = lastResort[0](given)
    print response
    


    
