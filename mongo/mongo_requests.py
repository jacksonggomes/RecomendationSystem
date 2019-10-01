from pymongo import MongoClient
import csv


def load_csv(path):
    file = open(path, newline='')
    reader = csv.reader(file)
    header = next(reader)
    header.remove('')
    data = []
    for line in reader:
        item = {
            "evaluator": "",
            "evaluations": []
        }

        for index, valor in enumerate(line):
            if index == 0:
                # Primeiro item da lista = nome do filme
                item["evaluator"] = str(valor).strip().lower()
                item["evaluations"] = {}
            else:
                # Demais itens = avaliacao de usuario
                """
                Como o nome do usuario ta no header, na mesma sequencia
                em que os itens são acessados, basta passar o index - 1,
                para saber de quem foi a nota
                """
                if valor != '':
                    item["evaluations"][str(header[index - 1]).strip().lower()] = int(valor)

        data.append(item)
    return data
def populate_database(path_dataset, service, is_company=False):


    data = load_csv(path_dataset)
    client = MongoClient('mongodb://localhost:27017/')
    db = client.employes_evaluations

    if is_company:
        collection= db[service+'_company']
    else:
        collection = db[service]
    for element in data:
        collection.insert_one(element)
def register(username, password):
    pass
def login (username,password):
    return True
def populate():

    path = "empresas_estagiarios.csv"
    path_1 =  "estagiarios.csv"
    populate_database(path_1, 'ios_testing', True)
    populate_database(path, 'ios_testing')
def evaluate (username,service, evaluation_elment, point, is_company = False):

    client = MongoClient('mongodb://localhost:27017/')
    db = client.employes_evaluations
    username = str(username)
    evaluation_elment = str(evaluation_elment)

    if is_company:
        collection = db[service + '_company']
    else:
        collection = db[service]
    print(collection)
    evaluator = collection.find_one({"evaluator": username})
    user_evaluations = False
    if evaluator:
        user_evaluations = evaluator['evaluations']

    if evaluation_elment not in user_evaluations:
        try:
            user_evaluations[evaluation_elment] = point
            collection.update_one({"evaluator": username}, {'$set': {'evaluations': user_evaluations}})
        except Exception as ex:
            return False
    else:
        return False
    return True
def get_all_services():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.employes_evaluations
    collection_names = db.list_collection_names()
    services = []
    for element in collection_names:
        if str(element).find('_company') == -1:
            services.append(element)
    return services


print(evaluate("carolinne de souza", "ios_testing", "yago kaic", 5, is_company=True))

