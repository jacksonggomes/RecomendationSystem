import csv
import copy
from math import sqrt
path = 'empresas_estagiarios.csv'
data = []

def loadCSV():
    file = open(path, newline='')
    reader = csv.reader(file)
    header = next(reader)
    header.remove('')

    for line in reader:
        item = {
            "Empresa": "",
            "Avaliacoes": []
        }

        for index, valor in enumerate(line):
            if index == 0:
                # Primeiro item da lista = nome do filme
                item["Empresa"] = valor
            else:
                # Demais itens = avaliacao de usuario
                """
                Como o nome do usuario ta no header, na mesma sequencia
                em que os itens são acessados, basta passar o index - 1,
                para saber de quem foi a nota
                """
                item["Avaliacoes"].append({
                    header[index - 1] : valor
                })

        data.append(item)

def cosseno(rating1, rating2):
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0

    n = 0
    for key in rating1:
        x=0
        y=0
        n += 1
        x = float(rating1[key])
        if key in rating2:
            y = float(rating2[key])
        sum_xy += x * y
        sum_x2 += pow(x, 2)
        sum_y2 += pow(y, 2)
        # now compute denominator
    denominator = sqrt(sum_x2) * sqrt(sum_y2)
    if denominator == 0:
        return 0
    else:
        return sum_xy / denominator

def computeNearestNeighbor(username, users):
    """creates a sorted list of users based on their distance to username"""
    distances = []
    for user in users:
        if user != username:
            distance = cosseno(users[user], users[username])
            distances.append((distance, user))
    # sort based on distance -- closest first
    distances.sort()
    return distances


def recommend(username, users):
    """Give list of recommendations"""
    # first find nearest neighbor
    nearest = computeNearestNeighbor(username, users)[0][1]

    recommendations = []
    # now find bands neighbor rated that user didn't
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    # using the fn sorted for variety - sort is more efficient
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1],
                  reverse = True)

loadCSV()

users = {}
for emp in data:
    #users[emp['Empresa']] = emp['Avaliacoes']
    di={}
    for j in emp['Avaliacoes']:
        di.update(j)
    users[emp['Empresa']] = di

backup = copy.deepcopy(users)
for j in users:
    for key in users[j]:
        if (users[j][key]==""):
            del backup[j][key]

print(recommend('APA COMERCIO DE MOVEIS', backup))
