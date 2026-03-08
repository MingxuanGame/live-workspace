from __future__ import annotations

from enum import IntEnum
from typing import Any, NoReturn, Optional, override

from nonebot.adapters import Event, Message
from nonebot.exception import NoLogException
from pydantic import BaseModel, Field


class Status(IntEnum):
    NOT_RUNNING = -1
    MAIN_MENU = 0
    EDITING_MAP = 1
    PLAYING = 2
    GAME_SHUTDOWN_ANIMATION = 3
    SONG_SELECT_EDIT = 4
    SONG_SELECT = 5
    WIP_NO_IDEA_WHAT_THIS_IS = 6
    RESULTS_SCREEN = 7
    GAME_STARTUP_ANIMATION = 10
    MULTIPLAYER_ROOMS = 11
    MULTIPLAYER_ROOM = 12
    MULTIPLAYER_SONG_SELECT = 13
    MULTIPLAYER_RESULTS_SCREEN = 14
    OSU_DIRECT = 15
    RANKING_TAG_COOP = 17
    RANKING_TEAM = 18
    PROCESSING_BEATMAPS = 19
    TOURNEY = 22
    UNKNOWN = -2


class State(BaseModel):
    number: Status
    name: str


class Session(BaseModel):
    play_time: int = Field(alias="playTime")
    play_count: int = Field(alias="playCount")


class ChatVisibilityStatus(BaseModel):
    number: Optional[int] = None
    name: str


class LeaderboardType(BaseModel):
    number: Optional[int] = None
    name: str


class Leaderboard(BaseModel):
    visible: bool
    type: LeaderboardType


class ProgressBar(BaseModel):
    number: int
    name: str


class Resolution(BaseModel):
    fullscreen: bool
    width: int
    height: int
    width_fullscreen: int = Field(alias="widthFullscreen")
    height_fullscreen: int = Field(alias="heightFullscreen")


class Client(BaseModel):
    update_available: bool = Field(alias="updateAvailable")
    branch: int
    version: str


class ScoreMeterType(BaseModel):
    number: int
    name: str


class ScoreMeter(BaseModel):
    type: ScoreMeterType
    size: float


class Cursor(BaseModel):
    use_skin_cursor: bool = Field(alias="useSkinCursor")
    auto_size: bool = Field(alias="autoSize")
    size: float
    menu_size: Optional[float] = Field(default=None, alias="menuSize")


class Mouse(BaseModel):
    raw_input: bool = Field(alias="rawInput")
    high_precision: Optional[bool] = Field(default=None, alias="highPrecision")
    disable_buttons: bool = Field(alias="disableButtons")
    disable_wheel: bool = Field(alias="disableWheel")
    sensitivity: float


class Tablet(BaseModel):
    enabled: bool
    x: int
    y: int
    width: int
    height: int
    rotation: int
    pressure_threshold: int = Field(alias="pressureThreshold")


class ScrollDirection(BaseModel):
    number: int
    name: str


class Mania(BaseModel):
    speed_bpm_scale: bool = Field(alias="speedBPMScale")
    use_per_beatmap_speed_scale: bool = Field(alias="usePerBeatmapSpeedScale")
    scroll_speed: Optional[int] = Field(default=None, alias="scrollSpeed")
    scroll_direction: Optional[ScrollDirection] = Field(
        default=None, alias="scrollDirection"
    )


class Sort(BaseModel):
    number: int
    name: str


class Group(BaseModel):
    number: int
    name: str


class Skin(BaseModel):
    use_default_skin_in_editor: bool = Field(alias="useDefaultSkinInEditor")
    ignore_beatmap_skins: bool = Field(alias="ignoreBeatmapSkins")
    tint_slider_ball: bool = Field(alias="tintSliderBall")
    use_taiko_skin: bool = Field(alias="useTaikoSkin")
    name: str


class Mode(BaseModel):
    number: Optional[int] = None
    name: str


class Volume(BaseModel):
    master_inactive: Optional[float] = Field(default=None, alias="masterInactive")
    master: float
    music: float
    effect: float


class Offset(BaseModel):
    universal: float


class Audio(BaseModel):
    ignore_beatmap_sounds: bool = Field(alias="ignoreBeatmapSounds")
    use_skin_samples: bool = Field(alias="useSkinSamples")
    volume: Volume
    offset: Offset


class Background(BaseModel):
    dim: float
    video: bool
    storyboard: bool
    blur: Optional[float] = None


class OsuKeybinds(BaseModel):
    k1: str
    k2: str
    smoke_key: str = Field(alias="smokeKey")


class FruitsKeybinds(BaseModel):
    k1: str
    k2: str
    dash: str = Field(alias="Dash")


class TaikoKeybinds(BaseModel):
    inner_left: str = Field(alias="innerLeft")
    inner_right: str = Field(alias="innerRight")
    outer_left: str = Field(alias="outerLeft")
    outer_right: str = Field(alias="outerRight")


class Keybinds(BaseModel):
    osu: OsuKeybinds
    fruits: FruitsKeybinds
    taiko: TaikoKeybinds
    quick_retry: str = Field(alias="quickRetry")


