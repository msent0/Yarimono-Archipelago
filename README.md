# Yarimono Archipelago
This is an Archipelago randomizer for the game Yarimono. The game goes by different names on different storefronts:
 - Steam - [Yarimono](https://store.steampowered.com/app/2696050/Yarimono/)
 - 072project - [YARISUTEMESUBUTA～PUMP & DUMP～](https://072project.com/r18/en/shop/RA25126183)
 - DLsite - [Yarimon Master: Using Cheats to Fuck 'em All!](https://www.dlsite.com/maniax/work/=/product_id/RJ01082861.html)

Things randomized:
  - Trainer levels gained from defeated trainers.
  - Trainer levels gained from various events (mushrooms mostly).
  - Chests and hidden item pickups.
  - Event items in shops.
  - Ultimate move unlocks for each type.
  - (Optional) Yariman Encyclopedia scene unlocks.
  - (Optional) Trainer battle money rewards.

There are four possible goals to choose from:
 - Defeat White God - Normal game completion.
 - Defeat Champion - Defeat the postgame fight against Athena (Default).
 - Defeat Tama - Defeat the boss of DLC2.
 - Defeat Nupuryu - Secret boss in the DLC2 dev room. Normally only accessible if you don't use cheat tackle through the whole game. Modified here to always be accessible.

Several trainers added in DLC1 and DLC2 that scale with the player have been modified to give them minimum levels.

There's an additional setting to limit the total number of cheat tackle uses and for unlocking gallery scenes to grant extra cheat tackle uses. Be warned that this can lead to soft locks (since you can't switch to easy and cheat tackle your way though) if you go into events like the ruins or chapter 5 sequence unprepared. You may want to make a separate save before entering these sections.

# Supported Versions
Only version 4.00 of the game is supported. This is the version currently available on DLsite, 072project, and the version you get if you buy the game and both DLCs on Steam and install the DLC2 patch. All three of these versions of 4.00 are compatible. Any other version of the game has not been tested and is unlikely to work, including the unpatched Steam version. The randomization should work with any language selected, but text replacements to show Archipelago items names for some items will not apply correctly on anything but English.

Requires Archipelago version 0.6.7 or higher.

# Installation Instructions
You are assumed to have the Archipelago launcher installed already.
- Download the .apworld file from the releases and add it to Archipelago.
- Run "Yarimono Patcher" from the launcher and select your game directory. This will patch the game with the plugin to communicate with Archipelago.
- Generate a template yaml options file ("Generate Template Options" in the launcher) and set any settings you want to set.
- Use that yaml file (along with any other yaml files for other games being randomized) to generate and host a multiworld.
- When you open the patched Yarimono and start a new game you'll be asked to connect to the Archipelago server.