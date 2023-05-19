# Updates made to fpp since Jasha forked from https://github.com/facebook/PathPicker

Most recent updates first.

- Return a non-zero exit code (i.e. 2) if the fpp is interrupted (e.g. with Ctrl+C) during
    path selection (i.e. when pathpicker.choose is running)
- Fpp now returns a non-zero exit code (i.e. 1) if no lines are matched.