class Settings(BaseModel):
    interface_visible: bool = Field(alias="interfaceVisible")
    replay_ui_visible: bool = Field(alias="replayUIVisible")
    chat_visibility_status: ChatVisibilityStatus = Field(alias="chatVisibilityStatus")
    leaderboard: Leaderboard
    progress_bar: ProgressBar = Field(alias="progressBar")
    bass_density: float = Field(alias="bassDensity")
    resolution: Resolution
    client: Client
    score_meter: ScoreMeter = Field(alias="scoreMeter")
    cursor: Cursor
    mouse: Mouse
    tablet: Optional[Tablet] = None
    mania: Mania
    sort: Sort
    group: Group
    skin: Skin
    mode: Mode
    audio: Audio
    background: Background
    keybinds: Keybinds


class UserStatus(BaseModel):
    number: Optional[int] = None
    name: str


class BanchoStatus(BaseModel):
    number: Optional[int] = None
    name: str


class CountryCode(BaseModel):
    number: Optional[int] = None
    name: str


class Profile(BaseModel):
    user_status: UserStatus = Field(alias="userStatus")
    bancho_status: BanchoStatus = Field(alias="banchoStatus")
    id: Optional[int] = None
    name: Optional[str] = None
    mode: Optional[Mode] = None
    ranked_score: Optional[int] = Field(default=None, alias="rankedScore")
    level: Optional[float] = None
    accuracy: Optional[float] = None
    pp: Optional[int] = None
    play_count: Optional[int] = Field(default=None, alias="playCount")
    global_rank: Optional[int] = Field(default=None, alias="globalRank")
    country_code: CountryCode = Field(alias="countryCode")
    background_colour: Optional[str] = Field(default=None, alias="backgroundColour")


class BeatmapTime(BaseModel):
    live: int
    first_object: int = Field(alias="firstObject")
    last_object: int = Field(alias="lastObject")
    mp3_length: Optional[int] = Field(default=None, alias="mp3Length")


class BeatmapStatus(BaseModel):
    number: Optional[int] = None


class Stars(BaseModel):
    live: float
    total: float
    aim: Optional[float] = None
    speed: Optional[float] = None
    flashlight: Optional[float] = None
    slider_factor: Optional[float] = Field(default=None, alias="sliderFactor")


class StatValue(BaseModel):
    original: float
    converted: float


class BPM(BaseModel):
    realtime: Optional[float] = None
    common: float
    min: float
    max: float


class BeatmapObjects(BaseModel):
    circles: int
    sliders: int
    spinners: int
    holds: int
    total: int


class BeatmapStats(BaseModel):
    stars: Stars
    ar: StatValue
    cs: StatValue
    od: StatValue
    hp: StatValue
    bpm: BPM
    objects: BeatmapObjects
    max_combo: int = Field(alias="maxCombo")


class Beatmap(BaseModel):
    is_kiai: Optional[bool] = Field(default=None, alias="isKiai")
    is_break: Optional[bool] = Field(default=None, alias="isBreak")
    is_convert: Optional[bool] = Field(default=None, alias="isConvert")
    time: BeatmapTime
    status: BeatmapStatus
    checksum: str
    id: int
    set: int
    mode: Optional[Mode] = None
    artist: str
    artist_unicode: str = Field(alias="artistUnicode")
    title: str
    title_unicode: str = Field(alias="titleUnicode")
    mapper: str
    version: str
    stats: BeatmapStats


class HealthBar(BaseModel):
    normal: float
    smooth: float


class Hits(BaseModel):
    hit_0: int = Field(default=0, alias="0")
    hit_50: int = Field(default=0, alias="50")
    hit_100: int = Field(default=0, alias="100")
    hit_300: int = Field(default=0, alias="300")
    geki: int
    katu: int
    slider_breaks: Optional[int] = Field(default=None, alias="sliderBreaks")
    slider_end_hits: Optional[int] = Field(default=None, alias="sliderEndHits")
    small_tick_hits: Optional[int] = Field(default=None, alias="smallTickHits")
    large_tick_hits: Optional[int] = Field(default=None, alias="largeTickHits")


class Combo(BaseModel):
    current: int
    max: int


class Mods(BaseModel):
    checksum: Optional[str] = None
    number: Optional[int] = None
    name: str
    array: Optional[list[Any]] = None
    rate: Optional[float] = None


class Rank(BaseModel):
    current: str
    max_this_play: str = Field(alias="maxThisPlay")


class PPDetailed(BaseModel):
    aim: float
    speed: float
    accuracy: float
    difficulty: float
    flashlight: float
    total: float


class PP(BaseModel):
    current: float
    fc: float
    max_achieved: Optional[float] = Field(default=None, alias="maxAchieved")
    max_achievable: Optional[float] = Field(default=None, alias="maxAchievable")
    max_achieved_this_play: Optional[float] = Field(
        default=None, alias="maxAchievedThisPlay"
    )
    detailed: Optional[dict[str, PPDetailed]] = None


