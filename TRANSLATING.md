Translating Hedy
================

Hedy is now (partly) available in Arabic, Bengali, Bulgarian, Czech, Dutch, English, French, Frisian, German, Greek, Hindi, Hungarian, Indonesian, Italian, Mandarin, Portugese (Brazilian and Portugese), Spanish and Swahili but we'd love to support more languages! Text that is not yet translated will be shown in English.

Help Hedy with translations (easy, no programming needed!)
----------------------------------------------------------

The easiest way to translate Hedy is by using the translation website of Weblate. You can find it [here](https://hosted.weblate.org/projects/hedy).

## Older method (little harder and incomplete)

Until recently this was the easy way, but harder to maintain for us. Translators allready using this method best finish their work en then move to the Weblate UI mentioned above.

To keep working with this method, go to https://www.hedycode.com/translate/en/new and translate our texts that are shown on the left in the boxes on the right. When you are done, you can use the three download button at the end of the page, and [send us the files](mailto:hedy@felienne.com).

![translating_page](https://user-images.githubusercontent.com/36051227/141782064-fb3645b3-d10e-404b-974b-4ed624cb7a5d.png)

You can also use this interface to extend or repair existing translations, then you have to use the iso code of the langage that you want to work with in the url instead of new, f.e. https://www.hedycode.com/translate/en/es for Spanish. That will show the existing translated texts for you to update. After you have made changes again download the files and send them to us per email.

Help Hedy with translations (in the code base, some coding experience needed)
-----------------------------------------------------------------------------

If you would like to add a new translation, there are five places where files are located that need to be translated:

1) The folder [level-defaults](https://github.com/Felienne/hedy/blob/main/coursedata/level-defaults/) has a file for each language. That file controls what the landing page for each levels looks like. It is probably easiest to copy the [English file](https://github.com/Felienne/hedy/blob/main/coursedata/level-defaults/en.yaml), rename it and translate that. Tip: example variables can be translated too, that is probably helpful for learners!
2) In the folder [texts](https://github.com/Felienne/hedy/tree/main/coursedata/texts) there is a file for each language too. That file translate UI-elements like menu headers, and, important, the error messages Hedy programmers will see. As above, copying the [English file](https://github.com/Felienne/hedy/blob/main/coursedata/texts/en.yaml) and translate that.
3) In the folder [keywords](https://github.com/Felienne/hedy/tree/main/coursedata/keywords) there is a file for each language too. That file makes it possible for kids to write code using a translation for keywords like 'print' or 'echo'.
4) The [folder](https://github.com/Felienne/hedy/tree/main/coursedata/adventures) that control the assignments kids see in the user interface for each of the levels. While not mandatory, the assignments in this section are of help for kids to better explore each level. If you do not translate them, the English version will be shown.
5) *optional* The folder [main](https://github.com/Felienne/hedy/tree/main/main) controls the web pages around Hedy. [start](https://github.com/Felienne/hedy/blob/main/main/start-en.md) holds the content of the start page, and there are page with press, contact info too. These do not necessariyl have to be translated, if you don't people will then see the English version, but kids can still program in their own native language.

Translated all of that?

Two more small things to do!

1) Add your language to the [menu](https://github.com/Felienne/hedy/blob/main/main/menu.json).
2) Now go to [app.py](https://github.com/Felienne/hedy/blob/main/app.py) and add your language to this list:

```
ALL_LANGUAGES = {
    'en': 'English',
    'nl': 'Nederlands',
    'es': 'Español',
    'fr': 'Français',
    'pt_br': 'Português',
    'de': 'Deutsch',
    'it': 'Italiano',
    .....
}
```
