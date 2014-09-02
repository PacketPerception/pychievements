import os
import random
import unittest
import tempfile

from pychievements import Achievement, icons
from pychievements import cli
from pychievements.trackers import AchievementTracker, NotRegistered, AlreadyRegistered
from pychievements.backends import SQLiteAchievementBackend
from pychievements.signals import receiver, goal_achieved, level_increased, highest_level_achieved


def AchievementFactory(name):
    attrs = {'name': name, 'category': random.choice(CATEGORIES),
             'keywords': random.sample(KEYWORDS, random.randrange(1, len(KEYWORDS))),
             'goals': tuple({'level': _, 'name': str(_), 'icon': icons.star, 'description': str(_)}
                            for _ in range(15, random.randrange(25, 50, 5), 5))}
    return type(name, (Achievement,), attrs)


CATEGORIES = ['itaque', 'sapiente', 'consectetur', 'voluptate', 'iusto', 'sint']
KEYWORDS = ['qui', 'officiis', 'expedita', 'saepe', 'placeat', 'perferendis', 'vitae',
            'ullam', 'aut', 'aut', 'enim', 'sint']
TRACKED_IDS = [3324, 608, 'deserunt', 'omnis', 'excepturi', 'dolores', 'vero']
ACHIEVEMENTS = [AchievementFactory("Achieve%d" % _) for _ in range(0, random.randrange(5, 10))]


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tracker = AchievementTracker()
        self.tracker.register(ACHIEVEMENTS)

    def test_bad_backend(self):
        self.assertRaises(ValueError, self.tracker.set_backend, AchievementTracker)

    def test_register_list(self):
        # achievements are added as a list in setUp
        self.assertEquals(len(self.tracker.achievements()), len(ACHIEVEMENTS))

    def test_register_single(self):
        self.tracker = AchievementTracker()
        for a in ACHIEVEMENTS:
            self.tracker.register(a)
        self.assertEquals(len(self.tracker.achievements()), len(ACHIEVEMENTS))
        self.assertRaises(AlreadyRegistered, self.tracker.register, ACHIEVEMENTS[0])

    def test_register_missing_cat(self):
        achiev = AchievementFactory('testFail')
        achiev.category = None
        self.assertRaises(ValueError, self.tracker.register, achiev)

    def test_unregister(self):
        self.tracker.unregister(ACHIEVEMENTS[0])
        self.assertEquals(len(self.tracker.achievements()), len(ACHIEVEMENTS)-1)
        self.assertRaises(NotRegistered, self.tracker.unregister, ACHIEVEMENTS[0])

    def test_is_registered(self):
        self.assertTrue(self.tracker.is_registered(ACHIEVEMENTS[0]))
        self.tracker.unregister(ACHIEVEMENTS[1])
        self.assertFalse(self.tracker.is_registered(ACHIEVEMENTS[1]))

    def test_achievements(self):
        self.assertEqual(len(self.tracker.achievements()), len(ACHIEVEMENTS))

    def test_achievements_category(self):
        cat = random.choice(CATEGORIES)
        num_achieves = len([_ for _ in ACHIEVEMENTS if _.category == cat])
        self.assertEqual(len(self.tracker.achievements(category=cat)), num_achieves)

    def test_achievements_keywords(self):
        keys = random.sample(KEYWORDS, 2)
        num_achieves = len([_ for _ in ACHIEVEMENTS
                            if keys[0] in _.keywords and keys[1] in _.keywords])
        self.assertEqual(len(self.tracker.achievements(keywords=keys)), num_achieves)

    def test_achievement_for_id(self):
        tid = random.choice(TRACKED_IDS)
        achiev = self.tracker.achievement_for_id(tid, random.choice(ACHIEVEMENTS))
        repr(achiev)
        self.assertEqual(self.tracker.current(tid, achiev), achiev.current)

        self.assertRaises(NotRegistered, self.tracker.achievement_for_id, tid, 'NotRegistered')

    def test_increment(self):
        tid = random.choice(TRACKED_IDS)
        num_increment = random.randint(20, 60)
        for _ in range(num_increment):
            self.tracker.increment(tid, random.choice(self.tracker.achievements()))
        total = sum([_.current[0] for _ in self.tracker.achievements_for_id(tid)])
        self.assertEqual(total, num_increment)

    def test_evaluate(self):
        tid = random.choice(TRACKED_IDS)
        self.assertEqual(self.tracker.evaluate(tid, random.choice(ACHIEVEMENTS)), [])

    def test_set_level(self):
        tid = 'randomeID'
        achiev = random.choice(ACHIEVEMENTS)
        self.tracker.set_level(tid, achiev, 100)
        self.assertEqual(self.tracker.current(tid, achiev)[0], 100)

    def test_remove_id(self):
        tid = random.choice(TRACKED_IDS)
        for _ in TRACKED_IDS:
            self.tracker.increment(_, random.choice(ACHIEVEMENTS))
        self.tracker.remove_id(tid)
        print(self.tracker.get_tracked_ids())
        self.assertEqual(len(self.tracker.get_tracked_ids()), len(TRACKED_IDS)-1)


class AchievementBackenedTests(unittest.TestCase):
    # only tests things that haven't been hit in TrackerTests
    def setUp(self):
        self.tracker = AchievementTracker()
        self.tracker.register(ACHIEVEMENTS)

    def test_set_level_for_id(self):
        self.tracker._backend.set_level_for_id('newid', random.choice(ACHIEVEMENTS), 100)


