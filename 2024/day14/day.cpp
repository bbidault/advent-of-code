// https://adventofcode.com/2024/day/14

#include <cmath>
#include <fstream>
#include <regex>
#include <vector>

/**
 * @brief Calculate the product (safety factor) of the number of robots in each regions of
 *        the space after 100 seconds.
 *
 * @param aInputFilePath the input file
 * @return int the product of the number of robots in each regions of the map after 100 seconds
 */
int compute( const std::string aInputFilePath )
{
   int safetyFactor = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      // parse the initial position and velocity of the robots
      std::vector<std::vector<int> > robots;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::vector<int> robot;
         std::regex  numReg( R"(-?\d+)" );
         std::smatch numMatch;
         std::string::const_iterator numSearchStart( line.cbegin() );
         while ( regex_search( numSearchStart, line.cend(), numMatch, numReg ) )
         {
            robot.push_back( std::stoi( numMatch[0] ) );
            numSearchStart = numMatch.suffix().first;
         }
         robots.push_back( robot );
      }

      // the dimensions of the space where the robots patrol
      int xLen = 101;
      int yLen = 103;

      // update the position of each robot for 100 seconds
      for ( int second = 0; second < 100; second++ )
      {
         for ( int i = 0; i < robots.size(); i++ )
         {
            int xLoc = robots[i][0];
            int yLoc = robots[i][1];
            int xVel = robots[i][2];
            int yVel = robots[i][3];
            robots[i][0] = ( xLoc + xVel + xLen ) % xLen;
            robots[i][1] = ( yLoc + yVel + yLen ) % yLen;
         }
      }

      // calculate the safety factor
      int northWest = 0;
      int northEast = 0;
      int southWest = 0;
      int southEast = 0;
      for ( int i = 0; i < robots.size(); i++ )
      {
         int xLoc = robots[i][0];
         int yLoc = robots[i][1];
         if ( ( xLoc < xLen / 2 ) && ( yLoc < yLen / 2 ) )
         {
            northWest++;
         }
         else if ( ( xLoc < xLen / 2 ) && ( yLoc > yLen / 2 ) )
         {
            northEast++;
         }
         else if ( ( xLoc > xLen / 2 ) && ( yLoc < yLen / 2 ) )
         {
            southWest++;
         }
         else if ( ( xLoc > xLen / 2 ) && ( yLoc > yLen / 2 ) )
         {
            southEast++;
         }
      }
      safetyFactor = northWest * northEast * southWest * southEast;
      inputFile.close();
   }
   return safetyFactor;
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
      printf( "Solution: %d\n", compute( argv[1] ) );
   }
   return 0;
}
