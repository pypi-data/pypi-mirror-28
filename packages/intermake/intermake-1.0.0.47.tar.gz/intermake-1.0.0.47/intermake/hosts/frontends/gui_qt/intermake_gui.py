from os import path

from mhelper import file_helper


__default_style_sheet = None


def default_style_sheet():
    """
    Gets the contents of the default style sheet.
    """
    global __default_style_sheet
    
    if __default_style_sheet is None:
        __default_style_sheet = file_helper.read_all_text( path.join( file_helper.get_directory( __file__ ), "main.css" ) )
        __default_style_sheet = __process_css( __default_style_sheet )
    
    return __default_style_sheet


def __process_css( source: str ) -> str:
    stage = 0
    lut = []
    r = []
    
    for line in source.split( "\n" ):
        for k, v in lut:
            line = line.replace( k, v )
        
        if stage == 0 and ":root" in line:
            stage = 1
        elif stage == 1 and "{" in line:
            stage = 2
        elif stage == 2 and "}" in line:
            stage = 0
        elif stage == 2 and ":" in line:
            e = line.split( ":", 1 )
            lut.append( (e[0].strip(), e[1].strip( " \t;" )) )
        elif "__" in line:
            raise ValueError( "CSS not recognised at line «{}»".format( line ) )
        else:
            r.append( line )
    
    return "\n".join( r )
