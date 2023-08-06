# disport
Wrapper for xrandr to easily handle multi monitor setup

## Description

Provides easy access to the most important xrandr functions (at least to the ones I use most often), namely:
* Send the same output to all connected displays
* Restrict the output to the main display
* Extend the viewport across several displays

If you need any more elaborate xrandr functions, you better just use xrandr.

## Usage

List connected displays and their resolutions:

    python main.py list

Clone output among all connected displays:

    python main.py clone

Restrict output to main display:

    python main.py solo

Extend output to the display left of the main display:

    python main.py extend left

Extend it to the right:

    python main.py extend right

## To-do

* Let the user specify the display for the restrict mode
* Let the user freely specify the arrangement of the displays for the extend mode
* Provide fallback if two displays have no common resolution
