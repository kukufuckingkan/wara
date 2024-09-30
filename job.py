from ali import excel,image
from apscheduler.schedulers.background import BackgroundScheduler
from conda import hub
from memory import database
from aminatu import sql
from sqlalchemy import Integer, String, Float,BINARY

SHEET_WORD = 'word'
SHEET_NAME = 'name'

WORD_DTYPES = column_types = {
    'id': Integer,
    'text': String,
    'meaning': Integer,
    'voice': BINARY,
    'root_id': Integer,
    'type': Integer,
    'version':Integer
}
WORD_INDEX = 'id'

def init_database(sheet_name: str):
    folder,sub_folder, asset = 'dictionary','english','dictionary'
    git = hub.Git(folder=folder,subFolder=sub_folder)
    file_data = git.retriveFile(asset=asset,extension='xlsx')
    excel_file = excel.getFile(data=file_data)
    frame = excel.getSheet(name=sheet_name,book=excel_file)
    db = database.Sqlite(folder= folder,subfolder=sub_folder)
    db.initFromFrame(frame=frame,table=sheet_name)
    # TODO stop job from running

def load_images():
    folder,sub_folder, asset = 'dictionary','english','dictionary'

    db = database.Sqlite(folder= folder,subfolder=sub_folder)
    connection = db.connection()
    query = sql.Query(connection=connection,table= SHEET_NAME)

    result = query.findAll()

    for i, row in enumerate(result):
        index,id,name,img = row
        git = hub.Git(folder='image', subFolder='animal')
        file_data = git.retriveFile(asset= str(id), extension='jpg')

        #image.display(file_data)




scheduler = BackgroundScheduler()
#scheduler.add_job(lambda : init_database(SHEET_WORD), 'interval', seconds=10)
#scheduler.add_job(lambda : init_database(SHEET_NAME), 'interval', seconds=10)
scheduler.add_job(lambda : load_images(), 'interval', seconds=40,replace_existing=True)
scheduler.start()