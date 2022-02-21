# standard
from datetime import datetime
# internal
from src import console
# pandas
import pandas as pd


class Snap(object):
    """Snap"""
    CREATED_AT_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, database_name, data_frames, created_at=None):
        self.database_name = database_name
        self.data_frames = data_frames
        self.created_at = created_at or datetime.now().strftime(self.CREATED_AT_FORMAT)

    @classmethod
    def from_database(cls, database, created_at=None, progress=True):
        data_frames = dict()
        tables = database.tables()
        if progress:
            tables = console.progress(tables, 'Snapping')
        for table in tables:
            columns = database.columns(table)
            records = [list(record) for record in database.records(table)]
            data_frames[table] = pd.DataFrame(records, columns=columns)
        return Snap(database.name, data_frames, created_at)

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
        changed = list()
        for frame in self.common(other):
            left, right = self.data_frames[frame].align(other.data_frames[frame], join='outer')
            r = left.compare(right)
            if not r.empty:
                changed.append(frame)
        return changed
