// https://adventofcode.com/2024/day/11

#include <cmath>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <vector>

/**
 * @brief
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   std::vector<int64_t> numbers;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::stringstream ss( line );
         std::string numbersStr;
         while ( ss >> numbersStr )
         {
            numbers.push_back( std::stoi( numbersStr ) );
         }
         for ( int i = 0; i < 25; i++ )
         {
            std::vector<int64_t> newNumbers;
            for ( int j = 0; j < numbers.size(); j++ )
            {
               if ( numbers[j] == 0 )
               {
                  newNumbers.push_back( 1 );
               }
               else if ( int( floor( log10( numbers[j] ) + 1 ) ) % 2 == 0 )
               {
                  int halfSize = int( floor( log10( numbers[j] ) + 1 ) ) / 2;
                  newNumbers.push_back( numbers[j] / pow( 10, halfSize ) );
                  newNumbers.push_back( numbers[j] - ( int64_t( numbers[j] / pow( 10, halfSize ) ) ) * pow( 10, halfSize ) );
               }
               else
               {
                  newNumbers.push_back( numbers[j] * 2024 );
               }
            }
            numbers = newNumbers;
         }
      }
      inputFile.close();
   }
   return numbers.size();
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
      printf( "Part 1 solution: %d\n", compute( argv[1], true ) );
      printf( "Part 2 solution: %d\n", compute( argv[1], false ) );
   }
   return 0;
}
