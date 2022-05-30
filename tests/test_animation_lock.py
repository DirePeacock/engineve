import includes
from engineve.mainfactory import factory
from engineve.enginecommands.basecommands.command import Command
from engineve.tags import TAGS, TaggedClass

def test_engine_is_waiting():
    ''' adding a wait sets wait to true'''
    engine = factory()
    engine.engine_sync.wait(10)
    assert engine.engine_sync.is_waiting()

def test_wait_attrs():
    ''' adding a wait sets wait to true'''
    engine = factory()
    t = 10
    engine.engine_sync.wait(t)
    i = list(engine.engine_sync.waits.keys())[0]
    assert engine.frame == engine.engine_sync.waits[i].start_frame
    assert engine.engine_sync.waits[i].end_frame == engine.frame + t
    assert engine.engine_sync.waits[i].length == t

def test_animation_unlocking():
    engine = factory()
    t = 10
    engine.engine_sync.wait(t)
    i = list(engine.engine_sync.waits.keys())[0]
    engine.frame += t
    engine.engine_sync.periodic()
    assert (not engine.engine_sync.is_waiting())

def test_lock_on_animation():
    engine = factory()
    anim_frames = 5
    engine.invoker.notify({TAGS.animation: anim_frames})
    
    assert engine.engine_sync.is_waiting()
def test_frame_rollover():
    pass
    # todo test befaviour at num max

