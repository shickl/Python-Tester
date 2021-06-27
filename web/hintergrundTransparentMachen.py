from PIL import Image
import numpy as np
import argparse

def hintergrundTransparentMachen( bildname ):
      ''' über Schwellenwert und Distanz lässt sich das Spektrum 
      der erkannten Weißtöne anpassen '''
      schwellenwert = 220 # Mindestgröße der Farbwerte
      distanz = 5 # max. Abstand zwischen Farbwerten
      bild = Image.open( bildname ).convert( 'RGBA' )

      bildArray = np.array( np.asarray( bild ) )
      r, g, b, a = np.rollaxis( bildArray, axis = -1 )    
      maske = ( ( r > schwellenwert )
            & ( g > schwellenwert )
            & ( b > schwellenwert )
            & ( np.abs( r - g ) < distanz )
            & ( np.abs( r - b ) < distanz )
            & ( np.abs( g - b ) < distanz )
            )

      bildArray[maske, 3] = 0
      bild = Image.fromarray( bildArray, mode = 'RGBA' )
      bildnameOhneEndung = bildname.split( "." )[0]
      bild.save( bildnameOhneEndung + '-transparent.png' )

def parserErstellen():
      ''' Nutzer kann den Dateinamen des Bilds in der Kommandozeile an den Skript-aufruf 
      anhängen
      '''
      parser = argparse.ArgumentParser( description = 'Dateinamen des Bilds angeben' )

      parser.add_argument( 'bildname', action = 'store', type = str,
                  help='Name des Bilds, dessen (weißer) Hintergrund transparent werden soll' )
      return parser

def main():
      parser = parserErstellen()
      nutzerOptionen = parser.parse_args()

      if nutzerOptionen.bildname:
            hintergrundTransparentMachen( nutzerOptionen.bildname )
      else:
            print( "Bitte hänge an den Skriptaufruf den Bildnamen mit Dateiendung an." )

if __name__ == "__main__":
      main()