from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def locals_to_kmz_response(locs):
    
    import zipfile
    import cStringIO
    
    kml = get_template('base.kml').render(
        Context(locs)    
    )
    
    kml = kml.encode('utf-8')
    
    ###############################################
    
    sio = cStringIO.StringIO()
    
    z = zipfile.ZipFile(sio, 'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("doc.kml", kml)
    
    from django.conf import settings
    big_icon = "%s/icons/big/base_pad.png" % settings.MEDIA_ROOT
    small_icon = "%s/icons/small/base_pad.png" % settings.MEDIA_ROOT
    
    z.write(big_icon, "files/big/base_pad.png")
    z.write(small_icon, "files/small/base_pad.png")
        
    z.close()

    return HttpResponse(sio.getvalue(),
                        mimetype="application/vnd.google-earth.kmz")
