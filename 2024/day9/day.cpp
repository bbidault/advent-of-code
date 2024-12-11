// https://adventofcode.com/2024/day/9

#include <algorithm>
#include <fstream>
#include <vector>

/**
 * @brief
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return
 */
int64_t compute( const std::string aInputFilePath, const bool aPart1 )
{
   int64_t checksum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         bool memoryBlock        = true;
         int  beginId            = 0;
         int  endId              = line.length() / 2;
         int  resultReaderPos    = 0;
         int  forwardReaderPos   = 0;
         int  backwardReaderPos  = line.length() - 1;
         int  memoryBlockCounter = line[backwardReaderPos] - '0';

         while ( forwardReaderPos < backwardReaderPos )
         {
            if ( memoryBlock )
            {
               for ( int i = 0; i < line[forwardReaderPos] - '0'; i++ )
               {
                  checksum += resultReaderPos * beginId;
                  resultReaderPos++;
               }
               memoryBlock = false;
               forwardReaderPos++;
               beginId++;
            }
            else
            {
               for ( int i = 0; i < line[forwardReaderPos] - '0'; i++ )
               {
                  if ( memoryBlockCounter <= 0 )
                  {
                     backwardReaderPos -= 2;
                     memoryBlockCounter = line[backwardReaderPos] - '0';
                     endId--;
                  }
                  checksum += resultReaderPos * endId;
                  memoryBlockCounter--;
                  resultReaderPos++;
               }
               memoryBlock = true;
               forwardReaderPos++;
            }
         }
         if ( memoryBlockCounter > 0 )
         {
            checksum += resultReaderPos * beginId;
         }
      }
      inputFile.close();
   }
   return checksum;
}

/**
 * @brief Main function
 *
 * @param argc number of argument(s)
 * @param argv the argument(s)
 * @return int exit code
 */
int main( int argc, char *argv[] )
{
   if ( argc == 2 )
   {
      printf( "Part 1 solution: %ld\n", compute( argv[1], true ) );
      // printf( "Part 2 solution: %d\n", compute( argv[1], false ) );
   }
   return 0;
}
