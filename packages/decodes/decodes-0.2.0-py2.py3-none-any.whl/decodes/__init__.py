print("http://decod.es")

__version__ = "0.2.0"
__title__ = "decodes"
__description__ = "a geometry library for 3d designers"
__uri__ = "http://decod.es/"
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = "Kyle Steinfeld"
__email__ = "ksteinfe@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2015 Kyle Steinfeld"


"""A Platform-Agnostic Computational Geometry Environment 

.. moduleauthor:: Kyle Steinfeld <ksteinfe@gmail.com>

"""



class Outies:
    # list here all the outies we currently support
    Rhino, Grasshopper, SVG , ACAD, Dynamo,ThreeJS,JSON = list(range(7))


# keep this up to date with what outies we support
def make_out(outtype, name="untitled", path=False, **kargs):
    """This function constructs a new outie of the given type.
    
        :param outtype: The type of outie to create
        :type outtype: int (enumerated from Outies class)
        :param name: The name of the outie to create.    This name is used in different ways, depending on the context to which we will be drawing geometry
        :type name: string or "untitled"
        :param path: If an outie creates a file, the filepath to save to.
        :type path: string
        :rtype: child of decodes.outies.outie
    """
    import io.outie

    if outtype == Outies.Rhino:
        import io.rhino_out
        return io.rhino_out.RhinoOut(name)
    elif outtype == Outies.ACAD:
        import io.autocad_out
        return io.autocad_out.AutocadOut(name)
    elif outtype == Outies.Grasshopper:
        import io.gh_out
        return io.gh_out.GrasshopperOut(name)
    elif outtype == Outies.SVG:
        import io.svg_out

        c_dim=False
        flip=False
        save_file=True
        verbose = False
        if "canvas_dimensions" in kargs : c_dim = kargs["canvas_dimensions"]
        if "save_file" in kargs : save_file = kargs["save_file"]
        if "flip_y" in kargs : 
            if c_dim is False : raise Exception("If you want to flip the y-axis of this SVG, you have to tell me the canvas_dimensions.  Please pass an Interval.")
            flip = kargs["flip_y"]
        if "verbose" in kargs : verbose = kargs["verbose"]
        
        if path : return io.svg_out.SVGOut(name, path, canvas_dimensions=c_dim, flip_y=flip,save_file=save_file,verbose=verbose)
        else : return io.svg_out.SVGOut(name, canvas_dimensions=c_dim, flip_y=flip,save_file=save_file,verbose=verbose)
    elif outtype == Outies.ThreeJS:
        import io.threejs_out
        save_file=True
        if "save_file" in kargs : save_file = kargs["save_file"]
        if path : return io.threejs_out.ThreeJSOut(name, path, save_file=save_file)
        else : return io.threejs_out.ThreeJSOut(name, save_file=save_file)
    elif outtype == Outies.JSON:
        import io.json_out
        save_file=True
        if "save_file" in kargs : save_file = kargs["save_file"]
        if path : return io.json_out.JsonOut(name, path, save_file=save_file)
        else : return io.json_out.JsonOut(name, save_file=save_file)
        
    elif outtype == Outies.Dynamo:
        import io.dynamo_out
        return io.dynamo_out.DynamoOut()
    else :
        print("!!! hey, i don't have an outie of type foo !!!")
        return False

# keep this up to date with what outies we support
def make_in(intype):
    if intype == innies.Rhino:
        return innies.RhinoIn()
    if intype == innies.Dynamo:
        return innies.DynamoIn()
    if intype == innies.Foo:
        if VERBOSE : print("!!! hey, i don't have an innie of type foo !!!")
        return False
