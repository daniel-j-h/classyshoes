# Basic headers we are supposed to send at least
def mkBaseHeaders(language, compression, client):
    return {'Accept-Language': language
          , 'Accept-Encoding': compression
          , 'x-client-name': client}

