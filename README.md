# AgriCraft Data Converter

A simple Python script that converts old AgriCraft data into the 1.20.1/1.20.4 format.

## How to Use

1. **Setup:**
   - Create a new directory with all the scripts.
   - Inside this directory, create a subfolder named `old`.

2. **Add Your Data:**
   - Place your old AgriCraft data inside the `old` folder. The folder structure should match the structure used in [AgriCraft/AgriPlants](https://github.com/AgriCraft/AgriPlants).
   - You can also add a lang file, eg. `en_us.json`. If you do that, make sure you update `LANG` constant in the `updater.py` to match your language.

3. **Run the Script:**
   - Execute `updater.py`.
   - Check the console for any files that were skipped.

4. **When the Script is Done:**
   - After running the script, you will find a new directory named `new` containing `datapack.zip` and `resourcepack.zip`. 
   - `datapack.zip` can be added to the `datapacks` directory of your Minecraft world.
   - `resourcepack.zip` can be added to the `resourcepacks` folder just like any other resourcepack.
