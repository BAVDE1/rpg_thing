

# Screen
FRAME_RATE = 30
BASE_RES = 288  # 256 + 32 for edges
BASE_UNIT = 16  # 16 x 16 grid (with one remainder for each edge, player sees 17x17, ascii needs to be 18x18)
RES_MUL = 2
RESOLUTION = BASE_RES * RES_MUL
UNIT = BASE_UNIT * RES_MUL

# Levels
OVERWORLD_LEVEL_DIR = "levels/overworld_0.txt"

# Textures
PLAYER_TEXTURE = "assets/textures/player.png"

GRASS_TEXTURE = "assets/textures/grass.png"
