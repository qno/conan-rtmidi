#include <RtMidi.h>

int main() {

   try
   {
      RtMidiIn midiin;
   } catch (const RtMidiError& error)
   {
      error.printMessage();
   }

   return 0;
}
