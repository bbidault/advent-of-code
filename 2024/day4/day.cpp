// https://adventofcode.com/2024/day/4

#include <fstream>
#include <vector>

/**
 * @brief Check whether the letter at the given location matches the given letter
 *
 * @param aCharArray an array of char (vector of strings)
 * @param aX the x coordinate of the letter in the array
 * @param aY the y coordinate of the letter in the array
 * @param aLetter the letter to check against
 * @return bool whether letter at the given location matches the given letter
 */
bool isLetter( const std::vector<std::string> &aCharArray, int aX, int aY, char aLetter )
{
   return ( aX >= 0 ) && ( aX < aCharArray.size() ) && ( aY >= 0 ) && ( aY < aCharArray[aX].length() ) && ( aCharArray[aX][aY] == aLetter );
}

/**
 * @brief Check whether the word red following the defined pattern matches the given word
 *
 * @param aCharArray an array of char (vector of strings)
 * @param aStartX the x coordinate of the start of the word in the array
 * @param aStartY the Y coordinate of the start of the word in the array
 * @param aIncrementX the increment of the word following the x axis
 * @param aIncrementY the increment of the word following the y axis
 * @param aWord the word to check against
 * @return bool whether the word red following the defined pattern matches the given word
 */
bool isWord( const std::vector<std::string> &aCharArray, int aStartX, int aStartY, int aIncrementX, int aIncrementY, std::string aWord )
{
   bool isWord = true;
   for ( int i = 0; i < aWord.length(); i++ )
   {
      if ( false == isLetter( aCharArray, aStartX + i * aIncrementX, aStartY + i * aIncrementY, aWord[i] ) )
      {
         isWord = false;
         break;
      }
   }
   return isWord;
}

/**
 * @brief For part 1, search for all "XMAS" in the given input.
 *        For part 2, search for "MAS" forming a X shape in the given input
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the count of "XMAS" or X shaped "MAS" found
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
            if ( aPart1 )
            {
               if ( isWord( input, i, j, 0, 1, "XMAS" ) || isWord( input, i, j, 0, 1, "SAMX" ) ) // horizontal
               {
                  count++;
               }
               if ( isWord( input, i, j, 1, 0, "XMAS" ) || isWord( input, i, j, 1, 0, "SAMX" ) ) // vertical
               {
                  count++;
               }
               if ( isWord( input, i, j, 1, 1, "XMAS" ) || isWord( input, i, j, 1, 1, "SAMX" ) ) // diagonal down
               {
                  count++;
               }
               if ( isWord( input, i, j, -1, 1, "XMAS" ) || isWord( input, i, j, -1, 1, "SAMX" ) ) // diagonal up
               {
                  count++;
               }
            }
            else
            {
               if ( isWord( input, i, j, 1, 1, "MAS" ) && isWord( input, i, j + 2, 1, -1, "MAS" ) ||
                    isWord( input, i, j, 1, 1, "MAS" ) && isWord( input, i, j + 2, 1, -1, "SAM" ) ||
                    isWord( input, i, j, 1, 1, "SAM" ) && isWord( input, i, j + 2, 1, -1, "MAS" ) ||
                    isWord( input, i, j, 1, 1, "SAM" ) && isWord( input, i, j + 2, 1, -1, "SAM" ) )
               {
                  count++;
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
