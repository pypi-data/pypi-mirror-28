from typing import Union, List

import sys

from mhelper import string_helper, ansi


class DefaultLogger:
    def __init__( self ):
        self.print = self.__print_stderr
    
    
    def __print_stderr( self, text ):
        print( text, file = sys.stderr )


DEFAULT_LOGGER = DefaultLogger()


class Logger:
    """
    Logging simplified.
    """
    
    
    def __init__( self, name: Union[str, bool], enabled: bool = None ):
        """
        CONSTRUCTOR
        :param name:        Name of the logger, or a value for :property:`target` 
        :param enabled:     A value for :property:`target` (if a name was specified) 
        """
        LOGGERS.append( self )
        if isinstance( name, bool ) and enabled is None:
            enabled = name
            name = "untitled"
        
        if name:
            self.__prefix = name + ": "
        else:
            self.__prefix = ""
        
        self.__target = None
        self.target = enabled
    
    
    @property
    def target( self ):
        """
        Gets or sets the target printer, which should accept one unnamed `str` parameter.
        The following are also accepted:
            `None` or `False`:  Disables printing
            `True`:             Prints to std-err.
        :return: 
        """
        return self.__target
    
    
    @target.setter
    def target( self, enabled: bool = None ):
        if enabled is True:
            self.__target = DEFAULT_LOGGER.print
        elif enabled is False or enabled is None:
            self.__target = None
        else:
            self.__target = enabled
    
    
    def __call__( self, *args, **kwargs ):
        if self.__target is None:
            return self
        
        if len( args ) == 1:
            self.print( args[0] )
        elif len( args ) > 1:
            vals = list( args[1:] )
            for i in range( len( vals ) ):
                v = vals[i]
                
                if type( v ) in (set, list, tuple):
                    vals[i] = string_helper.format_array( v )
                
                vals[i] = "«" + str( vals[i] ) + "»"
            
            self.print( args[0].format( *vals ) )
        
        return self
    
    
    def print( self, message ):
        if "\n" in message:
            for i, split in enumerate( message.split( "\n" ) ):
                self.print( ("\b\b: " if i != 0 else "") + split )
            
            return
        
        self.__target( ansi.DIM + self.__prefix + ansi.RESET + string_helper.highlight_quotes( message, "«", "»", ansi.FORE_YELLOW, ansi.RESET ) )
    
    
    def indent( self ):
        self.__prefix += "    "
        
        if len( self.__prefix ) > 100:
            from mhelper.exception_helper import ImplementationError
            raise ImplementationError( "Log indent too far." )
    
    
    def unindent( self ):
        self.__prefix = self.__prefix[:len( self.__prefix ) - 4]
    
    
    def __enter__( self ):
        self.indent()
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.unindent()


LOGGERS: List[Logger] = []
"""List of all loggers"""
