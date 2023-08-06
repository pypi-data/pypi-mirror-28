Khaki
=====

Khaki is a Pomodoro timer in Python using the standard `curses` module and
Pyglet.

How to use
----------

Run `khaki`. Once it is running, use `p` to toggle the timer. After the
long timer runs out, it is replaced by the rest timer, which needs to be
toggled as well.

Pressing `+` will reset the current timer and add one second to the max
time. Pressing `-` works the same way, but subtracts a second. The
changes are not yet persistent.

Pressing `c` will clear the timer. It will keep running if it was running,
and will continue paused if it was paused.

You can exit with `q`.

Why "Khaki"
-----------

It has a nice sound to it, and a Khaki is a great doppelganger for a tomato.