class Play(BaseModel):
    player_name: str = Field(alias="playerName")
    mode: Mode
    score: int
    accuracy: float
    health_bar: HealthBar = Field(alias="healthBar")
    hits: Hits
    hit_error_array: list[float] = Field(alias="hitErrorArray")
    combo: Combo
    mods: Mods
    rank: Rank
    pp: PP
    unstable_rate: float = Field(alias="unstableRate")


class AccuracyPerformance(BaseModel):
    acc_90: Optional[float] = Field(default=None, alias="90")
    acc_91: Optional[float] = Field(default=None, alias="91")
    acc_92: Optional[float] = Field(default=None, alias="92")
    acc_93: Optional[float] = Field(default=None, alias="93")
    acc_94: Optional[float] = Field(default=None, alias="94")
    acc_95: Optional[float] = Field(default=None, alias="95")
    acc_96: Optional[float] = Field(default=None, alias="96")
    acc_97: Optional[float] = Field(default=None, alias="97")
    acc_98: Optional[float] = Field(default=None, alias="98")
    acc_99: Optional[float] = Field(default=None, alias="99")
    acc_100: Optional[float] = Field(default=None, alias="100")


class Graph(BaseModel):
    series: list[Any]
    xaxis: list[Any]


class Performance(BaseModel):
    accuracy: AccuracyPerformance
    graph: Graph


class ResultsScreenHits(BaseModel):
    hit_0: int = Field(default=0, alias="0")
    hit_50: int = Field(default=0, alias="50")
    hit_100: int = Field(default=0, alias="100")
    hit_300: int = Field(default=0, alias="300")
    geki: int
    katu: int
    slider_end_hits: Optional[int] = Field(default=None, alias="sliderEndHits")
    small_tick_hits: Optional[int] = Field(default=None, alias="smallTickHits")
    large_tick_hits: Optional[int] = Field(default=None, alias="largeTickHits")


class ResultsScreenPP(BaseModel):
    current: float
    fc: float


class ResultsScreen(BaseModel):
    score_id: Optional[int] = Field(default=None, alias="scoreId")
    player_name: str = Field(alias="playerName")
    mode: Mode
    score: int
    accuracy: float
    name: Optional[str] = None
    hits: ResultsScreenHits
    mods: Mods
    rank: str
    max_combo: int = Field(alias="maxCombo")
    pp: ResultsScreenPP
    created_at: str = Field(alias="createdAt")


class Folders(BaseModel):
    game: str
    skin: str
    songs: str
    beatmap: str


class Files(BaseModel):
    beatmap: str
    background: str
    audio: str


class DirectPath(BaseModel):
    beatmap_file: str = Field(alias="beatmapFile")
    beatmap_background: str = Field(alias="beatmapBackground")
    beatmap_audio: str = Field(alias="beatmapAudio")
    beatmap_folder: str = Field(alias="beatmapFolder")
    skin_folder: str = Field(alias="skinFolder")


class Team(BaseModel):
    left: str
    right: str


class Points(BaseModel):
    left: int
    right: int


class TotalScore(BaseModel):
    left: int
    right: int


class TourneyUser(BaseModel):
    id: int
    name: str
    country: str
    accuracy: float
    ranked_score: int = Field(alias="rankedScore")
    play_count: int = Field(alias="playCount")
    global_rank: int = Field(alias="globalRank")
    total_pp: int = Field(alias="totalPP")


class TourneyClient(BaseModel):
    team: str
    user: TourneyUser
    play: Play


class Tourney(BaseModel):
    score_visible: bool = Field(alias="scoreVisible")
    stars_visible: bool = Field(alias="starsVisible")
    ipc_state: int = Field(alias="ipcState")
    best_of: int = Field(alias="bestOF")
    team: Team
    points: Points
    chat: list[Any]
    total_score: TotalScore = Field(alias="totalScore")
    clients: list[TourneyClient]


class TosuData(BaseModel):
    client: str
    server: Optional[str] = None
    state: State
    session: Session
    settings: Settings
    profile: Profile
    beatmap: Beatmap
    play: Play
    leaderboard: list[Any]
    performance: Performance
    results_screen: ResultsScreen = Field(alias="resultsScreen")
    folders: Folders
    files: Files
    direct_path: DirectPath = Field(alias="directPath")
    tourney: Tourney


class TosuEvent(TosuData, Event):
    @override
    def get_event_name(self) -> str:
        return "tosu_event"

    @override
    def get_type(self) -> str:
        return "tosu"

    @override
    def get_message(self) -> Message:
        raise ValueError("No message")

    @override
    def get_event_description(self) -> str:
        return "Tosu event"

    @override
    def get_user_id(self) -> str:
        return str(self.profile.id or 0)

    @override
    def get_session_id(self) -> str:
        return f"{self.settings.client}.{self.profile.id or 0}"

    @override
    def get_log_string(self) -> NoReturn:
        raise NoLogException("tosu")

    @override
    def is_tome(self) -> bool:
        return False
