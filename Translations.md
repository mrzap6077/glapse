# Introduction #

Have you enjoyed gLapse? Then, it would be fantastic if you could contribute translating it into another language. The process doesn't require programming skills and it's pretty easy, you only have to follow these simple instructions.


# Getting started #

gLapse uses [gettext](http://en.wikipedia.org/wiki/GNU_gettext) as a library to provide its multilanguage feature since it's considered nearly a standard. In a gettext project you'll find three different files.

  * **.pot file**: master file containing all key strings in the original language, usually English. All translations must derive from this file.
  * **.po file**: plain text file with string pairs: english text (key) and second language text (translated text). It's intended for human reading and editing only. They follow the [ISO\_639-1](http://en.wikipedia.org/wiki/ISO_639-1) naming pattern: en.po (English), es.po (Spanish), fr.po (French).
  * **.mo file**: binary version of a .po file.


# Creating a new translation #

If you want to contribute creating a new translation of gLapse you should check out the [glapse.pot](http://code.google.com/p/glapse/source/browse/#svn%2Ftrunk%2Fpo) file which contains every string in the application.

To create a new .po file you should type in a terminal:

`msginit -l es -o es.po -i glapse.pot`

That would be to create a new Spanish translation. If you wanted a German translation, you should have typed:

`msginit -l de -o de.po -i glapse.pot`

Check out [ISO\_639-1](http://en.wikipedia.org/wiki/ISO_639-1) Wikipedia page to get a more complete list of language codes.


# Translating strings #

The first thing you should do is pay attention to the first section of the resulting file:

```
msgid ""
msgstr ""
"Project-Id-Version: glapse 0.1\n"
"Report-Msgid-Bugs-To: david.saltares@gmail.com\n"
"POT-Creation-Date: 2011-05-15 12:42+0200\n"
"PO-Revision-Date: 2011-05-15 11:52+0200\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: Spanish\n"
"Language: es\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
```

Of course you want to change the Last-Translator parameter with your name and e-mail address. You deserve the credit! Now you are ready to start translating each string pair.

If you find this:

```
#: glapseGUI/glapseGUI.py:250
msgid "Dependencies error"
msgstr ""
```

You should change it for (Spanish):

```
#: glapseGUI/glapseGUI.py:250
msgid "Dependencies error"
msgstr "Error de dependencias"
```

However it is possible to find strings with symbols like this "%s". That's because the string could contain numbers and other variables in between. It's simple, you only have to translate it taking the order into account.

```
#: glapseGUI/glapseGUI.py:251
#, python-format
msgid "<b>%s was not found</b>"
msgstr ""
```

Would be translated like:

```
#: glapseGUI/glapseGUI.py:251
#, python-format
msgid "<b>%s was not found</b>"
msgstr "<b>no se encontró %s</b>"
```


# Updating an existing translation #

If tomorrow a new gLapse version launches and it contains new strings you may want to update your translation. Beware! Using the `msginit` command over the existing .po file would erase all your work. In this case you might want to use:

`msgmerge -s -U es.po glapse.po`


# Submit your new translation! #

Don't forget to submit your new translations! Open a new issue in the [issues section](http://code.google.com/p/glapse/issues/) and attach your new .po file.

**Thank you very much**