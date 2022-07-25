from setuptools import setup

setup(
    name='Toontown Prop Viewer',
    options={
        'build_apps': {
            # Build asteroids.exe as a GUI application
            'console_apps': {
                'Toontown Prop Viewer': 'PropViewerStart.py',
            },

            # Set up output logging, important for GUI apps!
             'log_filename': 'output.log',
             'log_append': False,
             'log_filename_strftime': True,

             # Including the config files
             'include_patterns': [
                'config/*'
             ],

            'use_optimized_wheels': True,
            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
