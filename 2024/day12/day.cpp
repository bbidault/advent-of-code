// https://adventofcode.com/2024/day/12

#include <fstream>
#include <vector>

/**
 * @brief Recursive function. Calculate the perimeter and area of the garden plot by performing a flood fill.
 *
 * @param aMap a map of garden plots
 * @param aX a origin location x coordinate
 * @param aY a origin location y coordinate
 * @param aPerimeter the perimeter of the garden plot
 * @param aArea the area of the garden plot
 * @param aVisited a map of the visited locations of the garden
 */
void visit( const std::vector<std::string>  &aMap,
            const int                       aX,
            const int                       aY,
            int                             &aPerimeter,
            int                             &aArea,
            std::vector<std::vector<bool> > &aVisited )
{
   aVisited[aX][aY] = true;
   aArea++; // increment the area
   if ( ( aX + 1 < aMap.size() ) && ( aMap[aX][aY] == aMap[aX + 1][aY] ) )
   {
      if ( false == aVisited[aX + 1][aY] )
      {
         visit( aMap, aX + 1, aY, aPerimeter, aArea, aVisited );
      }
   }
   else
   {
      aPerimeter++; // the current location is on the edge of the plot, increment the perimeter
   }
   if ( ( aX - 1 >= 0 ) && ( aMap[aX][aY] == aMap[aX - 1][aY] ) )
   {
      if ( false == aVisited[aX - 1][aY] )
      {
         visit( aMap, aX - 1, aY, aPerimeter, aArea, aVisited );
      }
   }
   else
   {
      aPerimeter++;
   }
   if ( ( aY + 1 < aMap[aX].size() ) && ( aMap[aX][aY] == aMap[aX][aY + 1] ) )
   {
      if ( false == aVisited[aX][aY + 1] )
      {
         visit( aMap, aX, aY + 1, aPerimeter, aArea, aVisited );
      }
   }
   else
   {
      aPerimeter++;
   }
   if ( ( aY - 1 >= 0 ) && ( aMap[aX][aY] == aMap[aX][aY - 1] ) )
   {
      if ( false == aVisited[aX][aY - 1] )
      {
         visit( aMap, aX, aY - 1, aPerimeter, aArea, aVisited );
      }
   }
   else
   {
      aPerimeter++;
   }
}

/**
 * @brief Recursive function. Populate a vector of vectors of locations occupied by a garden plot.
 *
 * @param aMap a map of garden plots
 * @param aX a origin location x coordinate
 * @param aY a origin location y coordinate
 * @param aVisited a map of the visited locations of the garden
 * @param aOccupied whether the location is occupied by the garden plot or not
 */
void floodFill( const std::vector<std::string>  &aMap,
                const int                       aX,
                const int                       aY,
                std::vector<std::vector<bool> > &aVisited,
                std::vector<std::vector<int> >  &aOccupied )
{
   aVisited[aX][aY]          = true;
   aOccupied[aX + 1][aY + 1] = 1; // this location is part of the garden plot of interest
   if ( ( aX + 1 < aMap.size() ) && ( aMap[aX][aY] == aMap[aX + 1][aY] ) && ( false == aVisited[aX + 1][aY] ) )
   {
      floodFill( aMap, aX + 1, aY, aVisited, aOccupied );
   }
   if ( ( aX - 1 >= 0 ) && ( aMap[aX][aY] == aMap[aX - 1][aY] ) && ( false == aVisited[aX - 1][aY] ) )
   {
      floodFill( aMap, aX - 1, aY, aVisited, aOccupied );
   }
   if ( ( aY + 1 < aMap[aX].size() ) && ( aMap[aX][aY] == aMap[aX][aY + 1] ) && ( false == aVisited[aX][aY + 1] ) )
   {
      floodFill( aMap, aX, aY + 1, aVisited, aOccupied );
   }
   if ( ( aY - 1 >= 0 ) && ( aMap[aX][aY] == aMap[aX][aY - 1] ) && ( false == aVisited[aX][aY - 1] ) )
   {
      floodFill( aMap, aX, aY - 1, aVisited, aOccupied );
   }
}

/**
 * @brief Count the number of sides of the garden plot by running masks against a map of occupied locations.
 *
 * @param aMap a map of garden plots
 * @param aX a origin location x coordinate
 * @param aY a origin location y coordinate
 * @return int the number of sides of the garden plot
 */
int countSides( const std::vector<std::string> &aMap, const int aX, const int aY )
{
   int count = 0;

   // populate a vector of vectors of locations occupied by the garden plot by performing a flood fill
   std::vector<std::vector<int> >  occupied( aMap.size() + 2, std::vector<int>( aMap[0].size() + 2, 0 ) );
   std::vector<std::vector<bool> > visited( aMap.size(), std::vector<bool>( aMap[0].size(), false ) );
   floodFill( aMap, aX, aY, visited, occupied );

   // iterate horizontaly through the locations to identify vertical edges of the garden plot
   std::vector<std::vector<int> > horizontalMasked( aMap.size(), std::vector<int>( aMap[0].size() + 1, 0 ) );
   for ( int i = 0; i < horizontalMasked.size(); i++ )
   {
      for ( int j = 0; j < horizontalMasked[i].size(); j++ )
      {
         // substract neighboring locations occupied value to identify edges
         horizontalMasked[i][j] = occupied[i + 1][j + 1] - occupied[i + 1][j];
      }
   }
   for ( int j = 0; j < horizontalMasked[0].size(); j++ )
   {
      int prev = 0;
      for ( int i = 0; i < horizontalMasked.size(); i++ )
      {
         // if two locations share the same value, they are part of the same side and should not be counted multiple times
         if ( ( abs( horizontalMasked[i][j] ) == 1 ) && ( horizontalMasked[i][j] != prev ) )
         {
            count++;
         }
         prev = horizontalMasked[i][j];
      }
   }

   // iterate verticaly through the locations to identify horizontal edges of the garden plot
   std::vector<std::vector<int> > verticalMasked( aMap.size() + 1, std::vector<int>( aMap[0].size(), 0 ) );
   for ( int j = 0; j < verticalMasked[0].size(); j++ )
   {
      for ( int i = 0; i < verticalMasked.size(); i++ )
      {
         verticalMasked[i][j] = occupied[i + 1][j + 1] - occupied[i][j + 1];
      }
   }
   for ( int i = 0; i < verticalMasked.size(); i++ )
   {
      int prev = 0;
      for ( int j = 0; j < verticalMasked[i].size(); j++ )
      {
         if ( ( abs( verticalMasked[i][j] ) == 1 ) && ( verticalMasked[i][j] != prev ) )
         {
            count++;
         }
         prev = verticalMasked[i][j];
      }
   }
   return count;
}

/**
 * @brief For part 1, sum of the perimeters * areas of the given garden plots.
 *        For part 2, sum of the number of sides * areas of the given garden plots.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the sum of the perimeters * areas or number of sides * areas of the given garden plots.
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::string> input;
      std::vector<std::vector<bool> > visited;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         input.push_back( line );
         visited.push_back( std::vector<bool>( line.length(), false ) );
      }
      for ( int i = 0; i < input.size(); i++ )
      {
         for ( int j = 0; j < input[i].length(); j++ )
         {
            if ( false == visited[i][j] )
            {
               int perimeter = 0;
               int area      = 0;
               visit( input, i, j, perimeter, area, visited );
               if ( aPart1 )
               {
                  sum += perimeter * area;
               }
               else
               {
                  sum += countSides( input, i, j ) * area;
               }
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
