import os, string, random, pandas
from datetime import datetime
from app import db, app

class File(db.Model):
	id = db.Column(db.String(30), primary_key = True)
	upload_date = db.Column(db.DateTime)
	processed_date = db.Column(db.DateTime)
	status = db.Column(db.String(30))
	result = db.Column(db.String(100))
	extension = db.Column(db.String(30))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.id = self._generator()
		self.upload_date = datetime.utcnow()
		self.status = 'Uploaded'

	def as_dict(self):
		return {
			'id': self.id,
			'upload_date': self.upload_date,
			'processed_date': self.processed_date,
			'status': self.status,
			'result': self.result,
		}

	def _generator(self, size = 20, chars = string.ascii_lowercase + string.digits + string.ascii_uppercase):
		return ''.join(random.choice(chars) for _ in range(size))

	def process(self):
		file = pandas.ExcelFile(os.path.join(app.config['UPLOAD_DIR'], '.'.join([self.id, self.extension])))
		self.status = 'Processing'
		for data in [file.parse(sheet) for sheet in file.sheet_names]:
			if 'after' in data.columns and 'before' in data.columns:
				print(data)
				x = data.before - data.after == 0
				indexOfX = x.idxmin()
				msg = {
					'before': 'removed {}',
					'after': 'added {}',
				}
				col = 'before'
				if data.after.count() > data.before.count():
					col = 'after'
				self.processed_date = datetime.utcnow()
				self.status = 'Ready'
				self.result = msg[col].format(data[col][indexOfX])
		db.session.commit()