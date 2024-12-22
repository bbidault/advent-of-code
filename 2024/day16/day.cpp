// https://adventofcode.com/2024/day/16

#include <fstream>
#include <limits.h>
#include <vector>

/**
 * @brief A cell of the score map, defines the score of the cell for each heading.
 */
struct Cell
{
   int mNorthScore = INT_MAX;
   int mSouthScore = INT_MAX;
   int mEastScore  = INT_MAX;
   int mWestScore  = INT_MAX;

   /**
    * @brief Return the minimum score of the cell.
    *
    * @return the minimum score of the cell
    */
   int min()
   {
      return std::min( std::min( mNorthScore, mSouthScore ), std::min( mWestScore, mEastScore ) );
   }
};

/**
 * @brief Recursive function. Calculates the score of each cell of the map for each north, south, east, west heading.
 *
 * @param aMap a map
 * @param aX a location of interest x coordinate
 * @param aY a location of interest y coordinate
 * @param aHeading the current heading for the recursive depth
 * @param score the current score for the recursive depth
 * @param aScoreMap a map of scores for each cell and heading
 */
void visit( const std::vector<std::string>  &aMap,
            const int                       aX,
            const int                       aY,
            const std::string               &aHeading,
            const int                       score,
            std::vector<std::vector<Cell> > &aScoreMap )
{
   bool continueVisit = true;
   // update the score for the current location, only if the new score is better
   if ( ( aHeading == "north" ) && ( aScoreMap[aX][aY].mNorthScore > score ) )
   {
      aScoreMap[aX][aY].mNorthScore = score;
      if ( aScoreMap[aX][aY].mSouthScore > score + 2000 ) // full 180 degrees turn adds 2000 points to the score
      {
         aScoreMap[aX][aY].mSouthScore = score + 2000;
      }
      if ( aScoreMap[aX][aY].mEastScore > score + 1000 ) // 90 degrees turn adds 1000 points to the score
      {
         aScoreMap[aX][aY].mEastScore = score + 1000;
      }
      if ( aScoreMap[aX][aY].mWestScore > score + 1000 )
      {
         aScoreMap[aX][aY].mWestScore = score + 1000;
      }
   }
   else if ( ( aHeading == "south" ) && ( aScoreMap[aX][aY].mSouthScore > score ) )
   {
      aScoreMap[aX][aY].mSouthScore = score;
      if ( aScoreMap[aX][aY].mNorthScore > score + 2000 )
      {
         aScoreMap[aX][aY].mNorthScore = score + 2000;
      }
      if ( aScoreMap[aX][aY].mEastScore > score + 1000 )
      {
         aScoreMap[aX][aY].mEastScore = score + 1000;
      }
      if ( aScoreMap[aX][aY].mWestScore > score + 1000 )
      {
         aScoreMap[aX][aY].mWestScore = score + 1000;
      }
   }
   else if ( ( aHeading == "east" ) && ( aScoreMap[aX][aY].mEastScore > score ) )
   {
      aScoreMap[aX][aY].mEastScore = score;
      if ( aScoreMap[aX][aY].mNorthScore > score + 1000 )
      {
         aScoreMap[aX][aY].mNorthScore = score + 1000;
      }
      if ( aScoreMap[aX][aY].mSouthScore > score + 1000 )
      {
         aScoreMap[aX][aY].mSouthScore = score + 1000;
      }
      if ( aScoreMap[aX][aY].mWestScore > score + 2000 )
      {
         aScoreMap[aX][aY].mWestScore = score + 2000;
      }
   }
   else if ( ( aHeading == "west" ) && ( aScoreMap[aX][aY].mWestScore > score ) )
   {
      aScoreMap[aX][aY].mWestScore = score;
      if ( aScoreMap[aX][aY].mNorthScore > score + 1000 )
      {
         aScoreMap[aX][aY].mNorthScore = score + 1000;
      }
      if ( aScoreMap[aX][aY].mSouthScore > score + 1000 )
      {
         aScoreMap[aX][aY].mSouthScore = score + 1000;
      }
      if ( aScoreMap[aX][aY].mEastScore > score + 2000 )
      {
         aScoreMap[aX][aY].mEastScore = score + 2000;
      }
   }
   else
   {
      // the best possible score will be the one that does not require a change of heading, if this score
      // was not updated, it is not worth continuing the recursive exploration of the map
      continueVisit = false;
   }

   // continue the recursive exploration for the neighboring locations that are not wall, nor where we came from
   if ( continueVisit )
   {
      // no need to visit the location where we came from, the score cannot get better
      if ( ( aMap[aX + 1][aY] != '#' ) && ( aHeading != "north" ) )
      {
         if ( aHeading == "south" )
         {
            // if the heading does not change, add +1 to the score
            visit( aMap, aX + 1, aY, "south", score + 1, aScoreMap );
         }
         else
         {
            // otherwise, add +1000 for the change of heading +1 for the step forward
            visit( aMap, aX + 1, aY, "south", score + 1001, aScoreMap );
         }
      }
      if ( ( aMap[aX - 1][aY] != '#' ) && ( aHeading != "south" ) )
      {
         if ( aHeading == "north" )
         {
            visit( aMap, aX - 1, aY, "north", score + 1, aScoreMap );
         }
         else
         {
            visit( aMap, aX - 1, aY, "north", score + 1001, aScoreMap );
         }
      }
      if ( ( aMap[aX][aY + 1] != '#' ) && ( aHeading != "west" ) )
      {
         if ( aHeading == "east" )
         {
            visit( aMap, aX, aY + 1, "east", score + 1, aScoreMap );
         }
         else
         {
            visit( aMap, aX, aY + 1, "east", score + 1001, aScoreMap );
         }
      }
      if ( ( aMap[aX][aY - 1] != '#' ) && ( aHeading != "east" ) )
      {
         if ( aHeading == "west" )
         {
            visit( aMap, aX, aY - 1, "west", score + 1, aScoreMap );
         }
         else
         {
            visit( aMap, aX, aY - 1, "west", score + 1001, aScoreMap );
         }
      }
   }
}

