from math import sqrt

# Avaliação com relação a testes
element_base_dict = {'Jordan': 0, 'Kazuo': 0, 'Hendria': 0, 'Cassio': 0, 'Paulo': 0, 'Andressa': 0}

users = {'Arthur': {'Jordan': 5, 'Kazuo': 3, 'Hendria': 5, 'Cassio': 2},
         'Rafael': {'Jordan': 2, 'Kazuo': 5, 'Cassio': 1},
         'Gabrielle': {'Jordan': 4, 'Hendria': 4, 'Kazuo': 3, 'Paulo': 2, 'Andressa': 5},
         'Frederico': {'Jordan': 1, 'Kazuo': 5, 'Hendria': 3},
         'Bruna': {'Jordan': 5, 'Hendria': 2, 'Cassio': 4},
         'Thiago': {'Kazuo': 2, 'Hendria': 4, 'Cassio': 3},
         'José': {'Kazuo': 3, 'Hendria': 3, 'Cassio': 4},
         'Daniel': {'Jordan': 5, 'Kazuo': 1, 'Hendria': 5, 'Cassio': 5},
         'Victor': {'Hendria': 3, 'Cassio': 1},
         'Novato': {'Hendria': 2}
         }


def __manhathan(user_1_evaluations, user_2_evaluations):

    '''
    :param user_1_evaluations: Dict with user_1 evaluations
    :param user_2_evaluations: Dict with user_2 evaluations
    :return: manharhan distance betwenn both users
    '''
    distance = 0

    for evaluation in user_1_evaluations:
        if evaluation in user_2_evaluations:
            distance += abs(user_1_evaluations[evaluation] - user_2_evaluations[evaluation])
    return distance


def __nearest_neightbors(username, users, element_base_dict,r=False, pearson=False, cos=False):

    '''

    :param username: name of user as str
    :param users: fict with all users evaluation
    :param r: if you want to use minkowiski distance ser r 1 or 2 any other values will used manhathan distance
    :param pearson: set TRUE if tou want use pearson distance
    :param cos: et TRUE if tou want use cos distance
    :return:
    '''

    distances = []
    for user in users:
        if user != username:

            if not pearson and not r and not cos:
                distance = __minkowiski(users[user], users[username], 1)
                distances.append((distance, user))

            if pearson:
                distance = __pearson(users[user], users[username])
                distances.append((distance, user))

            if cos:
                distance = __cossimilarity(users[user], users[username], element_base_dict)
                distances.append((distance, user))
            if r:

                if r > 2 or r < 1:
                    distance = __minkowiski(users[user], users[username], 1)
                    distances.append((distance, user))
                else:
                    distance = __minkowiski(users[user], users[username], r)
                    distances.append((distance, user))



    distances.sort()

    return distances


def __minkowiski(user_1_evaluations, user_2_evaluations, r):
    distance = 0
    common_elements = False

    for element in user_1_evaluations:
        if element in user_2_evaluations:
            distance += pow(abs(user_1_evaluations[element] - user_2_evaluations[element]), r)
            common_elements = True

    if common_elements:
        return pow(distance, 1/r)
    else:
        return 0


def __pearson(user_1_evaluations, user_2_evaluations):

    sun_xy = 0
    sun_x = 0
    sun_y = 0
    sun_x2 = 0
    sun_y2 = 0
    n = 0

    for element in user_1_evaluations:
        if element in user_2_evaluations:
            n += 1
            x = user_1_evaluations[element]
            y = user_2_evaluations[element]
            sun_xy += x * y
            sun_x += x
            sun_y += y
            sun_x2 += x**2
            sun_y2 += y**2


    if n == 0:
        return 0

    x = sun_x2 - (sun_x**2)/n
    y = sun_y2 - (sun_y ** 2)/n
    denominator = sqrt(x) * sqrt(y)

    if denominator == 0:
        return 0

    pearson_dist = (sun_xy - (sun_x - sun_y)/n) / denominator
    return pearson_dist


def __recomend(username, users, r=False, pearson= False, cos = False):

    '''
    :param username: uer name as str
    :param users: users as dict: try to use mongo database
    :return:
    '''

    if not  r and not pearson and not cos:
        nearest = __nearest_neightbors(username, users)[0][1]
    if r:
        nearest = __nearest_neightbors(username, users, r=r)[0][1]
    if pearson:
        nearest = __nearest_neightbors(username, users, pearson=True)[0][1]
    if cos:
        nearest = __nearest_neightbors(username, users, cos=True)[0][1]

    recomendations = []
    nearest_evaluations = users[nearest]
    user_evaluations = users[username]

    for element in nearest_evaluations:
        if not element in user_evaluations:
            recomendations.append((element, nearest_evaluations[element]))

    return sorted(recomendations, key=lambda elementTuple: elementTuple[1], reverse=True)


def __cossimilarity(user_1_evaluations, user_2_evaluations, element_base_dict):

    '''
    :param user_1_evaluations:
    :param user_2_evaluations:
    :param element_base_dict:
    :return:
    '''

    vector_user_1 = []
    vector_user_2 = []

    for key in element_base_dict:
        if key not in user_1_evaluations:
            vector_user_1.append(0)
        else:
            vector_user_1.append(user_1_evaluations[key])

    for key in element_base_dict:
        if key not in user_2_evaluations:
            vector_user_2.append(0)
        else:
            vector_user_2.append(user_2_evaluations[key])

    prudcut_vector = 0

    for i in range(len(vector_user_1)):
        product = vector_user_1[i]*vector_user_2[i]
        prudcut_vector += product

    module_vector_1 = 0

    for element in vector_user_1:
        module_vector_1 += element**2


    module_vector_1 = sqrt(module_vector_1)

    module_vector_2 = 0

    for element in vector_user_2:
        module_vector_2 += element ** 2


    module_vector_2 = sqrt(module_vector_2)

    cos_dist = prudcut_vector / (module_vector_1 * module_vector_2)

    return cos_dist


def __recomend_knn(username, users , element_base_dict, k):

    '''
    :param username: uer name as str
    :param users: users as dict: try to use mongo database
    :return:
    '''

    nearest = __nearest_neightbors(username, users, element_base_dict, pearson=True)
    starter_user = False
    for i in range(k):
        if nearest[i][0] == 0:
            starter_user = True
            break
    if starter_user:
        nearest = __nearest_neightbors(username, users, element_base_dict, cos=True)

    user_evaluations = users[username]
    nearests_neighbors = []
    nearests_neighbors_evaluations = []

    for i in range(k):
        nearests_neighbors.append(nearest[i])
        nearests_neighbors_evaluations.append((nearest[i][1], users[nearest[i][1]]))


    influence_dict = {}
    total_influence = 0
    for element in nearests_neighbors:
        total_influence += element[0]
    for element in nearests_neighbors:
        influence_dict[element[1]] = element[0]/total_influence

    total_evaluations_values = {}
    
    for element in nearests_neighbors_evaluations:
        for atribute in element[1]:

            if atribute not in user_evaluations:
                 if atribute not in total_evaluations_values:
                    total_evaluations_values[atribute] = 0
                 total_evaluations_values[atribute] += influence_dict[element[0]]*element[1][atribute]

    sorted_dict = sorted(total_evaluations_values, key=lambda item: item[0], reverse=True)
    return sorted_dict


def recomend_api(username, service):

    knn = __recomend_knn(username, users, element_base_dict, 3)
    if len(knn) > 0:
        return knn[0]
    else:
        return False

if __name__ == '__main__':

    recomend = recomend_api('Novato')
    print(recomend)
