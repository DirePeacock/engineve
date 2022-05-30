import logging
import time
import rich



from rich import box, print
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.console import Console
from rich.progress_bar import ProgressBar
from rich.progress import Progress
from .gameengine import GameEngine
from .gametypes.actor import Actor
from .tags import TAGS

MAP_WIDTH = 10
MAP_HEIGHT = 10
MAP_CHAR_WIDTH = 3
EMPTY_CHAR = '.'
DEMO_FPS = 2
attack_frames = 2
class SlowDemoEngine(GameEngine):
    fps = DEMO_FPS
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.flip_flop = True
    def periodic(self):
        if not self.engine_sync.is_waiting():
            if self.flip_flop:
                self.engine_state.periodic(self.game_state, self.invoker)
            else:
                self.invoker.periodic(self.game_state)
            self.flip_flop = not self.flip_flop
        
        self.engine_sync.periodic()
        self.frame += 1
def factory(spawn=False):
    GAMEENGINE = SlowDemoEngine()
    if spawn:
        for team_id in [0, 1]:
            GAMEENGINE.spawn_actors(actor_class=Actor, num=3, team=team_id)
    for a_id in GAMEENGINE.game_state.actors.keys():
        for m_id in GAMEENGINE.game_state.actors[a_id].game_moves.keys():
            if 'attack' in m_id.lower():
                GAMEENGINE.game_state.actors[a_id].game_moves[m_id].add_tag(dict({TAGS.animation: attack_frames}))
    
    return GAMEENGINE

def EMPTY_MAP(): 
    return [[' . ' for i in list(range(0,MAP_WIDTH))] for i in range(0,MAP_HEIGHT)]

def _get_color(hp):
    return "[red]" if hp < 1 else "[green]"
def _get_team_color(team):
    return "[blue]" if team < 1 else "[red]"
def _get_team_char(team):
    return "b" if team < 1 else "r"

