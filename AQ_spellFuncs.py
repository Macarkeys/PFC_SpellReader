from Levenshtein import distance

def levenshteinSort(spellData, name: str, nameList):
    LevenshteinList = []
    for i in nameList:
        LevenshteinList.append(distance(str(name), str(i), weights=(1,1,2)))
    print(LevenshteinList)
    if min(LevenshteinList) < 10:
        ind = LevenshteinList.index(min(LevenshteinList))
        return nameList[ind]
    else:
        return None
def levenshteinSearch(spellData, name: str):
    minL = 100
    i_spell = None
    j_spell = None
    k_spell = None
    for i in spellData.keys():
        for j in spellData[i].keys():
            for k in spellData[i][j].keys():
                nameTest = k.replace("\u2013","").strip()
                minP = distance(str(name.lower()), str(nameTest.lower()), weights=(1,1,3))
                if minP < minL:
                    minL = minP
                    i_spell, j_spell, k_spell = i, j, k
    if minL <= 6:
        return (i_spell,j_spell,k_spell)
    else:
        return (None, None, None)

def getSpellTags(spellData, tagStr: str):
    #need to search every tag for the string
    tagDict = {}
    for i in spellData.keys():
        for j in spellData[i].keys():
            for k in spellData[i][j]:
                ind = list(spellData[i][j][k].keys())[5]
                if tagStr in spellData[i][j][k][ind]:
                    tagDict[spellData[i][j][k][ind]] = [i,j,k] 
    return tagDict

def spellEmoji(b):
    pass