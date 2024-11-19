from database import execute_query

def get_goals(cursor):
    """
    :param cursor:
    :return
    List: Returns a list with dictionary key, value pairs for all goals:
    """
    sql = "SELECT * from goals"
    return execute_query(cursor,sql)

def get_goal(cursor,primary_id: int):
    """

    :param cursor:
    :param primary_id: Primary id for the specific goal to be returned
    :return: data for the goal with the given primary_id
    """
    sql = "SELECT * from goals where id = %s"

    result = execute_query(cursor,sql,(primary_id,))
    return result if len(result) > 0 else "No goal with that primary id"
