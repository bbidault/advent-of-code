// https://adventofcode.com/2024/day/20

#include <fstream>
#include <limits.h>
#include <vector>

/**
 * @brief Recursive function. Calculates the distance of each location from the start.
 *
 * @param aMap a map
 * @param aX a location of interest x coordinate
 * @param aY a location of interest y coordinate
 * @param aDistanceMap a map of distances for each location
 * @param aPath
 */
void race( const std::vector<std::string>    &aMap,
           int                               aX,
           int                               aY,
           std::vector<std::vector<int> >    &aDistanceMap,
           std::vector<std::pair<int, int> > &aPath )
{
   int distance = 0;
   while ( true )
   {
      aPath.push_back( std::make_pair( aX, aY ) );
      aDistanceMap[aX][aY] = distance;
      if ( ( aMap[aX + 1][aY] != '#' ) && ( aDistanceMap[aX + 1][aY] > distance ) )
      {
         aX++;
      }
      else if ( ( aMap[aX - 1][aY] != '#' ) && ( aDistanceMap[aX - 1][aY] > distance ) )
      {
         aX--;
      }
      else if ( ( aMap[aX][aY + 1] != '#' ) && ( aDistanceMap[aX][aY + 1] > distance ) )
      {
         aY++;
      }
      else if ( ( aMap[aX][aY - 1] != '#' ) && ( aDistanceMap[aX][aY - 1] > distance ) )
      {
         aY--;
      }
      else
      {
         break;
      }
      distance++;
   }
}

/**
 * @brief Calculate the number of cheats (travelling through walls) that can shorten the race by 100 picoseconds or more.
 *
 * @param aInputFilePath the input file
 * @param aMaxCheatDuration the maximum duration of the cheat
 * @return int the number of cheats that can shorten the race by 100 picoseconds or more
 */
int64_t compute( const std::string aInputFilePath, const int aMaxCheatDuration )
{
   int64_t count = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::string> map;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         map.push_back( line );
      }
      int startX = 0;
      int startY = 0;
      for ( int x = 0; x < map.size(); x++ )
      {
         for ( int y = 0; y < map[x].size(); y++ )
         {
            if ( map[x][y] == 'S' )
            {
               startX = x;
               startY = y;
               break;
            }
         }
      }
      std::vector<std::vector<int> >    distanceMap( map.size(), std::vector<int>( map[0].size(), INT_MAX ) );
      std::vector<std::pair<int, int> > racePath;
      race( map, startX, startY, distanceMap, racePath );
      // for each pair of locations
      for ( int i = 0; i < racePath.size() - 1; i++ )
      {
         for ( int j = i + 1; j < racePath.size(); j++ )
         {
            // the carthesian distance between the two locations is the cheat duration
            int cheatDuration = abs( racePath[j].first - racePath[i].first ) + abs( racePath[j].second - racePath[i].second );
            // make sure the gain is significant and the cheat is not too long
            if ( ( distanceMap[racePath[j].first][racePath[j].second] - distanceMap[racePath[i].first][racePath[i].second] - cheatDuration > 99 ) &&
                 ( cheatDuration <= aMaxCheatDuration ) )
            {
               count++;
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
      printf( "Part 1 solution: %ld\n", compute( argv[1], 2 ) );
      printf( "Part 2 solution: %ld\n", compute( argv[1], 20 ) );
   }
   return 0;
}
