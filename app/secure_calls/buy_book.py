from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
	logger.debug("Buy Book Handle Request")
	db = g.db
	cur = g.db.cursor()
	bookid = request.args.get('book_id')
	print("Book ID is: " + bookid)
	
	try:
		# clean up query
		query = sql.SQL("insert into {table} ({fieldOne}, {fieldTwo}, {fieldThree}) values (%s, %s, current_timestamp);").format(
			table = sql.Identifier('purchases'),
			fieldOne = sql.Identifier('username'),
			fieldTwo = sql.Identifier('book_id'),
			fieldThree = sql.Identifier('purchased_on')
		)
		
		# execute the query then commit to db
		cur.execute(query, (g.jwt_data['sub'], bookid))
		db.commit()
		
		print("Purchased saved into database.")
		return json_response(message = "Book purchased successfully.", token = create_token(g.jwt_data))
	except:
		return json_response(message = "Error while writing to database.", token = create_token(g.jwt_data), status = 500)