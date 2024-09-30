import json

from ali import excel
from aminatu import sql
from conda import hub
from flask import Flask, Response
from flask_cors import CORS
from memory import database
from sqlalchemy.engine import Row
from typing import Any, Sequence

from job import scheduler

# from pyspark.sql import Row  # or replace Row with the appropriate class for your context


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/word')
def find_word():
    folder,sub_folder, asset,sheet_name = 'dictionary','english','dictionary','word'
    git = hub.Git(folder=folder,subFolder=sub_folder)
    file_data = git.retriveFile(asset=asset,extension='xlsx')
    excel_file = excel.getFile(data=file_data)
    frame = excel.getSheet(name=sheet_name,book=excel_file)
    db = database.Sqlite(folder= folder,subfolder=sub_folder)
    db.initFromFrame(frame=frame,table=sheet_name)

    connection = db.connection()
    query = sql.Query(connection=connection,table= sheet_name)

    query_result = query.findAll()
    result = rows_to_json(query_result)

    return Response(result,mimetype='application/json')





def rows_to_json(rows: Sequence[Row[tuple[Any, ...]]]) -> str:
    # Convert each Row object to a dictionary using _asdict() method
    rows_as_dict = [dict(row._mapping) for row in rows]  # Convert to dictionaries
    # Convert the list of dictionaries to JSON format
    return json.dumps(rows_as_dict, indent=4)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        scheduler.shutdown()  # Shutdown the scheduler when exiting the app
