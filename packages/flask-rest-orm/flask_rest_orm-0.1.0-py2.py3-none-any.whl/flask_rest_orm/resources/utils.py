from sqlalchemy import desc


def query_from_request(model, request):
    """
    Perform a filtered search in the database model table using query parameters in the http URL,
    disposed on the request args.

    It also paginate the response if a 'page' value is present in the query parameters. A 'per_page'
    value in the query parameters defines the page length, default to 20 items.

    Ordered search is available using 'order_by=<col_name>' providing the name of the model column to be the
    ordination key. A 'desc' in the query parameters make the ordination in a descending order.

    :param class model:
        SQLAlchemy model class representing a database resource

    :param request:
        Flask http request data

    :rtype: list
    :return: the items for the current page
    """
    builder = model.query
    for key in request.args:
        if hasattr(model, key):
            vals = request.args.getlist(key)  # one or many
            builder = builder.filter(getattr(model, key).in_(vals))
    if 'order_by' in request.args:
        col = getattr(model,request.args['order_by'])
        if 'desc' in request.args:
            builder = builder.order_by(desc(col))
        else:
            builder = builder.order_by(col)
    if 'page' not in request.args:
        resources = builder.all()
    else:
        resources = builder.paginate().items
    return resources
