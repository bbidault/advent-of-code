// https://adventofcode.com/2024/day/2

#include <algorithm>
#include <fstream>
#include <sstream>
#include <vector>

/**
 * @brief Count the number of reports that are safe, a report is "safe" if its numbers called levels all increase
 *        with a difference between 1 and 3 from one to the next, or all decrease with a difference between -3
 *        and -1 from one to the next.
 *        For part 2 a report is still considered "safe" if one of its levels does not meet the above criteria.
 *
 * @param aInputFilePath the input file
 * @param aPart2 whether we are solving part 1 (false) or part 2 (true)
 * @return the number of reports that are safe
 */
int compute( const std::string aInputFilePath, const bool aPart2 )
{
   int count = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::string levelsStr;
         std::vector<int>  levels;
         std::stringstream ss( line );
         while ( ss >> levelsStr )
         {
            levels.push_back( std::stoi( levelsStr ) );
         }
         // for part 1, we loop only once since we don't erase levels from the vector
         for ( int jdx = 0; ( jdx < 1 ) || ( aPart2 && ( jdx < levels.size() ) ); jdx++ )
         {
            std::vector<int> levelsCopy = levels; // shallow copy of levels
            if ( aPart2 )
            {
               levelsCopy.erase( std::next( levelsCopy.begin(), jdx ) ); // erase one of the levels from the vector
            }
            // calculate the difference from one level to the next one
            std::vector<int> differences;
            for ( int idx = 0; idx < levelsCopy.size() - 1; idx++ )
            {
               differences.push_back( levelsCopy[idx] - levelsCopy[idx + 1] );
            }
            // if the level differences are all comprised between 1 and 3 or -3 and 1, the report is safe
            if ( ( std::all_of( differences.cbegin(),
                                differences.cend(),
                                []( int num )
                                {
                                   return ( num >= 1 ) && ( num <= 3 );
                                } ) ||
                   std::all_of( differences.cbegin(),
                                differences.cend(),
                                []( int num )
                                {
                                   return ( num >= -3 ) && ( num <= -1 );
                                } ) ) )
            {
               count++;
               break; // break to count a valid report once only
            }
         }
      }
      inputFile.close();
   }
   return count;
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
      printf( "Part 1 solution: %d\n", compute( argv[1], false ) );
      printf( "Part 2 solution: %d\n", compute( argv[1], true ) );
   }
   return 0;
}
