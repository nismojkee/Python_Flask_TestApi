import os, string, random, xlrd
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
		file = xlrd.open_workbook(os.path.join(app.config['UPLOAD_DIR'], '.'.join([self.id, self.extension])))
		self.status = 'Processing'
		ar1 = []
		ar2 = []
		x = []
		needCol = []
		for sheet in file.sheets():
				for row in range(sheet.nrows):
					for col in range(sheet.ncols):
						if sheet.cell_value(row, col) == 'before':
							ar1 = sheet.col_values(col)
						if sheet.cell_value(row, col) == 'after':
							ar2 = sheet.col_values(col)
						x = list(set(ar1) & set(ar2))
						needCol = 'before: removed {}'
						if ar1.count(ar1) > ar2.count(ar2):
							needCol = 'after: added {}'
		self.processed_date = datetime.utcnow()
		self.status = 'Ready'
		self.result = needCol.format(int(x[0]))
		db.session.commit()