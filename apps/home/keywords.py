
def key(text):
    from rake_nltk import Rake
    r = Rake()
    t = text
    l = []
    r.extract_keywords_from_text(t)

    for rating, keyword in r.get_ranked_phrases_with_scores():
        l.append((rating, keyword))

    # Sort the keywords based on their ratings in descending order
    l.sort(reverse=True)

    top_10_keywords = [keyword for rating, keyword in l[:10]]
    return top_10_keywords

