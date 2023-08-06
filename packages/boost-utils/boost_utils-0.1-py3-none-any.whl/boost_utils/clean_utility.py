# clean_utility.py
import bstu, re, math


def clean_kosmos(_text):  
    #lower case
    _text = _text.lower()
    #separate out punctuation
    _text = re.sub(r"([^\w\s])", " \\1 ", _text)
    #number cleanup
    _text = re.sub(r"\d", "9", _text)      
    # line feed clean
    _text = _text.replace("< lf >", "\n")    
    # replace double/triple/quadrubple/... spaces with one space
    _text = re.sub(r"\s{2,}", " ", _text)           
    #remove most #
    _timeregex = r"\b\d{1,2}(?::\d{2}){1,2}\b(?!:)"
    _amountregex = r"\b\d{1,3}(?:,?\d{1,3}){0,2}\.\d{2}\b"
    _smallnumberregex = r"\b\d{1,3}\b"
    _mediumnumberregex = r"\b\d{4,8}\b"
    _bignumberregex = r"\b\d{9,}\b"
    _tagregex = r"#(?=date|time|amou|smal|medn|bign)"    
    _text = re.sub(_tagregex, "~", _text)
    _text = _text.replace("#", "")
    _text = _text.replace("~", "#")
    _text = re.sub(_timeregex, "#time", _text)
    _text = re.sub(_amountregex, "#amount", _text)
    _text = re.sub(_bignumberregex, "#bignum", _text)
    _text = re.sub(_mediumnumberregex, "#mednum", _text)
    _text = re.sub(_smallnumberregex, "#smallnum", _text)    
    return _text

    
# Kevin' clean function
def clean_kylo(text):
    abbrevregex1 = r"(?<=\b(?:[a-z]))\."
    abbrevregex2 = r"(?<=\b(?:co|no|jr|sr))\."
    abbrevregex3 = r"(?<=\b(?:inc|ltd))\."
    dateregex = r"\b\d{1,2}[-/]\d{1,2}[-/](?:\d{2}|\d{4})\b"
    timeregex = r"\b\d{1,2}(?::\d{2}){1,2}\b(?!:)"
    amountregex = r"\b\d{1,3}(?:,?\d{1,3}){0,2}\.\d{2}\b"
    smallnumberregex = r"\b\d{1,3}\b"
    mediumnumberregex = r"\b\d{4,8}\b"
    bignumberregex = r"\b\d{9,}\b"
    tagregex = r"#(?=date|time|amou|smal|medn|bign)"
    text = re.sub(dateregex, "#date", text)
    text = re.sub(r"\s+|/|_|@|-", " ", text)
    #change number representation
    text = re.sub(r"\d", "9", text)
    #lower case
    text = text.lower()
    #separate out 's
    text = re.sub(r"(?<=[a-z])'s\b", " 's", text)
    #separate out .com
    text = re.sub(r"(?<=[a-z]).com\b", " .com", text)
    #remove most punctuation
    text = re.sub(r"[^a-z9.',:\s#]", "", text)
    #remove most commas
    text = re.sub(r"(?<=\d),(?=\d)", "~", text)
    text = re.sub(r"(?<=num),(?=#)", "~", text)
    text = text.replace(",", "")
    text = text.replace("~", ",")
    #remove most colons
    text = re.sub(r"(?<=\d):(?=\d)", "~", text)
    text = re.sub(r"(?<=num):(?=#)", "~", text)
    text = text.replace(":", "")
    text = text.replace("~", ":")
    #remove most apostrophes
    text = re.sub(r"(?<=[a-z])'(?=[a-z])", "~", text)
    text = re.sub(r"(?<=\s)'s\b", "~s", text)
    text = text.replace("'", "")
    text = text.replace("~", "'")
    #remove most periods
    text = re.sub(r"(?<=\d)\.(?=\d)", "~", text)
    text = re.sub(r"(?<=num)\.(?=#)", "~", text)
    text = re.sub(abbrevregex1, "~", text)
    text = re.sub(abbrevregex2, "~", text)
    text = re.sub(abbrevregex3, "~", text)
    text = re.sub(r"(?<=\s).com\b", "~com", text)
    text = text.replace(".", "")
    text = text.replace("~", ".")
    text = re.sub("\s+", " ", text)
    #remove most #
    text = re.sub(tagregex, "~", text)
    text = text.replace("#", "")
    text = text.replace("~", "#")
    text = re.sub(timeregex, "#time", text)
    text = re.sub(amountregex, "#amount", text)
    text = re.sub(bignumberregex, "#bignum", text)
    text = re.sub(mediumnumberregex, "#mednum", text)
    text = re.sub(smallnumberregex, "#smallnum", text)
    return text


# clean without cleaning any numerics 
def clean_lonelynum(_text):
    _text = _text.lower()    
    # line feed clean
    _text = _text.replace("<lf>", "abclinefeedxyz")       
    #separate out punctuation
    _text = re.sub(r"([^\w\s])", " \\1 ", _text)     
    # replace double/triple/quadrubple/... spaces with one space
    _text = re.sub(r"\s{2,}", " ", _text)        
    # ...       
    return _text


def clean_for_numeric_vars_version1(_text):   
    return clean_lonelynum(_text)


def clean_for_numeric_vars_version3(_text):           
    return clean_spaceynum(_text)


def clean_spaceynum(_text):
    _text = _text.lower()    
    # line feed clean
    _text = _text.replace("<lf>", "abclinefeedxyz")       
    #separate out punctuation
    _text = re.sub(r"([^\w\s])", " \\1 ", _text)   
    # make numbers spacey      
    _text = re.sub(r"(\d)", " \\1 ", _text) 
    # replace double/triple/quadrubple/... spaces with one space
    _text = re.sub(r"\s{2,}", " ", _text)            
    return _text