// https://adventofcode.com/2024/day/3

#include <iostream>
#include <fstream>
#include <regex>
#include <sstream>

/**
 * @brief Sum the product of the two numbers in a regular expression of the form "mul\(\d{1,3},\d{1,3}\)".
 *        For part 2, ignore the products located between a "don't" and "do" expression.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return The sum of the products
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int  sum    = 0;
   bool active = true; // whether multiplications are active or not, not used for part 1
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::regex  mulReg( R"(mul\(\d{1,3},\d{1,3}\)|(don't)|(do))" ); // regex for multiplications, do and don't keywords
      std::regex  numReg( R"(\d{1,3})" );                             // regex for 1 to 3 digits numbers
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::smatch mulMatch;
         std::string::const_iterator mulSearchStart( line.cbegin() );
         while ( regex_search( mulSearchStart, line.cend(), mulMatch, mulReg ) )
         {
            std::string word = mulMatch[0];
            if ( word == "do" )
            {
               active = true;
            }
            else if ( word == "don't" )
            {
               active = false;
            }
            else if ( active || aPart1 ) // word matches the "mul" expression
            {
               std::smatch numMatch;
               std::string::const_iterator numSearchStart( word.cbegin() );
               int product = 1;
               while ( regex_search( numSearchStart, word.cend(), numMatch, numReg ) )
               {
                  product       *= std::stoi( numMatch[0] );
                  numSearchStart = numMatch.suffix().first;
               }
               sum += product;
            }
            else
            {
               // should not get here, do nothing
            }
            mulSearchStart = mulMatch.suffix().first;
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
