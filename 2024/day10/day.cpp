// https://adventofcode.com/2024/day/10

#include <fstream>
#include <set>
#include <vector>

/**
 * @brief Recursive function. Calculates the number of distinct trails that start at the given location
 *        and populate a set of 9 elevation destinations reachable from the given location.
 *
 * @param aDestinations a set of destinations reachable from the given location
 * @param aMap a topographic map
 * @param aX a origin location x coordinate
 * @param aY a origin location y coordinate
 * @return int the number of distinct trails that start at the given location
 */
int findTrails( std::set<std::pair<int, int> > &aDestinations, std::vector<std::string> aMap, int aX, int aY )
{
   int count = 0;
   if ( aMap[aX][aY] == '9' ) // trail ends at 9 elevation
   {
      aDestinations.insert( std::make_pair( aX, aY ) );
      return 1; // counts as a distinct trail
   }
   if ( ( aX + 1 < aMap.size() ) && ( aMap[aX][aY] + 1 == aMap[aX + 1][aY] ) )
   {
      count += findTrails( aDestinations, aMap, aX + 1, aY );
   }
   if ( ( aX - 1 >= 0 ) && ( aMap[aX][aY] + 1 == aMap[aX - 1][aY] ) )
   {
      count += findTrails( aDestinations, aMap, aX - 1, aY );
   }
   if ( ( aY + 1 < aMap[aX].size() ) && ( aMap[aX][aY] + 1 == aMap[aX][aY + 1] ) )
   {
      count += findTrails( aDestinations, aMap, aX, aY + 1 );
   }
   if ( ( aY - 1 >= 0 ) && ( aMap[aX][aY] + 1 == aMap[aX][aY - 1] ) )
   {
      count += findTrails( aDestinations, aMap, aX, aY - 1 );
   }
   return count;
}

/**
 * @brief For part 1, calculate the number of topographic 0 and 9 pairs connected by a path following a gradual
 *        increase in elevation (+1 per north/south/east/west step).
 *        For part 2, calculate the number of distinct trails connecting a topographic 0 to a 9 following a gradual
 *        increase in elevation.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the number of trail start/end pairs for part 1 or the number of distinct trails for part 2
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int count = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::string> input;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         input.push_back( line );
      }
      for ( int i = 0; i < input.size(); i++ )
      {
         for ( int j = 0; j < input[i].length(); j++ )
         {
            if ( input[i][j] == '0' )                       // trail begins at 0 elevation
            {
               std::set<std::pair<int, int> > destinations; // use a set to prevent duplicate trails
               if ( aPart1 )
               {
                  findTrails( destinations, input, i, j );
                  count += destinations.size();
               }
               else
               {
                  count += findTrails( destinations, input, i, j );
               }
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
      printf( "Part 1 solution: %d\n", compute( argv[1], true ) );
      printf( "Part 2 solution: %d\n", compute( argv[1], false ) );
   }
   return 0;
}
