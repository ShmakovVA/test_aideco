from airport.utils.utils_prof import prof


@prof
def get_foreign_object(resource_calss, query_set):
    """
    Выполнение полной дегидрации объектов
    :param resource_calss: класс ресурса
    :param query_set: набор объектов для дегидрации
    :return:
    """
    resource = resource_calss()
    return {'objects': [resource.full_dehydrate(resource.build_bundle(obj)) for obj in query_set]}
