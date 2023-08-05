#!/usr/bin/python3.6

import argparse
import logging
import time
from os.path import abspath

import coloredlogs

from .bot_factory import retrieve_bots
from .bot_storage import LocalBotStorage, SscaitBotStorage
from .docker import check_docker_requirements, BASE_VNC_PORT, launch_game, stop_containers
from .game import GameType
from .map import check_map_exists, SC_MAP_DIR
from .player import HumanPlayer, PlayerRace, bot_regex, SC_BOT_DIR
from .utils import random_string
from .vnc import check_vnc_exists

# Default bot dirs
SC_LOG_DIR = abspath("logs")
SC_BWAPI_DATA_BWTA_DIR = abspath("bwapi-data/BWTA")
SC_BWAPI_DATA_BWTA2_DIR = abspath("bwapi-data/BWTA2")
SC_BOT_DATA_READ_DIR = abspath("bot-data/read")
SC_BOT_DATA_WRITE_DIR = abspath("bot-data/write")
SC_BOT_DATA_LOGS_DIR = abspath("bot-data/logs")

SC_IMAGE = "ggaic/starcraft:play"

parser = argparse.ArgumentParser(
    description='Launch StarCraft docker images for bot/human headless/headful play',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--bots', nargs="+", required=True, type=bot_regex,
                    metavar="BOT_NAME[:RACE]",
                    help='Specify the names of the bots that should play.\n'
                         f'Optional RACE can be one of {[race.value for race in PlayerRace]} \n'
                         'If RACE isn\'t specified it will be loaded from cache if possible.\n'
                         'The bots are looked up in the --bot_dir directory.\n'
                         'If some does not exist, launcher \n'
                         'will try to download it from SSCAIT server.\n'
                         'Examples: \n'
                         '  --bots Tyr:P PurpleWave:P\n'
                         '  --bots Tyr PurpleWave '
                    )
parser.add_argument('--human', action='store_true',
                    help="Allow play as human against bot.\n")

# todo: support builtin AI
# parser.add_argument('--builtin_ai', type=int, default=0,
#                     help="Add builtin (default) AI to play against.\n"
#                          "Specify how many AIs will play the game. (default 0)")

parser.add_argument('--map', type=str, metavar="MAP.scx", default="sscai/(2)Benzene.scx",
                    help="Name of map on which SC should be played,\n"
                         "relative to --map_dir")
parser.add_argument('--headless', action='store_true',
                    help="Launch play in headless mode. \n"
                         "No VNC viewer will be launched.")

# Game settings
parser.add_argument("--game_name", type=str, default=random_string(8),
                    help="Override the auto-generated game name")
parser.add_argument("--game_type", type=str, metavar="GAME_TYPE",
                    default=GameType.FREE_FOR_ALL.value,
                    choices=[game_type.value for game_type in GameType],
                    help="Set game type. It can be one of:\n- " +
                         "\n- ".join([game_type.value for game_type in GameType]))
parser.add_argument("--game_speed", type=int, default=0,
                    help="Set game speed (pause of ms between frames),\n"
                         "use -1 for game default.")
parser.add_argument("--timeout", type=int, default=None,
                    help="Kill docker container after timeout seconds.\n"
                         "If not set, run without timeout.")

# Volumes
parser.add_argument('--bot_dir', type=str, default=SC_BOT_DIR,
                    help=f"Directory where bots are stored, default:\n{SC_BOT_DIR}")
parser.add_argument('--log_dir', type=str, default=SC_LOG_DIR,
                    help=f"Directory where logs are stored, default:\n{SC_LOG_DIR}")
parser.add_argument('--map_dir', type=str, default=SC_MAP_DIR,
                    help=f"Directory where maps are stored, default:\n{SC_MAP_DIR}")

#  BWAPI data volumes
parser.add_argument('--bwapi_data_bwta_dir', type=str, default=SC_BWAPI_DATA_BWTA_DIR,
                    help=f"Directory where BWTA map caches are stored, "
                         f"default:\n{SC_BWAPI_DATA_BWTA_DIR}")
parser.add_argument('--bwapi_data_bwta2_dir', type=str, default=SC_BWAPI_DATA_BWTA2_DIR,
                    help=f"Directory where BWTA2 map caches are stored, "
                         f"default:\n{SC_BWAPI_DATA_BWTA2_DIR}")

# VNC
parser.add_argument('--vnc_base_port', type=int, default=BASE_VNC_PORT,
                    help="VNC lowest port number (for server).\n"
                         "Each consecutive n-th client (player)\n"
                         "has higher port number - vnc_base_port+n ")

# Settings
parser.add_argument('--show_all', action="store_true",
                    help="Launch VNC viewers for all containers, not just the server.")
parser.add_argument('--log_level', type=str, default="INFO",
                    choices=['DEBUG', 'INFO', 'WARN', 'ERROR'],
                    help="Logging level.")
parser.add_argument('--read_overwrite', action="store_true",
                    help="At the end of each game, copy the contents\n"
                         "of 'write' directory to the read directory\n"
                         "of the bot.\n"
                         "Needs to be explicitly turned on.")
parser.add_argument('--docker_image', type=str, default=SC_IMAGE,
                    help="The name of the image that should \n"
                         "be used to launch the game.\n"
                         "This helps with local development.")
parser.add_argument('--opt', type=str,
                    help="Specify custom docker run options")

# todo: add support for multi-PC play.
# We need to think about how to setup docker IPs,
# maybe we will need to specify manually routing tables? :/

logger = logging.getLogger(__name__)


def main():
    args = parser.parse_args()
    coloredlogs.install(level=args.log_level)

    check_docker_requirements()
    check_map_exists(args.map_dir + "/" + args.map)
    if not args.headless:
        check_vnc_exists()

    if args.human and args.headless:
        raise Exception("Cannot use human play in headless mode")
    if args.headless and args.show_all:
        raise Exception("Cannot show all screens in headless mode")

    game_name = "GAME_" + args.game_name

    players = []
    if args.human:
        players.append(HumanPlayer())

    bot_storages = (LocalBotStorage(args.bot_dir), SscaitBotStorage(args.bot_dir))
    players += retrieve_bots(args.bots, bot_storages)

    opts = [] if not args.opt else args.opt.split(" ")

    launch_params = dict(
        # game settings
        headless=args.headless,
        game_name=game_name,
        map_name=args.map,
        game_type=GameType(args.game_type),
        game_speed=args.game_speed,
        timeout=args.timeout,

        # mount dirs
        log_dir=args.log_dir,
        bot_dir=args.bot_dir,
        map_dir=args.map_dir,
        bwapi_data_bwta_dir=args.bwapi_data_bwta_dir,
        bwapi_data_bwta2_dir=args.bwapi_data_bwta2_dir,

        # vnc
        vnc_base_port=args.vnc_base_port,

        # docker
        docker_image=args.docker_image,
        docker_opts=opts
    )

    time_start = time.time()
    try:
        launch_game(players, launch_params, args.show_all, args.read_overwrite)
        diff = time.time() - time_start
        logger.info(f"Game finished in {diff:.2f} seconds.")

    except KeyboardInterrupt:
        logger.info("Caught interrupt, shutting down containers")
        logger.info("This can take a moment, please wait.")
        stop_containers(game_name)
        diff = time.time() - time_start
        logger.info(f"Game cancelled after {diff:.2f} seconds.")


if __name__ == '__main__':
    main()
