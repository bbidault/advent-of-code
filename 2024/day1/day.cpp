// https://adventofcode.com/2024/day/1

#include <algorithm>
#include <fstream>
#include <sstream>
#include <vector>

/**
 * @brief For part 1, sum the absolute values of the difference of numbers of the two given list sorted.
 *        For part 2, sum the counts of number from the first column in the second column multiplied by
 *        the number from the first column
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the sum of the absolute values of the difference of numbers of the two given list sorted
 *         or the sum of the counts of number from the first column in the second column multiplied by
 *         the number from the first column
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<int> rightColumn;
      std::vector<int> leftColumn;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::string numbersStr;
         std::vector<int>  numbers;
         std::stringstream ss( line );
         while ( ss >> numbersStr )
         {
            numbers.push_back( std::stoi( numbersStr ) );
         }
         rightColumn.push_back( numbers[0] );
         leftColumn.push_back( numbers[1] );
      }
      std::sort( rightColumn.begin(), rightColumn.end() );
      std::sort( leftColumn.begin(), leftColumn.end() );
      for ( int idx = 0; idx < rightColumn.size(); idx++ ) // assume the vectors are of the same length
      {
         if ( aPart1 )
         {
            sum += std::abs( rightColumn[idx] - leftColumn[idx] );
         }
         else
         {
            sum += std::count( leftColumn.begin(), leftColumn.end(), rightColumn[idx] ) * rightColumn[idx];
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
      printf( "Part 1 solution: %d\n", compute( argv[1], true ) );
      printf( "Part 2 solution: %d\n", compute( argv[1], false ) );
   }
   return 0;
}
