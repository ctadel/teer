import os

class Parameter:

    # CORE PARAMETERS
    #To support Python 3.8 and earlier versions
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    APPLICATION_TITLE = f'{os.uname()[1]} | dotfiles'
    CONFIG_FILE_PATH = 'config.json'
    DEFAULT_REMOTE_DIRECTORY = '~'
    DOTFILES_REPOSITORY = os.environ.get('DOTFILES_REPOSITORY', '')
    LAUNCH_FILE_REPOSITORY = '~/.local/share/applications'

    # DISPLAY PARAMETERS
    SYNC_INTERVAL_DURATION = 0.05
    REFRESH_FRAME_INTERVAL = 0.5
    DISPLAY_LINES_ON_CONSOLE = 10

    # LAUNCH PARAMETERS
    FORCE_OVERWRITE = False
    INTERACTIVE_SYNC = False
    LOGGING_ENABLED = False
    LOG_FILE_PATH = '/tmp/teer.log'


    @staticmethod
    def defaults():
        return {
            'CORE': {
                'APPLICATION_TITLE': (Parameter.APPLICATION_TITLE, str),
                'CONFIG_FILE_PATH': (Parameter.CONFIG_FILE_PATH, str),
                'DEFAULT_REMOTE_DIRECTORY': (Parameter.DEFAULT_REMOTE_DIRECTORY, str),
                'DOTFILES_REPOSITORY': (Parameter.DOTFILES_REPOSITORY, str),
                'LAUNCH_FILE_REPOSITORY': (Parameter.LAUNCH_FILE_REPOSITORY, str),
            },
            'DISPLAY': {
                'SYNC_INTERVAL_DURATION': (Parameter.SYNC_INTERVAL_DURATION, float),
                'REFRESH_FRAME_INTERVAL': (Parameter.REFRESH_FRAME_INTERVAL, float),
                'DISPLAY_LINES_ON_CONSOLE': (Parameter.DISPLAY_LINES_ON_CONSOLE, int),
            },
            'LAUNCH': {
                'FORCE_OVERWRITE': (Parameter.FORCE_OVERWRITE, bool),
                'INTERACTIVE_SYNC': (Parameter.INTERACTIVE_SYNC, bool),
                'LOGGING_ENABLED': (Parameter.LOGGING_ENABLED, bool),
                'LOG_FILE_PATH': (Parameter.LOG_FILE_PATH, str),
            }
        }

    @staticmethod
    def update_params(parser):
        default_schema = Parameter.defaults()
        data_type_mapper = {
                int         : parser.getint,
                float       : parser.getfloat,
                bool        : parser.getboolean,
                str         : parser.get
            }
        for section in default_schema.keys():
            for key, (value, value_type) in default_schema[section].items():
                setattr(Parameter, key, data_type_mapper.get(value_type, parser.get)\
                        (section, key, fallback=value)
                    )

        if not os.path.exists(Parameter.DOTFILES_REPOSITORY) \
                or not os.path.isdir(Parameter.DOTFILES_REPOSITORY):
            if parser.get('CORE', 'DOTFILES_REPOSITORY', fallback=None):
                print(f"\nInvalid DOTFILES_REPOSITORY: {Parameter.DOTFILES_REPOSITORY}")
                print("Update this key in parameters.cfg file")
            elif os.environ.get('DOTFILES_REPOSITORY'):
                print("\nInvalid file path exported to DOTFILES_REPOSITORY")
                print("Please check again and run again")
            else:
                print("\nYour Dotfiles repository is not defined yet")
                print("\nYou can define this inside the parameters file: parameters.cfg")
                print("\nOr you can export your dotfiles repo path to $DOTFILES_REPOSITORY")
                print("export DOTFILES_REPOSITORY=/path/to/dotfiles/repo/")
            exit(1)


    @staticmethod
    def get_application_header():
        user_title = f"{Parameter.APPLICATION_TITLE[:80]:>80}"
        return \
f'''
                                                                                                 ~
            ~((-                                                                                [[]                ▒▒▒▒▒▒▒▒▒▒▒▒
           <[[]-                                                                               -[[]              ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
          -[[[]-                                                                               -[[]            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        -^>[[[[>^^^^^=          -*<](<*-               -*<](<*              -^<    =<<^-       -[[]           ▒▒▒▒▒▒▒▒     ▒▒▒▒▒▒▒▒
       *]]][[[[]]]]]]^       -<[(^==>[[[[^          -([(^==<[[[[>     -<][[[[[[  ^[[[[[[>      -[[]           ▒▒▒▒▒▒▒ ▒▒▒▒▒  ▒▒▒▒▒▒
          -[[[]-            <[(-      >[[[(        ([]       ([[[(-    --*][[[(~[]<>][[[^      -[[]           ▒▒▒▒▒▒▒ ▒▒▒▒▒▒ ▒▒▒▒▒▒
          -[[[]-          -[[(        -([[[^     ~[[(         [[[[>       *[[[[]-     ~-       -[[]           ▒▒▒▒▒▒▒  ▒▒▒▒ ▒▒▒▒▒▒▒
          -[[[]-          [[[<*******^>[[[[<    ~][[>********>[[[[>       *[[[]                -[[]           ▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒▒
          -[[[]-         <[[[(<<<<>>^^^***=     >[[[<<<<<>>^^^***=        *[[[<                -[[]            ▒▒▒▒▒▒ ▒▒▒▒▒▒ ▒▒▒▒▒
          -[[[]-         [[[[-                 -([[[                      *[[[<                -[[]              ▒▒▒▒ ▒▒▒▒▒▒ ▒▒▒
          -[[[]-         [[[[*                 -([[[~                     *[[[<                -[[]                ▒▒ ▒▒▒▒▒▒ ▒
          -[[[]-         >[[[]~                 >[[[[                     *[[[<                -[[]                   ▒▒▒▒▒▒
          -[[[]-          ][[[[*           =    -([[[[=           -       *[[[<                -[[]                   ▒▒▒▒▒▒
          -[[[[<     -     <[[[[[<*-   -*([*      <[[[[[<*-   -*<[^       *[[[<                -[[]                  ▒▒▒▒▒▒▒
           *[[[[[[][]=      ~<[[[[[[[[[[[>-        ~([[[[[[[[[[[<-     -~^][[[[>=~-            -[[]               ▒▒▒▒▒▒▒▒▒▒▒▒▒
             =>]](*-           -*<]]](^-              -*<]]](^-       ->>^******^^>*           -[[]                 ▒▒▒▒▒▒▒▒▒
                                                                                               -[[]                   ▒▒▒▒▒▒
         {user_title}      -[[]                     ▒▒
                                                                                               -[[]
                                                                                                 ~
'''
