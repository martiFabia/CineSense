import re

def old_strip_emojis(text):
    ## See:
    ## https://stackoverflow.com/a/58356570
    ## this one missed some emojis, like ⏹️

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    
    return emoji_pattern.sub(r"", text)

def strip_emojis(text):
    ## Original implementation by:
    ## https://stackoverflow.com/a/58356570
    ## fixes for missing emojis from:
    ## https://github.com/diasks2/pragmatic_tokenizer/issues/20#issuecomment-374352212

    emoji_pattern = re.compile("["
        u"\U000000A9-\U000000AE" # copyright symbols
        u"\U0000200D"            # weird leftover from some flags and skin tone variants
        u"\U0000203C-\U00003299"
        u"\U0000FE0F"            # dingbats
        u"\U00010000-\U0010FFFF"
        u"\U0001F000-\U0001F644"
                    "]+", re.UNICODE)
    
    text = emoji_pattern.sub(' ', text)     # replace with a space to avoid unwanted word concats
    return trim_spaces(text)


def strip_hashtags(text):
    return re.sub(r'#(\w+)', '', text)

def strip_special_chars(text):
    # Mantieni .,!? e l'apostrofo
    text = re.sub(r'[^A-Za-z0-9.,!?\'\s]+', ' ', text)  
    return text



def strip_mentions(text):
    return re.sub(r'@(\w+)', '', text)


def strip_links(text):
    

    link_pattern =  r'\b(?:https?|ftp)?:\/\/(?:www\.)?[\w-]+(?:\.[\w-]+)+[\w\-./?%&=]*\b'

    
    text = re.sub(link_pattern, "", text)
    

    return trim_spaces(text)


def trim_spaces(text):
    text = text.strip()                    # trim leading and trailing spaces
    text = re.sub(r' {2,}', " ", text)     # trim repeated spaces
    return text


def replace_abbreviations(text):
    # Common abbreviations
    abbreviations = {
 'u': 'you',
 'ur': 'your',
 'r': 'are',
 'b4': 'before',
 'gr8': 'great',
 'l8r': 'later',
 'thx': 'thanks',
 'pls': 'please',
 'omg': 'oh my god',
 'idk': "i don't know",
 'lol': 'laughing out loud',
 'brb': 'be right back',
 'btw': 'by the way',
 'ttyl': 'talk to you later',
 'afaik': 'as far as i know',
 'imo': 'in my opinion',
 'imho': 'in my humble opinion',
 'tbh': 'to be honest',
 'np': 'no problem',
 'nvm': 'never mind',
 'msg': 'message',
 'dm': 'direct message',
 'bc': 'because',
 'bff': 'best friends forever',
 'jk': 'just kidding',
 'bday': 'birthday',
 'cya': 'see you',
 'fyi': 'for your information',
 'asap': 'as soon as possible',
 'tba': 'to be announced',
 'tbd': 'to be decided',
 'omw': 'on my way',
 'irl': 'in real life',
 'w/e': 'whatever',
 'w/o': 'without',
 'atm': 'at the moment',
 'fomo': 'fear of missing out',
 'smh': 'shaking my head',
 'rofl': 'rolling on the floor laughing',
 'wfh': 'work from home',
 'ftw': 'for the win',
 'rn': 'right now',
 'yt': 'youtube',
 'fb': 'facebook',
 'ig': 'instagram',
 'snap': 'snapchat',
 'tmi': 'too much information',
 'pov': 'point of view',
 'hmu': 'hit me up',
 'ama': 'ask me anything',
 'wth': 'what the hell',
 'wtf': 'what the fuck',
 'yolo': 'you only live once',
 'bae': 'before anyone else',
 'lmao': 'laughing my ass off',
 'cuz': 'because',
 'ppl': 'people',
 'b4n': 'bye for now',
 'gtg': 'got to go',
 'xoxo': 'hugs and kisses',
 'icymi': 'in case you missed it',
 'ttys': 'talk to you soon',
 'lmk': 'let me know',
 'wyd': 'what are you doing',
 'wya': 'where are you at',
 'imh': 'in my humble opinion',
 'idc': "i don't care",
 'tbf': 'to be fair',
 'wbu': 'what about you',
 'g2g': 'got to go',
 'diy': 'do it yourself',
 'gg': 'good game',
 'gn': 'good night',
 'gm': 'good morning',
 'ftl': 'for the loss',
 'm8': 'mate',
 'nm': 'not much',
 'pm': 'private message',
 'nsfw': 'not safe for work',
 'tldr': "too long didn't read",
 'bruh': 'brother',
 'fam': 'family',
 'idgaf': "i don't give a fuck",
 'roflmao': 'rolling on the floor laughing my ass off',
 'q&a': 'questions and answers',
 'fwiw': "for what it's worth",
 'l8': 'late',
 'b/c': 'because',
 'bbl': 'be back later',
 'jfc': 'jesus fucking christ',
 "y'all": 'you all',
 'plz': 'please',
 'stfu': 'shut the fuck up'
 }
    
    for abbr, full_form in abbreviations.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full_form, text)
    return text

def strip_censorship(text):
    
    text = re.sub(r'\b\w\*+\b', '', text)
    
    return text


    

def filter_string(text):
     
    text = old_strip_emojis(text) 
    text = strip_emojis(text)
    
    text = strip_hashtags(text)
    text = strip_mentions(text)
    text = strip_links(text)
    
    text = replace_abbreviations(text)
    
    text = strip_censorship(text)
    
    text = strip_special_chars(text)
    
    text = trim_spaces(text)
    return text
   
   
   

    
    


    