class GraphicsEngineDemo:
    def __init__(self):
        self.layout = Layout()
        self.console = Console()
        
        self.layout.split_row(Layout(name="screen", minimum_size=MAP_CHAR_WIDTH*MAP_WIDTH),
                              Layout(name="tables"),
                              Layout(name="log"))
        self.layout['screen'].split_column(Layout(name="map"),
                                           Layout(name="animations"))        
        self.layout['tables'].split_column(Layout(name="stack"),
                                           Layout(name="actors"), 
                                           Layout(name="init"))
    def draw(self, engine) -> Layout:
        
        self.layout['tables']['actors'].update(self._drawActors(engine.game_state))
        self.layout['tables']['init'].update(self._drawInit(engine.game_state))
        self.layout['tables']['stack'].update(self._drawStack(engine.game_state.log.stack))
        self.layout['screen']['map'].update(self._drawMap(engine.game_state))
        self.layout['screen']['animations'].update(self._drawAnimationBar(engine.engine_sync))
        self.layout['log'].update(self._drawLog(engine.game_state.log.history))
        return self.layout
    
    def main(self, fps):
        engine = factory(spawn=True)
        with Live(self.layout, console=self.console, screen=False, refresh_per_second=fps) as livelayout:
            for i in range(1000):
                engine.periodic()
                livelayout.update(self.draw(engine))
                time.sleep(1/fps)
            time.sleep(1)
            quit(0)
    
    @classmethod
    def run(cls, fps, *args, **kwargs):
        inst = cls(*args, **kwargs)
        inst.main(fps)
    
    def _drawAnimationBar(self, engine_sync):
        wait_ends = {wid: wait.end_frame for wid, wait in engine_sync.waits.items()}
        if len(wait_ends) == 0:
            return Text('no active animations')
        
        wid = max(wait_ends, key=wait_ends.get)
        now = engine_sync.engine.frame - engine_sync.waits[wid].start_frame
        end = engine_sync.waits[wid].length
        now = min(now, end)
        
        return ProgressBar(100.0, ((100.0 * now)/end))
    def _drawActors(self, game_state):
        actorTable = Table()
        actorTable.add_column('name')
        actorTable.add_column('hp')
        for actor in game_state.actors.values():
            # GAME_STATE.actors:
            actorTable.add_row(f"[b]{_get_team_color(actor.team)}{actor.name}[/]", f"{_get_color(actor.hp)}{actor.hp}")
        return actorTable
    
    def _drawActors(self, game_state):
        actorTable = Table()
        actorTable.add_column('name')
        actorTable.add_column('hp')
        actorTable.add_column('loc')
        for actor in game_state.actors.values():
            # GAME_STATE.actors:
            actorTable.add_row(f"[b]{_get_team_color(actor.team)}{actor.name}[/]", 
                               f"{_get_color(actor.hp)}{actor.hp}",
                               f"{actor.loc}")
        return actorTable
    
    def _drawInit(self, game_state):
        actorTable = Table()
        actorTable.add_column('turn')
        actorTable.add_column('name')
        actorTable.add_column('init')
        if 0 == len(game_state.combat.order.keys()):
            return actorTable

        ordered_inits = list(game_state.combat.order.keys())
        ordered_inits.sort(reverse=True)
        for val in ordered_inits:
            actor_id = game_state.combat.order[val]
        # for val, actor_id in game_state.combat.order.items():
            # GAME_STATE.actors:
            turn_str = "X" if val == game_state.combat.current_iter else " "
            actorTable.add_row(turn_str, f"{game_state.actors[actor_id].name}", str(val))
        return actorTable

    def _drawLog(self, log):
        logPanel = Text()
        visible_lines = ['---LOG---']
        if len(log) >= 1:
            [visible_lines.append(line) for line in log[-self.console.height:]]
        
        while len(visible_lines) < self.console.height:
            visible_lines.append('.')
        logPanel.append(Text('\n'.join(visible_lines))) 
        
        return logPanel

    def _drawStack(self, stack):
        logPanel = Text()
        visible_lines = ['---STACK---']
        if len(stack) >= 1:
            [visible_lines.append(line) for line in stack[-self.console.height:]]
        
        while len(visible_lines) < self.console.height:
            visible_lines.append('.')
        logPanel.append(Text('\n'.join(visible_lines))) 
        
        return logPanel

    def _drawMap(self, game_state):
        MAP = EMPTY_MAP()
        for actor in [game_state.actors[a_id] for a_id in game_state.combat.actor_ids]:
            inverted_y_loc = MAP_HEIGHT - (actor.loc[1]+1)
            
            # MAP[inverted_y_loc][actor.loc[0]] = f"[b]{_get_team_color(actor.team)}{actor.name[0].upper()}[/]"
            team_char = _get_team_char(actor.team)
            map_str = f"{team_char}{actor.name[0].upper()}{max(0,actor.hp)}"
            MAP[inverted_y_loc][actor.loc[0]] = map_str
        
        for i in range((MAP_HEIGHT - 1), -1, -1):
            visual_index = (MAP_HEIGHT - 1 - i )
            MAP[visual_index].insert(0,"|")
            MAP[visual_index].insert(0,f"{i}")
            if i < 10:
                MAP[visual_index].insert(0," ")

        mapstr = Text('')
        # for line in [''.join([row_char for row_char in column]) for column in MAP]:
        for column in MAP:
            for row in column:
                mapstr.append_text(Text(row))    
            mapstr.append_text(Text("\n"))
        last_row_rule_offset = '   '
        rowstr = ''.join([f" {i} " if i<10 else f"{i} "  for i in range(MAP_WIDTH)])
        mapstr.append_text(Text(last_row_rule_offset + rowstr))
        MAP_TEXT = Panel(mapstr, title='MAP', height=MAP_HEIGHT+3, width=(MAP_CHAR_WIDTH * MAP_WIDTH)+7)
        return MAP_TEXT
    
    
def rich_main(debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    GraphicsEngineDemo.run(fps=DEMO_FPS)