class SQLiteBackendTests(unittest.TestCase):
    def setUp(self):
        self.dbfile = tempfile.NamedTemporaryFile(delete=False)
        self.dbfile.close()
        self.backend = SQLiteAchievementBackend(self.dbfile.name)
        self.tracker = AchievementTracker()
        self.tracker.set_backend(self.backend)
        self.tracker.register(ACHIEVEMENTS)

    def tearDown(self):
        os.remove(self.dbfile.name)

    def test_increment(self):
        tid = random.choice(TRACKED_IDS)
        num_increment = random.randint(20, 60)
        for _ in range(num_increment):
            self.tracker.increment(tid, random.choice(self.tracker.achievements()))
        total = sum([_.current[0] for _ in self.tracker.achievements_for_id(tid)])
        self.assertEqual(total, num_increment)

    def test_achievement_for_id(self):
        tid = random.choice(TRACKED_IDS)
        achiev = self.tracker.achievement_for_id(tid, random.choice(ACHIEVEMENTS))
        self.assertEqual(self.tracker.current(tid, achiev), achiev.current)
        self.assertRaises(NotRegistered, self.tracker.achievement_for_id, tid, 'NotRegistered')

    def test_set_level(self):
        tid = 'randomID'
        achiev = random.choice(ACHIEVEMENTS)
        self.tracker.set_level(tid, achiev, 100)
        self.assertEqual(self.tracker.current(tid, achiev)[0], 100)

    def test_remove_id(self):
        tid = random.choice(TRACKED_IDS)
        for _ in TRACKED_IDS:
            self.tracker.increment(_, random.choice(ACHIEVEMENTS))
        self.tracker.remove_id(tid)
        self.assertEqual(len(self.tracker.get_tracked_ids()), len(TRACKED_IDS)-1)


@receiver([goal_achieved, level_increased, highest_level_achieved])
def recv(*args, **kwargs):
    pass


@receiver(goal_achieved)
def recv2(*args, **kwargs):
    pass


class recvClass:
    def __self__(self):
        return self

    def __func__(self, *args, **kwargs):
        pass


class SignalsTest(unittest.TestCase):
    def setUp(self):
        self.tracker = AchievementTracker()
        self.tracker.register(ACHIEVEMENTS)
        self.signal_received = False

    def test_goal_achieved(self):
        rec = lambda s=self, *args, **kwargs: setattr(s, 'signal_received', True)
        goal_achieved.connect(rec, dispatch_uid='test')

        tid = random.choice(TRACKED_IDS)
        achiev = self.tracker.achievement_for_id(tid, random.choice(ACHIEVEMENTS))
        self.tracker.set_level(tid, achiev, achiev.goals[-2]['level']+1)
        self.assertTrue(self.signal_received)
        goal_achieved.disconnect(rec, dispatch_uid='test')

    def test_level_increased(self):
        rec = lambda s=self, *args, **kwargs: setattr(s, 'signal_received', True)
        receiver(rec)
        level_increased.connect(rec)

        tid = random.choice(TRACKED_IDS)
        achiev = self.tracker.achievement_for_id(tid, random.choice(ACHIEVEMENTS))
        self.tracker.increment(tid, achiev)
        self.assertTrue(self.signal_received)
        level_increased.disconnect(rec)

    def test_highest_level_achieved(self):
        rec = lambda s=self, *args, **kwargs: setattr(s, 'signal_received', True)
        highest_level_achieved.connect(rec)

        tid = random.choice(TRACKED_IDS)
        achiev = self.tracker.achievement_for_id(tid, random.choice(ACHIEVEMENTS))
        self.tracker.set_level(tid, achiev, achiev.goals[-1]['level']+1)
        self.assertTrue(self.signal_received)
        highest_level_achieved.disconnect(rec)

    def test_duplicate_reciever(self):
        highest_level_achieved.connect(recvClass)
        highest_level_achieved.connect(recvClass)
        self.assertTrue(highest_level_achieved.has_listeners())
        highest_level_achieved.disconnect(recvClass)

    def test_signal_send(self):
        rec = lambda s=self, *args, **kwargs: setattr(s, 'signal_received', True)
        highest_level_achieved.connect(rec)
        highest_level_achieved.send(self)
        highest_level_achieved.disconnect(rec)

    def test_callback_exception(self):
        def raise_exc(*args, **kwargs):
            raise Exception('test')
        highest_level_achieved.connect(raise_exc)
        r = highest_level_achieved.send_robust(self)
        self.assertNotEqual(r, [])
        highest_level_achieved.disconnect(raise_exc)


class IconsTests(unittest.TestCase):
    def test_color_catcher(self):
        import sys
        del sys.modules['pychievements.icons']
        textui = sys.modules['clint.textui']
        sys.modules['clint.textui'] = sys.modules['nose']
        import pychievements.icons
        c = pychievements.icons.ColorCatcher()
        self.assertEqual(c.red('test'), 'test')
        sys.modules['clint.textui'] = textui


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tracker = AchievementTracker()
        self.tracker.register(ACHIEVEMENTS)

    def test_print_goal(self):
        cli.print_goal(ACHIEVEMENTS[0].goals[0], achieved=True, level=100)

    def test_print_goals(self):
        cli.print_goals(ACHIEVEMENTS[0])

    def test_print_goals_for_tracked(self):
        cli.print_goals_for_tracked(random.choice(TRACKED_IDS), unachieved=True)
        cli.print_goals_for_tracked(random.choice(TRACKED_IDS), ACHIEVEMENTS[0], unachieved=True,
                                    tracker=self.tracker)
        cli.print_goals_for_tracked(random.choice(TRACKED_IDS), ACHIEVEMENTS, unachieved=True,
                                    tracker=self.tracker)
        cli.print_goals_for_tracked(random.choice(TRACKED_IDS), only_current=True,
                                    tracker=self.tracker)


if __name__ == '__main__':
    unittest.main()
