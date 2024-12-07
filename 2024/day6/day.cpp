// https://adventofcode.com/2024/day/4

#include <fstream>
#include <tuple>
#include <vector>

/**
 * @brief Generate the guard patrol through the given map, count the number of locations visited by the guard
 *        and determine if the patrol is a loop.
 *
 * @param aMap a map of obstacles and free spaces, passed by copy because we need to modify it many times in part 2
 * @param aGuardLoc the initial location of the guard, also passed by copy
 * @return int the number of locations visited by the guard before she exits the map or -1 if the patrol is a loop
 */
int patrol( std::vector<std::string> aMap, std::pair<int, int> aGuardLoc )
{
   int count = 1;
   std::tuple<int, int, char> dir( -1, 0, '^' );
   while ( true )
   {
      std::pair<int, int> nextLoc( aGuardLoc.first + std::get<0>( dir ), aGuardLoc.second + std::get<1>( dir ) );
      if ( ( nextLoc.first >= 0 ) &&
           ( nextLoc.first < aMap.size() ) &&
           ( nextLoc.second >= 0 ) &&
           ( nextLoc.second < aMap[0].size() ) )
      {
         if ( aMap[nextLoc.first][nextLoc.second] == '.' )
         {
            aGuardLoc                               = nextLoc;
            aMap[aGuardLoc.first][aGuardLoc.second] = std::get<2>( dir );
            count++;
         }
         else if ( aMap[nextLoc.first][nextLoc.second] == std::get<2>( dir ) )
         {
            // already visited this location while pointing in the same direction, the patrol is a loop
            return -1;
         }
         else if ( aMap[nextLoc.first][nextLoc.second] == '#' )
         {
            // update the direction of the guard
            if ( ( std::get<0>( dir ) == -1 ) && ( std::get<1>( dir ) == 0 ) )
            {
               dir = std::tuple<int, int, char>( 0, 1, '>' );
            }
            else if ( ( std::get<0>( dir ) == 0 ) && ( std::get<1>( dir ) == 1 ) )
            {
               dir = std::tuple<int, int, char>( 1, 0, 'v' );
            }
            else if ( ( std::get<0>( dir ) == 1 ) && ( std::get<1>( dir ) == 0 ) )
            {
               dir = std::tuple<int, int, char>( 0, -1, '<' );
            }
            else // ( std::get<0>( dir ) == 0 ) && ( std::get<1>( dir ) == -1 )
            {
               dir = std::tuple<int, int, char>( -1, 0, '^' );
            }
         }
         else
         {
            aGuardLoc = nextLoc;
         }
      }
      else
      {
         break;
      }
   }
   return count;
}

/**
 * @brief For part 1, generate the patrol of the guard and count the number of locations visited.
 *        For part 2, count the number of locations where an obstacles can be placed to make the patrol a loop.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the number of locations visited by the patrol or the number of locations where placing
               an obstacle would make the patrol a loop.
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int count = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::string> input;
      std::string line = "";
      std::pair<int, int> guardLoc;
      int xCoor = 0;
      while ( std::getline( inputFile, line ) )
      {
         input.push_back( line );
         for ( int yCoor = 0; yCoor < line.length(); yCoor++ )
         {
            if ( line[yCoor] == '^' )
            {
               guardLoc = std::pair<int, int>( xCoor, yCoor );
            }
         }
         xCoor++;
      }

      if ( aPart1 )
      {
         count = patrol( input, guardLoc );
      }
      else
      {
         // try placing an obstacle at every free locations, a simple optimization would be to place
         // obstacles only along the original patrol as the guard cannot reach other locations without
         // being deviated from her path
         for ( int i = 0; i < input.size(); i++ )
         {
            for ( int j = 0; j < input[i].size(); j++ )
            {
               if ( input[i][j] == '.' )
               {
                  input[i][j] = '#'; // add an obstacle
                  if ( patrol( input, guardLoc ) == -1 )
                  {
                     count++;
                  }
                  input[i][j] = '.'; // remove the obstacle for the next loop around
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
