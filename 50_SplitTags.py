
def splitbytag(x):
    list_tags =x.split("#")
    list_tags.pop(0)
    return list_tags

x="adaewwe#tag1#tag2#tag3"
print(splitbytag(x))