/**
 * @brief Recursive function. Backtrack the score map to identify locations that are part of the best path(s).
 *
 * @param aX a location of interest x coordinate
 * @param aY a location of interest y coordinate
 * @param aScoreMap a map of scores for each cell and heading
 * @param aVisited a map of visited location, to prevent counting a location twice
 * @param aBestScore the best score possible for the maze
 * @return the number of locations that are part of the best path(s)
 */
int backtrack( const int                       aX,
               const int                       aY,
               std::vector<std::vector<Cell> > &aScoreMap,
               std::vector<std::vector<bool> > &aVisited,
               const int                       aBestScore )
{
   int count = 1;
   aVisited[aX][aY] = true;
   if ( ( false == aVisited[aX + 1][aY] ) &&                                     // not visited yet
        ( aScoreMap[aX + 1][aY].mNorthScore < aScoreMap[aX][aY].mNorthScore ) && // the score is lower, following the heading
        ( aScoreMap[aX + 1][aY].mNorthScore < aBestScore ) )                     // the location is along the best path(s)
   {
      count += backtrack( aX + 1, aY, aScoreMap, aVisited, aBestScore );
   }
   if ( ( false == aVisited[aX - 1][aY] ) &&
        ( aScoreMap[aX - 1][aY].mSouthScore < aScoreMap[aX][aY].mSouthScore ) &&
        ( aScoreMap[aX - 1][aY].mSouthScore < aBestScore ) )
   {
      count += backtrack( aX - 1, aY, aScoreMap, aVisited, aBestScore );
   }
   if ( ( false == aVisited[aX][aY + 1] ) &&
        ( aScoreMap[aX][aY + 1].mWestScore < aScoreMap[aX][aY].mWestScore ) &&
        ( aScoreMap[aX][aY + 1].mWestScore < aBestScore ) )
   {
      count += backtrack( aX, aY + 1, aScoreMap, aVisited, aBestScore );
   }
   if ( ( false == aVisited[aX][aY - 1] ) &&
        ( aScoreMap[aX][aY - 1].mEastScore < aScoreMap[aX][aY].mEastScore ) &&
        ( aScoreMap[aX][aY - 1].mEastScore < aBestScore ) )
   {
      count += backtrack( aX, aY - 1, aScoreMap, aVisited, aBestScore );
   }
   return count;
}

/**
 * @brief For part 1, calculate the best score a Reindeer can get in the Reindeer Olympics Reindeer Maze.
 *        For part 2, calculate the number of locations along the best path(s) in the Reindeer Maze.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the best score a Reindeer can get or the number of locations along the best path(s) in the Maze.
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::string> map;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         map.push_back( line );
      }
      int startX = map.size() - 2;
      int startY = 1;
      int endX   = 1;
      int endY   = map[0].size() - 2;
      std::vector<std::vector<Cell> > scoreMap( map.size(), std::vector<Cell>( map[0].size(), Cell() ) );
      visit( map, startX, startY, "east", 0, scoreMap );
      int bestScore = scoreMap[endX][endY].min();
      if ( aPart1 )
      {
         return bestScore;
      }
      else
      {
         std::vector<std::vector<bool> > visited( map.size(), std::vector<bool>( map[0].size(), false ) );
         return backtrack( endX, endY, scoreMap, visited, bestScore );
      }
      inputFile.close();
   }
   return 0;
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
