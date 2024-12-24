// https://adventofcode.com/2024/day/18

#include <fstream>
#include <limits.h>
#include <regex>
#include <vector>

/**
 * @brief Recursive function. Dijkstra's algorithm to evaluate the number of steps necessary to reach
 *        each unoccupied locations on the map.
 *
 * @param aX a location x coordinate
 * @param aY a location y coordinate
 * @param aSteps the number of steps necessary to reach this location
 * @param aOccupied a map of occupied locations
 * @param aStepsMap a map to keep track of the number of steps necessary to reach each locations
 */
void visit( const int                             aX,
            const int                             aY,
            const int                             aSteps,
            const std::vector<std::vector<bool> > &aOccupied,
            std::vector<std::vector<int> >        &aStepsMap )
{
   aStepsMap[aX][aY] = aSteps;
   if ( ( aX + 1 < aOccupied.size() ) &&
        ( false == aOccupied[aX + 1][aY] ) &&
        ( aSteps + 1 < aStepsMap[aX + 1][aY] ) )
   {
      visit( aX + 1, aY, aSteps + 1, aOccupied, aStepsMap );
   }
   if ( ( aX - 1 >= 0 ) &&
        ( false == aOccupied[aX - 1][aY] ) &&
        ( aSteps + 1 < aStepsMap[aX - 1][aY] ) )
   {
      visit( aX - 1, aY, aSteps + 1, aOccupied, aStepsMap );
   }
   if ( ( aY + 1 < aOccupied[0].size() ) &&
        ( false == aOccupied[aX][aY + 1] ) &&
        ( aSteps + 1 < aStepsMap[aX][aY + 1] ) )
   {
      visit( aX, aY + 1, aSteps + 1, aOccupied, aStepsMap );
   }
   if ( ( aY - 1 >= 0 ) &&
        ( false == aOccupied[aX][aY - 1] ) &&
        ( aSteps + 1 < aStepsMap[aX][aY - 1] ) )
   {
      visit( aX, aY - 1, aSteps + 1, aOccupied, aStepsMap );
   }
}

/**
 * @brief For part 1, calculate the number of steps necessary to reach the end of the map after 1024 bytes have dropped.
 *        For part 2, identify the location of the byte that will block off the path to the end of the map.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 */
void compute( const std::string aInputFilePath, const bool aPart1 )
{
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::vector<int> > bytes;
      // parse the input
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::vector<int> byte;
         std::regex  numReg( R"(\d+)" );
         std::smatch numMatch;
         std::string::const_iterator numSearchStart( line.cbegin() );
         while ( regex_search( numSearchStart, line.cend(), numMatch, numReg ) )
         {
            byte.push_back( std::stoi( numMatch[0] ) );
            numSearchStart = numMatch.suffix().first;
         }
         bytes.push_back( byte );
      }
      int mapSize = 71;
      std::vector<std::vector<bool> > occupied( mapSize, std::vector<bool>( mapSize, false ) );
      for ( int i = 0; i < 1024; i++ )
      {
         occupied[bytes[i][0]][bytes[i][1]] = true;
      }
      if ( aPart1 )
      {
         std::vector<std::vector<int> > stepsMap( mapSize, std::vector<int>( mapSize, INT_MAX ) );
         visit( 0, 0, 0, occupied, stepsMap );
         printf( "%d\n", stepsMap[mapSize - 1][mapSize - 1] );
      }
      else
      {
         // brute force solution, try blocking one new location at a time
         for ( int i = 1024; i < bytes.size(); i++ )
         {
            occupied[bytes[i][0]][bytes[i][1]] = true;
            std::vector<std::vector<int> > stepsMap( mapSize, std::vector<int>( mapSize, INT_MAX ) );
            visit( 0, 0, 0, occupied, stepsMap );
            if ( stepsMap[mapSize - 1][mapSize - 1] == INT_MAX )
            {
               printf( "%d,%d\n", bytes[i][0], bytes[i][1] );
               break;
            }
         }
      }
      inputFile.close();
   }
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
      printf( "Part 1 solution: " );
      compute( argv[1], true );
      printf( "Part 2 solution: " );
      compute( argv[1], false );
   }
   return 0;
}
