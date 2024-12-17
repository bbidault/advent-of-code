// https://adventofcode.com/2024/day/15

#include <algorithm>
#include <fstream>
#include <set>
#include <sstream>
#include <vector>

/**
 * @brief Recursive function. Determine whether the object at the given x and y coordinates can move based on wether the object(s)
 *        in its path can move or not.
 *
 * @param aMap a map of walls, boxes, empty space and robot
 * @param xCoor the x coordinate of the object to move
 * @param yCoor the y coordinate of the object to move
 * @param xMove the move along the x axis
 * @param yMove the move along the y axis
 * @param aToMove the objects that will need to move for the current robot move, use a set to prevent duplicates
 * @return whether the objet can move or not
 */
bool canMove( std::vector<std::string> &aMap, int xCoor, int yCoor, int xMove, int yMove, std::set<std::pair<int, int> > &aToMove )
{
   bool canMv = false;
   if ( aMap[xCoor][yCoor] == '.' ) // free space
   {
      canMv = true;
   }
   else if ( ( aMap[xCoor][yCoor] == 'O' ) || ( aMap[xCoor][yCoor] == '@' ) ) // box or robot
   {
      // add the object of interest to the set of objects to move
      aToMove.insert( std::make_pair( xCoor, yCoor ) );
      canMv = canMove( aMap, xCoor + xMove, yCoor + yMove, xMove, yMove, aToMove );
   }
   else if ( ( aMap[xCoor][yCoor] == '[' ) || ( aMap[xCoor][yCoor] == ']' ) )
   {
      aToMove.insert( std::make_pair( xCoor, yCoor ) );
      if ( xMove == 0 ) // yMove != 0
      {
         // boxes of part 1 and 2 move the same way along the y axis
         canMv = canMove( aMap, xCoor, yCoor + yMove, xMove, yMove, aToMove );
      }
      else // xMove != 0 && yMove == 0
      {
         if ( aMap[xCoor][yCoor] == '[' )
         {
            // insert the other half of the box in the set of objects to potentially move
            aToMove.insert( std::make_pair( xCoor, yCoor + 1 ) );
            // make sure both halves of the box can move
            canMv = canMove( aMap, xCoor + xMove, yCoor, xMove, yMove, aToMove ) &&
                    canMove( aMap, xCoor + xMove, yCoor + 1, xMove, yMove, aToMove );
         }
         else // aMap[xCoor][yCoor] == ']'
         {
            aToMove.insert( std::make_pair( xCoor, yCoor - 1 ) );
            canMv = canMove( aMap, xCoor + xMove, yCoor, xMove, yMove, aToMove ) &&
                    canMove( aMap, xCoor + xMove, yCoor - 1, xMove, yMove, aToMove );
         }
      }
   }
   else // wall
   {
      // cannot move, do nothing
   }
   return canMv;
}

/**
 * @brief Move the given set of object in the given direction.
 *
 * @param aMap a map of walls, boxes, empty space and robot
 * @param xMove the move along the x axis
 * @param yMove the move along the y axis
 * @param aToMove the objects to move
 */
