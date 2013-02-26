git-plot-tools
=========

Here's just a simple tool for plotting git commits against time.

To use:

	$ git log --pretty="%at, %s" [start hash]..[end hash] > output
	$ ./topic-time-plot.py output

This will generate a file called: commit-chart.png
Which will show the commits broken up by patch topic by date.

If you run into problems, its likely because you'll need to have
matplotlib 1.0 or greater installed. But if you hit anything else
do let me know!

You can also tweak the chart_opts dictionary if you want slightly
different output.

Fairly straight forward. I'm pretty terrible with python, so if you
have suggestions for improvements, let me know!

	John Stultz <john.stultz@linaro.org>

