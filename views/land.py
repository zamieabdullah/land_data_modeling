from datetime import datetime
from flask import Blueprint, jsonify, request
from models.model import engine
from sqlalchemy import Table, MetaData, and_, or_

metadata = MetaData()

country = Table('country', metadata, autoload_with=engine)
state = Table('state', metadata, autoload_with=engine)
county = Table('county', metadata, autoload_with=engine)
zipcode = Table('zipcode', metadata, autoload_with=engine)

bp = Blueprint('routes', __name__)

# Get all past data on specific state
@bp.route('/state', methods=['GET'])
def get_state():
    req_state = request.args.get('state')
    current_date = datetime.now()

    conditions = []
    conditions.append(or_(state.c.state == req_state, state.c.state_id == req_state))
    conditions.append(state.c.year == current_date.year)

    with engine.connect() as connection:
        query = state.select()
        if len(conditions) > 0:
            query = query.where(and_(*conditions))

        res = connection.execute(query)
        response = [dict(zip(res.keys(), row)) for row in list(res)]    

    return jsonify(response)

# Get most recent data on specific state
@bp.route('/curr-state', methods=['GET'])
def get_curr_state():
    req_state = request.args.get('state')
    current_date = datetime.now()

    conditions = []
    conditions.append(or_(state.c.state == req_state, state.c.state_id == req_state))
    conditions.append(state.c.year == current_date.year)

    with engine.connect() as connection:
        query = state.select()
        if len(conditions) > 0:
            query = query.where(and_(*conditions))

        res = connection.execute(query)
        first = res.first()
        
        response = dict(zip(res.keys(), first))

    return jsonify(response)