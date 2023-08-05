from typing import Optional, cast

import stringcoercion
from stringcoercion import Coercer, CoercionInfo

from intermake.visualisables.visualisable import IVisualisable
from intermake.visualisables.visualisable_operations import PathToVisualisable
from intermake.plugins import console_explorer


class VisualisableCoercion( Coercer ):
    def coerce( self, info: CoercionInfo ) -> Optional[object]:
        r = console_explorer.follow_path( path = info.source, restrict = info.annotation.value )
        
        if r is None:
            return None
        
        return r.get_last()
    
    
    def can_handle( self, info: CoercionInfo ):
        return info.annotation.is_directly_below( IVisualisable )


class VisualisablePathCoercion( Coercer ):
    def coerce( self, info: CoercionInfo ) -> Optional[object]:
        return console_explorer.follow_path( path = info.source, restrict = info.annotation.value.type_restriction() )
    
    
    def can_handle( self, info: CoercionInfo ):
        return info.annotation.is_directly_below( PathToVisualisable )


class MAnnotationCoercer( Coercer ):
    def coerce( self, args: CoercionInfo ):
        return args.collection.coerce( args.annotation.mannotation_arg, args.source )  # the result is the type, not the annotation!
    
    
    def can_handle( self, info: CoercionInfo ):
        return info.annotation.is_mannotation


# Register them
stringcoercion.get_default_coercer().register( VisualisableCoercion(), VisualisablePathCoercion(), MAnnotationCoercer() )
