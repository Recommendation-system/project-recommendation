from itis_project.apps.content.models import UserProfile, Subject
import math

similarity = dict()


def get_user_rates(course=1, count=5):
    info = dict()
    for profile in UserProfile.objects.filter(course_number=course):
        if count == 0:
            break

        user = profile.user
        info[user] = dict()
        for subject in Subject.objects.filter(course_number=course):
            info[user][subject] = profile.user.like_set.filter(post__subject__course_number=1,
                                                               post__subject=subject).count()
            count -= 1
    return info


def distCosine(vecA, vecB):
    dotProduct = 0.0  # скалярное произведение vecA и vecB
    dotSquareA = 0.0  # скалярный квадрат (квадрат длины) вектора A
    dotSquareB = 0.0  # скалярный квадрат вектора B
    for dim in vecA:
        dotSquareA += vecA[dim] * vecA[dim]
        if dim in vecB:
            dotProduct += vecA[dim] * vecB[dim]
    for dim in vecB:
        dotSquareB += vecB[dim] * vecB[dim]
    sqrt = math.sqrt(dotSquareA * dotSquareB)
    if sqrt == 0:
        result = 0
    else:
        result = dotProduct / sqrt
    return result


def create_recommendations(user, users_count):
    userRates = get_user_rates(count=users_count, course=UserProfile.objects.get(user=user).course_number)
    matches = [(u, distCosine(userRates[user], userRates[u])) for u in userRates if u != user]
    topMatches = sorted(matches, key=lambda x: x[1], reverse=True)

    similarity_all = sum([x[1] for x in topMatches])
    topMatches = dict([x for x in topMatches if x[1] > 0.0])
    for relatedUser in topMatches:
        for post in userRates[relatedUser]:
            if not post in similarity:
                similarity[post] = 0.0
            similarity[post] += userRates[relatedUser][post] * topMatches[relatedUser]
            similarity[post] /= similarity_all

    return similarity


def get_recommendations():
    return similarity
