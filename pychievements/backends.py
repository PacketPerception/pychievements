import sqlite3


class AchievementBackend(object):
    """
    AchievementBackend

    Achievement backends implement the getting/setting/updating of achievements for ``tracked_id``.
    Achievements in the system are tracked for a specific, unique ID, ``tracked_id``.

    AchievementBackend is the most basic implementation of an AchievementBackend, storing all
    tracked information in memory and never persisting it. All of the functions of an
    AchievementBackend work to retrieve an ``Achievement`` instance for a given ``tracked_id``, and
    run the appropriate function on it, storing the results. In the least, storing results for a
    specific achievement, for a specific ``target_id`` should include the ``target_id``, the
    ``Achievement`` class name (``Achievement.__name__``), and the current level
    (``Achievement.current``)

    .. note::
        AchievementBackend is NOT thread safe
    """
    def __init__(self):
        self._tracked = {}

    def achievement_for_id(self, tracked_id, achievement):
        """ Retrieves the current ``Achievement`` for the given ``tracked_id``. If the given
        ``tracked_id`` does not exist yet, it should be created. Also, if the given ``tracked_id``
        hasn't tracked the given ``Achievement`` yet, a new instance of the ``Achievement`` should
        be created for the given ``tracked_id``"""
        if tracked_id not in self._tracked:
            self._tracked[tracked_id] = {}
        if achievement.__name__ not in self._tracked[tracked_id]:
            self._tracked[tracked_id][achievement.__name__] = achievement()
        return self._tracked[tracked_id][achievement.__name__]

    def achievements_for_id(self, tracked_id, achievements):
        """
        Returns the current achievement for each achievement in ``achievements`` for the given
        tracked_id """
        r = []
        for a in achievements:
            r.append(self.achievement_for_id(tracked_id, a))
        return r

    def set_level_for_id(self, tracked_id, achievement, level):
        """ Set the ``level`` for an ``Achievement`` for the given ``tracked_id`` """
        if tracked_id not in self._tracked:
            self._tracked[tracked_id] = {}
        if achievement.__name__ not in self._tracked[tracked_id]:
            self._tracked[tracked_id][achievement.__name__] = achievement(current=level)
        self._tracked[tracked_id][achievement.__name__].set_level(level)

    def get_tracked_ids(self):
        return self._tracked.keys()

    def remove_id(self, tracked_id):
        """ Removes *tracked_id* from the backend """
        if tracked_id in self._tracked:
            del self._tracked[tracked_id]


class SQLiteAchievementBackend(AchievementBackend):
    """
    Stores achievement data in a SQLite database.

    Arguments:

        dbfile
            The full path and file name to store the SQLite database

    To use, create the backend and then use the :py:func:`set_backend` method of the tracker.

    .. code-block:: python

        mybackend = SQLiteAchievementBackend('/some/db.file')
        tracker.set_backend(mybackend)
    """
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        with self.conn:
            c = self.conn.cursor()
            c.execute('create table if not exists pychievements (tracked_id text, '
                      'achievement text, level integer)')

    def achievement_for_id(self, tracked_id, achievement):
        with self.conn:
            c = self.conn.cursor()
            c.execute('select level from pychievements where achievement=? and tracked_id=?',
                      (achievement.__name__, str(tracked_id)))
            rows = c.fetchall()
            if not rows:
                c.execute('insert into pychievements values(?, ?, ?)',
                          (str(tracked_id), achievement.__name__, 0))
                return achievement(current=0)
            return achievement(current=rows[0][0])

    def achievements_for_id(self, tracked_id, achievements):
        r = []
        achievements = dict((_.__name__, _) for _ in achievements)
        with self.conn:
            c = self.conn.cursor()
            c.execute('select achievement, level from pychievements where tracked_id=? and '
                      'achievement in (%s)' % ','.join('?'*len(achievements.keys())),
                      [str(tracked_id)] + list(achievements.keys()))
            rows = c.fetchall()
            for i, _ in enumerate(rows):
                r.append(achievements[_[0]](current=_[1]))
        return r

    def set_level_for_id(self, tracked_id, achievement, level):
        with self.conn:
            c = self.conn.cursor()
            c.execute('update pychievements set level=? where achievement=? and tracked_id=?',
                      (level, achievement.__name__, str(tracked_id)))

    def get_tracked_ids(self):
        with self.conn:
            c = self.conn.cursor()
            c.execute('select distinct tracked_id from pychievements')
            rows = c.fetchall()
            return [_[0] for _ in rows]

    def remove_id(self, tracked_id):
        with self.conn:
            c = self.conn.cursor()
            c.execute('delete from pychievements where tracked_id=?', (str(tracked_id),))
