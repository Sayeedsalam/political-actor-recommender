import re
from pprint import pprint

from fuzzywuzzy import fuzz

from ClusterSImilarity import MinhashClusterSimilarity


class ClusterSimilarity:

    def matches(self, stra, strb):
        return stra in strb

    def measure(self, currentActor, newActor):
        wordsCurrentActor = currentActor.split("_")
        wordsNewActor = newActor.split("_")

        if len(wordsCurrentActor) >= len(wordsNewActor): #current actor name may be a superset of the new name suggested
            i = 0
            j = 0
            while i < len(wordsCurrentActor):
                if self.matches(wordsNewActor[j], wordsCurrentActor[i]):
                    j = j + 1
                i = i + 1
            return float(j) / len(wordsNewActor)

        else:
            i = 0
            j = 0
            while i < len(wordsNewActor):
                if self.matches(wordsCurrentActor[j], wordsNewActor[i]):
                    j = j + 1
                i = i + 1
            return float(j)/len(wordsNewActor)

#==================================================================================================
class FuzzyClusterSimilarity(ClusterSimilarity):

    THRESHOLD = 0.7

    def measure(self, currentActor, newActor):
        return fuzz.partial_ratio(currentActor.replace("_"," "), newActor.replace("_"," "))




#===================================================================================================
clusterSimilarity = MinhashClusterSimilarity()

actorFile  = open("data/dictionaries/Phoenix.International.actors.txt")

currentActor = None
actorNamesDict = {}

for line in actorFile:
    line = line.strip()
    if line.startswith('#') or len(line) == 0:  # if it is a comment
        continue
    line = line.split('#')[0]

    line = re.sub(r'\[[^\]]*\]', '', line).strip()

    if len(line) != 0:
        if line.startswith("+"):
            if currentActor not in actorNamesDict:
                actorNamesDict[currentActor] = []
            actorNamesDict[currentActor].append(line.replace("+",""))
        else:
            currentActor = line


#pprint(actorNamesDict)

actorSynsetRatio = {}

for key in actorNamesDict:
    actorSynonyms = actorNamesDict[key]
    actorSynsetRatio[key] = {}
    for other in actorSynonyms:
        res = clusterSimilarity.measure(key, other)
        actorSynsetRatio[key][other] = res

pprint(actorSynsetRatio)


diffActorRatio = {}

actorNames = []

for key in actorNamesDict:
    actorNames.append(key)

i = 0
for i in range(0, len(actorNames)):
    diffActorRatio[actorNames[i]] = {}
    for j in range(i+1, len(actorNames)):
        res = clusterSimilarity.measure(actorNames[i], actorNames[j])
        diffActorRatio[actorNames[i]][actorNames[j]] = res

print "\n"
pprint(diffActorRatio)

print clusterSimilarity.measure("Donald Trump", "Melanila Trump")









