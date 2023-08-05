=======
History
=======

0.1.42 (2018-01-14)
-------------------

Fixed
~~~~~
* Increase number of MQTT reconnect attempts.


0.1.41 (2017-10-22)
-------------------

Fixed
~~~~~
* Make sure send 0 minute timer notification after timer finishes.


0.1.40 (2017-10-22)
-------------------

Fixed
~~~~~
* Make sure we process timer status messages.


0.1.39 (2017-10-22)
-------------------

Changed
~~~~~~~
* Refactor entire execution code. Because my imaginary friend said so.


0.1.38 (2017-10-21)
-------------------

Changed
~~~~~~~
* Simplify timer messages.


0.1.37 (2017-10-17)
-------------------

Fixed
~~~~~
* Fixed bug generating action for timer update.


0.1.36 (2017-10-17)
-------------------

Fixed
~~~~~
* Fixed bugs associated with timer.

Changed
~~~~~~~
* Timer uses current action for first event.
* Ability to replace/cancel timers.
* Add timer cancel notification.


0.1.35 (2017-10-01)
-------------------

Changed
~~~~~~~
* Add timer count down from previous event.


0.1.34 (2017-09-30)
-------------------

Changed
~~~~~~~
* Minor tweaks to timer algorithm.


0.1.33 (2017-09-30)
-------------------

Changed
~~~~~~~
* Don't send MQTT timer or template messages, these are handled locally.


0.1.32 (2017-09-30)
-------------------

Changed
~~~~~~~
* Don't send MQTT message on timer=0 minutes.
* Send more data on MQTT messages.


0.1.31 (2017-09-29)
-------------------

Added
~~~~~
* Added server side timer.
* Add ability to schedule template at arbitrary time.

Changed
~~~~~~~
* Update to latest aiolifxc.


0.1.30 (2017-09-22)
-------------------

Added
~~~~~
* Abilty to turn lights on and set color.
* Pause music before annoucements and resume if required.
* Ability to play sound files.


0.1.29 (2017-09-13)
-------------------

Added
~~~~~
* Add ability to run without scheduler and process incoming actions.


0.1.28 (2017-09-09)
-------------------

Changed
~~~~~~~
* Specify the plugin for each input and output.
* Publish complete action on MQTT output.


0.1.27 (2017-09-08)
-------------------

Fixed
~~~~~
* Ensure disabled lights actions are disabled.


0.1.26 (2017-09-07)
-------------------

Changed
~~~~~~~
* Refactor locations.
* Locations now intersect or subtract from parent locations.


0.1.25 (2017-09-06)
-------------------

Added
~~~~~
* Add ability to turn off lights.

Changed
~~~~~~~
* Renamed location setting to locations.


0.1.24 (2017-09-02)
-------------------

Changed
~~~~~~~
* Combine log files into one.
* MQTT message to replace schedule.


0.1.23 (2017-08-26)
-------------------

Fixed
~~~~~
* More bugs fixed.


0.1.22 (2017-08-26)
-------------------

Fixed
~~~~~
* Various bugs fixed.


0.1.21 (2017-08-26)
-------------------
The "I Accidentally incremented the version two times release".

Fixed
~~~~~
* Add missing files.


0.1.19 (2017-08-26)
-------------------

Added
~~~~~
* MQTT support for execute request/response.
* MQTT support for audio events.

Changed
~~~~~~~
* Execute one task at a time.
* Refactor input/output code.


0.1.18 (2017-08-20)
-------------------

Added
~~~~~
* Support multiple audio destinations per daemon.


0.1.17 (2017-08-19)
-------------------

Added
~~~~~
* Ability to specify list of tasks.

Changed
~~~~~~~
* Move configuration to config directory and remove "-sample" substring.


0.1.16 (2017-08-13)
-------------------

Added
~~~~~
* Add new REST API to carry out actions.
* New executor config file.

Changed
~~~~~~~
* Lights flash at same time as audio.

Fixed
~~~~~
* Make http error handling more robost.


0.1.15 (2017-07-22)
-------------------

Fixed
~~~~~
* Add aiohttp to setup.py depends.
* Fix bad disabled logic.


0.1.14 (2017-07-22)
-------------------

Added
~~~~~
* New location system.

Fixed
~~~~~
* Mypy errors.


0.1.13 (2017-07-10)
-------------------

Changed
~~~~~~~
* Update aiolifxc from 0.5.3 to 0.5.4.
* Update pytest from 3.1.2 to 3.1.3.

Fixed
~~~~~
* Flash lights red, not green.
* Update sample schedule file.
* Clear playlist before adding new songs.
* Ignore mypy cache directory.


0.1.12 (2017-07-04)
-------------------

Added
~~~~~
* Ability for audio to run list of commands.
* Ability to schedule music.


0.1.11 (2017-07-04)
------------------

Changed
~~~~~~~
* Flash light flashes 2 times, not 10.

Fixed
~~~~~
* Fix get_days_for_date replaces functionality.


0.1.10 (2017-07-02)
------------------

Fixed
~~~~~
* Actually change requirements.txt to require aiolifxc version 0.5.2.
* Update setup.py to reflect this also.


0.1.9 (2017-07-02)
------------------

Added
~~~~~
* Support aiolifxc version 0.5.2.

Fixed
~~~~~
* LIFX errors.


0.1.8 (2017-06-27)
------------------

Added
~~~~~
* Declare Python 3.6 support.
* Use aiolifxc library.
* Added new config files.
* Add music support.
* Add ability to customize command line for say program.

0.1.7 (2017-06-26)
------------------

Added
~~~~~
* Enhancements to schedule processing.
* Ability to disable LIFX support.

0.1.6 (2017-06-25)
------------------

Added
~~~~~
* disabled option for schedules, to disable without deleting.

Fixes
~~~~~
* Don't replace other schedules unless this one is active.

0.1.5 (2017-06-25)
------------------

Added
~~~~~
* Support acting on list of lights or groups.
* Sending message to all lights asynchronously.
* One schedule can override another schedule.

0.1.4 (2017-06-24)
------------------

Fixes
~~~~~
* Add missing required depends.
* Handle Device Offline errors correctly.

0.1.3 (2017-06-24)
------------------

Added
~~~~~
* Schedule config file support.
* Requires my fork of aiolifx.

0.1.2 (2017-06-19)
------------------

Fixed
~~~~~
* PyPI meta information.
* day_of_week value incorrect.

0.1.1 (2017-06-18)
------------------

* No changes.

0.1.0 (2017-06-18)
------------------

* First release on PyPI.
