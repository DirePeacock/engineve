from .utils import get_id
from .enginecommands.observer.observer import Observer
from .tags import TAGS, check_tags

class Wait():
    '''I have ids, I'''
    def __init__(self, start_frame, end_frame):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.id = get_id()
    
    @property
    def length(self):
        return self.end_frame - self.start_frame
    
    @length.setter
    def length(self, length):
        self.end_frame = self.start_frame + length

class EngineSync(Observer):
    max_wait_seconds = 10
    def __init__(self, engine):
        super().__init__(trigger=self._has_animation, 
                         reaction=self.wait_for_animation)
        self.waits = {}
        self.engine = engine
        self.max_wait = engine.fps * self.max_wait_seconds

    @staticmethod
    def _has_animation(meta):
        return check_tags(meta, TAGS.animation)
    
    def wait_for_animation(self, meta):
        # TODO you probably want to start an animation as soon as the command is resolved
        #      make sure that this works looks ok later
        animation_frames = meta[TAGS.animation] if meta[TAGS.animation] is not None else 1
        self.wait(animation_frames)

    def wait(self, frames):
        new_wait = Wait(self.engine.frame, (self.engine.frame + frames))
        self.waits[new_wait.id] = new_wait
        return new_wait.id
    
    def remove_wait(self, wait_id):
        del self.waits[wait_id]

    def async_await(self):
        '''some callback should please'''
        return self.wait(self.max_wait)

    def periodic(self):
        '''hopefully there aren't many things pausing the engine itself simultaneously ''' 
        for w_id in [w_id for w_id, wait_obj in self.waits.items() if wait_obj.end_frame <= self.engine.frame]:
            self.remove_wait(w_id)

    
    def is_waiting(self):
        return 0 < len(self.waits)

    def max_rollover(self):
        pass
        # TODO, handle this someday
        # int.