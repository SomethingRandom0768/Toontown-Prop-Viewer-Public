# Toontown-Prop-Viewer-Public
Installation Instructions:
- Download from the Releases Page
- Put the TTR Phase Files in the main directory (make sure to use the multify command to extract the folders, more information can be found
[here](https://toontownrewritten.fandom.com/wiki/Phase_files)
- Run Toontown Prop Viewer.exe

**NOTE FOR FULL DISCLOSURE: One of the features, namely the Playground loader, utilizes the XML parser found in the Toontown Rewritten 2014 Source Code. This is to provide the end-user with areas most authentic to the game. I hope that the potential benefits of this entire tool for the Content Pack community outweight any potential negatives.**

FAQ:
"What are the empty buttons whenever I generate props in the Prop GUI?" 
- A good chunk of them are animation files! It's 

"How do I get Content Pack support?"
- Make a folder called "multifiles"
- Put in any multifiles you have, and press the "Reload Packs" button in the Options Menu to generate them inside the Options.

"How do I build from source?"
- Go into command prompt/whichever terminal you use and call python3 setup.py bdist_apps (note that you should have Python installed for this step. I personally used Python 3.9, but it may differ for you).

"Can I use this in my own project?"
- You can! However, please credit this repo if you do. I put in a lot of effort, and I would be disappointed to see it used without attribution.
