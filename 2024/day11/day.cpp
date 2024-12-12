// https://adventofcode.com/2024/day/11

#include <algorithm>
#include <cmath>
#include <fstream>
#include <map>
#include <sstream>
#include <vector>

/**
 * @brief Update the given stones according to the defines rules at each blink.
 *
 * @param aInputFilePath the input file
 * @param aBlinks the number of blinks (loop calls)
 * @return The number of stones at the end of the loop
 */
int64_t compute( const std::string aInputFilePath, const int aBlinks )
{
   int64_t sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         // map the stone number to the number of stone with said number
         std::map<int64_t, int64_t> stones;
         std::stringstream ss( line );
         std::string numbersStr;
         while ( ss >> numbersStr )
         {
            stones[std::stoi( numbersStr )] = 1; // each stone appears only once in both the test input and the main input
         }
         for ( int blink = 0; blink < aBlinks; blink++ )
         {
            // map an stone input number to its output (how a number changes after a blink), for memoization
            std::map<int64_t, std::vector<int64_t> > output;
            std::map<int64_t, int64_t> newStones;

            std::map<int64_t, int64_t>::iterator stone_itr = stones.begin();
            for (; stone_itr != stones.end(); stone_itr++ )
            {
               // if the number is not in the output map already, populate the map
               if ( output.find( stone_itr->first ) == output.end() )
               {
                  if ( stone_itr->first == 0 ) // if the number is 0
                  {
                     output[stone_itr->first].push_back( 1 );
                  }
                  else if ( int( floor( log10( stone_itr->first ) + 1 ) ) % 2 == 0 ) // if the number has an even number of digits
                  {
                     int numHalfSize = int( floor( log10( stone_itr->first ) + 1 ) ) / 2;
                     int powerOf10   = pow( 10, numHalfSize );
                     output[stone_itr->first].push_back( stone_itr->first / powerOf10 );
                     output[stone_itr->first].push_back( stone_itr->first - ( int64_t( stone_itr->first / powerOf10 ) ) * powerOf10 );
                  }
                  else
                  {
                     output[stone_itr->first].push_back( stone_itr->first * 2024 );
                  }
               }
               // populate the new map of stones
               std::vector<int64_t> outputs = output[stone_itr->first];
               for ( int idx = 0; idx < outputs.size(); idx++ )
               {
                  if ( newStones.find( outputs[idx] ) != newStones.end() )
                  {
                     newStones[outputs[idx]] += stone_itr->second;
                  }
                  else
                  {
                     newStones[outputs[idx]] = stone_itr->second;
                  }
               }
            }
            stones = newStones;
         }
         // sum all the stones counts
         std::map<int64_t, int64_t>::iterator stone_itr = stones.begin();
         for (; stone_itr != stones.end(); stone_itr++ )
         {
            sum += stone_itr->second;
         }
      }
      inputFile.close();
   }
   return sum;
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
      printf( "Part 1 solution: %ld\n", compute( argv[1], 25 ) );
      printf( "Part 2 solution: %ld\n", compute( argv[1], 75 ) );
   }
   return 0;
}
