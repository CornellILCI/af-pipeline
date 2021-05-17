
def add(db_session, _object):
    db_session.add(_object)
    db_session.commit()
    return _object
