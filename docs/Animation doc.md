animation Doc

the animation function used in this project is called leanier interpolation equation or "Lerp" in short
it is the most common one.

def lerp(a, b, t, easing):
return a + (b - a) \* easing(t)

the way it works is that the function receives A - a starting point, B- a destination point, T - a number betnween 0 and 1 which represents which % are we in the process of the animation

as time passes T increases until it reaches 1. by that point the animation has ended.

there are various variations for the lerp function that can be found in easing_functions.py

the returned value of the function is then passed into the corresponding pygame feature such as rotate, rect movement, and whatever we need it to be.
