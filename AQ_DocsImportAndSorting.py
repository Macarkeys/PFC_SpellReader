
''' What needs to be done:
Completed 1. Creating a list of each column that has been converted to text.
Completed 2. Making a dictionary of each spell in spell list with key = spell name
Completed 3. Value of each dictionary is going to be another dictionary with the spell details.
Completed 4. Spell description is going to be the last thing added as 'Description':'Spell description'
5. Do the same for every file
6. Convert to JSON and figure out how to run.
'''
# combines paragraphs from a list of paragraphs
def collatPara(paragraphList):
  strPara = ''
  for i in paragraphList:
    strPara += i.text
  return strPara
# Cleans the lists in spell table and preps. Removes the little header row and changes the empty row at bottom of every spell to be the description, removing the third column.
def cleanSpellTable(SpellTable):
  cleanedSpells = [[],[]]
  for i in range(len(SpellTable[0])):
    if (SpellTable[0][i],SpellTable[1][i]) != ('','') and ('Description' not in SpellTable[2][i]):
      cleanedSpells[0].append(SpellTable[0][i])
      cleanedSpells[1].append(SpellTable[1][i])
    elif SpellTable[0][i].strip() == '':
      cleanedSpells[0].append('Description:')
      cleanedSpells[1].append(SpellTable[2][i-6])
  return cleanedSpells
# Gets the indexes of each spell in each spell table
def getSpellIndexes(SpellTable):
  spellIndex = []
  for i in range(len(SpellTable[0])):
    if i % 8 == 0:
      spellIndex.append(i)
  return spellIndex
# gets the spells for that spell table as a dictionary
def getSpellDicts(SpellTable):
  spellListDict = {}
  for i in getSpellIndexes(SpellTable):
    keyL = SpellTable[0][i+1:i+8]
    valL = SpellTable[1][i+1:i+8]
    spellDict = {}
    for j in range(len(keyL)):
      spellDict[keyL[j]] = valL[j]
    spellListDict[SpellTable[0][i]] = spellDict
  return spellListDict
# This is the main function that is taking in a table and outputing a fully cleaned and organized spell table as a dictionary. Ex: SpellTable['1 - Concern']
def organizeTable(docTable):
  colLen = len(list(docTable.columns))
  rowLen = len(list(docTable.rows))
  docTableCells = [docTable.column_cells(i) for i in range(colLen)]
  SpellTable = []
  for i in range(colLen):
    SpellTable.append([docTableCells[i][j].paragraphs for j in range(rowLen)])
    SpellTable[i] = list(map(collatPara,SpellTable[i]))
  SpellTable = cleanSpellTable(SpellTable)
  SpellTable = getSpellDicts(SpellTable)
  return SpellTable

def getDocsSpells(doc):
  # creating empty lists to one day combine into a dictionary
  spellGroupTitles = []
  spellGroups = []
  tableing = [False, -1]
  docSpellName = None
  for element in doc.element.body:
    # Finds the headers of the spell groups and signifies when to start collecting tables
    if isinstance(element, CT_P):
      if element.style == 'Heading5':
        tableing[0] = True
        tableing[1] += 1
        spellGroupTitles.append(element.text)
        spellGroups.append({})
      if element.style == 'Heading2' and not docSpellName:
        docSpellName = element.text
    # checks if element is a table, then accesses it as a table (?!?!), then combines the dictionary already present (empty dict if first) with the new one
    if isinstance(element, CT_Tbl) and tableing[0]:
      table = Table(element, doc)
      if len(table._cells) > 10:
        spellGroups[tableing[1]] = {**spellGroups[tableing[1]], **organizeTable(table)}
  # Creating a dictionary from the spell group titles (keys) and spell group dictionaries (values)
  docSpellDict = {}
  for i in range(len(spellGroupTitles)):
    docSpellDict[spellGroupTitles[i]] = spellGroups[i]
  return docSpellDict, docSpellName

if __name__ == "__main__":
  from docx import Document
  from docx.table import Table
  from docx.oxml.text.paragraph import CT_P
  from docx.text.paragraph import Paragraph
  from docx.oxml.table import CT_Tbl
  import json
  import os
  #opening the document as a docx.Document object
  allSpells = {}
  for file in os.listdir('spellFolder'):
    docSpell = getDocsSpells(Document("spellFolder\\"+file))
    allSpells[docSpell[1]] = docSpell[0]
  # next steps is to do this for every spell document and make sure there is no errors then combine them into a big dictionary so bigDict['Orus']['Love']['1 - Concern'] (- not –)
  #print(docSpellDict['Hate']['10 – Malevolence']) # currently an issue is present where – is present in spell names not -. They may look similiar but not the same
  with open('pfc-elemental-divine-spells.json', 'w') as outfile:
    json.dump(allSpells, outfile, indent=4)