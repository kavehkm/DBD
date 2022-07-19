# standard
import os
from datetime import datetime
# internal
from src import console

# pandas
import pandas as pd


class Snap(object):
    """Snap"""
    CREATED_AT_FORMAT = '%Y-%m-%d %H-%M-%S'

    def __init__(self, database_name, data_frames, created_at=None):
        self.database_name = database_name.replace("./","")
        self.data_frames = data_frames
        self.created_at = created_at or datetime.now().strftime(self.CREATED_AT_FORMAT)

    @staticmethod
    def from_database(database, created_at=None, progress=True):
        data_frames = dict()
        tables = database.tables()
        if progress:
            tables = console.progress(tables, 'Snapping')
        for table in tables:
            columns = database.columns(table)
            records = [list(record) for record in database.records(table)]
            data_frames[table] = pd.DataFrame(records, columns=columns)
        return Snap(database.name, data_frames, created_at)

    @staticmethod
    def from_pickle(path):
        base_name = os.path.basename(path).replace('Snap__', '')
        database_name, created_at = base_name.rsplit('@', 1)
        frames = dict()
        for content in os.listdir(path):
            if content.endswith('.pickle'):
                frame = pd.read_pickle(os.path.join(path, content))
                name = content.split('.')[0]
                frames[name] = frame
        return Snap(database_name, frames, created_at)

    def to_pickle(self, path, progress=True):
        name = 'Snap__{}@{}'.format(self.database_name, self.created_at)
        path = os.path.join(path, name)
        if not os.path.exists(path):
            os.mkdir(path)
        frames = self.data_frames.keys()
        if progress:
            frames = console.progress(frames, 'Saving')
        for frame in frames:
            df = self.data_frames[frame]
            df.to_pickle(os.path.join(path, f'{frame}.pickle'))

    def difference(self, other):
        """deleted: frames that does not exists in other"""
        return list(set(self.data_frames.keys()) - set(other.data_frames.keys()))

    def r_difference(self, other):
        """new: frames that does not exists in self"""
        return list(set(other.data_frames.keys()) - set(self.data_frames.keys()))

    def common(self, other):
        """frames that exists in both `self` and `other`"""
        return list(set(self.data_frames.keys()) & set(other.data_frames.keys()))

    def changed(self, other):
        """common frames that changed"""

        #saving changed column titles
        column_changed = {}

        #saving details of the changes in each column
        rows_changed = []

        for frame in self.common(other):
            left, right = self.data_frames[frame].align(other.data_frames[frame], join='outer')
            r = left.compare(right)
            
            if not r.empty:
                rows_changed.append({frame:r})

                #using sets to omit redundancy
                column_changed[frame]=set()
                
                for c, i in r.items():
                    column_changed.get(frame).add(c[0])
        

        return [column_changed,rows_changed]