void move( std::vector<std::string> &aMap, int xMove, int yMove, std::set<std::pair<int, int> > &aToMoveSet )
{
   std::vector<std::pair<int, int> > toMoveVector;
   // convert the set to a vector so we can use sort
   toMoveVector.assign( aToMoveSet.begin(), aToMoveSet.end() );
   // use a different comparison based on the direction of the move, moving the objects in a specific order
   // prevents overwriting box cells with empty cells
   if ( xMove == -1 )
   {
      std::sort( toMoveVector.begin(),
                 toMoveVector.end(),
                 []( std::pair<int, int> &aLeft, std::pair<int, int> &aRight )
                 {
                    return aLeft.first < aRight.first;
                 } );
   }
   else if ( yMove == 1 )
   {
      std::sort( toMoveVector.begin(),
                 toMoveVector.end(),
                 []( std::pair<int, int> &aLeft, std::pair<int, int> &aRight )
                 {
                    return aLeft.second > aRight.second;
                 } );
   }
   else if ( xMove == 1 )
   {
      std::sort( toMoveVector.begin(),
                 toMoveVector.end(),
                 []( std::pair<int, int> &aLeft, std::pair<int, int> &aRight )
                 {
                    return aLeft.first > aRight.first;
                 } );
   }
   else // yMove == -1
   {
      std::sort( toMoveVector.begin(),
                 toMoveVector.end(),
                 []( std::pair<int, int> &aLeft, std::pair<int, int> &aRight )
                 {
                    return aLeft.second < aRight.second;
                 } );
   }
   // move the objects
   std::vector<std::pair<int, int> >::iterator toMove_itr = toMoveVector.begin();
   for (; toMove_itr != toMoveVector.end(); toMove_itr++ )
   {
      aMap[toMove_itr->first + xMove][toMove_itr->second + yMove] = aMap[toMove_itr->first][toMove_itr->second];
      aMap[toMove_itr->first][toMove_itr->second]                 = '.';
   }
}

/**
 * @brief Calculate the sum of the GPS (Goods Positioning System) of the boxes after the robot is done moving following
 *        the given instructions. The initial position of the walls, boxes and robot is defined in the input
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the sum of the GPS of the boxes
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::string> map;
      std::string line = "";
      bool readMap     = true;
      // robot initial location
      int rX = 0;
      int rY = 0;
      while ( std::getline( inputFile, line ) )
      {
         if ( line.empty() )
         {
            readMap = false;
            // find the initial location of the robot
            for ( int i = 0; i < map.size(); i++ )
            {
               for ( int j = 0; j < map[i].length(); j++ )
               {
                  if ( map[i][j] == '@' )
                  {
                     rX = i;
                     rY = j;
                  }
               }
            }
         }
         else if ( readMap )
         {
            if ( aPart1 )
            {
               map.push_back( line );
            }
            else // for part 2, the input is doubly wide, except the robot
            {
               std::string newLine = "";
               char location;
               std::stringstream ss( line );
               while ( ss >> location )
               {
                  if ( location == '#' )
                  {
                     newLine += "##";
                  }
                  else if ( location == '.' )
                  {
                     newLine += "..";
                  }
                  else if ( location == 'O' )
                  {
                     newLine += "[]";
                  }
                  else // '@'
                  {
                     newLine += "@.";
                  }
               }
               map.push_back( newLine );
            }
         }
         else // read robot instructions
         {
            char instruction;
            std::stringstream ss( line );
            while ( ss >> instruction )
            {
               std::set<std::pair<int, int> > toMoveSet;
               if ( instruction == '^' )
               {
                  if ( canMove( map, rX, rY, -1, 0, toMoveSet ) )
                  {
                     move( map, -1, 0, toMoveSet );
                     rX--;
                  }
               }
               else if ( instruction == '>' )
               {
                  if ( canMove( map, rX, rY, 0, 1, toMoveSet ) )
                  {
                     move( map, 0, 1, toMoveSet );
                     rY++;
                  }
               }
               else if ( instruction == 'v' )
               {
                  if ( canMove( map, rX, rY, 1, 0, toMoveSet ) )
                  {
                     move( map, 1, 0, toMoveSet );
                     rX++;
                  }
               }
               else // '<'
               {
                  if ( canMove( map, rX, rY, 0, -1, toMoveSet ) )
                  {
                     move( map, 0, -1, toMoveSet );
                     rY--;
                  }
               }
            }
         }
      }
      // sum the GPS of the boxes
      for ( int i = 0; i < map.size(); i++ )
      {
         for ( int j = 0; j < map[i].length(); j++ )
         {
            if ( ( map[i][j] == 'O' ) || ( map[i][j] == '[' ) )
            {
               sum += i * 100 + j;
            }
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
