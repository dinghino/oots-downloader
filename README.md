oots-downloader
===============

Original project is from @duploduplo. I'm working on a PyQt4 implementation of the project, while fixing some minor bugs.

Original README
----------------

A simple "The Order Of The Stick" comic downloader written in python.

I'm a big fan of this webcomic, but I find very annoying to read it from the original website. This script helps me to download the latest comics and read them comfortably in my Mac.

You can find the original comics by Rich Burlew here: http://www.giantitp.com/Comics.html

Wikipedia page of the comic: http://en.wikipedia.org/wiki/Order_of_the_Stick

Wikipedia page of the author: http://en.wikipedia.org/wiki/Rich_Burlew


Installation & Usage
====================

You'll need PyQt4 to run this program with it's interface, or you can run `/downloader/downloader.py` to run it in the interpreter.

With the UI
-----------

When first running the application click on the download button and enjoy. It will take a while for now to get all the comics but you can read them as they come as long you leave the dialog open.

You may get some ERROR from the logger. if the log is about `Error in creating the image` but everything shows, don't worry and go on.

To navigate the images you can use the directional keys or the buttons:

* `up` for the first comic
* `down` for the last
* `left` for the previous
* `right` for the next


TODO
====

* [ ] Fix image position
* [ ] Move controls into a proper toolbar with icons
* [ ] Add notification for when there are no new comics to download
* [ ] Add multithreading support to speed up the download.
* [ ] Make the image zoomable and pannable
